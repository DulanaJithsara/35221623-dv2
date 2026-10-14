"""
prepare_data.py — builds the tidy CSV files used by the Vega-Lite charts.

Sources
  1. RSPCA Australia, National Statistics 2024-2025 (Tables 1-6)
     https://www.rspca.org.au/about/annual-statistics/
  2. Australian Bureau of Statistics, National, state and territory population,
     June 2025 (estimated resident population, released 19 Dec 2025)
     https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/jun-2025

Cleaning notes (also described in the submission):
  * Figures were transcribed from the RSPCA PDF tables into the lists below.
  * In the PDF's text layer the NSW and NT columns of Tables 3 and 4 come out
    swapped. This was corrected by checking against the RSPCA NSW Annual Report
    2025 (5,994 animals adopted = sum of the corrected NSW "Rehomed" row).
  * "Other animals" outcome rows in Table 4 do not sum exactly to the reported
    state totals (6,221 vs 6,267). Reported totals are used for totals; outcome
    rows are used for outcome shares. No values were altered.
  * Species are grouped into five groups for consistent colour:
    Dogs, Cats, Wildlife, Livestock & horses, Other pets.
"""
import csv
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT, exist_ok=True)

STATES = ["ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"]
STATE_NAMES = {
    "ACT": "Australian Capital Territory", "NSW": "New South Wales",
    "NT": "Northern Territory", "QLD": "Queensland", "SA": "South Australia",
    "TAS": "Tasmania", "VIC": "Victoria", "WA": "Western Australia",
}
# ABS ERP 30 June 2025 ('000)
POP = {"NSW": 8593.9, "VIC": 7074.5, "QLD": 5669.8, "SA": 1902.3,
       "WA": 3043.7, "TAS": 576.0, "NT": 264.4, "ACT": 484.8}


def fix(row):
    """PDF text order is ACT, NT, NSW, QLD, SA, TAS, VIC, WA -> return in STATES order."""
    act, nt, nsw, qld, sa, tas, vic, wa = row
    return [act, nsw, nt, qld, sa, tas, vic, wa]


# ---------------- Table 4: animals received by state, 2024-25 ----------------
T4 = {
    "Dogs": {
        "Reclaimed": [109, 0, 229, 1647, 501, 0, 646, 71],
        "Returned": [75, 18, 243, 204, 33, 48, 83, 23],
        "Rehomed": [310, 119, 1350, 2922, 867, 220, 704, 347],
        "Currently in care": [60, 53, 442, 397, 204, 91, 199, 226],
        "Transferred": [5, 0, 162, 63, 49, 0, 159, 91],
        "Euthanased": [36, 14, 878, 1133, 303, 20, 210, 174],
        "Other / died in care": [0, 0, 16, 35, 6, 0, 14, 43],
        "_total": [595, 204, 3320, 6401, 1963, 379, 2015, 975],
        "_last": [676, 310, 4554, 6531, 1814, 130, 2550, 903],
    },
    "Cats": {
        "Reclaimed": [120, 1, 122, 443, 117, 0, 157, 19],
        "Returned": [33, 0, 116, 99, 51, 22, 39, 21],
        "Rehomed": [1433, 186, 3863, 4992, 2191, 488, 2688, 604],
        "Currently in care": [171, 58, 607, 543, 251, 73, 344, 81],
        "Transferred": [2, 2, 40, 87, 58, 0, 81, 28],
        "Euthanased": [151, 9, 1768, 1772, 663, 109, 471, 146],
        "Other / died in care": [25, 3, 105, 83, 24, 8, 50, 21],
        "_total": [1935, 259, 6621, 8019, 3355, 700, 3830, 920],
        "_last": [2065, 357, 7007, 7650, 3033, 1063, 4611, 918],
    },
    "Horses": {
        "Reclaimed": [0, 0, 0, 2, 0, 0, 0, 0],
        "Returned": [0, 0, 1, 2, 0, 0, 2, 0],
        "Rehomed": [0, 0, 31, 8, 0, 2, 131, 6],
        "Currently in care": [0, 0, 44, 9, 39, 3, 69, 17],
        "Transferred": [0, 0, 1, 1, 18, 0, 34, 1],
        "Euthanased": [0, 0, 24, 5, 9, 5, 67, 2],
        "Other / died in care": [0, 0, 2, 0, 0, 0, 2, 0],
        "_total": [0, 0, 103, 27, 66, 10, 305, 26],
        "_last": [0, 0, 142, 51, 24, 19, 231, 16],
    },
    "Livestock": {
        "Reclaimed": [0, 0, 1, 13, 13, 0, 0, 3],
        "Returned": [0, 0, 41, 2, 1, 0, 1, 0],
        "Rehomed": [43, 2, 104, 234, 40, 28, 32, 68],
        "Currently in care": [7, 0, 15, 32, 98, 26, 19, 5],
        "Transferred": [0, 0, 46, 16, 94, 0, 21, 8],
        "Euthanased": [11, 0, 50, 196, 26, 2, 20, 25],
        "Other / died in care": [0, 0, 2, 16, 7, 0, 3, 4],
        "_total": [61, 2, 259, 509, 279, 56, 96, 113],
        "_last": [88, 0, 406, 404, 310, 2, 176, 98],
    },
    "Wildlife": {
        "Released to the wild": [1, 0, 1, 2521, 59, 0, 13, 0],
        "Currently in care": [4, 0, 3, 172, 13, 0, 8, 0],
        "Transferred": [27, 0, 103, 5591, 173, 0, 18, 0],
        "Euthanased": [71, 0, 301, 17307, 103, 0, 239, 0],
        "Other / died in care": [5, 0, 11, 973, 13, 0, 64, 0],
        "_total": [108, 0, 419, 26564, 361, 0, 342, 0],
        "_last": [205, 0, 468, 27423, 328, 10, 650, 0],
    },
    "Other pets": {
        "Reclaimed": [19, 24, 0, 2, 10, 8, 12, 4],
        "Returned": [8, 0, 215, 23, 12, 0, 7, 3],
        "Rehomed": [191, 0, 646, 652, 241, 71, 651, 269],
        "Currently in care": [8, 0, 117, 222, 226, 8, 743, 32],
        "Transferred": [1, 0, 167, 34, 118, 0, 55, 6],
        "Euthanased": [17, 0, 476, 421, 128, 1, 105, 32],
        "Other / died in care": [11, 0, 54, 94, 26, 0, 40, 11],
        "_total": [249, 0, 1688, 1521, 772, 80, 1601, 356],
        "_last": [333, 17, 1898, 1931, 489, 121, 1155, 502],
    },
}
TOTAL_ALL = fix([2948, 465, 12410, 43041, 6796, 1225, 8189, 2390])
TOTAL_ALL_LAST = fix([3367, 684, 14475, 43990, 5998, 1345, 9373, 2437])

GROUP = {"Dogs": "Dogs", "Cats": "Cats", "Wildlife": "Wildlife",
         "Horses": "Livestock & horses", "Livestock": "Livestock & horses",
         "Other pets": "Other pets"}

# Outcome families used for colour in the Marimekko / butterfly charts
OUTCOME_FAMILY = {
    "Reclaimed": "Reunited with owner", "Returned": "Reunited with owner",
    "Rehomed": "Rehomed", "Released to the wild": "Released to the wild",
    "Currently in care": "Still in care or transferred",
    "Transferred": "Still in care or transferred",
    "Euthanased": "Euthanased", "Other / died in care": "Other / died in care",
}

# sanity checks against reported totals
for sp, rows in T4.items():
    for i in range(8):
        s = sum(v[i] for k, v in rows.items() if not k.startswith("_"))
        if s != rows["_total"][i]:
            print(f"  note: {sp} col{i}: outcomes sum {s} vs reported total {rows['_total'][i]}")
col_tot = [sum(T4[sp]["_total"][i] for sp in T4) for i in range(8)]
assert fix(col_tot) == TOTAL_ALL, (fix(col_tot), TOTAL_ALL)
assert sum(TOTAL_ALL) == 77464

# outcomes_2425.csv (long)
with open(os.path.join(OUT, "outcomes_2425.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["state", "species", "group", "outcome", "outcome_family", "count"])
    for sp, rows in T4.items():
        for outcome, vals in rows.items():
            if outcome.startswith("_"):
                continue
            for st, v in zip(STATES, fix(vals)):
                w.writerow([st, sp, GROUP[sp], outcome, OUTCOME_FAMILY[outcome], v])

# received_by_state.csv (group totals, both years)
with open(os.path.join(OUT, "received_by_state.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["state", "state_name", "group", "received_2425", "received_2324",
                "population_2025", "per_10k_2425"])
    for st_i, st in enumerate(STATES):
        agg, agg_last = {}, {}
        for sp, rows in T4.items():
            g = GROUP[sp]
            agg[g] = agg.get(g, 0) + fix(rows["_total"])[st_i]
            agg_last[g] = agg_last.get(g, 0) + fix(rows["_last"])[st_i]
        pop = POP[st] * 1000
        for g in ["Dogs", "Cats", "Wildlife", "Livestock & horses", "Other pets"]:
            w.writerow([st, STATE_NAMES[st], g, agg[g], agg_last[g], int(pop),
                        round(agg[g] / pop * 10000, 2)])
        w.writerow([st, STATE_NAMES[st], "All animals", TOTAL_ALL[st_i],
                    TOTAL_ALL_LAST[st_i], int(pop),
                    round(TOTAL_ALL[st_i] / pop * 10000, 2)])

# ---------------- Table 3: reasons for euthanasia ----------------
T3 = {
    "Dogs": {"Infectious disease": [0, 0, 6, 28, 3, 0, 4, 22],
             "Medical": [25, 7, 235, 410, 109, 17, 97, 40],
             "Behavioural": [11, 7, 627, 672, 161, 3, 100, 71],
             "Legal": [0, 0, 2, 19, 20, 0, 6, 7],
             "Other": [0, 0, 8, 4, 10, 0, 3, 34]},
    "Cats": {"Infectious disease": [2, 0, 246, 348, 31, 0, 39, 0],
             "Medical": [69, 6, 871, 932, 237, 24, 157, 83],
             "Behavioural": [80, 3, 321, 473, 383, 85, 179, 52],
             "Legal": [0, 0, 0, 2, 0, 0, 47, 0],
             "Other": [0, 0, 330, 17, 12, 0, 49, 11]},
}
with open(os.path.join(OUT, "euthanasia_reasons_2425.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["state", "species", "reason", "count"])
    for sp, rows in T3.items():
        for reason, vals in rows.items():
            for st, v in zip(STATES, fix(vals)):
                w.writerow([st, sp, reason, v])
    # cross-check with Table 4 euthanased rows
    for sp in T3:
        tot = [sum(T3[sp][r][i] for r in T3[sp]) for i in range(8)]
        assert tot == T4[sp]["Euthanased"], sp

# ---------------- Table 5: inspectorate by state (NT has no RSPCA enforcement) ----
T5_STATES = ["ACT", "NSW", "QLD", "SA", "TAS", "VIC", "WA"]
T5 = {
    "complaints_investigated": [744, 16713, 13874, 5125, 1915, 10206, 7195],
    "prosecutions_finalised": [5, 226, 3, 37, 2, 47, 61],
    "successful_prosecutions": [5, 119, 0, 32, 2, 47, 59],
    "charges_laid": [0, 991, 0, 192, 56, 204, 165],
    "people_charged": [5, 0, 3, 44, 4, 49, 59],
    "cases_pending": [0, 104, 0, 46, 20, 19, 46],
    "routine_inspections": [9, 49, 0, 8, 31, 12, 0],
}
assert sum(T5["complaints_investigated"]) == 55772
assert sum(T5["prosecutions_finalised"]) == 381
with open(os.path.join(OUT, "inspectorate_by_state_2425.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["state", "state_name", "population_2025", *T5.keys(), "complaints_per_10k"])
    for i, st in enumerate(T5_STATES):
        pop = POP[st] * 1000
        w.writerow([st, STATE_NAMES[st], int(pop), *[T5[k][i] for k in T5],
                    round(T5["complaints_investigated"][i] / pop * 10000, 1)])

# ---------------- Table 2: national trend 2020-21 to 2024-25 ----------------
YEARS5 = ["2020-21", "2021-22", "2022-23", "2023-24", "2024-25"]
T2 = {
    "Dogs": {"other": [19809, 16737, 15903, 14626, 13084],
             "euth": [2502, 2484, 2875, 2842, 2768],
             "total": [22311, 19221, 18778, 17468, 15852]},
    "Cats": {"other": [33968, 29065, 27523, 21556, 20550],
             "euth": [8604, 6506, 6224, 5148, 5089],
             "total": [42572, 35571, 33747, 26704, 25639]},
    "Other animals": {"other": [17597, 18983, 18228, 16480, 16330],
                      "euth": [20577, 21053, 16712, 21017, 19643],
                      "total": [38174, 40036, 34940, 37497, 35973]},
}
for g in T2:
    for i in range(5):
        assert T2[g]["other"][i] + T2[g]["euth"][i] == T2[g]["total"][i], (g, i)
with open(os.path.join(OUT, "national_trend.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year", "group", "received", "euthanased", "euthanased_pct"])
    for g in T2:
        for i, y in enumerate(YEARS5):
            w.writerow([y, g, T2[g]["total"][i], T2[g]["euth"][i],
                        round(T2[g]["euth"][i] / T2[g]["total"][i] * 100, 1)])

# ---------------- Table 6: complaints & prosecutions 2019-20 to 2024-25 ----------
with open(os.path.join(OUT, "inspectorate_trend.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["year", "complaints", "prosecutions"])
    for y, c, p in zip(["2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25"],
                       [73997, 73301, 69014, 69623, 71514, 67237],
                       [359, 426, 318, 251, 248, 381]):
        w.writerow([y, c, p])

print("data written to", os.path.abspath(OUT))
