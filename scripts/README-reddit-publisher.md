# Reddit Publisher

Local replacement for the old Devvit-backed Reddit publish flow.

## What it does

- Validates `text`, `link`, and `comment` payloads
- Supports `dry-run` mode with no Reddit credentials required
- Writes structured JSONL logs to `mission-control/data/reddit_publish_log.jsonl`
- Publishes queued drafts from `mission-control/data/reddit_queue.json`
- Supports a pluggable direct client; current live client uses Reddit OAuth via stdlib `urllib`

## CLI

### New standalone CLI

```bash
python3 scripts/reddit_publisher.py validate --kind text --subreddit SignalAndCircuit --title "Hello" --body "World"
python3 scripts/reddit_publisher.py publish --mode dry-run --kind link --subreddit SignalAndCircuit --title "Link" --url "https://example.com"
python3 scripts/reddit_publisher.py publish-draft --id R-TEST --mode dry-run
```

### Backward-compatible queue CLI

```bash
python3 scripts/publish_reddit_draft.py list
python3 scripts/publish_reddit_draft.py publish --id R-TEST --mode dry-run
```

## Live Reddit auth

Live publishing requires these environment variables:

- `REDDIT_CLIENT_ID`
- `REDDIT_CLIENT_SECRET`
- `REDDIT_USERNAME`
- `REDDIT_PASSWORD`
- optional: `REDDIT_USER_AGENT`

Example:

```bash
export REDDIT_CLIENT_ID=...
export REDDIT_CLIENT_SECRET=...
export REDDIT_USERNAME=...
export REDDIT_PASSWORD=...
export REDDIT_USER_AGENT='openclaw-reddit-publisher/0.1 by u/yourname'
python3 scripts/reddit_publisher.py publish-draft --id R-TEST --mode oauth
```

## Notes

- `text` posts require `subreddit`, `title`, and `body`
- `link` posts require `subreddit`, `title`, and `url`
- `comment` requires `parentId` and `body`
- Dry-run updates queue items to `published-dry-run` so the pipeline can verify end-to-end behavior without sending anything to Reddit
