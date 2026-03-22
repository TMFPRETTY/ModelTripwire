#!/usr/bin/env python3
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path('/Users/jeremypretty/.openclaw/workspace')
DATA_DIR = WORKSPACE / 'mission-control' / 'data'
STATE_FILE = WORKSPACE / '.openclaw' / 'signalandcircuit-mail-monitor-state.json'

ROOMS = [
    {'id': 'command-center', 'name': 'command-center', 'channelId': '1484651751108775946', 'kind': 'command'},
    {'id': 'ops-desk', 'name': 'ops-desk', 'channelId': '1484651772193673349', 'kind': 'ops'},
    {'id': 'support-inbox', 'name': 'support-inbox', 'channelId': '1484651808772198462', 'kind': 'support'},
    {'id': 'caruso-growth', 'name': 'caruso-growth', 'channelId': '1484651836966436934', 'kind': 'growth'},
    {'id': 'caruso-product', 'name': 'caruso-product', 'channelId': '1484651869593669762', 'kind': 'product'},
    {'id': 'security-infra', 'name': 'security-infra', 'channelId': '1484651900812001491', 'kind': 'security'},
    {'id': 'research-lab', 'name': 'research-lab', 'channelId': '1484655635336265758', 'kind': 'research'},
    {'id': 'signal-and-circuit', 'name': 'signal-and-circuit', 'channelId': '1485042311959416832', 'kind': 'editorial'},
    {'id': 'engineering', 'name': 'engineering', 'channelId': '1484988049229086850', 'kind': 'engineering'},
]

AGENTS = [
    {'id': 'command-center', 'roomId': 'command-center', 'mission': 'Provide top-level mission control, priorities, blockers, approvals, and daily focus.', 'skills': ['command-center-digest'], 'phase': 'active', 'approvalBoundary': 'Summarizes and escalates; no external side effects.'},
    {'id': 'ops-desk', 'roomId': 'ops-desk', 'mission': 'Coordinate operations, failures, drift, queues, and next actions.', 'skills': ['ops-desk'], 'phase': 'active', 'approvalBoundary': 'Coordinates and reports; risky operational changes still require approval.'},
    {'id': 'caruso-growth', 'roomId': 'caruso-growth', 'mission': 'Find, package, and route growth opportunities for Caruso.', 'skills': ['caruso-growth'], 'phase': 'active', 'approvalBoundary': 'Public posting requires approval.'},
    {'id': 'caruso-product', 'roomId': 'caruso-product', 'mission': 'Convert support/growth/research/market signals into product recommendations.', 'skills': ['caruso-product'], 'phase': 'active', 'approvalBoundary': 'Recommendations are internal by default.'},
    {'id': 'security-infra', 'roomId': 'security-infra', 'mission': 'Monitor host/runtime health, security posture, and infrastructure drift.', 'skills': ['security-infra'], 'phase': 'active', 'approvalBoundary': 'Can inspect and recommend freely; impactful changes require approval.'},
    {'id': 'research-lab', 'roomId': 'research-lab', 'mission': 'Discover and rank business/SaaS/product opportunities.', 'skills': ['research-lab'], 'phase': 'active', 'approvalBoundary': 'Research and ranking only.'},
    {'id': 'engineering', 'roomId': 'engineering', 'mission': 'Shared implementation lane for code, debugging, automation changes, integrations, and code QA coordination.', 'skills': ['qa-review'], 'phase': 'active', 'approvalBoundary': 'High-risk changes require approval.'},
    {'id': 'qa-review', 'roomId': 'engineering', 'mission': 'Review outputs, code, automations, prompts, and configs for quality, correctness, and risk.', 'skills': ['qa-review'], 'phase': 'embedded', 'approvalBoundary': 'Can block/rework/recommend but not override human approvals.'},
    {'id': 'support-inbox', 'roomId': 'support-inbox', 'mission': 'Triage support mail, summarize issues, and prepare safe responses.', 'skills': ['support-triage'], 'phase': 'transitional', 'approvalBoundary': 'Sensitive replies require approval.'},
    {'id': 'signal-and-circuit', 'roomId': 'signal-and-circuit', 'mission': 'Combined room for editorial lookout, inbox activity, article routing, AdSense/site-quality work, and traffic growth.', 'skills': ['signal-and-circuit-adsense', 'signal-and-circuit-growth'], 'phase': 'transitional', 'approvalBoundary': 'Publishing and risky outward actions should remain controlled.'},
]


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def run_json(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise RuntimeError(res.stderr or res.stdout)
    return json.loads(res.stdout)


def run_text(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True, check=False)
    return (res.stdout + res.stderr).strip()


def room_for_job(name):
    mapping = {
        'morning-command-center-digest-weekdays-830am': 'command-center',
        'ops-desk-midday-status-weekdays-1pm': 'ops-desk',
        'caruso-marketing-opportunity-scan-every-4h': 'caruso-growth',
        'caruso-weekly-marketing-pack-mondays-9am': 'caruso-growth',
        'caruso-daily-reply-pack-weekdays-930am': 'caruso-growth',
        'caruso-reddit-draft-queue-weekdays-10am': 'caruso-growth',
        'caruso-competitor-watch-every-6h': 'caruso-growth',
        'caruso-product-signal-digest-weekdays-1230pm': 'caruso-product',
        'security-infra-daily-healthcheck-weekdays-845am': 'security-infra',
        'research-lab-weekly-idea-scan-mondays-11am': 'research-lab',
        'signalandcircuit-mail-monitor-every-2m': 'signal-and-circuit',
        'engineering-midday-intake-status-weekdays-2pm': 'engineering',
        'engineering-qa-review-check-weekdays-215pm': 'engineering',
        'gaming-trends-video-game-news-every-2h': 'retired',
    }
    return mapping.get(name)


def load_mail_state():
    if not STATE_FILE.exists():
        return {}
    return json.loads(STATE_FILE.read_text())


def build_jobs(cron_jobs):
    jobs = []
    for j in cron_jobs.get('jobs', []):
        st = j.get('state', {})
        last = st.get('lastRunStatus', 'unknown')
        status = 'paused' if not j.get('enabled', False) else ('warning' if last == 'error' else 'active')
        jobs.append({
            'id': j['id'],
            'name': j['name'],
            'roomId': room_for_job(j['name']),
            'status': status,
            'enabled': j.get('enabled', False),
            'lastRunAt': datetime.fromtimestamp(st['lastRunAtMs']/1000, tz=timezone.utc).isoformat().replace('+00:00','Z') if st.get('lastRunAtMs') else None,
            'nextRunAt': datetime.fromtimestamp(st['nextRunAtMs']/1000, tz=timezone.utc).isoformat().replace('+00:00','Z') if st.get('nextRunAtMs') else None,
            'lastResult': 'failed' if last == 'error' else ('ok' if last == 'ok' else 'unknown'),
            'recentFailureCount': st.get('consecutiveErrors', 0),
            'summary': st.get('lastError') or ('Running now' if st.get('runningAtMs') else 'Healthy'),
            'destination': {
                'type': j.get('delivery', {}).get('mode', 'none'),
                'channelId': (j.get('delivery', {}).get('to') or '').replace('channel:', '') if j.get('delivery', {}).get('to') else None,
            }
        })
    return jobs


def build_agents(jobs):
    by_room = {}
    by_agent = {}
    for job in jobs:
        if job['roomId']:
            by_room.setdefault(job['roomId'], []).append(job['id'])
    out = []
    for a in AGENTS:
        out.append({
            'id': a['id'],
            'name': a['id'],
            'status': a['phase'],
            'roomId': a['roomId'],
            'mission': a['mission'],
            'jobs': by_room.get(a['roomId'], []) if a['id'] != 'qa-review' else [],
            'skills': a['skills'],
            'approvalBoundary': a['approvalBoundary'],
            'phase': a['phase'],
        })
    return out


def build_rooms(jobs, mail_state):
    room_jobs = {}
    for job in jobs:
        room_jobs.setdefault(job['roomId'], []).append(job)
    pending_mail = len([i for i in mail_state.get('items', {}).values() if i.get('status') == 'pending'])
    rooms = []
    for room in ROOMS:
        rjobs = room_jobs.get(room['id'], [])
        failed = sum(1 for j in rjobs if j['lastResult'] == 'failed')
        running = any(j['summary'] == 'Running now' for j in rjobs)
        status = 'quiet'
        if failed:
            status = 'warning'
        elif rjobs:
            status = 'active' if running else 'healthy'
        headline = 'No live job activity yet.'
        if room['id'] == 'signal-and-circuit' and pending_mail:
            headline = f'{pending_mail} pending inbox item(s) in Signal and Circuit.'
        elif failed:
            headline = f'{failed} job issue(s) need attention.'
        elif rjobs:
            headline = 'Jobs healthy and delivering.'
        last_updates = [j['lastRunAt'] for j in rjobs if j.get('lastRunAt')]
        rooms.append({
            'id': room['id'],
            'name': room['name'],
            'channelId': room['channelId'],
            'status': status,
            'headline': headline,
            'lastUpdateAt': max(last_updates) if last_updates else None,
            'agents': [a['id'] for a in AGENTS if a['roomId'] == room['id'] and a['phase'] != 'planned'],
            'badges': {
                'approvals': 0,
                'alerts': failed,
                'queue': pending_mail if room['id'] == 'signal-and-circuit' else 0,
            },
            'kind': room['kind'],
        })
    return rooms


def build_alerts(jobs, rooms):
    alerts = []
    for job in jobs:
        if job['lastResult'] == 'failed' or job['recentFailureCount']:
            alerts.append({
                'id': f"alert-{job['id']}",
                'title': f"Job issue: {job['name']}",
                'roomId': job['roomId'],
                'severity': 'warning',
                'summary': job['summary'] or 'Recent failure detected.',
                'createdAt': job['lastRunAt'] or now_iso(),
                'status': 'open',
                'sourceType': 'job',
                'sourceRef': job['id'],
            })
    return alerts


def build_activity(jobs, alerts, approvals, mail_state):
    items = []
    for job in jobs:
        if job['lastRunAt']:
            items.append({
                'id': f"activity-{job['id']}",
                'roomId': job['roomId'],
                'kind': 'result',
                'title': job['name'],
                'summary': job['summary'],
                'priority': 'high' if job['lastResult'] == 'failed' else 'normal',
                'at': job['lastRunAt'],
                'sourceType': 'job',
                'sourceRef': job['id'],
            })
    for approval in approvals:
        items.append({
            'id': f"activity-{approval['id']}",
            'roomId': approval['roomId'],
            'kind': 'approval_request',
            'title': approval['title'],
            'summary': approval['summary'],
            'priority': 'high' if approval['risk'] in ('high','urgent') else 'normal',
            'at': approval['requestedAt'],
            'sourceType': 'approval',
            'sourceRef': approval['id'],
        })
    pending_mail = [i for i in mail_state.get('items', {}).values() if i.get('status') == 'pending']
    for item in pending_mail[:5]:
        items.append({
            'id': f"activity-mail-{item.get('gmailMessageId','unknown')}",
            'roomId': 'signal-and-circuit',
            'kind': 'email',
            'title': f"[EMAIL] {item.get('subject','(no subject)')}",
            'summary': item.get('summary') or item.get('from') or 'Pending inbox item',
            'priority': 'normal',
            'at': item.get('createdAt') or now_iso(),
            'sourceType': 'mail_state',
            'sourceRef': item.get('gmailMessageId'),
        })
    items.sort(key=lambda x: x['at'] or '', reverse=True)
    return items[:25]


def build_system(jobs, status_text):
    failing = sum(1 for j in jobs if j['lastResult'] == 'failed')
    warnings = sum(1 for j in jobs if j['status'] == 'warning')
    overall = 'healthy' if failing == 0 else 'warning'
    notes = []
    if 'Gateway status' in status_text:
        notes.append('OpenClaw status captured successfully.')
    if any(j['summary'] == 'Running now' for j in jobs):
        notes.append('One or more jobs are currently running.')
    return {
        'overallStatus': overall,
        'hostLabel': 'Jeremy’s MacBook Pro',
        'gatewayStatus': 'running' if 'running' in status_text.lower() or status_text else 'unknown',
        'runtime': 'openclaw',
        'activeJobCount': sum(1 for j in jobs if j['enabled']),
        'failingJobCount': failing,
        'warningCount': warnings,
        'notes': notes,
    }


def build_overview(rooms, agents, jobs, alerts, mail_state):
    needs = []
    if alerts:
        for a in alerts[:3]:
            needs.append({'title': a['title'], 'roomId': a['roomId'], 'priority': 'high'})
    pending_mail = len([i for i in mail_state.get('items', {}).values() if i.get('status') == 'pending'])
    if pending_mail:
        needs.append({'title': f'Signal and Circuit has {pending_mail} pending email item(s).', 'roomId': 'signal-and-circuit', 'priority': 'normal'})
    recs = [
        'Check the highest-priority warning room first.',
        'Review pending Signal and Circuit inbox items and hand engineering tasks off explicitly.',
        'Tune or retry any warning-status job before cutover.'
    ]
    return {
        'globalHealth': {
            'systemStatus': 'warning' if alerts else 'healthy',
            'activeRooms': len(rooms),
            'activeAgents': len([a for a in agents if a['phase'] in ('active', 'embedded')]),
            'pendingApprovals': 0,
            'openAlerts': len(alerts),
            'failingJobs': sum(1 for j in jobs if j['lastResult'] == 'failed'),
        },
        'needsAttention': needs[:5],
        'recommendedFocus': recs,
    }


def write_json(name, payload):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / name).write_text(json.dumps(payload, indent=2) + '\n')


def main():
    cron_jobs = run_json(['openclaw','cron','list','--json'])
    jobs = build_jobs(cron_jobs)
    agents = build_agents(jobs)
    mail_state = load_mail_state()
    rooms = build_rooms(jobs, mail_state)
    alerts = build_alerts(jobs, rooms)
    approvals = []
    activity = build_activity(jobs, alerts, approvals, mail_state)
    status_text = run_text(['openclaw','status'])
    system = build_system(jobs, status_text)
    overview = build_overview(rooms, agents, jobs, alerts, mail_state)
    generated = now_iso()
    write_json('rooms.json', {'generatedAt': generated, 'rooms': rooms})
    write_json('agents.json', {'generatedAt': generated, 'agents': agents})
    write_json('jobs.json', {'generatedAt': generated, 'jobs': jobs})
    write_json('system.json', {'generatedAt': generated, 'system': system})
    write_json('alerts.json', {'generatedAt': generated, 'alerts': alerts})
    write_json('approvals.json', {'generatedAt': generated, 'approvals': approvals})
    write_json('activity.json', {'generatedAt': generated, 'activity': activity})
    write_json('overview.json', {'generatedAt': generated, 'overview': overview})
    print('Mission Control snapshots generated in', DATA_DIR)

if __name__ == '__main__':
    main()
