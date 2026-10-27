# Through the Shelter Door — RSPCA animal welfare in Australia

FIT3179 Data Visualisation 2 · Monash University · Semester 2, 2026
Author: Dulana Jithsara Sarathchandra · October 2026

A single-page data story built with **Vega-Lite** (and one **Vega** treemap) about the animals the RSPCA receives, what happens to them, and how its cruelty inspectorate is changing.

## Repository layout

```
index.html            the web page
css/style.css         layout (12-column grid) and typography
js/main.js            embeds every chart with vega-embed + shared theme
specs/                one human-readable JSON specification per chart
  c01_national_trend.vg.json        line chart
  c02_waterfall.vg.json             waterfall chart
  c03_treemap.vg.json               treemap (Vega)
  c04_marimekko.vg.json             Marimekko / mosaic chart
  c05_slope_euthanasia.vg.json      slope chart
  c06_choropleth.vg.json            MAP 1 — choropleth (interactive dropdown)
  c07_dot_density.vg.json           MAP 2 — dot density map (legend filter)
  c08_dumbbell.vg.json              dumbbell chart
  c09_heatmap_reasons.vg.json       heatmap (small multiples)
  c10_butterfly.vg.json             butterfly / back-to-back bar chart
  c11_proportional_symbols.vg.json  MAP 3 — proportional symbol map
  c12_connected_scatter.vg.json     connected scatterplot
  c13_prosecutions_by_state.vg.json bar chart (bullet style)
data/                 CSV + TopoJSON files used by the charts (~80 KB total)
scripts/prepare_data.py   how the CSV files were produced from the source tables
```

## Data sources

1. RSPCA Australia, *National Statistics 2024–2025*, Tables 2–6 — https://www.rspca.org.au/about/annual-statistics/
2. Australian Bureau of Statistics, *National, state and territory population, June 2025* — https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/jun-2025
3. State boundaries: https://github.com/rowanhogan/australian-states, simplified with mapshaper (4%), dots generated with `mapshaper -dots` (1 dot = 50 animals).

## Data preparation (summary)

- Table values were transcribed into `scripts/prepare_data.py`, which writes the tidy CSVs and checks them against the reported totals (77,464 animals; euthanasia reasons = euthanased counts).
- The NSW and NT columns in the PDF's text layer come out swapped; this was corrected and verified against the RSPCA NSW Annual Report 2025 (5,994 animals adopted).
- RSPCA's own "other animals" outcome rows do not sum to its totals (6,221 vs 6,267); no values were changed.
- Per-10,000-resident rates use ABS estimated resident population at 30 June 2025.

## Use of AI

Claude (Anthropic) was used to help write chart code and check grammar. All data comes from the sources listed above.
