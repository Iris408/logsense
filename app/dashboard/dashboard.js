/* LogSense read-only dashboard: safe DOM rendering, no external libraries. */
'use strict';

const $ = (id) => document.getElementById(id);
let storedRows = [];
const severityOrder = ['INFO', 'WARNING', 'ERROR', 'UNKNOWN'];
const dayFormat = new Intl.DateTimeFormat('en-GB', { weekday: 'short', timeZone: 'UTC' });
const importedFormat = new Intl.DateTimeFormat('en-GB', {
  year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit',
  minute: '2-digit', timeZone: 'UTC', hourCycle: 'h23'
});

function element(name, className, label) {
  const el = document.createElement(name);
  if (className) el.className = className;
  if (label !== undefined) el.textContent = String(label);
  return el;
}

function replaceChildren(parent, nodes) { parent.replaceChildren(...nodes); }
function displayNumber(value) { return Number(value || 0).toLocaleString('en-GB'); }
function isoToUtc(value) {
  if (!value) return '—';
  // PostgreSQL timestamps currently have no timezone, and represent UTC.
  const iso = /[zZ]$|[+-]\d\d:\d\d$/.test(value) ? value : value + 'Z';
  const date = new Date(iso);
  return Number.isNaN(date.getTime()) ? '—' : importedFormat.format(date) + ' UTC';
}

function renderSummary(summary) {
  $('total-logs').textContent = displayNumber(summary.total_logs);
  $('error-count').textContent = displayNumber(summary.counts.ERROR);
  $('warning-count').textContent = displayNumber(summary.counts.WARNING);
  $('info-count').textContent = displayNumber(summary.counts.INFO);
  $('last-import').textContent = summary.last_imported_at ? isoToUtc(summary.last_imported_at) : 'Not yet imported';
  const total = Math.max(0, Number(summary.total_logs) || 0);
  const segments = [];
  const bars = [];
  for (const level of severityOrder) {
    const count = Number(summary.counts[level] || 0);
    const percentage = total ? (count / total) * 100 : 0;
    const segment = element('div', `segment ${level}`);
    segment.style.width = `${percentage}%`;
    segments.push(segment);
    const row = element('div', 'severity-row');
    const progress = element('div', 'progress');
    const fill = element('div', `progress-fill ${level}`);
    fill.style.width = `${percentage}%`;
    progress.append(fill);
    row.append(element('span', 'severity-label', level), progress, element('strong', 'severity-value', displayNumber(count)));
    bars.push(row);
  }
  replaceChildren($('severity-segment'), segments);
  replaceChildren($('severity-bars'), bars);

  const days = summary.errors_by_day || [];
  const maxCount = Math.max(1, ...days.map(day => Number(day.count || 0)));
  replaceChildren($('error-chart'), days.map(day => {
    const container = element('div', 'day');
    const date = new Date(day.date + 'T12:00:00Z');
    const count = Number(day.count || 0);
    const track = element('div', 'day-bar-track');
    const bar = element('div', 'day-bar');
    bar.style.height = `${(count / maxCount) * 100}%`;
    track.append(bar);
    container.append(element('span', 'day-count', count), track,
      element('span', 'day-name', dayFormat.format(date)));
    container.title = `${day.date}: ${count} errors`;
    return container;
  }));

  const topErrors = summary.top_errors || [];
  if (!topErrors.length) {
    replaceChildren($('top-errors'), [element('li', 'muted', 'No imported errors to display.')]);
  } else {
    replaceChildren($('top-errors'), topErrors.map((item, index) => {
      const li = element('li');
      li.append(element('span', 'error-rank', index + 1),
        element('span', 'error-name', item.message),
        element('span', 'error-count', `${item.count}×`));
      return li;
    }));
  }
}

function renderRecords() {
  const search = $('search').value.trim().toLowerCase();
  const selected = $('severity-filter').value;
  const visible = storedRows.filter(row =>
    (selected === 'ALL' || row.severity === selected) &&
    String(row.message || '').toLowerCase().includes(search));
  if (!visible.length) {
    replaceChildren($('log-rows'), [(() => {
      const tr = element('tr');
      const td = element('td', 'muted', storedRows.length ? 'No records match these filters.' : 'No records imported. Use the command in “About this view”.');
      td.colSpan = 3;
      tr.append(td);
      return tr;
    })()]);
  } else {
    replaceChildren($('log-rows'), visible.map(item => {
      const tr = element('tr');
      const levelCell = element('td');
      levelCell.append(element('span', `severity-pill ${severityOrder.includes(item.severity) ? item.severity : 'UNKNOWN'}`, item.severity));
      tr.append(levelCell, element('td', '', isoToUtc(item.created_at)), element('td', '', item.message));
      return tr;
    }));
  }
  $('records-count').textContent = `Showing ${visible.length} of ${storedRows.length} most recent imported records`;
}

async function loadDashboard() {
  const refresh = $('refresh');
  const status = $('fetch-status');
  refresh.disabled = true;
  status.classList.remove('error');
  status.textContent = 'Loading stored log data…';
  try {
    const [summaryResponse, recordsResponse] = await Promise.all([
      fetch('/logs/dashboard-summary', { cache: 'no-store' }),
      fetch('/logs/stored?limit=100', { cache: 'no-store' })
    ]);
    if (!summaryResponse.ok || !recordsResponse.ok) throw new Error('The LogSense API returned an error.');
    const [summary, records] = await Promise.all([summaryResponse.json(), recordsResponse.json()]);
    storedRows = Array.isArray(records.logs) ? records.logs : [];
    renderSummary(summary);
    renderRecords();
    status.textContent = summary.total_logs
      ? 'Showing imported database records · refreshed just now'
      : 'No logs imported yet · follow the import command below to populate this view';
  } catch (error) {
    status.classList.add('error');
    status.textContent = `Unable to load the dashboard. ${error.message}`;
  } finally {
    refresh.disabled = false;
  }
}

$('refresh').addEventListener('click', loadDashboard);
$('search').addEventListener('input', renderRecords);
$('severity-filter').addEventListener('change', renderRecords);
loadDashboard();
