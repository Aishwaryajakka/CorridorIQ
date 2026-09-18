# CorridorIQ

## From Event Investment to Urban Legacy

**CorridorIQ is a spatial decision-support platform that identifies urban mismatches, overlays mega-event relevance, and lets cities test which corridor investment strategies could create longer-term value.**

Built for the Rice University Urban Sustainability Hackathon, **Track 4 — High Intensity Corridors & Future Growth Districts**.

## The Problem

Mega-events create a short window for infrastructure investment, but cities often lack a transparent way to determine where event-related improvements can also address existing long-term urban needs. Using Houston and FIFA 2026 as a case study, CorridorIQ asks where event relevance overlaps with an existing community activity–mobility mismatch—and how different screening strategies change that diagnostic picture.

## The Core Insight

### Mismatch, not magnitude.

Individual indicators are useful, but planning insight often emerges from the relationship between them. A tract can be dense without being mobility-constrained, or close to an event venue without showing an underlying community mismatch.

CorridorIQ compares urban activity with mobility conditions, detects positive imbalance, and overlays event relevance. The result is an explainable prioritization framework rather than another map of isolated indicators.

## How CorridorIQ Works

```text
Urban Conditions
       ↓
    Urban DNA
       ↓
Mismatch Detection × Event Relevance
       ↓
Legacy Opportunity
       ↓
Strategy Simulation
       ↓
Citywide Outcomes
```

1. **Urban Conditions:** Join Census population, income, vehicle availability, tract area, and local transit-stop locations.
2. **Urban DNA:** Convert economic, activity, mobility-need, and transit-supply indicators to comparable 0–100 scores.
3. **Mismatch Detection:** Identify where activity intensity exceeds modeled mobility capacity.
4. **Event Relevance:** Measure proximity to NRG Stadium and combine it with transit accessibility.
5. **Legacy Opportunity:** Surface tracts where community mismatch overlaps event relevance.
6. **Strategy Simulation:** Apply consistent illustrative mobility-score changes to transparent tract portfolios.
7. **Citywide Outcomes:** Compare diagnostic mismatch counts, affected population, priority areas, maps, and phased scenarios.

## Features

- City Baseline Map with selectable planning indicators
- Urban Opportunity Matrix and balance line
- Urban DNA Fingerprint heatmap
- FIFA Legacy Mode and event-network reference layer
- Legacy Opportunity Matrix and decision funnel
- Guided 60-second demo mode
- Strategy Simulator: FIFA Corridor Focus, Equity First, Highest Mismatch, and custom tracts
- Model-derived before/after citywide outcomes
- Baseline, Scenario, and Change maps
- Illustrative implementation timeline
- FIFA Legacy Watchlist with potential intervention categories
- Tract Explorer and Urban DNA profile
- Single-tract Scenario Lab with recalculated priority rank
- Two-Corridor Comparison
- Data-completeness and proximity sensitivity analysis
- Downloadable ranked CSV results

## Data

The current model uses only local, reproducible inputs:

- **U.S. Census Bureau, 2024 ACS 5-Year Estimates**
  - B01003 — Total Population
  - B19013 — Median Household Income
  - B08201 — Household Size by Vehicles Available
- **U.S. Census Bureau, 2024 TIGER/Line** — Texas census-tract boundaries, filtered to Harris County
- **Houston METRO GTFS** — local stop locations used to calculate stops per square mile
- **NRG Stadium** — approximate coordinate `29.6847, -95.4107`, used as the scored FIFA anchor
- **FIFA Event Mobility Spine** — manually defined, clearly labeled reference points shown for planning context; these are not measured visitor movements and do not alter saved scores

H-GAC parcel land use is **not** included in the current model.

## Methodology

### Normalization

Economic, activity, mobility-need, and transit-supply indicators use robust min-max scaling:

```text
score = 100 × (clipped_value − lower_bound) / (upper_bound − lower_bound)
```

The bounds are the observed 2nd and 98th percentiles. Values outside them are clipped, missing values remain missing, and constant observed series receive a neutral score of 50.

### Scores

```text
Economic Score = normalized median household income

Activity Score = normalized population density

Mobility Need Score = normalized no-vehicle household percentage

Transit Supply Score = normalized transit stops per square mile

Mobility Score =
    0.70 × Transit Supply Score
  + 0.30 × (100 − Mobility Need Score)

Mismatch Raw = Activity Score − Mobility Score

Mismatch Severity Raw = max(Mismatch Raw, 0)

Mismatch Score = normalized Mismatch Severity Raw

NRG Proximity = max(0, 100 × (1 − distance_to_NRG / 20 miles))

FIFA Relevance =
    0.70 × NRG Proximity
  + 0.30 × Transit Supply Score

Legacy Priority = Mismatch Score × FIFA Relevance / 100
```

### Scenario logic

```text
Scenario Mobility = min(100, Mobility Score + improvement points)

Scenario Mismatch Raw = max(Activity Score − Scenario Mobility, 0)
```

Scenario mismatch uses the same baseline normalization bounds, after which Legacy Priority is recalculated with unchanged FIFA Relevance. Untargeted tracts remain unchanged.

**Legacy Priority is a prioritization index, not a prediction.** It does not estimate congestion, demand, return on investment, emissions, or guaranteed project outcomes.

## Findings

1. **217 of 1,110 tracts with complete activity and mobility signals—19.5%—have Activity Scores above Mobility Scores.**
2. **42 tracts meet both transparent Legacy Opportunity criteria:** Mismatch at or above 21.2, the median among positive-mismatch tracts, and FIFA Relevance at or above 55.7, the countywide 75th percentile.
3. Under **FIFA Corridor Focus with a Medium (+20) illustrative mobility improvement**, high-mismatch tracts change from **109 to 91**, population in high-mismatch tracts changes from **424,185 to 371,978**, and average mismatch across targeted tracts changes from **66.6 to 32.8**.

Census Tract 3143.01 ranks first under the baseline framework with Mismatch **100.0**, FIFA Relevance **77.2**, Legacy Priority **77.2**, and a centroid **0.44 miles from NRG Stadium**.

## Scenario Analysis

Users can test four tract-selection strategies:

- **FIFA Corridor Focus:** existing High Mismatch plus Strong FIFA Relevance
- **Equity First:** high-mismatch tracts with the largest no-vehicle household shares
- **Highest Mismatch:** the strongest mismatch signals regardless of event relevance
- **Custom / selected tracts:** a user-defined portfolio

Low, Medium, and High intensities add 10, 20, or 30 mobility-score points using the same scenario formula. The app reports model-derived changes in high-mismatch tract counts, population within those tracts, average targeted mismatch, targeted no-vehicle households, and Legacy Opportunity counts. It also provides Baseline, Scenario, and Change maps plus an illustrative phased pathway.

These scenarios demonstrate model responsiveness and planning tradeoffs. They are **illustrative scenarios, not forecasts**.

## Sustainability + Legacy

FIFA 2026 is the case study, but the decision framework is reusable. Houston could adapt the event-relevance layer for the Houston Livestock Show and Rodeo, sporting events, conventions, concerts, future mega-events, or long-term corridor initiatives. The enduring value is a transparent way to connect short-term funding opportunities to persistent community conditions.

## Limitations

- This is a prototype tract-level model; tract averages conceal within-tract variation.
- Median household income is a limited economic-condition proxy, not a complete measure of economic intensity.
- Transit-stop density does not measure frequency, reliability, travel time, or capacity.
- The event-spine anchors are planning reference points, not measured visitor movement.
- ACS sampling uncertainty is not incorporated into the scores.
- The model does not produce causal traffic forecasts, construction recommendations, economic ROI, or guaranteed infrastructure outcomes.
- Parcel land use, employment density, development pipelines, and growth forecasts are not included in the current model.

## Future Work

- Validated parcel-level land use
- Employment and job density
- Development pipelines and permits
- Detailed transit frequency, reliability, and capacity
- Hotel and event-demand data
- Flood, heat, and subsidence resilience overlays
- Pedestrian and bicycle network accessibility
- Stakeholder-tested weights and thresholds
- Additional FIFA host cities and other event geographies

## Tech Stack

- Python
- Pandas
- GeoPandas
- Streamlit
- Plotly

## Run Locally

```bash
python -m pip install -r requirements.txt
python prepare_data.py
streamlit run app.py
```

The deployed app reads these committed runtime artifacts:

- `data/processed/corridoriq_tracts.csv`
- `data/processed/corridoriq_tracts.geojson`

## Live Demo

**LIVE_APP_URL_HERE**

## Team

Built for the Rice University Urban Sustainability Hackathon. Add confirmed team-member names here before submission.
