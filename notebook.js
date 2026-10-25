const input = document.getElementById("nb-q");
const list = document.getElementById("nb-list");
const empty = document.getElementById("nb-empty");
const count = document.getElementById("nb-count");
const filters = document.querySelectorAll(".nb-filter");
const items = [...document.querySelectorAll(".nb-item")];

let tag = "all";

function hay(item) {
  return (item.dataset.search || item.textContent).toLowerCase();
}

function paint() {
  const q = (input ? input.value : "").trim().toLowerCase();
  let shown = 0;
  items.forEach((item) => {
    const tagOk = tag === "all" || item.dataset.tag === tag;
    const textOk = !q || hay(item).includes(q);
    const on = tagOk && textOk;
    item.hidden = !on;
    if (on) shown += 1;
  });
  if (empty) empty.hidden = shown > 0;
  if (count) count.textContent = shown + " of " + items.length;
}

if (list) {
  if (input) input.addEventListener("input", paint);
  filters.forEach((button) => {
    button.addEventListener("click", () => {
      tag = button.dataset.tag;
      filters.forEach((item) => item.classList.toggle("is-on", item === button));
      paint();
    });
  });
  paint();
}
