# Signal and Circuit Mail Monitor

This monitor watches:

- editorial@signalandcircuit.com
- press@signalandcircuit.com
- advertising@signalandcircuit.com
- newsletter@signalandcircuit.com

It posts new mail into Discord channel `1484600889506533576`, creates a thread per email, and supports:

- `send`
- `reply: <your text>`
- `ignore`

## Files

- Script: `scripts/signalandcircuit_mail_monitor.py`
- State: `.openclaw/signalandcircuit-mail-monitor-state.json`

## Notes

- First run seeds the current inbox state and does **not** backfill old mail.
- Replies are sent from the same mailbox that received the original email.
- Suggested replies are simple rule-based drafts for now.
