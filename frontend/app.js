const API_BASE_URL = "http://127.0.0.1:8000";

function renderTable(containerId, rows) {
  const container = document.getElementById(containerId);

  if (!rows || rows.length === 0) {
    container.innerHTML = '<p class="empty">Нет данных.</p>';
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

function renderLoading(containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = '<p class="loading">Загрузка...</p>';
}

function renderError(containerId, message) {
  const container = document.getElementById(containerId);
  container.innerHTML = `<p class="error">${message}</p>`;
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
    renderError(containerId, `Ошибка загрузки driver points: ${error.message}`);
  }
}

async function loadConstructorPoints() {
  const containerId = "constructor-points-table";
  renderLoading(containerId);

  try {
    const data = await fetchJson(`${API_BASE_URL}/constructor-points?limit=20`);
    renderTable(containerId, data);
  } catch (error) {
    renderError(containerId, `Ошибка загрузки constructor points: ${error.message}`);
  }
}

async function loadDriverPodiums() {
  const containerId = "driver-podiums-table";
  renderLoading(containerId);

  try {
    const data = await fetchJson(`${API_BASE_URL}/driver-podiums?limit=20`);
    renderTable(containerId, data);
  } catch (error) {
    renderError(containerId, `Ошибка загрузки podiums: ${error.message}`);
  }
}

async function loadRaceResults() {
  const containerId = "race-results-table";
  renderLoading(containerId);

  const season = document.getElementById("season-select").value;
  const round = document.getElementById("round-select").value;

  try {
    const data = await fetchJson(
      `${API_BASE_URL}/race-results?season=${season}&round_number=${round}`
    );
    renderTable(containerId, data);
  } catch (error) {
    renderError(containerId, `Ошибка загрузки race results: ${error.message}`);
  }
}

async function loadAvailableSeasons() {
  const seasonSelect = document.getElementById("season-select");

  try {
    const seasons = await fetchJson(`${API_BASE_URL}/available-seasons`);
    seasonSelect.innerHTML = seasons
      .map((season) => `<option value="${season}">${season}</option>`)
      .join("");

    if (seasons.includes(2023)) {
      seasonSelect.value = "2023";
    }

    populateRounds();
  } catch (error) {
    console.error("Не удалось загрузить сезоны", error);
  }
}

function populateRounds() {
  const roundSelect = document.getElementById("round-select");
  roundSelect.innerHTML = "";

  for (let i = 1; i <= 24; i++) {
    const option = document.createElement("option");
    option.value = String(i);
    option.textContent = String(i);
    roundSelect.appendChild(option);
  }

  roundSelect.value = "1";
}

async function refreshAll() {
  await Promise.all([
    loadDriverPoints(),
    loadConstructorPoints(),
    loadDriverPodiums(),
  ]);

  await loadRaceResults();
}

document.getElementById("refresh-all").addEventListener("click", refreshAll);
document.getElementById("load-race-results").addEventListener("click", loadRaceResults);
document.getElementById("season-select").addEventListener("change", loadRaceResults);
document.getElementById("round-select").addEventListener("change", loadRaceResults);

window.addEventListener("DOMContentLoaded", async () => {
  await loadAvailableSeasons();
  await refreshAll();
});