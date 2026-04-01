#!/usr/bin/env python3
"""Standalone Reddit publisher with dry-run, validation, and pluggable clients.

Supports text, link, and comment payloads. Live publishing uses Reddit's OAuth API
through urllib and environment variables; dry-run works with no credentials.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Optional, Protocol

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_QUEUE_FILE = ROOT / "mission-control" / "data" / "reddit_queue.json"
DEFAULT_LOG_FILE = ROOT / "mission-control" / "data" / "reddit_publish_log.jsonl"
DEFAULT_USER_AGENT = "openclaw-reddit-publisher/0.1"
VALID_KINDS = {"text", "link", "comment"}


class ValidationError(ValueError):
    """Raised when a payload is invalid."""


class PublishError(RuntimeError):
    """Raised when publishing fails."""


@dataclass
class RedditPayload:
    subreddit: Optional[str] = None
    title: Optional[str] = None
    body: Optional[str] = None
    url: Optional[str] = None
    kind: str = "text"
    parent_id: Optional[str] = None
    channel: Optional[str] = None
    draft_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: Mapping[str, Any]) -> "RedditPayload":
        return cls(
            subreddit=_clean_optional(data.get("subreddit")),
            title=_clean_optional(data.get("title")),
            body=_clean_optional(data.get("body")),
            url=_clean_optional(data.get("url")),
            kind=_clean_optional(data.get("kind")) or "text",
            parent_id=_clean_optional(data.get("parentId") or data.get("parent_id")),
            channel=_clean_optional(data.get("channel")),
            draft_id=_clean_optional(data.get("id") or data.get("draft_id")),
            metadata=dict(data.get("metadata") or {}),
        )

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["parentId"] = data.pop("parent_id")
        data["draft_id"] = data.pop("draft_id")
        return {k: v for k, v in data.items() if v not in (None, "", {}, [])}


@dataclass
class PublishResult:
    ok: bool
    dry_run: bool
    kind: str
    subreddit: Optional[str]
    id: Optional[str] = None
    name: Optional[str] = None
    permalink: Optional[str] = None
    url: Optional[str] = None
    parent_id: Optional[str] = None
    draft_id: Optional[str] = None
    created_utc: Optional[float] = None
    response: Optional[Dict[str, Any]] = None
    warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in asdict(self).items() if v not in (None, [], {})}


class PublishClient(Protocol):
    def publish(self, payload: RedditPayload) -> PublishResult:
        ...


class DryRunPublishClient:
    def publish(self, payload: RedditPayload) -> PublishResult:
        now = time.time()
        fake_id = f"dry_{uuid.uuid4().hex[:10]}"
        fake_name = f"t3_{fake_id}" if payload.kind != "comment" else f"t1_{fake_id}"
        permalink = _build_fake_permalink(payload, fake_id)
        return PublishResult(
            ok=True,
            dry_run=True,
            kind=payload.kind,
            subreddit=payload.subreddit,
            id=fake_id,
            name=fake_name,
            permalink=permalink,
            url=f"https://reddit.com{permalink}" if permalink else None,
            parent_id=payload.parent_id,
            draft_id=payload.draft_id,
            created_utc=now,
            response={"preview": payload.to_dict()},
            warnings=["dry-run only; nothing was sent to Reddit"],
        )


class RedditOAuthClient:
    """Direct Reddit publisher via OAuth and API submit/comment endpoints."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        username: str,
        password: str,
        user_agent: str = DEFAULT_USER_AGENT,
        timeout: int = 30,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.user_agent = user_agent
        self.timeout = timeout

    @classmethod
    def from_env(cls) -> "RedditOAuthClient":
        required = {
            "REDDIT_CLIENT_ID": os.getenv("REDDIT_CLIENT_ID"),
            "REDDIT_CLIENT_SECRET": os.getenv("REDDIT_CLIENT_SECRET"),
            "REDDIT_USERNAME": os.getenv("REDDIT_USERNAME"),
            "REDDIT_PASSWORD": os.getenv("REDDIT_PASSWORD"),
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            raise PublishError(
                "Missing Reddit auth env vars: " + ", ".join(missing)
            )
        return cls(
            client_id=required["REDDIT_CLIENT_ID"] or "",
            client_secret=required["REDDIT_CLIENT_SECRET"] or "",
            username=required["REDDIT_USERNAME"] or "",
            password=required["REDDIT_PASSWORD"] or "",
            user_agent=os.getenv("REDDIT_USER_AGENT", DEFAULT_USER_AGENT),
        )

    def publish(self, payload: RedditPayload) -> PublishResult:
        token = self._fetch_token()
        if payload.kind == "comment":
            response = self._submit_comment(token, payload)
            data = response.get("json", {}).get("data", {})
            things = data.get("things") or []
            thing = things[0] if things else {}
            return PublishResult(
                ok=not bool(data.get("errors")),
                dry_run=False,
                kind=payload.kind,
                subreddit=payload.subreddit,
                id=thing.get("id"),
                name=thing.get("name"),
                permalink=thing.get("data", {}).get("permalink") or thing.get("permalink"),
                url=_full_reddit_url(thing.get("data", {}).get("permalink") or thing.get("permalink")),
                parent_id=payload.parent_id,
                draft_id=payload.draft_id,
                created_utc=time.time(),
                response=response,
                warnings=_extract_errors(data),
            )
        response = self._submit_post(token, payload)
        json_data = response.get("json", {})
        errors = _extract_errors(json_data)
        result_data = json_data.get("data", {}) if isinstance(json_data, dict) else {}
        url = result_data.get("url")
        return PublishResult(
            ok=not errors,
            dry_run=False,
            kind=payload.kind,
            subreddit=payload.subreddit,
            id=result_data.get("id"),
            name=result_data.get("name"),
            permalink=_permalink_from_url(url),
            url=url,
            parent_id=payload.parent_id,
            draft_id=payload.draft_id,
            created_utc=time.time(),
            response=response,
            warnings=errors,
        )

    def _fetch_token(self) -> str:
        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode("utf-8")).decode("ascii")
        data = urllib.parse.urlencode(
            {
                "grant_type": "password",
                "username": self.username,
                "password": self.password,
            }
        ).encode("utf-8")
        request = urllib.request.Request(
            "https://www.reddit.com/api/v1/access_token",
            data=data,
            headers={
                "Authorization": f"Basic {auth}",
                "User-Agent": self.user_agent,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )
        response = _json_request(request, timeout=self.timeout)
        token = response.get("access_token")
        if not token:
            raise PublishError(f"Reddit token response missing access_token: {response}")
        return str(token)

    def _submit_post(self, token: str, payload: RedditPayload) -> Dict[str, Any]:
        data = {
            "api_type": "json",
            "kind": "self" if payload.kind == "text" else "link",
            "resubmit": "true",
            "sr": payload.subreddit or "",
            "title": payload.title or "",
        }
        if payload.kind == "text":
            data["text"] = payload.body or ""
        elif payload.kind == "link":
            data["url"] = payload.url or ""
        return self._oauth_form_post("https://oauth.reddit.com/api/submit", token, data)

    def _submit_comment(self, token: str, payload: RedditPayload) -> Dict[str, Any]:
        data = {
            "api_type": "json",
            "thing_id": payload.parent_id or "",
            "text": payload.body or "",
        }
        return self._oauth_form_post("https://oauth.reddit.com/api/comment", token, data)

    def _oauth_form_post(self, url: str, token: str, data: Mapping[str, Any]) -> Dict[str, Any]:
        encoded = urllib.parse.urlencode(data).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=encoded,
            headers={
                "Authorization": f"bearer {token}",
                "User-Agent": self.user_agent,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )
        return _json_request(request, timeout=self.timeout)


def _json_request(request: urllib.request.Request, timeout: int = 30) -> Dict[str, Any]:
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise PublishError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise PublishError(f"Request failed: {exc}") from exc

    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise PublishError(f"Invalid JSON response: {raw[:500]}") from exc


class StructuredLogger:
    def __init__(self, log_file: Path = DEFAULT_LOG_FILE) -> None:
        self.log_file = log_file

    def log(self, event: str, payload: Mapping[str, Any]) -> None:
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "event": event,
            **payload,
        }
        with self.log_file.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")


class RedditPublisher:
    def __init__(self, client: PublishClient, logger: Optional[StructuredLogger] = None) -> None:
        self.client = client
        self.logger = logger or StructuredLogger()

    def publish(self, payload: RedditPayload) -> PublishResult:
        validate_payload(payload)
        self.logger.log("reddit.publish.attempt", payload.to_dict())
        result = self.client.publish(payload)
        self.logger.log("reddit.publish.result", result.to_dict())
        if not result.ok:
            raise PublishError("Publish returned non-ok result", result.to_dict())
        return result


def validate_payload(payload: RedditPayload) -> None:
    kind = payload.kind.strip().lower()
    if kind not in VALID_KINDS:
        raise ValidationError(f"Unsupported kind '{payload.kind}'. Expected one of {sorted(VALID_KINDS)}")
    payload.kind = kind

    if kind in {"text", "link"}:
        if not payload.subreddit:
            raise ValidationError("subreddit is required for text/link posts")
        if not payload.title:
            raise ValidationError("title is required for text/link posts")
    if kind == "text":
        if not payload.body:
            raise ValidationError("body is required for text posts")
        if payload.url:
            raise ValidationError("text posts cannot include url")
    elif kind == "link":
        if not payload.url:
            raise ValidationError("url is required for link posts")
        if payload.body:
            raise ValidationError("link posts cannot include body")
        _validate_url(payload.url)
    elif kind == "comment":
        if not payload.parent_id:
            raise ValidationError("parentId is required for comments")
        if not payload.body:
            raise ValidationError("body is required for comments")
        if payload.title:
            raise ValidationError("comments cannot include title")
        if payload.url:
            raise ValidationError("comments cannot include url")

    if payload.title and len(payload.title) > 300:
        raise ValidationError("title exceeds 300 chars")
    if payload.body and len(payload.body) > 40000:
        raise ValidationError("body exceeds 40000 chars")


def load_queue(queue_file: Path = DEFAULT_QUEUE_FILE) -> Dict[str, Any]:
    if not queue_file.exists():
        return {"drafts": []}
    return json.loads(queue_file.read_text(encoding="utf-8"))


def save_queue(data: Mapping[str, Any], queue_file: Path = DEFAULT_QUEUE_FILE) -> None:
    queue_file.parent.mkdir(parents=True, exist_ok=True)
    queue_file.write_text(json.dumps(dict(data), indent=2) + "\n", encoding="utf-8")


def find_draft(draft_id: str, queue_file: Path = DEFAULT_QUEUE_FILE) -> Dict[str, Any]:
    data = load_queue(queue_file)
    for draft in data.get("drafts", []):
        if draft.get("id") == draft_id:
            return draft
    raise PublishError(f"Draft {draft_id} not found in {queue_file}")


def update_draft_after_publish(draft_id: str, result: PublishResult, queue_file: Path = DEFAULT_QUEUE_FILE) -> Dict[str, Any]:
    data = load_queue(queue_file)
    for draft in data.get("drafts", []):
        if draft.get("id") == draft_id:
            draft["status"] = "published-dry-run" if result.dry_run else "published"
            draft["publishedAt"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            draft["redditId"] = result.id
            draft["permalink"] = result.url or (f"https://reddit.com{result.permalink}" if result.permalink else None)
            draft["publishResult"] = result.to_dict()
            save_queue(data, queue_file)
            return draft
    raise PublishError(f"Draft {draft_id} not found in {queue_file}")


def build_client(mode: str) -> PublishClient:
    if mode == "dry-run":
        return DryRunPublishClient()
    if mode == "oauth":
        return RedditOAuthClient.from_env()
    raise PublishError(f"Unsupported mode: {mode}")


def _clean_optional(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _validate_url(url: str) -> None:
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValidationError(f"Invalid URL: {url}")


def _extract_errors(data: Mapping[str, Any]) -> List[str]:
    errors = data.get("errors") if isinstance(data, Mapping) else None
    if not errors:
        return []
    results = []
    for item in errors:
        if isinstance(item, (list, tuple)):
            results.append(" | ".join(str(part) for part in item))
        else:
            results.append(str(item))
    return results


def _full_reddit_url(permalink: Optional[str]) -> Optional[str]:
    if not permalink:
        return None
    if permalink.startswith("http://") or permalink.startswith("https://"):
        return permalink
    return f"https://reddit.com{permalink}"


def _permalink_from_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    parsed = urllib.parse.urlparse(url)
    return parsed.path if parsed.netloc else url


def _build_fake_permalink(payload: RedditPayload, fake_id: str) -> Optional[str]:
    if payload.kind == "comment":
        return f"/r/{payload.subreddit or 'unknown'}/comments/mock/thread/{fake_id}/"
    slug = (payload.title or "post").strip().lower().replace(" ", "-")[:40]
    return f"/r/{payload.subreddit or 'unknown'}/comments/{fake_id}/{slug}/"


def cmd_validate(args: argparse.Namespace) -> int:
    payload = _payload_from_args(args)
    validate_payload(payload)
    print(json.dumps({"ok": True, "payload": payload.to_dict()}, indent=2))
    return 0


def cmd_publish(args: argparse.Namespace) -> int:
    payload = _payload_from_args(args)
    publisher = RedditPublisher(
        client=build_client(args.mode),
        logger=StructuredLogger(Path(args.log_file)),
    )
    result = publisher.publish(payload)
    print(json.dumps(result.to_dict(), indent=2))
    return 0


def cmd_publish_draft(args: argparse.Namespace) -> int:
    draft = find_draft(args.id, Path(args.queue_file))
    payload = RedditPayload.from_mapping(draft)
    publisher = RedditPublisher(
        client=build_client(args.mode),
        logger=StructuredLogger(Path(args.log_file)),
    )
    result = publisher.publish(payload)
    updated = update_draft_after_publish(args.id, result, Path(args.queue_file))
    print(json.dumps({"result": result.to_dict(), "draft": updated}, indent=2))
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    drafts = load_queue(Path(args.queue_file)).get("drafts", [])
    for draft in drafts:
        print(json.dumps(draft, sort_keys=True))
    if not drafts:
        print("[]")
    return 0


def _payload_from_args(args: argparse.Namespace) -> RedditPayload:
    if getattr(args, "payload_file", None):
        path = Path(args.payload_file)
        return RedditPayload.from_mapping(json.loads(path.read_text(encoding="utf-8")))
    return RedditPayload(
        subreddit=args.subreddit,
        title=args.title,
        body=args.body,
        url=args.url,
        kind=args.kind,
        parent_id=args.parent_id,
        channel=getattr(args, "channel", None),
        draft_id=getattr(args, "draft_id", None),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Standalone Reddit publisher")
    parser.add_argument("--log-file", default=str(DEFAULT_LOG_FILE))
    parser.add_argument("--queue-file", default=str(DEFAULT_QUEUE_FILE))

    sub = parser.add_subparsers(dest="command", required=True)

    payload_parent = argparse.ArgumentParser(add_help=False)
    payload_parent.add_argument("--payload-file")
    payload_parent.add_argument("--subreddit")
    payload_parent.add_argument("--title")
    payload_parent.add_argument("--body")
    payload_parent.add_argument("--url")
    payload_parent.add_argument("--kind", choices=sorted(VALID_KINDS), default="text")
    payload_parent.add_argument("--parent-id")
    payload_parent.add_argument("--channel")
    payload_parent.add_argument("--draft-id")

    validate_p = sub.add_parser("validate", parents=[payload_parent], help="Validate a payload")
    validate_p.set_defaults(func=cmd_validate)

    publish_p = sub.add_parser("publish", parents=[payload_parent], help="Publish a payload")
    publish_p.add_argument("--mode", choices=["dry-run", "oauth"], default="dry-run")
    publish_p.set_defaults(func=cmd_publish)

    publish_draft_p = sub.add_parser("publish-draft", help="Publish a queued draft by id")
    publish_draft_p.add_argument("--id", required=True)
    publish_draft_p.add_argument("--mode", choices=["dry-run", "oauth"], default="dry-run")
    publish_draft_p.set_defaults(func=cmd_publish_draft)

    list_p = sub.add_parser("list-drafts", help="List queued drafts as JSON lines")
    list_p.set_defaults(func=cmd_list)

    return parser


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        return int(args.func(args))
    except ValidationError as exc:
        print(json.dumps({"ok": False, "error": str(exc), "type": "validation"}, indent=2), file=sys.stderr)
        return 2
    except PublishError as exc:
        message = exc.args[0] if exc.args else str(exc)
        extra = exc.args[1] if len(exc.args) > 1 else None
        payload = {"ok": False, "error": message, "type": "publish"}
        if extra is not None:
            payload["details"] = extra
        print(json.dumps(payload, indent=2), file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
