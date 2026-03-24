async function loadJson(name) {
  const res = await fetch(`./data/${name}`);
  if (!res.ok) throw new Error(`Failed to load ${name}`);
  return res.json();
}

function statusClass(status) {
  if (['healthy', 'active', 'ok'].includes(status)) return 'good';
  if (['warning'].includes(status)) return 'warn';
  if (['blocked', 'failed', 'error', 'critical'].includes(status)) return 'bad';
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
  const [overview, rooms, agents, activity] = await Promise.all([
    loadJson('overview.json'),
    loadJson('rooms.json'),
    loadJson('agents.json'),
    loadJson('activity.json'),
  ]);

  document.getElementById('generatedAt').textContent = `Updated ${fmt(overview.generatedAt)}`;

  const stats = overview.overview.globalHealth;
  const statItems = [
    ['Studio', stats.systemStatus],
    ['Active rooms', stats.activeRooms],
    ['Studio roles', stats.activeAgents],
    ['Open risks', stats.openAlerts],
    ['Game channels', stats.connectedChannels],
    ['HQ mode', stats.mode],
  ];
  const statsWrap = document.getElementById('stats');
  statItems.forEach(([label, value]) => {
    const card = el('div', 'stat');
    card.append(el('div', 'label', label));
    card.append(el('div', 'value', String(value)));
    statsWrap.append(card);
  });

  const needs = document.getElementById('needsAttention');
  (overview.overview.needsAttention.length ? overview.overview.needsAttention : [{ title: 'No urgent game-side issues surfaced yet.' }]).forEach(item => {
    needs.append(el('li', '', item.title));
  });

  const focus = document.getElementById('recommendedFocus');
  overview.overview.recommendedFocus.forEach(item => focus.append(el('li', '', item)));

  const roomsGrid = document.getElementById('roomsGrid');
  rooms.rooms.forEach(room => {
    const card = el('div', `card ${statusClass(room.status)}`);
    card.append(el('div', 'title', room.name));
    const meta = el('div', 'meta');
    meta.append(el('span', `badge ${room.status}`, room.status));
    meta.append(document.createTextNode(`  •  ${room.kind}`));
    card.append(meta);
    card.append(el('div', 'headline', room.headline));
    card.append(el('div', 'meta', `Channel: ${room.channelId}`));
    card.append(el('div', 'meta', `Roles: ${room.agents.join(', ')}`));
    roomsGrid.append(card);
  });

  const agentsGrid = document.getElementById('agentsGrid');
  agents.agents.forEach(agent => {
    const card = el('div', `card ${statusClass(agent.phase || 'active')}`);
    card.append(el('div', 'title', agent.name));
    const meta = el('div', 'meta');
    meta.append(el('span', `badge ${agent.phase || 'active'}`, agent.phase || 'active'));
    meta.append(document.createTextNode(`  •  room: ${agent.roomId || '—'}`));
    card.append(meta);
    card.append(el('div', 'headline', agent.mission));
    if (agent.model) card.append(el('div', 'meta', `Model: ${agent.model}`));
    agentsGrid.append(card);
  });

  const activityFeed = document.getElementById('activityFeed');
  (activity.activity.length ? activity.activity : [{ title: 'Studio structure initialized.', summary: 'Game Mission Control is online and waiting for live room traffic.', at: null }]).forEach(item => {
    const row = el('div', 'feed-item');
    row.append(el('div', 'title', `${item.roomId || 'studio'} — ${item.title}`));
    row.append(el('div', 'meta', item.summary));
    row.append(el('div', 'meta', fmt(item.at)));
    activityFeed.append(row);
  });
}

main().catch(err => {
  document.body.innerHTML = `<pre style="color:white;padding:20px">Game Mission Control failed to load:\n${err.stack || err}</pre>`;
});
