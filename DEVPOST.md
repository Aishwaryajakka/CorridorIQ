# Inspiration

Mega-events create a rare window of infrastructure investment, political attention, and cross-agency coordination. But cities often struggle to answer a basic question:

**Where should those investments go so they support the event today and still create value for residents afterward?**

For Houston, FIFA World Cup 2026 provided a strong case study. Rather than building another dashboard that simply maps density, transit, or income independently, we wanted to understand where urban systems are **out of alignment**.

That became the core idea behind CorridorIQ:

> **Mismatch, not magnitude.**

A corridor may not be the highest on any one indicator, but if urban activity is high while mobility conditions lag behind, that relationship can reveal a more meaningful planning signal.

Our goal was to help cities move from **baseline → diagnosis → prioritization → strategy**.

---

# What it does

**CorridorIQ is an interactive urban decision-support platform for identifying high-intensity corridors and legacy investment opportunities.**

The platform analyzes Harris County census tracts and combines:

- urban activity
- mobility conditions
- resident economic context
- vehicle availability
- event relevance
- tract-level spatial patterns

to build an interpretable **Urban DNA** profile for each tract.

CorridorIQ then detects where activity and mobility conditions are out of alignment and overlays FIFA-related planning relevance to identify **Legacy Opportunity Areas**.

The application provides two complementary planning lenses.

### Citywide Analysis

Answers:

> **Where are Houston’s urban systems most out of alignment?**

Users can explore activity, mobility, mismatch, corridor type, and Urban DNA patterns across the county.

### FIFA Legacy Mode

Answers:

> **Where can event-driven mobility investment create lasting urban value?**

This mode focuses on where an existing urban mismatch overlaps the FIFA planning context.

Instead of treating proximity to the event as the entire problem, CorridorIQ separates:

**Community Need**  
Existing activity–mobility mismatch

**Event Opportunity**  
FIFA relevance

**Legacy Opportunity**  
Where those two conditions overlap

---

# The core insight

Most urban dashboards evaluate indicators independently.

CorridorIQ focuses on the **relationship between them**.

The prototype compares urban activity with mobility conditions and calculates a diagnostic mismatch.

Conceptually:

```text
Activity
−
Mobility
=
Mismatch
```

Then:

```text
Mismatch
×
FIFA Relevance
=
Legacy Priority
```

This means a tract does not rank highly simply because it is close to the stadium.

It must also show an underlying activity–mobility mismatch.

That distinction is central to the project:

> **Proximity creates the opportunity. The existing mismatch creates the reason to investigate.**

---

# Key features

CorridorIQ includes:

- Interactive tract-level Houston map
- Citywide and FIFA Legacy analysis modes
- Urban Opportunity Matrix
- Urban DNA tract profiles
- Urban DNA heatmap
- Priority Watchlist
- Guided 60-second demo
- Scenario Lab
- Strategy Lab
- Two-corridor comparison
- Baseline vs scenario analysis
- Sensitivity testing
- Data completeness indicators
- CSV export

The guided demo walks a user through one consistent planning story:

1. Identify a citywide mismatch
2. Add the FIFA event lens
3. Test an illustrative mobility intervention
4. Check whether the ranking remains stable under different assumptions

---

# How we built it

CorridorIQ was built in Python using:

- Streamlit
- Pandas
- GeoPandas
- Plotly
- NumPy

The spatial unit is the Census tract.

The prototype currently analyzes **1,115 Harris County tracts**.

We used 2024 U.S. Census Bureau ACS 5-Year Estimates including:

- B01003 — Total Population
- B19013 — Median Household Income
- B08201 — Vehicle Availability

We also used 2024 U.S. Census TIGER/Line tract boundaries.

Population density was calculated from Census population and tract land area.

Vehicle availability was used to derive the percentage of households with no vehicle available.

All tract geometry used for the web application is standardized for web mapping.

---

# Methodology

CorridorIQ uses a transparent, rule-based methodology rather than a black-box machine-learning model.

### Activity Score

Population density is used as the current proxy for urban activity intensity.

### Economic Score

Median household income is used as a resident economic-context indicator.

### Mobility Score

The mobility score uses available mobility-related indicators, including vehicle availability and transit context where available in the processed dataset.

### Mismatch Score

The model compares Activity Score and Mobility Score.

A simplified representation is:

```text
Mismatch Raw =
Activity Score - Mobility Score
```

Only positive gaps contribute to the positive mismatch diagnostic.

### FIFA Relevance

The MVP uses event proximity as a planning proxy for FIFA relevance.

It should not be interpreted as measured visitor demand.

### Legacy Priority

```text
Legacy Priority =
Mismatch Score × FIFA Relevance / 100
```

Legacy Priority is a **prioritization index**, not a prediction of economic impact or infrastructure performance.

---

# Example finding

One of the strongest prototype signals is **Census Tract 3143.01**.

- Activity Score: **82.4**
- Mobility Score: **20.4**
- Mismatch Score: **100.0**
- FIFA Relevance: **77.2**
- Legacy Priority: **77.2**
- Distance to NRG: **0.44 miles**

The tract is not highlighted simply because it is close to NRG.

Its urban activity signal is substantially higher than its modeled mobility signal, creating one of the strongest mismatch diagnostics in the dataset.

That makes the location interesting from a legacy-planning perspective: an event-related mobility investment could potentially align with a pre-existing urban need.

---

# Scenario analysis

CorridorIQ includes an illustrative Scenario Lab where users can test hypothetical changes to a tract’s mobility score.

Available scenarios include:

- Baseline
- Moderate Mobility Improvement
- Strong Mobility Improvement
- Custom improvement

The application recalculates:

- mobility
- mismatch
- Legacy Priority
- ranking

and compares baseline and scenario values.

These scenarios are explicitly labeled:

> **Illustrative planning scenario — not a forecast.**

The goal is not to predict actual congestion or emissions reductions.

The goal is to let decision-makers understand how the prioritization framework responds when modeled conditions change.

---

# Sensitivity analysis

A good prioritization tool should make its assumptions visible.

CorridorIQ therefore tests multiple assumptions about how quickly FIFA relevance declines with distance.

The prototype compares 10-mile, 15-mile, and 20-mile proximity assumptions and evaluates:

- tract ranking
- Legacy Priority
- top-10 overlap

This is presented as **prototype sensitivity analysis**, not statistical validation.

It helps users see whether a result depends heavily on one arbitrary parameter.

---

# Challenges we ran into

One of our biggest challenges was keeping the model ambitious enough to be useful while remaining transparent and defensible.

Urban planning datasets often come from different sources, geographic scales, and time periods. We had to carefully align tract boundaries, Census indicators, mobility inputs, and event context without overstating what each dataset could prove.

We also explored more detailed land-use data, but reliability and integration constraints made it impractical for the final MVP. Rather than force a weak layer into the model, we kept the final methodology focused on indicators we could clearly explain and validate.

Another challenge was designing the application so that users could understand the logic quickly. The final interface therefore emphasizes a guided journey from:

**citywide need → FIFA opportunity → intervention → legacy**

rather than presenting users with a collection of disconnected charts.

---

# Accomplishments that we're proud of

We are proud that CorridorIQ goes beyond simply ranking neighborhoods.

The project:

- detects relationships between indicators rather than only mapping magnitude
- uses an explainable prioritization methodology
- allows users to compare alternative scenarios
- exposes modeling assumptions through sensitivity analysis
- connects a temporary mega-event opportunity to longer-term urban planning
- translates tract-level data into an interactive decision-support workflow

The resulting application is not just a visualization of conditions.

It is a prototype for asking:

> **Where should a city investigate first, why, and what changes under a different strategy?**

---

# What we learned

We learned that the most useful planning insight often comes from the relationship between systems.

A high-density tract is not automatically a problem.

A transit-poor tract is not automatically the highest priority.

But when high activity, weak mobility conditions, limited vehicle access, and event relevance overlap, the combined signal can reveal a more actionable planning opportunity.

We also learned the importance of methodological transparency.

Rather than presenting one score as an unquestionable answer, CorridorIQ allows users to:

- inspect the underlying indicators
- compare tracts
- test scenarios
- change assumptions
- examine data completeness

That makes the tool more useful for discussion and decision support.

---

# Impact and legacy

FIFA 2026 is the case study, but the framework is designed to extend beyond one event.

The same approach could support planning around:

- Houston Livestock Show and Rodeo
- major sporting events
- concerts
- conventions
- festivals
- future international events
- long-term corridor planning

The event layer can change while the underlying question remains the same:

> **Where can short-term investment reinforce long-term city needs?**

That is the legacy we want CorridorIQ to support.

---

# What's next for CorridorIQ

Future versions could strengthen the model with:

- parcel-level land use
- employment density
- business activity
- development permits
- housing-unit growth
- transit frequency
- ridership
- pedestrian infrastructure
- bike infrastructure
- hotel and event-demand data
- flood exposure
- extreme heat
- land subsidence
- additional FIFA host cities

A production version could also shift from Census tracts toward true corridor geometries built from transit routes, road networks, activity centers, and development districts.

---

# Built with

- Python
- Streamlit — interactive web application
- Pandas — data processing and analysis
- GeoPandas — geospatial analysis
- NumPy — numerical operations
- Plotly — interactive charts and visualizations
- U.S. Census ACS 5-Year Estimates — population, income, and vehicle-availability indicators
- U.S. Census TIGER/Line — Census tract boundaries
- GitHub — version control and source repository
- Streamlit Community Cloud — web deployment

---

# Final takeaway

> **CorridorIQ helps cities turn temporary mega-event investment into permanent urban value.**

It does that by focusing on one simple idea:

> **The most important signal is not always where one metric is highest. It is often where urban systems are out of alignment.**

**Mismatch, not magnitude.**  
**FIFA is the catalyst, not the endpoint.**  
**From event investment to urban legacy.**
