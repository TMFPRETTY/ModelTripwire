#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

WORKSPACE = Path('/Users/jeremypretty/.openclaw/workspace')
STATE_DIR = WORKSPACE / '.openclaw'
STATE_FILE = STATE_DIR / 'signalandcircuit-mail-monitor-state.json'
CONFIG = {
    'guild_id': '1484525388054007969',
    'channel_id': '1484600889506533576',
    'accounts': [
        'editorial@signalandcircuit.com',
        'press@signalandcircuit.com',
        'advertising@signalandcircuit.com',
        'newsletter@signalandcircuit.com',
    ],
    'gmail_query': 'in:inbox newer_than:14d',
    'gmail_max': 20,
    'discord_scan_limit': 30,
}


def sh(cmd: List[str], input_text: Optional[str] = None) -> str:
    proc = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(cmd)}\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}")
    return proc.stdout


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_state() -> Dict[str, Any]:
    if not STATE_FILE.exists():
        return {
            'initialized': False,
            'createdAt': now_iso(),
            'updatedAt': now_iso(),
            'seen': {},
            'items': {},
            'threads': {},
        }
    return json.loads(STATE_FILE.read_text())


def save_state(state: Dict[str, Any]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state['updatedAt'] = now_iso()
    STATE_FILE.write_text(json.dumps(state, indent=2, sort_keys=True) + '\n')


def gog_messages(account: str) -> List[Dict[str, Any]]:
    out = sh([
        'gog', 'gmail', 'messages', 'search', CONFIG['gmail_query'],
        '--max', str(CONFIG['gmail_max']),
        '--include-body', '--json', '--account', account,
    ])
    data = json.loads(out)
    return data.get('messages', [])


def truncate(text: str, limit: int) -> str:
    text = re.sub(r'\s+', ' ', (text or '')).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + '…'


def extract_email(text: str) -> Optional[str]:
    m = re.search(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}', text or '', re.I)
    return m.group(0) if m else None


def classify(msg: Dict[str, Any]) -> Dict[str, str]:
    blob = ' '.join(filter(None, [msg.get('subject', ''), msg.get('from', ''), msg.get('body', '')])).lower()
    category = 'general'
    priority = 'medium'
    if any(k in blob for k in ['advertis', 'sponsor', 'media kit', 'rate card', 'campaign']):
        category = 'advertising'
    elif any(k in blob for k in ['press', 'interview', 'comment request', 'journalist', 'media inquiry']):
        category = 'press'
    elif any(k in blob for k in ['newsletter', 'subscribe', 'subscriber', 'issue', 'digest']):
        category = 'newsletter'
    elif any(k in blob for k in ['editorial', 'guest post', 'pitch', 'submission', 'article']):
        category = 'editorial'

    if any(k in blob for k in ['urgent', 'asap', 'deadline today', 'embargo lifts', 'breaking']):
        priority = 'high'
    elif any(k in blob for k in ['fyi', 'hello', 'checking in']):
        priority = 'low'

    if any(k in blob for k in ['unsubscribe', 'casino', 'seo service', 'crypto promo', 'guest post service']):
        category = 'spam'
        priority = 'low'

    return {'category': category, 'priority': priority}


def summarize(msg: Dict[str, Any]) -> Dict[str, str]:
    body = (msg.get('body') or '').replace('\r', ' ').replace('\n', ' ')
    summary = truncate(body or msg.get('subject', ''), 240) or 'No body text available.'
    meta = classify(msg)
    sender_email = extract_email(msg.get('from', '')) or 'unknown sender'
    recipient = msg.get('_account', '')
    category = meta['category']
    subject = msg.get('subject', '(no subject)')

    if category == 'spam':
        suggested = 'None. Likely spam / low-value outreach. Ignore unless you want to respond manually.'
    elif category == 'press':
        suggested = (
            f"Hi, thanks for reaching out to {recipient}. We received your press inquiry about \"{subject}\". "
            f"We’ll review the details and get back to you shortly."
        )
    elif category == 'advertising':
        suggested = (
            f"Hi, thanks for contacting {recipient}. We received your advertising inquiry about \"{subject}\". "
            f"Please send any relevant goals, budget, and timing if you haven’t already, and we’ll follow up shortly."
        )
    elif category == 'newsletter':
        suggested = (
            f"Hi, thanks for emailing {recipient}. We received your newsletter-related note about \"{subject}\" and will review it shortly."
        )
    else:
        suggested = (
            f"Hi, thanks for reaching out to {recipient}. We received your message about \"{subject}\" and will follow up shortly."
        )

    return {
        'summary': summary,
        'category': category,
        'priority': meta['priority'],
        'suggested_reply': suggested,
        'sender_email': sender_email,
    }


def discord_send(channel_id: str, message: str) -> Dict[str, Any]:
    out = sh([
        'openclaw', 'message', 'send', '--channel', 'discord', '--target', f'channel:{channel_id}', '--json', '-m', message
    ])
    return json.loads(out)


def discord_thread_create(channel_id: str, message_id: str, name: str, initial_message: str) -> Dict[str, Any]:
    out = sh([
        'openclaw', 'message', 'thread', 'create', '--channel', 'discord', '--target', f'channel:{channel_id}', '--message-id', message_id,
        '--thread-name', name, '--json', '-m', initial_message
    ])
    return json.loads(out)


def discord_read(target: str, limit: int = 20, include_thread: bool = False) -> Dict[str, Any]:
    cmd = ['openclaw', 'message', 'read', '--channel', 'discord', '--target', target, '--limit', str(limit), '--json']
    if include_thread:
        cmd.append('--include-thread')
    out = sh(cmd)
    return json.loads(out)


def discord_thread_reply(thread_target: str, message: str) -> Dict[str, Any]:
    out = sh([
        'openclaw', 'message', 'thread', 'reply', '--channel', 'discord', '--target', thread_target, '--json', '-m', message
    ])
    return json.loads(out)


def parse_message_payload(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    p = payload.get('payload', {})
    if isinstance(p, dict):
        if isinstance(p.get('messages'), list):
            return p['messages']
        if isinstance(p.get('items'), list):
            return p['items']
        if isinstance(p.get('data'), list):
            return p['data']
    return []


def get_author_id(msg: Dict[str, Any]) -> Optional[str]:
    for key in ('authorId', 'senderId', 'userId'):
        if msg.get(key):
            return str(msg[key])
    author = msg.get('author') or msg.get('sender') or {}
    if isinstance(author, dict):
        for key in ('id', 'userId'):
            if author.get(key):
                return str(author[key])
    return None


def get_message_id(msg: Dict[str, Any]) -> Optional[str]:
    for key in ('id', 'messageId'):
        if msg.get(key):
            return str(msg[key])
    return None


def get_message_text(msg: Dict[str, Any]) -> str:
    for key in ('text', 'message', 'body', 'content'):
        val = msg.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()
    return ''


def get_send_message_id(payload: Dict[str, Any]) -> Optional[str]:
    p = payload.get('payload', {})
    candidates = [p, p.get('message') if isinstance(p, dict) else None]
    for obj in candidates:
        if isinstance(obj, dict):
            for key in ('id', 'messageId'):
                if obj.get(key):
                    return str(obj[key])
    return None


def get_thread_target(payload: Dict[str, Any]) -> Optional[str]:
    p = payload.get('payload', {})
    candidates = [p, p.get('thread') if isinstance(p, dict) else None]
    for obj in candidates:
        if isinstance(obj, dict):
            for key in ('id', 'threadId', 'channelId'):
                if obj.get(key):
                    return str(obj[key])
    return None


def format_alert(msg: Dict[str, Any], info: Dict[str, str]) -> str:
    return '\n'.join([
        'New Signal and Circuit email',
        f"- Inbox: {msg['_account']}",
        f"- From: {msg.get('from', 'Unknown')}",
        f"- Subject: {msg.get('subject', '(no subject)')}",
        f"- Category: {info['category']}",
        f"- Priority: {info['priority']}",
        f"- Summary: {info['summary']}",
        f"- Suggested reply: {info['suggested_reply']}",
        '- Actions: open the thread and reply with `send`, `reply: <your text>`, or `ignore`.',
    ])


def format_thread_intro(msg: Dict[str, Any], info: Dict[str, str]) -> str:
    return '\n'.join([
        f"Tracking email `{msg['id']}`",
        f"Mailbox: {msg['_account']}",
        f"Sender email: {info['sender_email']}",
        f"Original subject: {msg.get('subject', '(no subject)')}",
        f"Suggested reply:\n{info['suggested_reply']}",
        '',
        'Commands:',
        '- `send` → send the suggested reply',
        '- `reply: <your text>` → send your manual reply',
        '- `ignore` → mark handled with no reply',
    ])


def send_gmail_reply(item: Dict[str, Any], body: str) -> None:
    subject = item.get('subject') or '(no subject)'
    with tempfile.NamedTemporaryFile('w', delete=False) as f:
        f.write(body.strip() + '\n')
        temp_path = f.name
    try:
        sh([
            'gog', 'gmail', 'send',
            '--account', item['account'],
            '--reply-all',
            '--reply-to-message-id', item['gmailMessageId'],
            '--subject', f"Re: {subject}",
            '--body-file', temp_path,
        ])
    finally:
        try:
            os.unlink(temp_path)
        except FileNotFoundError:
            pass


def bootstrap(state: Dict[str, Any]) -> None:
    for account in CONFIG['accounts']:
        state['seen'].setdefault(account, [])
        for msg in gog_messages(account):
            if msg.get('id'):
                state['seen'][account].append(msg['id'])
        state['seen'][account] = sorted(set(state['seen'][account]))[-500:]
    state['initialized'] = True
    save_state(state)
    discord_send(CONFIG['channel_id'], 'Signal and Circuit mail monitor is live. I seeded the current inbox state and will alert here for new email going forward.')


def detect_new_messages(state: Dict[str, Any]) -> List[Dict[str, Any]]:
    fresh: List[Dict[str, Any]] = []
    for account in CONFIG['accounts']:
        state['seen'].setdefault(account, [])
        seen = set(state['seen'][account])
        msgs = gog_messages(account)
        for msg in reversed(msgs):
            msg_id = msg.get('id')
            if not msg_id:
                continue
            if msg_id in seen:
                continue
            msg['_account'] = account
            fresh.append(msg)
            state['seen'][account].append(msg_id)
        state['seen'][account] = sorted(set(state['seen'][account]))[-500:]
    return fresh


def create_tracking_thread(state: Dict[str, Any], msg: Dict[str, Any]) -> None:
    info = summarize(msg)
    alert = format_alert(msg, info)
    send_payload = discord_send(CONFIG['channel_id'], alert)
    parent_message_id = get_send_message_id(send_payload)
    if not parent_message_id:
        raise RuntimeError(f'Could not determine Discord message id from send payload: {json.dumps(send_payload)}')
    thread_name = truncate((msg.get('subject') or 'email')[:80], 80)
    thread_payload = discord_thread_create(CONFIG['channel_id'], parent_message_id, thread_name, format_thread_intro(msg, info))
    thread_target = get_thread_target(thread_payload)
    if not thread_target:
        raise RuntimeError(f'Could not determine Discord thread id from thread payload: {json.dumps(thread_payload)}')
    state['items'][msg['id']] = {
        'gmailMessageId': msg['id'],
        'threadId': msg.get('threadId'),
        'account': msg['_account'],
        'from': msg.get('from'),
        'subject': msg.get('subject'),
        'summary': info['summary'],
        'suggested_reply': info['suggested_reply'],
        'status': 'pending',
        'discordParentMessageId': parent_message_id,
        'discordThreadTarget': thread_target,
        'createdAt': now_iso(),
    }
    state['threads'][thread_target] = {
        'gmailMessageId': msg['id'],
        'lastProcessedDiscordMessageId': None,
        'status': 'pending',
    }


def process_thread_commands(state: Dict[str, Any]) -> None:
    for thread_target, thread_meta in list(state.get('threads', {}).items()):
        gmail_id = thread_meta['gmailMessageId']
        item = state['items'].get(gmail_id)
        if not item or item.get('status') != 'pending':
            continue
        payload = discord_read(thread_target, limit=CONFIG['discord_scan_limit'])
        messages = parse_message_payload(payload)
        if not messages:
            continue
        messages = list(reversed(messages))
        last_seen = thread_meta.get('lastProcessedDiscordMessageId')
        started = last_seen is None
        for msg in messages:
            msg_id = get_message_id(msg)
            if not msg_id:
                continue
            if not started:
                if msg_id == last_seen:
                    started = True
                continue
            text = get_message_text(msg).strip()
            if not text:
                thread_meta['lastProcessedDiscordMessageId'] = msg_id
                continue
            author_id = get_author_id(msg)
            if author_id == '1484526071687811082':
                thread_meta['lastProcessedDiscordMessageId'] = msg_id
                continue
            lower = text.lower()
            if lower == 'send':
                send_gmail_reply(item, item['suggested_reply'])
                item['status'] = 'sent-suggested'
                thread_meta['status'] = item['status']
                discord_thread_reply(thread_target, f"Sent suggested reply from {item['account']}.")
            elif lower.startswith('reply:'):
                body = text.split(':', 1)[1].strip()
                if body:
                    send_gmail_reply(item, body)
                    item['status'] = 'sent-manual'
                    item['manual_reply'] = body
                    thread_meta['status'] = item['status']
                    discord_thread_reply(thread_target, f"Sent manual reply from {item['account']}.")
                else:
                    discord_thread_reply(thread_target, 'I saw `reply:` but no text after it. Send `reply: <your text>`.')
            elif lower == 'ignore':
                item['status'] = 'ignored'
                thread_meta['status'] = 'ignored'
                discord_thread_reply(thread_target, 'Marked ignored. No email sent.')
            thread_meta['lastProcessedDiscordMessageId'] = msg_id


def main() -> int:
    state = load_state()
    if not state.get('initialized'):
        bootstrap(state)
        return 0
    fresh = detect_new_messages(state)
    for msg in fresh:
        create_tracking_thread(state, msg)
    process_thread_commands(state)
    save_state(state)
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise
