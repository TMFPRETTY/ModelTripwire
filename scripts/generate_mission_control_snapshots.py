#!/usr/bin/env python3
import json
import os
import platform
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
WORKSPACE = HOME / '.openclaw' / 'workspace'
DATA_DIR = WORKSPACE / 'mission-control' / 'data'
GAME_DATA_DIR = WORKSPACE / 'mission-control' / 'game' / 'data'
STATE_FILE = WORKSPACE / '.openclaw' / 'signalandcircuit-mail-monitor-state.json'
OPENCLAW_BIN = shutil.which('openclaw') or '/Users/tmfprettybot/.nvm/versions/node/v22.22.1/bin/openclaw'
HOST_LABEL = os.environ.get('MISSION_CONTROL_HOST_LABEL') or platform.node() or 'Local host'
GAME_REPO = Path('/Users/tmfprettybot/Documents/Game/Untitled-2d-Isometric-RPG')

ROOMS = [
    {'id': 'command-center', 'name': 'command-center', 'channelId': '1484651751108775946', 'kind': 'command'},
    {'id': 'ops-desk', 'name': 'ops-desk', 'channelId': '1484651772193673349', 'kind': 'ops'},
    {'id': 'support-inbox', 'name': 'support-inbox', 'channelId': '1484651808772198462', 'kind': 'support'},
    {'id': 'caruso-growth', 'name': 'caruso-growth', 'channelId': '1484651836966436934', 'kind': 'growth'},
    {'id': 'caruso-product', 'name': 'caruso-product', 'channelId': '1484651869593669762', 'kind': 'product'},
    {'id': 'caruso-product-lab', 'name': 'caruso-product-lab', 'channelId': '1486097589760950282', 'kind': 'product-lab'},
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
    {'id': 'caruso-product-lab', 'roomId': 'caruso-product-lab', 'mission': 'Explore rough product ideas, refine concepts, and ground product thinking in the real Caruso codebase and README files.', 'skills': ['caruso-product-lab'], 'phase': 'active', 'approvalBoundary': 'Exploration and internal drafts are fine; commitments and implementation still require handoff or approval.'},
    {'id': 'security-infra', 'roomId': 'security-infra', 'mission': 'Monitor host/runtime health, security posture, and infrastructure drift.', 'skills': ['security-infra'], 'phase': 'active', 'approvalBoundary': 'Can inspect and recommend freely; impactful changes require approval.'},
    {'id': 'research-lab', 'roomId': 'research-lab', 'mission': 'Discover and rank business/SaaS/product opportunities.', 'skills': ['research-lab'], 'phase': 'active', 'approvalBoundary': 'Research and ranking only.'},
    {'id': 'engineering', 'roomId': 'engineering', 'mission': 'Shared implementation lane for code, debugging, automation changes, integrations, and code QA coordination.', 'skills': ['qa-review'], 'phase': 'active', 'approvalBoundary': 'High-risk changes require approval.'},
    {'id': 'qa-review', 'roomId': 'engineering', 'mission': 'Review outputs, code, automations, prompts, and configs for quality, correctness, and risk.', 'skills': ['qa-review'], 'phase': 'embedded', 'approvalBoundary': 'Can block/rework/recommend but not override human approvals.'},
    {'id': 'support-inbox', 'roomId': 'support-inbox', 'mission': 'Triage support mail, summarize issues, and prepare safe responses.', 'skills': ['support-triage'], 'phase': 'transitional', 'approvalBoundary': 'Sensitive replies require approval.'},
    {'id': 'signal-and-circuit', 'roomId': 'signal-and-circuit', 'mission': 'Combined room for editorial lookout, inbox activity, article routing, AdSense/site-quality work, and traffic growth.', 'skills': ['signal-and-circuit-adsense', 'signal-and-circuit-growth'], 'phase': 'transitional', 'approvalBoundary': 'Publishing and risky outward actions should remain controlled.'},
]


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def _cmd(cmd):
    if cmd and cmd[0] == 'openclaw':
        return [OPENCLAW_BIN] + cmd[1:]
    return cmd


def run_json(cmd):
    res = subprocess.run(_cmd(cmd), capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise RuntimeError(res.stderr or res.stdout)
    return json.loads(res.stdout)


def run_text(cmd):
    res = subprocess.run(_cmd(cmd), capture_output=True, text=True, check=False)
    return (res.stdout + res.stderr).strip()


def room_for_job(name):
    mapping = {
        'morning-command-center-digest-weekdays-830am': 'command-center',
        'ops-desk-midday-status-weekdays-1pm': 'ops-desk',
        'caruso-marketing-opportunity-scan-every-4h': 'caruso-growth',
        'caruso-marketing-opportunity-scan-daily-1115am': 'caruso-growth',
        'caruso-weekly-marketing-pack-mondays-9am': 'caruso-growth',
        'caruso-daily-reply-pack-weekdays-930am': 'caruso-growth',
        'caruso-reddit-draft-queue-weekdays-10am': 'caruso-growth',
        'caruso-competitor-watch-every-6h': 'caruso-growth',
        'caruso-competitor-watch-daily-530pm': 'caruso-growth',
        'caruso-product-signal-digest-weekdays-1230pm': 'caruso-product',
        'daily-cross-room-standup-weekdays-915am': 'command-center',
        'engineering-context-sync-weekdays-145pm': 'engineering',
        'security-infra-daily-healthcheck-weekdays-845am': 'security-infra',
        'research-lab-weekly-idea-scan-mondays-11am': 'research-lab',
        'signalandcircuit-mail-monitor-every-2m': 'signal-and-circuit',
        'engineering-midday-intake-status-weekdays-2pm': 'engineering',
        'engineering-qa-review-check-weekdays-215pm': 'engineering',
        'mission-control-snapshot-refresh-every-5m': 'command-center',
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


def build_approvals(mail_state, jobs):
    approvals = []
    pending_mail = [i for i in mail_state.get('items', {}).values() if i.get('status') == 'pending']
    for idx, item in enumerate(pending_mail[:10], start=1):
        subject = item.get('subject', '(no subject)')
        summary = item.get('summary') or item.get('from') or 'Pending email item requires review/triage.'
        risk = 'medium'
        lowered = f"{subject} {summary}".lower()
        if any(k in lowered for k in ['urgent', 'asap', 'access', 'billing', 'sponsor', 'advertis', 'press']):
            risk = 'high'
        approvals.append({
            'id': f"approval-mail-{item.get('gmailMessageId', idx)}",
            'title': f"Review Signal and Circuit email: {subject}",
            'roomId': 'signal-and-circuit',
            'risk': risk,
            'decisionType': 'review',
            'summary': summary,
            'requestedAt': item.get('createdAt') or now_iso(),
            'status': 'pending'
        })
    for job in jobs:
        if job['roomId'] == 'caruso-growth' and job['lastResult'] == 'failed':
            approvals.append({
                'id': f"approval-job-{job['id']}",
                'title': 'Decide how to handle Caruso growth rate limit issue',
                'roomId': 'caruso-growth',
                'risk': 'medium',
                'decisionType': 'review',
                'summary': job['summary'] or 'Caruso growth scan is failing and may need retry/tuning.',
                'requestedAt': job['lastRunAt'] or now_iso(),
                'status': 'pending'
            })
    return approvals


def build_alerts(jobs, mail_state):
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
    pending_mail = [i for i in mail_state.get('items', {}).values() if i.get('status') == 'pending']
    if pending_mail:
        alerts.append({
            'id': 'alert-signal-and-circuit-pending-mail',
            'title': 'Signal and Circuit inbox needs triage',
            'roomId': 'signal-and-circuit',
            'severity': 'warning' if len(pending_mail) < 5 else 'critical',
            'summary': f'{len(pending_mail)} pending inbox item(s) are still open in the mail monitor state.',
            'createdAt': pending_mail[0].get('createdAt') or now_iso(),
            'status': 'open',
            'sourceType': 'mail_state',
            'sourceRef': 'signalandcircuit-mail-monitor-state'
        })
    return alerts


def build_rooms(jobs, mail_state, approvals, alerts):
    room_jobs = {}
    for job in jobs:
        room_jobs.setdefault(job['roomId'], []).append(job)
    pending_mail = len([i for i in mail_state.get('items', {}).values() if i.get('status') == 'pending'])
    rooms = []
    for room in ROOMS:
        rjobs = room_jobs.get(room['id'], [])
        failed = sum(1 for j in rjobs if j['lastResult'] == 'failed')
        running = any(j['summary'] == 'Running now' for j in rjobs)
        room_approvals = [a for a in approvals if a.get('roomId') == room['id']]
        room_alerts = [a for a in alerts if a.get('roomId') == room['id']]
        status = 'quiet'
        if failed or room_alerts:
            status = 'warning'
        elif rjobs:
            status = 'active' if running else 'healthy'
        headline = 'No live job activity yet.'
        if room['id'] == 'signal-and-circuit' and pending_mail:
            headline = f'{pending_mail} pending inbox item(s) need triage.'
        elif room['id'] == 'caruso-growth' and failed:
            headline = 'Growth scan hit a rate limit and may need retry/tuning.'
        elif room['id'] == 'engineering' and room_approvals:
            headline = f'{len(room_approvals)} item(s) waiting on engineering/QA follow-through.'
        elif room['id'] == 'caruso-product-lab':
            headline = 'Exploratory product room for codebase-grounded ideation and concept refinement.'
        elif room['id'] == 'support-inbox' and room_approvals:
            headline = f'{len(room_approvals)} support item(s) likely need human approval.'
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
                'approvals': len(room_approvals),
                'alerts': len(room_alerts) or failed,
                'queue': pending_mail if room['id'] == 'signal-and-circuit' else 0,
            },
            'kind': room['kind'],
        })
    return rooms


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
            'priority': 'high' if approval['risk'] in ('high', 'urgent') else 'normal',
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
        'hostLabel': HOST_LABEL,
        'gatewayStatus': 'running' if 'running' in status_text.lower() or status_text else 'unknown',
        'runtime': 'openclaw',
        'activeJobCount': sum(1 for j in jobs if j['enabled']),
        'failingJobCount': failing,
        'warningCount': warnings,
        'notes': notes,
    }


def build_overview(rooms, agents, jobs, alerts, approvals, mail_state):
    needs = []
    if alerts:
        for a in alerts[:4]:
            needs.append({'title': a['title'], 'roomId': a['roomId'], 'priority': 'high'})
    pending_mail = len([i for i in mail_state.get('items', {}).values() if i.get('status') == 'pending'])
    if pending_mail and not any(n['roomId'] == 'signal-and-circuit' for n in needs):
        needs.append({'title': f'Signal and Circuit has {pending_mail} pending email item(s).', 'roomId': 'signal-and-circuit', 'priority': 'normal'})
    recs = []
    if any(j['roomId'] == 'caruso-growth' and j['lastResult'] == 'failed' for j in jobs):
        recs.append('Retry or tune the Caruso marketing opportunity scan after the rate limit issue.')
    if pending_mail:
        recs.append('Review pending Signal and Circuit inbox items and hand engineering tasks off explicitly.')
    if not recs:
        recs.append('Check the highest-priority room first and verify outputs still feel useful.')
    recs.append('Use engineering + QA loop for any implementation work that moves out of planning rooms.')
    return {
        'globalHealth': {
            'systemStatus': 'warning' if alerts else 'healthy',
            'activeRooms': len(rooms),
            'activeAgents': len([a for a in agents if a['phase'] in ('active', 'embedded')]),
            'pendingApprovals': len(approvals),
            'openAlerts': len(alerts),
            'failingJobs': sum(1 for j in jobs if j['lastResult'] == 'failed'),
        },
        'needsAttention': needs[:5],
        'recommendedFocus': recs[:3],
    }


def write_json(name, payload, base_dir=DATA_DIR):
    base_dir.mkdir(parents=True, exist_ok=True)
    (base_dir / name).write_text(json.dumps(payload, indent=2) + '\n')


def build_game_rooms():
    return [
        {'id': 'game-dev', 'name': 'game-dev', 'channelId': '1485801109087060018', 'kind': 'studio-hq'},
        {'id': 'game-design', 'name': 'game-design', 'channelId': '1485809313653063700', 'kind': 'design'},
        {'id': 'game-engineering', 'name': 'game-engineering', 'channelId': '1485809436890239086', 'kind': 'engineering'},
        {'id': 'game-qa', 'name': 'game-qa', 'channelId': '1485809535560974456', 'kind': 'qa'},
    ]


def build_game_agents():
    return [
        {'id': 'game-dev', 'name': 'game-dev', 'roomId': 'game-dev', 'phase': 'active', 'mission': 'Main game project room for direction, priorities, prompts, and cross-functional coordination.', 'model': 'openai/gpt-5.1-codex'},
        {'id': 'game-design', 'name': 'game-design', 'roomId': 'game-design', 'phase': 'active', 'mission': 'Design room for systems, AI, economy, UX, and player-experience questions.', 'model': 'openai-codex/gpt-5.4'},
        {'id': 'game-engineering', 'name': 'game-engineering', 'roomId': 'game-engineering', 'phase': 'active', 'mission': 'Implementation room for code, debugging, architecture, tools, and builds.', 'model': 'openai-codex/gpt-5.4'},
        {'id': 'game-qa', 'name': 'game-qa', 'roomId': 'game-qa', 'phase': 'active', 'mission': 'Validation room for QA review, exploit pressure, regression checks, and release confidence.', 'model': 'openai/gpt-5.1-codex'},
        {'id': 'Chief of Staff', 'name': 'Chief of Staff', 'roomId': 'game-dev', 'phase': 'embedded', 'mission': 'Studio coordination, synthesis, prioritization, and conflict resolution.', 'model': None},
        {'id': 'Game Director', 'name': 'Game Director', 'roomId': 'game-dev', 'phase': 'embedded', 'mission': 'Protects vision, fun, cohesion, and core fantasy.', 'model': None},
        {'id': 'Executive Producer', 'name': 'Executive Producer', 'roomId': 'game-dev', 'phase': 'embedded', 'mission': 'Protects scope realism, production sequencing, and ship viability.', 'model': None},
        {'id': 'Technical Director', 'name': 'Technical Director', 'roomId': 'game-engineering', 'phase': 'embedded', 'mission': 'Protects architecture, maintainability, and technical debt control.', 'model': None},
        {'id': 'Head of QA', 'name': 'Head of QA', 'roomId': 'game-qa', 'phase': 'embedded', 'mission': 'Defines quality standards, coverage priorities, and release confidence.', 'model': None},
    ]


def build_game_snapshot():
    rooms_seed = build_game_rooms()
    agents = build_game_agents()
    rooms = []
    for room in rooms_seed:
        rooms.append({
            'id': room['id'],
            'name': room['name'],
            'channelId': room['channelId'],
            'status': 'healthy',
            'headline': {
                'game-dev': 'Studio HQ online. Use this room for direction, prompts, scope calls, and cross-functional decisions.',
                'game-design': 'Design room ready for systems, UX, economy, AI, and player-experience work.',
                'game-engineering': 'Engineering room ready for repo work, debugging, architecture, and implementation tasks.',
                'game-qa': 'QA room ready for review passes, exploit pressure, and release confidence checks.',
            }.get(room['id'], 'Room online.'),
            'lastUpdateAt': now_iso(),
            'agents': [a['name'] for a in agents if a['roomId'] == room['id']],
            'badges': {'approvals': 0, 'alerts': 0, 'queue': 0},
            'kind': room['kind'],
        })
    activity = [
        {
            'id': 'game-activity-bootstrap',
            'roomId': 'game-dev',
            'kind': 'bootstrap',
            'title': 'Game studio rooms wired',
            'summary': 'Game Mission Control is online with dev, design, engineering, and QA rooms plus the initial specialist roster.',
            'priority': 'normal',
            'at': now_iso(),
            'sourceType': 'workspace',
            'sourceRef': 'GAME_PROJECT_OPERATING_SPEC.md',
        }
    ]
    overview = {
        'globalHealth': {
            'systemStatus': 'healthy',
            'activeRooms': len(rooms),
            'activeAgents': len(agents),
            'pendingApprovals': 0,
            'openAlerts': 0,
            'failingJobs': 0,
            'connectedChannels': len(rooms),
            'mode': 'live-room routing',
        },
        'needsAttention': [
            {'title': 'Start sending real prompts into the game rooms to generate live room traffic and workflow history.', 'roomId': 'game-dev', 'priority': 'normal'},
            {'title': 'Use game-engineering -> game-qa as the default implementation/review loop.', 'roomId': 'game-qa', 'priority': 'normal'},
        ],
        'recommendedFocus': [
            'Use game-dev for top-level game asks, routing, and studio decisions.',
            'Use game-design for systems, UX, AI, economy, and player-facing design refinement.',
            'Use game-engineering and game-qa as the build-and-review loop before work is treated as complete.',
        ],
    }
    system = {
        'overallStatus': 'healthy',
        'hostLabel': HOST_LABEL,
        'gatewayStatus': 'running',
        'runtime': 'openclaw-game-studio',
        'activeJobCount': 0,
        'failingJobCount': 0,
        'warningCount': 0,
        'notes': [
            'Game Mission Control is a separate studio-side view layered on top of the same host.',
            f'Game repo anchored at {GAME_REPO}',
        ],
    }
    generated = now_iso()
    write_json('rooms.json', {'generatedAt': generated, 'rooms': rooms}, base_dir=GAME_DATA_DIR)
    write_json('agents.json', {'generatedAt': generated, 'agents': agents}, base_dir=GAME_DATA_DIR)
    write_json('activity.json', {'generatedAt': generated, 'activity': activity}, base_dir=GAME_DATA_DIR)
    write_json('overview.json', {'generatedAt': generated, 'overview': overview}, base_dir=GAME_DATA_DIR)
    write_json('system.json', {'generatedAt': generated, 'system': system}, base_dir=GAME_DATA_DIR)


def main():
    cron_jobs = run_json(['openclaw', 'cron', 'list', '--json'])
    jobs = build_jobs(cron_jobs)
    agents = build_agents(jobs)
    mail_state = load_mail_state()
    approvals = build_approvals(mail_state, jobs)
    alerts = build_alerts(jobs, mail_state)
    rooms = build_rooms(jobs, mail_state, approvals, alerts)
    activity = build_activity(jobs, alerts, approvals, mail_state)
    status_text = run_text(['openclaw', 'status'])
    system = build_system(jobs, status_text)
    overview = build_overview(rooms, agents, jobs, alerts, approvals, mail_state)
    generated = now_iso()
    write_json('rooms.json', {'generatedAt': generated, 'rooms': rooms})
    write_json('agents.json', {'generatedAt': generated, 'agents': agents})
    write_json('jobs.json', {'generatedAt': generated, 'jobs': jobs})
    write_json('system.json', {'generatedAt': generated, 'system': system})
    write_json('alerts.json', {'generatedAt': generated, 'alerts': alerts})
    write_json('approvals.json', {'generatedAt': generated, 'approvals': approvals})
    write_json('activity.json', {'generatedAt': generated, 'activity': activity})
    write_json('overview.json', {'generatedAt': generated, 'overview': overview})
    build_game_snapshot()
    print('Mission Control snapshots generated in', DATA_DIR, 'and', GAME_DATA_DIR)


if __name__ == '__main__':
    main()
