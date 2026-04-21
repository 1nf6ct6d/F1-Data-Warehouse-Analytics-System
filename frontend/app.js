const API_BASE_URL = "http://127.0.0.1:8000";

function renderTable(containerId, rows) {
  const container = document.getElementById(containerId);

  if (!rows || rows.length === 0) {
    container.innerHTML = "<p>No data found.</p>";
    return;
  }

  const columns = Object.keys(rows[0]);

  const headerHtml = columns.map((col) => `<th>${col}</th>`).join("");
  const bodyHtml = rows
    .map((row) => {
      const cells = columns.map((col) => `<td>${row[col] ?? ""}</td>`).join("");
      return `<tr>${cells}</tr>`;
    })
    .join("");

  container.innerHTML = `
    <div class="table-wrapper">
      <table>
        <thead>
          <tr>${headerHtml}</tr>
        </thead>
        <tbody>
          ${bodyHtml}
        </tbody>
      </table>
    </div>
  `;
}

function renderError(containerId, message) {
  const container = document.getElementById(containerId);
  container.innerHTML = `<p class="error">${message}</p>`;
}

function renderLoading(containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = `<p class="loading">Loading...</p>`;
}

async function fetchJson(url) {
  const response = await fetch(url);

  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }

  return response.json();
}

async function loadDriverPoints() {
  const containerId = "driver-points-table";
  renderLoading(containerId);

  try {
    const data = await fetchJson(`${API_BASE_URL}/driver-points?limit=20`);
    renderTable(containerId, data);
  } catch (error) {
    renderError(containerId, `Failed to load driver points: ${error.message}`);
  }
}

async function loadConstructorPoints() {
  const containerId = "constructor-points-table";
  renderLoading(containerId);

  try {
    const data = await fetchJson(`${API_BASE_URL}/constructor-points?limit=20`);
    renderTable(containerId, data);
  } catch (error) {
    renderError(containerId, `Failed to load constructor points: ${error.message}`);
  }
}

async function loadDriverPodiums() {
  const containerId = "driver-podiums-table";
  renderLoading(containerId);

  try {
    const data = await fetchJson(`${API_BASE_URL}/driver-podiums?limit=20`);
    renderTable(containerId, data);
  } catch (error) {
    renderError(containerId, `Failed to load driver podiums: ${error.message}`);
  }
}

async function loadRaceResults() {
  const containerId = "race-results-table";
  renderLoading(containerId);

  const season = document.getElementById("season-input").value;
  const round = document.getElementById("round-input").value;

  try {
    const data = await fetchJson(
      `${API_BASE_URL}/race-results?season=${season}&round_number=${round}`
    );
    renderTable(containerId, data);
  } catch (error) {
    renderError(containerId, `Failed to load race results: ${error.message}`);
  }
}

document.getElementById("load-driver-points").addEventListener("click", loadDriverPoints);
document.getElementById("load-constructor-points").addEventListener("click", loadConstructorPoints);
document.getElementById("load-driver-podiums").addEventListener("click", loadDriverPodiums);
document.getElementById("load-race-results").addEventListener("click", loadRaceResults);