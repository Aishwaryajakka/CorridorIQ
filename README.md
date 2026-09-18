# CorridorIQ
## From Event Investment to Urban Legacy

> **CorridorIQ helps cities identify where urban systems are out of alignment, determine which of those gaps intersect with a mega-event opportunity, and test how targeted interventions could create longer-term value.**

**Track 4 — High Intensity Corridors & Future Growth Districts**  
Rice University Urban Sustainability Hackathon · FIFA World Cup 2026

[Live Demo](https://corridor-iq.streamlit.app) · [Demo Video](DEMO_VIDEO_URL_HERE)

---

## The Question

### How can a city make a temporary mega-event investment create value long after the event is over?

Cities already collect large amounts of information about population, transportation, economic conditions, land use, and development.

The challenge is that those indicators are often evaluated independently.

A place may have:

- high urban activity,
- limited mobility access,
- many households without vehicles,
- strong event relevance,
- and significant development pressure,

but no single indicator reveals the relationship between those conditions.

**CorridorIQ focuses on those relationships.**

Instead of asking only:

> Where is density highest?

or:

> Where is transit weakest?

CorridorIQ asks:

> **Where are urban systems out of alignment, and where does a mega-event create a timely opportunity to address that mismatch?**

---

# Why CorridorIQ?

## Mismatch, not magnitude.

Most urban dashboards tell planners whether individual indicators are high or low.

CorridorIQ asks whether those indicators are **aligned**.

For example, a highly active urban district may not necessarily be a planning priority if its mobility conditions already match its intensity.

But a district with:

- high activity,
- comparatively weak mobility,
- high event relevance,
- and many residents dependent on alternatives to private vehicles

may deserve much closer attention.

That relationship is the core idea behind CorridorIQ.

---

# The CorridorIQ Framework

```text
URBAN CONDITIONS
Economic + Activity + Mobility
        ↓
    URBAN DNA
        ↓
MISMATCH DETECTION
        ×
FIFA EVENT RELEVANCE
        ↓
LEGACY OPPORTUNITY
        ↓
STRATEGY SIMULATION
        ↓
CITYWIDE OUTCOMES
```

CorridorIQ moves from **baseline → diagnosis → prioritization → scenario testing**.

---

# Two Planning Lenses

CorridorIQ provides two complementary ways to explore Houston.

## 1. Citywide Analysis

**Question:**

> Where are Houston's urban systems most out of alignment?

Citywide Analysis focuses on the underlying urban conditions themselves.

Users can explore:

- urban activity
- mobility conditions
- resident economic context
- no-vehicle households
- activity–mobility mismatch
- corridor classification
- Urban DNA profiles
- citywide priority patterns

This mode diagnoses the city **before adding the mega-event lens**.

---

## 2. FIFA Legacy Mode

**Question:**

> Where can event-driven investment create lasting urban value?

FIFA Legacy Mode overlays the existing urban mismatch with an event-relevance proxy.

It separates two concepts:

### Community Need
Existing activity–mobility mismatch.

### Event Opportunity
Proximity-based FIFA planning relevance.

### Legacy Opportunity
Where those two conditions overlap.

The goal is not simply to identify places near the stadium.

It is to identify places where **event relevance intersects with an existing urban need**.

---

# What CorridorIQ Does

## Interactive Houston Decision Surface

An interactive tract-level map allows users to explore multiple indicators across Harris County.

Available views include:

- Activity Score
- Mobility Score
- Economic Score
- Mismatch Score
- FIFA Relevance
- Legacy Priority
- Corridor Type

The map helps answer:

> **Where?**

---

## Urban Opportunity Matrix

The Opportunity Matrix visualizes:

- **X-axis:** Mobility Score
- **Y-axis:** Activity Score

A balance line represents:

```text
Activity = Mobility
```

Tracts farther above that line exhibit a larger positive activity–mobility mismatch under the prototype model.

This answers:

> **Why was this area flagged?**

---

## Urban DNA Fingerprints

CorridorIQ does not reduce a community to one number.

Each tract receives a multi-dimensional profile across indicators such as:

- Economic
- Activity
- Mobility
- Mismatch
- FIFA Relevance
- Legacy Priority

The Urban DNA heatmap makes it possible to see how similarly ranked tracts may reach that ranking for very different reasons.

---

## Priority Watchlist

CorridorIQ ranks candidate areas using the Legacy Priority index.

The watchlist gives planners a transparent shortlist containing metrics such as:

- tract
- corridor classification
- mismatch
- FIFA relevance
- Legacy Priority
- distance to NRG
- data completeness

Results can also be exported as CSV for additional analysis.

---

# Scenario Lab

CorridorIQ includes an interactive planning scenario tool.

Users can select a tract and test a hypothetical mobility-score improvement.

Available scenarios include:

- **Baseline:** +0
- **Moderate Mobility Improvement:** +15
- **Strong Mobility Improvement:** +30
- **Custom:** 0–30 points

The model recalculates:

- Mobility Score
- Mismatch Score
- Legacy Priority
- Priority Rank

and displays the results side-by-side.

> **Important:** Scenario Lab is an illustrative planning tool, not a traffic forecast or prediction of real-world infrastructure performance.

---

# Strategy Lab

Beyond single-tract exploration, CorridorIQ supports strategy-oriented analysis.

Potential planning lenses include:

### FIFA Corridor Focus
Prioritize areas where high mismatch overlaps strong event relevance.

### Equity First
Prioritize areas with meaningful mismatch and high levels of households without access to a vehicle.

### Highest Mismatch
Focus on the largest activity–mobility diagnostic gaps regardless of event relevance.

The goal is to help users explore **tradeoffs between alternative prioritization strategies**, rather than assuming that one ranking is universally correct.

---

# Citywide Scenario Outcomes

CorridorIQ can aggregate scenario results across targeted tracts.

Model-derived outputs may include:

- number of high-mismatch tracts
- population within targeted areas
- average mismatch in targeted corridors
- no-vehicle households within selected areas
- number of high-priority areas remaining under a scenario

These outputs describe changes **inside the CorridorIQ model**.

They should not be interpreted as guaranteed changes in:

- traffic congestion
- emissions
- economic output
- travel time
- construction cost

without additional modeling and data.

---

# Baseline → Scenario → Change

Scenario results can be interpreted through three views:

### Baseline
Existing modeled conditions.

### Scenario
Conditions after the selected illustrative mobility intervention.

### Change
The modeled difference between baseline and scenario.

This allows decision-makers to see not only which areas rank highly, but **where a proposed strategy changes the diagnostic picture**.

---

# Prototype Implementation Pathway

The hackathon challenge asks teams to consider impacts over time.

CorridorIQ therefore supports an illustrative implementation pathway such as:

| Stage | Interpretation |
|---|---|
| **2026** | Existing modeled baseline |
| **2027** | Phase 1 priority corridors |
| **2028** | Phase 2 expansion |
| **2030** | Full illustrative scenario |

> This timeline is an **illustrative implementation pathway, not a forecast**.

Its purpose is to demonstrate how phased intervention strategies could be compared over time.

---

# Corridor Comparison

Users can compare two tracts side-by-side using:

- Population
- Population Density
- Median Household Income
- No-Vehicle %
- Economic Score
- Activity Score
- Mobility Score
- Mismatch Score
- FIFA Relevance
- Legacy Priority
- Distance to NRG
- Corridor Type

This is particularly useful when two corridors appear similar on one metric but receive different priority scores because of the relationship between their indicators.

---

# Sensitivity Analysis

A prioritization model should not hide its assumptions.

CorridorIQ therefore tests alternative assumptions for how quickly FIFA relevance declines with distance.

The prototype evaluates:

- 10-mile proximity assumption
- 15-mile proximity assumption
- 20-mile proximity assumption

For each assumption, the app recalculates:

- FIFA relevance
- Legacy Priority
- tract ranking
- top-10 overlap

This helps answer:

> **Does the priority signal depend heavily on one arbitrary proximity parameter?**

We refer to this as **prototype sensitivity analysis**, not statistical validation.

---

# Guided 60-Second Demo

CorridorIQ includes a guided walkthrough designed around one consistent tract example.

### Step 1 — Find the mismatch
Identify where urban activity and mobility are out of alignment.

### Step 2 — Add the FIFA lens
Determine whether the same tract is relevant to the mega-event planning context.

### Step 3 — Test an intervention
Apply an illustrative mobility improvement and recalculate the tract's diagnostic priority.

### Step 4 — Check stability
Test whether the result remains similar under alternative FIFA proximity assumptions.

The walkthrough follows one narrative:

```text
CITYWIDE NEED
     ↓
FIFA OPPORTUNITY
     ↓
INTERVENTION
     ↓
LEGACY + SENSITIVITY
```

---

# Example Finding

One of the strongest signals identified by the prototype is:

## Census Tract 3143.01

| Metric | Value |
|---|---:|
| Activity Score | **82.4** |
| Mobility Score | **20.4** |
| Mismatch Score | **100.0** |
| FIFA Relevance | **77.2** |
| Legacy Priority | **77.2** |
| Distance to NRG | **0.44 mi** |

Why is this interesting?

The tract is not highlighted merely because it is close to NRG.

Its activity signal is substantially higher than its modeled mobility signal, producing one of the strongest mismatch diagnostics in the dataset.

Its proximity to the FIFA event context then makes that existing mismatch particularly timely for planning consideration.

> **Proximity creates the opportunity. The existing mismatch creates the reason to investigate.**

---

# Other Prototype Findings

### Census Tract 4214.02

- Population density: approximately **58,805 people/sq. mi.**
- Activity Score: **100.0**
- Mobility Score: **55.1**
- Mismatch Score: **99.0**
- Legacy Priority: **68.3**

This example illustrates why CorridorIQ looks at relationships rather than density in isolation.

---

### Census Tract 3140.04

- Activity Score: **100.0**
- Mobility Score: **70.0**
- Mismatch Score: **66.1**
- FIFA Relevance: **97.2**
- Legacy Priority: **64.3**
- No-vehicle households: **32.9%**
- Distance to NRG: **0.81 mi**

This tract demonstrates how a moderate-to-high mismatch can become more timely when combined with strong event relevance.

---

# Methodology

CorridorIQ is intentionally designed as a **transparent rule-based prototype**, rather than a black-box machine-learning system.

The goal is for planners and residents to understand why a tract receives a particular result.

---

## Geographic Unit

The current prototype analyzes Census tracts in Harris County, Texas.

Number of tracts analyzed:

**1,115**

Geometry is standardized to:

```text
EPSG:4326
```

for web mapping.

---

## Population Density

Population density is calculated using Census population and TIGER/Line land area.

```text
Population Density
=
Population / Land Area
```

Land area is converted from square meters to square miles.

---

## Economic Score

The prototype uses **median household income** as a resident economic-condition indicator.

Values are normalized to a 0–100 score.

Median household income should not be interpreted as a complete measure of commercial or employment intensity.

Future versions should incorporate:

- employment density
- business establishments
- commercial floor area
- job accessibility
- development activity

---

## Activity Score

Activity Score currently uses population density as the primary urban-intensity signal.

Higher density receives a higher normalized Activity Score.

This provides a transparent proxy for urban intensity but does not capture every form of activity.

---

## Mobility Score

The mobility dimension incorporates available mobility-related indicators, including household vehicle availability and locally available transit context where included in the processed dataset.

One core input is:

```text
No-Vehicle %
=
Households with no vehicle available
/
Total households
× 100
```

The Mobility Score is an analytical proxy.

It should not be interpreted as directly measured transportation capacity, congestion, travel time, or service quality.

---

# Mismatch Score

The central analytical idea is the relationship between Activity and Mobility.

The prototype begins with:

```text
Mismatch Raw
=
Activity Score - Mobility Score
```

Only positive gaps are treated as positive mismatch signals:

```text
Positive Mismatch
=
max(Activity Score - Mobility Score, 0)
```

The resulting signal is normalized to a 0–100 Mismatch Score.

A high mismatch means:

> the tract's modeled urban activity exceeds its modeled mobility condition by a relatively large amount.

It does **not** mean measured congestion.

---

# FIFA Relevance

The MVP uses proximity to NRG Stadium as a transparent event-relevance proxy.

Approximate NRG Stadium reference point:

```text
29.6847, -95.4107
```

Distance from each tract centroid is calculated after projecting the geometry appropriately for distance measurement.

FIFA relevance then decreases as distance increases under a prototype distance-decay assumption.

The app also tests multiple proximity assumptions through sensitivity analysis.

FIFA Relevance should be interpreted as:

> **an event-proximity planning proxy**

not actual visitor demand.

---

# Legacy Priority

The prototype combines mismatch and event relevance using:

```text
Legacy Priority
=
Mismatch Score × FIFA Relevance / 100
```

This intentionally requires both conditions.

A tract with:

- high mismatch but little FIFA relevance

and a tract with:

- high FIFA relevance but no positive mismatch

will not automatically receive a high Legacy Priority.

This creates the central decision concept:

> **Where do an existing urban gap and a temporary mega-event opportunity overlap?**

Legacy Priority is a **prioritization index**, not a prediction of economic impact or infrastructure ROI.

---

# Corridor Classification

CorridorIQ uses explainable rule-based categories rather than machine learning.

Prototype classifications include:

- **High-Intensity / Mobility Gap**
- **Established Urban Hub**
- **Emerging Opportunity**
- **Lower Priority**

The purpose is interpretability.

A user should be able to understand why an area belongs to a particular category.

---

# Data Completeness

CorridorIQ reports tract-level completeness using core inputs such as:

- population
- population density
- median household income
- no-vehicle percentage

Missing values are preserved rather than silently replaced with zero.

For example:

```text
4 of 4 fields available = 100%
3 of 4 fields available = 75%
```

This prevents missing data from being mistaken for an actual observed value.

---

# Data Sources

## U.S. Census Bureau — 2024 ACS 5-Year Estimates

Tables currently used include:

### B01003 — Total Population

Used for:

- tract population
- population density

### B19013 — Median Household Income

Used as the current economic-condition indicator.

### B08201 — Household Size by Vehicles Available

Used to calculate:

- total households
- households with no vehicle available
- no-vehicle household percentage

---

## U.S. Census Bureau TIGER/Line

2024 Census tract boundaries for Texas.

The prototype filters the statewide tract file to:

```text
State FIPS: 48
County FIPS: 201
```

corresponding to Harris County.

---

## Transit Context

Local transit-stop information is incorporated where available in the current processed project data.

Transit information is used as planning context rather than treated as a complete representation of:

- service frequency
- reliability
- capacity
- travel time
- ridership

---

# Why FIFA?

FIFA World Cup 2026 is used as a **mega-event case study**, not as the endpoint of the product.

Mega-events create unusually concentrated periods of:

- infrastructure attention
- transportation demand
- public investment
- inter-agency coordination
- political visibility

CorridorIQ asks whether that temporary planning window can help accelerate improvements in places that already show longer-term urban needs.

The central idea is:

> **FIFA is the catalyst, not the endpoint.**

---

# Legacy Beyond FIFA

The same framework can be reused for other high-intensity events and planning contexts, including:

- Houston Livestock Show and Rodeo
- major football games
- concerts
- conventions
- international sporting events
- large festivals
- future host-city events
- long-range corridor planning

The event layer can change.

The underlying question remains:

> Where can short-term event investment reinforce long-term city needs?

---

# Sustainability Connection

For CorridorIQ, sustainability is not limited to environmental accounting.

The prototype focuses on improving alignment between:

- urban intensity
- transportation access
- households with limited vehicle availability
- major-event infrastructure opportunity
- long-term corridor planning

Better alignment can support planning for:

- multimodal accessibility
- reduced dependence on event-only transportation responses
- more durable infrastructure investments
- equitable access
- resilient high-intensity districts

Future versions could also incorporate environmental-resilience layers such as:

- flood exposure
- extreme heat
- land subsidence
- energy resilience

These are intentionally left as future extensions rather than being inserted into the current model without sufficient data.

---

# Limitations

CorridorIQ is a hackathon prototype and should be interpreted accordingly.

### 1. Tract-level geography

Census tracts do not perfectly represent real-world transportation or development corridors.

Future work should evaluate corridor-level aggregation using roads, transit routes, activity centers, and parcel data.

### 2. Economic intensity

Median household income is a resident economic indicator, not a complete measure of economic activity.

Future versions should incorporate employment, business, commercial property, and job-density data.

### 3. Land use

Detailed parcel-level land-use information is not yet a core component of the final MVP.

Adding reliable land-use classifications would substantially strengthen Track 4 analysis.

### 4. Development potential

The current model does not provide a complete parcel-level development-potential forecast.

Future work could include:

- housing-unit growth
- population growth
- development permits
- vacant land
- zoning capacity
- development pipeline data

### 5. Mobility

The Mobility Score is a screening indicator.

It is not equivalent to measured roadway capacity, transit capacity, congestion, or accessibility.

### 6. FIFA relevance

The current FIFA relevance model is primarily proximity-based.

It does not represent actual visitor movement or observed event demand.

### 7. Scenario analysis

Scenario interventions modify model indicators.

They do not predict actual reductions in:

- congestion
- emissions
- travel time
- operating cost

More detailed transportation modeling would be required for those claims.

---

# Future Work

A production version of CorridorIQ could incorporate:

### Better economic-intensity data

- employment density
- business establishments
- commercial activity
- visitor spending
- job accessibility

### Land use

- parcel-level land use
- mixed-use intensity
- vacant / developable land
- zoning

### Development potential

- building permits
- housing-unit growth
- population growth
- planned developments

### Transportation

- transit frequency
- service hours
- ridership
- travel time
- bike infrastructure
- sidewalk connectivity
- first/last-mile accessibility

### Mega-event geography

- official event zones
- hotels
- fan festival locations
- transit hubs
- observed visitor movement

### Resilience

- flood risk
- extreme heat
- land subsidence
- power resilience

### Geographic expansion

The framework could ultimately be applied to:

- additional Houston districts
- other U.S. FIFA host cities
- other mega-events

---

# Tech Stack

- **Python**
- **Pandas**
- **GeoPandas**
- **NumPy**
- **Plotly**
- **Streamlit**
- **U.S. Census ACS**
- **U.S. Census TIGER/Line**

---

# Project Structure

```text
CorridorIQ/
│
├── app.py
├── prepare_data.py
├── requirements.txt
├── README.md
├── DEVPOST.md
├── SUBMISSION_CHECKLIST.md
├── .gitignore
│
├── data/
│   ├── processed/
│   │   ├── corridoriq_tracts.csv
│   │   └── corridoriq_tracts.geojson
│   │
│   └── raw/
│       └── local source data
│
└── archive/
    └── optional development/debug utilities
```

Raw data is intentionally excluded from Git where appropriate.

Processed deployment files required by the application are included.

---

# Run Locally

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd CorridorIQ
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it.

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If you need to regenerate processed data:

```bash
python prepare_data.py
```

Start the app:

```bash
streamlit run app.py
```

Then open the local Streamlit URL displayed in the terminal.

---

# Deployment

The application can be deployed using **Streamlit Community Cloud**.

The deployed application requires:

```text
app.py
requirements.txt
data/processed/corridoriq_tracts.csv
data/processed/corridoriq_tracts.geojson
```

plus any other processed files referenced directly by `app.py`.

All runtime paths should remain relative to the repository root.

---

# Live Demo

### Try CorridorIQ

**[Launch the interactive application →](https://corridor-iq.streamlit.app)**

For the fastest introduction, click:

> **See how CorridorIQ works — 60 sec**

The guided walkthrough moves through:

1. Citywide mismatch
2. FIFA opportunity
3. Intervention scenario
4. Sensitivity / legacy

---

# Screenshots

## Houston Decision Surface

_Add screenshot here_

```markdown
![CorridorIQ Decision Surface](docs/images/decision-surface.png)
```

## Urban Opportunity Matrix

_Add screenshot here_

```markdown
![Urban Opportunity Matrix](docs/images/opportunity-matrix.png)
```

## Strategy Lab

_Add screenshot here_

```markdown
![CorridorIQ Strategy Lab](docs/images/strategy-lab.png)
```

---

# Hackathon Alignment

## Track 4 — High Intensity Corridors & Future Growth Districts

The challenge calls for a:

> data-driven classification system that identifies and maps urban corridors, districts, and communities based on economic intensity, mobility patterns, land-use characteristics, and development potential.

CorridorIQ contributes a prototype approach based on:

- tract-level spatial classification
- urban activity indicators
- mobility indicators
- resident economic context
- mismatch detection
- event relevance
- scenario testing
- sensitivity analysis
- decision-support visualization

The current MVP is strongest in **activity, mobility, classification, and scenario analysis**.

More detailed land-use, employment-intensity, and development-pipeline data are identified as next-stage extensions.

---

# Hackathon Deliverable Alignment

The hackathon asks teams to combine:

- **data**
- **maps**
- **charts**
- **scenario comparisons**
- **priority identification**
- **measurable intervention effects**
- **outcomes over time**

CorridorIQ addresses those through:

| Requirement | CorridorIQ |
|---|---|
| Interactive visualization | Streamlit decision-support application |
| Maps | Tract-level Houston decision surface |
| Charts | Opportunity Matrix, Urban DNA profiles, scenario charts |
| Priority areas | Legacy Priority + corridor classification |
| Scenario comparison | Baseline vs illustrative mobility intervention |
| Tradeoffs | Strategy and corridor comparison tools |
| Impact | Model-derived before/after diagnostic outcomes |
| Over time | Illustrative phased implementation pathway |
| Transparency | Sensitivity analysis + data completeness |
| Legacy | Reusable framework beyond FIFA 2026 |

---

# Core Takeaway

> **The most important planning signal is not always where one indicator is highest. It may be where multiple urban systems are out of alignment.**

CorridorIQ makes those relationships visible.

FIFA 2026 provides the case study.

The larger goal is to help cities turn:

**temporary event investment**

into:

**long-term urban legacy.**

---

# Team

**Team:** CorridorIQ

Team members:

- Aishwarya Jakka
- Shubham Gupta

Built for the **Rice University Urban Sustainability Hackathon — World Cup 2026 HACK**.

---

# Disclaimer

CorridorIQ is a research and hackathon prototype.

The outputs are intended for exploratory planning and decision-support purposes.

They should not be interpreted as:

- engineering recommendations
- transportation forecasts
- causal impact estimates
- infrastructure investment guarantees
- official City of Houston, METRO, FIFA, Rice University, or H-GAC recommendations

All scenario outputs should be interpreted as illustrative model results.

---

## CorridorIQ

### **Mismatch, not magnitude.**
### **FIFA is the catalyst, not the endpoint.**
### **From event investment to urban legacy.**
