#!/usr/bin/env python3
"""Manage queued Reddit drafts and publish them through the local publisher.

This keeps the old entrypoint name but removes the Devvit localhost dependency.
For real Reddit publishing, use --mode oauth with the required REDDIT_* env vars.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
QUEUE_FILE = ROOT / 'mission-control' / 'data' / 'reddit_queue.json'

# Import sibling module when executed directly.
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from reddit_publisher import (  # noqa: E402
    DEFAULT_LOG_FILE,
    RedditPayload,
    StructuredLogger,
    build_client,
    load_queue,
    save_queue,
    update_draft_after_publish,
    validate_payload,
    RedditPublisher,
)


def list_drafts() -> None:
    drafts = load_queue(QUEUE_FILE).get('drafts', [])
    if not drafts:
        print('No drafts queued.')
        return
    for draft in drafts:
        status = draft.get('status', 'pending')
        kind = draft.get('kind', 'text')
        print(f"{draft.get('id')} • r/{draft.get('subreddit')} • {kind} • {status}")


def show_draft(args: argparse.Namespace) -> None:
    draft = next((d for d in load_queue(QUEUE_FILE).get('drafts', []) if d.get('id') == args.id), None)
    if not draft:
        raise SystemExit(f"Draft {args.id} not found")
    print(json.dumps(draft, indent=2))


def add_draft(args: argparse.Namespace) -> None:
    data = load_queue(QUEUE_FILE)
    drafts = data.setdefault('drafts', [])
    if any(d.get('id') == args.id for d in drafts):
        raise SystemExit(f"Draft {args.id} already exists")
    draft: Dict[str, Any] = {
        'id': args.id,
        'createdAt': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'channel': args.channel,
        'subreddit': args.subreddit,
        'title': args.title,
        'body': args.body,
        'url': args.url,
        'kind': args.kind,
        'parentId': args.parent,
        'status': 'pending',
    }
    validate_payload(RedditPayload.from_mapping(draft))
    drafts.append(draft)
    save_queue(data, QUEUE_FILE)
    print(f"Draft {args.id} added for r/{args.subreddit}")


def publish_draft(args: argparse.Namespace) -> None:
    data = load_queue(QUEUE_FILE)
    draft = next((d for d in data.get('drafts', []) if d.get('id') == args.id), None)
    if not draft:
        raise SystemExit(f"Draft {args.id} not found")
    if draft.get('status') == 'published' and not args.force:
        print(f"Draft {args.id} already published ({draft.get('permalink')})")
        return

    publisher = RedditPublisher(
        client=build_client(args.mode),
        logger=StructuredLogger(Path(args.log_file)),
    )
    result = publisher.publish(RedditPayload.from_mapping(draft))
    update_draft_after_publish(args.id, result, QUEUE_FILE)
    print(json.dumps(result.to_dict(), indent=2))


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description='Manage Reddit drafts queue')
    parser.add_argument('--log-file', default=str(DEFAULT_LOG_FILE))
    sub = parser.add_subparsers(dest='command')

    sub.add_parser('list', help='List queued drafts')

    show_p = sub.add_parser('show', help='Display one draft as JSON')
    show_p.add_argument('--id', required=True)

    add_p = sub.add_parser('add', help='Add a draft manually')
    add_p.add_argument('--id', required=True)
    add_p.add_argument('--channel', default='manual')
    add_p.add_argument('--subreddit', required=False)
    add_p.add_argument('--title')
    add_p.add_argument('--body')
    add_p.add_argument('--url')
    add_p.add_argument('--kind', choices=['text', 'link', 'comment'], default='text')
    add_p.add_argument('--parent')

    pub_p = sub.add_parser('publish', help='Publish a queued draft locally')
    pub_p.add_argument('--id', required=True)
    pub_p.add_argument('--mode', choices=['dry-run', 'oauth'], default='dry-run')
    pub_p.add_argument('--force', action='store_true')

    args = parser.parse_args(argv)
    if args.command == 'list':
        list_drafts()
    elif args.command == 'show':
        show_draft(args)
    elif args.command == 'add':
        add_draft(args)
    elif args.command == 'publish':
        publish_draft(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
