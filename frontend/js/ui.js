export function el(tag, props = {}, ...kids) {
  const n = document.createElement(tag);
  Object.assign(n, props);
  for (const k of kids) n.append(k?.nodeType ? k : document.createTextNode(k));
  return n;
}

export function chip(title, onRemove) {
  const close = el("span", { className: "remove", title: "Remove" }, "✖");
  close.onclick = () => onRemove(title);
  return el("span", { className: "chip" }, title, close);
}

export function card(item, onFav, onMore) {
  const gs = (item.genres || "")
    .split("|")
    .slice(0, 3)
    .filter(Boolean)
    .map((g) => el("span", { className: "badge" }, g));
  const fav = el("button", { className: "ghost" }, "⭐ Favorite");
  fav.onclick = () => onFav(item);
  const more = el("button", { className: "ghost" }, "More");
  more.onclick = () => onMore(item);
  return el(
    "div",
    { className: "card" },
    el("h3", { className: "title" }, item.title),
    el("div", { className: "meta" }, `Similarity: ${item.similarity ?? "—"}`),
    el("div", { className: "actions-row" }, fav, more),
    el("div", {}, ...gs)
  );
}

export function showStatus(t = "") {
  document.getElementById("status").textContent = t;
}
export function renderGrid(items, onFav, onMore) {
  const g = document.getElementById("grid");
  g.innerHTML = "";
  items.forEach((i) => g.appendChild(card(i, onFav, onMore)));
}
export function setApiInfo(x) {
  document.getElementById("apiInfo").textContent = x;
}
export function openModal(html) {
  const m = document.getElementById("modal");
  const b = document.getElementById("modalBody");
  b.innerHTML = html;
  m.classList.remove("hidden");
  document.getElementById("modalClose").onclick = () =>
    m.classList.add("hidden");
}
