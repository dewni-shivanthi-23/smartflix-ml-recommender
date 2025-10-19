import { apiSearch, apiRecommend, apiRecommendBatch, apiInfo } from "./api.js";
import { chip, renderGrid, showStatus, setApiInfo, openModal } from "./ui.js";

const input = document.getElementById("movieInput");
const addBtn = document.getElementById("addMovieBtn");
const chipsBox = document.getElementById("chips");
const suggestBox = document.getElementById("suggestions");
const recommendBtn = document.getElementById("recommendBtn");
const topKInput = document.getElementById("topK");
const clearBtn = document.getElementById("clearBtn");
const favBtn = document.getElementById("favoritesBtn");

let liked = new Set(JSON.parse(localStorage.getItem("likedMovies") || "[]"));
let seeds = new Set();

function saveFavs() {
  localStorage.setItem("likedMovies", JSON.stringify([...liked]));
}
function renderChips() {
  chipsBox.innerHTML = "";
  seeds.forEach((t) => chipsBox.appendChild(chip(t, removeSeed)));
}
function addSeed(t) {
  t = t.trim();
  if (!t) return;
  seeds.add(t);
  renderChips();
  input.value = "";
  document.getElementById("suggestions").innerHTML = "";
  clearResults();
}
function removeSeed(title) {
  seeds.delete(title);
  renderChips();

  if (seeds.size === 0) {
    // nothing selected anymore → wipe recommendations
    clearResults();
  } else {
    // optional: keep results in sync by recomputing
    clearResults(); // ← if you’d rather NOT auto-refresh, delete this line
  }
}

function clearResults() {
  document.getElementById("grid").innerHTML = "";
  showStatus(""); // clears “Error:” or “Showing …”
  document.getElementById("suggestions").innerHTML = "";
}

async function doSearch(q) {
  if (!q || q.length < 2) {
    suggestBox.innerHTML = "";
    return;
  }
  try {
    const items = await apiSearch(q, 8);
    suggestBox.innerHTML = "";
    items.forEach((i) => {
      const row = document.createElement("div");
      row.className = "suggestion";
      row.textContent = `${i.title} • ${i.genres}`;
      row.onclick = () => addSeed(i.title);
      suggestBox.appendChild(row);
    });
  } catch {}
}

async function getRecs() {
  const titles = Array.from(seeds);
  clearResults();
  if (!titles.length) {
    showStatus("Add at least one movie.");
    return;
  }
  showStatus("Fetching recommendations…");
  try {
    const k = Math.max(1, Math.min(50, parseInt(topKInput.value || "10", 10)));
    const items =
      titles.length === 1
        ? await apiRecommend(titles[0], k)
        : await apiRecommendBatch(titles, k);
    renderGrid(
      items,
      (it) => {
        liked.add(it.title);
        saveFavs();
        showStatus(`Added to favorites: ${it.title}`);
      },
      (it) =>
        openModal(
          `<h3>${it.title}</h3><p><strong>Genres:</strong> ${
            it.genres || "-"
          }</p><p><strong>Similarity:</strong> ${it.similarity ?? "—"}</p>`
        )
    );
    showStatus(
      items.length ? `Showing ${items.length} recommendations` : "No results."
    );
  } catch (err) {
    showStatus(`Error: ${err.message || err}`);
  }
}

addBtn.onclick = () => addSeed(input.value);
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    const parts = input.value
      .split(",")
      .map((s) => s.trim())
      .filter(Boolean);
    if (parts.length > 1) parts.forEach(addSeed);
    else addSeed(input.value);
  }
});
input.addEventListener("input", (e) => doSearch(e.target.value));
recommendBtn.onclick = getRecs;
clearBtn.onclick = () => {
  seeds = new Set();
  renderChips();
  clearResults();
};

favBtn.onclick = () => {
  const items = [...liked].map((t) => ({
    title: t,
    similarity: "★",
    genres: "",
  }));
  renderGrid(
    items,
    () => {},
    (i) => openModal(`<h3>${i.title}</h3><p>Saved in Favorites</p>`)
  );
  showStatus(`Favorites (${items.length})`);
};

setApiInfo(apiInfo());
renderChips();
