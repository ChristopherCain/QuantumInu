const state = { baseUrl: localStorage.getItem('pythontrader.api') || 'http://127.0.0.1:8000' };

async function api(path, options = {}) {
  const response = await fetch(`${state.baseUrl}${path}`, {
    headers: { 'Accept': 'application/json', 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`${response.status} ${response.statusText}: ${body}`);
  }
  return response.json();
}

async function refresh() {
  const [status, universe, venues] = await Promise.all([
    api('/v1/universal/status'),
    api('/v1/universal/universe'),
    api('/v1/universal/venues'),
  ]);
  document.querySelector('#status').textContent = JSON.stringify(status, null, 2);
  document.querySelector('#universe').textContent = JSON.stringify(universe, null, 2);
  document.querySelector('#venues').textContent = JSON.stringify(venues, null, 2);
}

window.pythonTrader = { api, refresh, state };
window.addEventListener('DOMContentLoaded', () => refresh().catch((error) => {
  document.querySelector('#status').textContent = error.message;
}));
