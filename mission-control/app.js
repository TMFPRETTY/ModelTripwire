async function loadJson(name) {
  const res = await fetch(`./data/${name}`);
  if (!res.ok) throw new Error(`Failed to load ${name}`);
  return res.json();
}

function statusClass(status) {
  if (['healthy', 'active', 'ok'].includes(status)) return 'good';
  if (['warning'].includes(status)) return 'warn';
  if (['blocked', 'failed', 'error'].includes(status)) return 'bad';
  return 'quiet';
}

function fmt(ts) {
  if (!ts) return '—';
  return new Date(ts).toLocaleString();
}

function el(tag, cls, text) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text !== undefined) node.textContent = text;
  return node;
}

async function main() {
  const [overview, rooms, agents, jobs, alerts, activity, approvals] = await Promise.all([
    loadJson('overview.json'),
    loadJson('rooms.json'),
    loadJson('agents.json'),
    loadJson('jobs.json'),
    loadJson('alerts.json'),
    loadJson('activity.json'),
    loadJson('approvals.json'),
  ]);

  document.getElementById('generatedAt').textContent = `Updated ${fmt(overview.generatedAt)}`;

  const stats = overview.overview.globalHealth;
  const statItems = [
    ['System', stats.systemStatus],
    ['Active rooms', stats.activeRooms],
    ['Active agents', stats.activeAgents],
    ['Approvals', stats.pendingApprovals],
    ['Alerts', stats.openAlerts],
    ['Failing jobs', stats.failingJobs],
  ];
  const statsWrap = document.getElementById('stats');
  statItems.forEach(([label, value]) => {
    const card = el('div', 'stat');
    card.append(el('div', 'label', label));
    const val = el('div', 'value', String(value));
    card.append(val);
    statsWrap.append(card);
  });

  const needs = document.getElementById('needsAttention');
  (overview.overview.needsAttention.length ? overview.overview.needsAttention : [{title:'No urgent issues currently surfaced.'}]).forEach(item => {
    needs.append(el('li', '', item.title));
  });

  const focus = document.getElementById('recommendedFocus');
  overview.overview.recommendedFocus.forEach(item => focus.append(el('li', '', item)));

  const roomsGrid = document.getElementById('roomsGrid');
  rooms.rooms.forEach(room => {
    const card = el('div', `card ${statusClass(room.status)}`);
    card.append(el('div', 'title', room.name));
    const meta = el('div', 'meta');
    const badge = el('span', `badge ${room.status}`, room.status);
    meta.append(badge);
    meta.append(document.createTextNode(`  •  ${room.kind}`));
    card.append(meta);
    card.append(el('div', 'headline', room.headline));
    card.append(el('div', 'meta', `Last update: ${fmt(room.lastUpdateAt)}`));
    roomsGrid.append(card);
  });

  const activityFeed = document.getElementById('activityFeed');
  activity.activity.slice(0, 10).forEach(item => {
    const row = el('div', 'feed-item');
    row.append(el('div', 'title', `${item.roomId || 'system'} — ${item.title}`));
    row.append(el('div', 'meta', item.summary));
    row.append(el('div', 'meta', fmt(item.at)));
    activityFeed.append(row);
  });

  const jobsTable = document.getElementById('jobsTable');
  jobs.jobs.slice().sort((a,b) => (a.lastResult === 'failed' ? -1 : 1)).forEach(job => {
    const tr = document.createElement('tr');
    const status = `<span class="badge ${job.lastResult}">${job.lastResult}</span>`;
    tr.innerHTML = `<td>${job.name}</td><td>${job.roomId || '—'}</td><td>${status}</td><td>${fmt(job.lastRunAt)}</td><td>${fmt(job.nextRunAt)}</td>`;
    jobsTable.append(tr);
  });

  const alertsList = document.getElementById('alertsList');
  const alertItems = alerts.alerts.length ? alerts.alerts : [{title:'No open alerts.', summary:'System currently has no explicit alert items.', createdAt:null}];
  alertItems.forEach(item => {
    const row = el('div', 'feed-item');
    row.append(el('div', 'title', item.title));
    row.append(el('div', 'meta', item.summary));
    row.append(el('div', 'meta', fmt(item.createdAt)));
    alertsList.append(row);
  });

  const agentsGrid = document.getElementById('agentsGrid');
  agents.agents.forEach(agent => {
    const card = el('div', `card ${statusClass(agent.phase)}`);
    card.append(el('div', 'title', agent.name));
    const meta = el('div', 'meta');
    meta.append(el('span', `badge ${agent.phase}`, agent.phase));
    meta.append(document.createTextNode(`  •  room: ${agent.roomId || '—'}`));
    card.append(meta);
    card.append(el('div', 'headline', agent.mission));
    card.append(el('div', 'meta', `Skills: ${agent.skills.join(', ')}`));
    agentsGrid.append(card);
  });
}

main().catch(err => {
  document.body.innerHTML = `<pre style="color:white;padding:20px">Mission Control failed to load:\n${err.stack || err}</pre>`;
});
el('span', `badge ${agent.phase}`, agent.phase));
    meta.append(document.createTextNode(`  •  room: ${agent.roomId || '—'}`));
    card.append(meta);
    card.append(el('div', 'headline', agent.mission));
    card.append(el('div', 'meta', `Skills: ${agent.skills.join(', ')}`));
    agentsGrid.append(card);
  });
}

main().catch(err => {
  document.body.innerHTML = `<pre style="color:white;padding:20px">Mission Control failed to load:\n${err.stack || err}</pre>`;
});
