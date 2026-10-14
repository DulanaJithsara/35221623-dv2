// Embeds every chart on the page with vega-embed and drives the sticky
// scrollytelling text. Each chart's JSON specification lives in /specs.

const FONT = "IBM Plex Sans, Segoe UI, Helvetica, Arial, sans-serif";

// Shared dark theme for every chart
const theme = {
  background: null,
  font: FONT,
  view: { stroke: null },
  axis: {
    labelFont: FONT, titleFont: FONT,
    labelFontSize: 12, titleFontSize: 12.5, titleFontWeight: 600,
    labelColor: "#9DAEC4", titleColor: "#9DAEC4",
    domainColor: "#3A5275", tickColor: "#3A5275",
    gridColor: "#24395A", gridWidth: 1
  },
  legend: {
    labelFont: FONT, titleFont: FONT,
    labelFontSize: 12.5, titleFontSize: 12.5, titleFontWeight: 700,
    labelColor: "#E9EEF5", titleColor: "#E9EEF5"
  },
  header: { labelFont: FONT, titleFont: FONT, labelColor: "#E9EEF5" },
  text: { font: FONT, color: "#E9EEF5" },
  title: { font: FONT, color: "#E9EEF5" }
};

// [element id, spec file]
const charts = [
  ["#c01", "specs/c01_national_trend.vg.json"],
  ["#c02", "specs/c02_waterfall.vg.json"],
  ["#c03", "specs/c03_treemap.vg.json"],
  ["#c04", "specs/c04_marimekko.vg.json"],
  ["#c05", "specs/c05_slope_euthanasia.vg.json"],
  ["#c06", "specs/c06_choropleth.vg.json"],
  ["#c07", "specs/c07_dot_density.vg.json"],
  ["#c08", "specs/c08_dumbbell.vg.json"],
  ["#c09", "specs/c09_heatmap_reasons.vg.json"],
  ["#c10", "specs/c10_butterfly.vg.json"],
  ["#c11", "specs/c11_proportional_symbols.vg.json"],
  ["#c12", "specs/c12_connected_scatter.vg.json"],
  ["#c13", "specs/c13_prosecutions_by_state.vg.json"]
];

async function embedAll() {
  if (document.fonts && document.fonts.ready) {
    try { await document.fonts.ready; } catch (e) { /* continue */ }
  }
  for (const [el, url] of charts) {
    const target = document.querySelector(el);
    if (!target) continue;
    const opts = { actions: false, renderer: "svg", config: theme };
    // The treemap (chart 3) is a Vega chart with a fixed width, so we give it
    // the card's width ourselves and update it whenever the card resizes.
    const isTreemap = url.includes("treemap");
    const cardWidth = () => Math.max(320, Math.floor(target.getBoundingClientRect().width));
    if (isTreemap) opts.width = cardWidth();
    vegaEmbed(el, url, opts)
      .then((result) => {
        if (!isTreemap) return;
        new ResizeObserver(() => {
          const w = cardWidth();
          if (Math.abs(w - result.view.width()) > 1) result.view.width(w).runAsync();
        }).observe(target);
      })
      .catch((err) => {
        target.innerHTML = '<p class="err">Chart failed to load: ' + err.message + "</p>";
        console.error(url, err);
      });
  }
}

// ---- Scrollytelling: show the story step that matches the chart in view ----
function setupSteps() {
  const wide = window.matchMedia("(min-width: 960px)");
  document.querySelectorAll(".story").forEach((story) => {
    const steps = story.querySelectorAll(".step");
    const cards = story.querySelectorAll("figure.card[data-step]");
    const counter = story.querySelector(".step-count");
    const activate = (n) => {
      steps.forEach((s) => s.classList.toggle("active", s.dataset.step === n));
      cards.forEach((c) => c.classList.toggle("in-view", c.dataset.step === n));
      if (counter) counter.textContent = n + " / " + cards.length;
    };
    activate(cards[0] ? cards[0].dataset.step : "1");
    const io = new IntersectionObserver((entries) => {
      if (!wide.matches) return;
      entries.forEach((e) => { if (e.isIntersecting) activate(e.target.dataset.step); });
    }, { rootMargin: "-45% 0px -45% 0px" });
    cards.forEach((c) => io.observe(c));
  });
}

// ---- Reading progress bar + active nav link ----
function setupProgress() {
  const bar = document.querySelector(".progress span");
  const links = [...document.querySelectorAll(".topnav a[href^='#']")];
  const secs = links.map((a) => document.querySelector(a.getAttribute("href")));
  const onScroll = () => {
    const h = document.documentElement;
    const p = h.scrollTop / Math.max(1, h.scrollHeight - h.clientHeight);
    if (bar) bar.style.width = (p * 100).toFixed(1) + "%";
    let idx = -1;
    secs.forEach((s, i) => { if (s && s.getBoundingClientRect().top < window.innerHeight * 0.35) idx = i; });
    links.forEach((a, i) => a.classList.toggle("on", i === idx));
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
}

embedAll();
setupSteps();
setupProgress();