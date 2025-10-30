const API_BASE = "http://127.0.0.1:8000"; // change if needed

export async function apiSearch(query, limit = 10) {
  const r = await fetch(
    `${API_BASE}/search?query=${encodeURIComponent(query)}&limit=${limit}`
  );
  if (!r.ok) throw new Error(await r.text());
  return (await r.json()).items;
}

export async function apiRecommend(title, topN = 10) {
  const r = await fetch(`${API_BASE}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, top_n: topN }),
  });
  if (!r.ok) throw new Error(await r.text());
  return (await r.json()).items;
}

export async function apiRecommendBatch(titles, topN = 10) {
  const r = await fetch(`${API_BASE}/recommend_batch`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ titles, top_n: topN }),
  });
  if (!r.ok) throw new Error(await r.text());
  return (await r.json()).items;
}

export function apiInfo() {
  return API_BASE;
}
