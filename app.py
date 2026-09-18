"""CorridorIQ: polished civic decision-support demo for FIFA 2026 planning."""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

CSV = Path("data/processed/corridoriq_tracts.csv")
GEOJSON = Path("data/processed/corridoriq_tracts.geojson")
NRG_LAT, NRG_LON = 29.6847, -95.4107

st.set_page_config(page_title="CorridorIQ", page_icon="◈", layout="wide")
st.markdown(
    """
    <style>
      :root {color-scheme:dark;}
      html, body, [class*="st-"] {font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
      .stApp, [data-testid="stAppViewContainer"] {background:#1D1D1B; color:#F4F0E6;}
      .block-container {max-width:1240px; padding-top:3rem !important; padding-bottom:4rem;}
      h1, h2, h3, h4 {color:#F4F0E6 !important; font-family:inherit;}
      h1 {font-size:3rem !important; line-height:1.05 !important; font-weight:700 !important;
          letter-spacing:-.045em; margin-bottom:.2rem !important;}
      h2 {font-size:1.9rem !important; line-height:1.2 !important; font-weight:700 !important;
          letter-spacing:-.025em; padding-top:2.7rem !important; margin-bottom:.75rem !important;}
      h3 {font-size:1.4rem !important; font-weight:600 !important;}
      h4 {font-size:1.15rem !important; font-weight:600 !important;}
      [data-testid="stMarkdownContainer"] p, [data-testid="stCaptionContainer"] {line-height:1.6;}
      .eyebrow, .stage-label {color:#D6AE52; font-weight:600; font-size:.78rem; letter-spacing:.1em; text-transform:uppercase;}
      .stage-label {margin:3.2rem 0 .65rem;}
      .subtitle {font-size:1.4rem; font-weight:600; color:#F4F0E6; margin:.25rem 0 .5rem;}
      .tagline {font-size:1.08rem; max-width:820px; color:#A9A59C; line-height:1.65;}
      .badge {display:inline-block; background:rgba(214,174,82,.12); color:#D6AE52;
              border:1px solid rgba(214,174,82,.42); padding:.35rem .7rem; border-radius:999px;
              font-size:.78rem; font-weight:600; margin:.55rem 0 1rem;}
      .card {border:1px solid rgba(38,37,33,.10); border-radius:12px; padding:1.05rem 1.15rem;
             background:#F4F0E6; color:#262521; box-shadow:none; min-height:0; height:auto;
             overflow-wrap:anywhere;}
      .card div, .card b, .card strong {color:#262521;}
      .hero-card {border-left:4px solid #7A263A; background:#F4F0E6;}
      .card .card-label, .card-label {font-size:.78rem; color:rgba(38,37,33,.68); font-weight:600;
                                     letter-spacing:.05em; text-transform:none;}
      .card .big-number, .big-number {font-size:1.75rem; font-weight:700; color:#262521;
                                     line-height:1.15; margin:.4rem 0;}
      .card span, .card-subtext {color:rgba(38,37,33,.68);}
      .flow {text-align:center; border:1px solid rgba(244,240,230,.10); border-radius:10px;
             padding:.8rem .5rem; background:#292824; color:#F4F0E6; min-height:0; height:auto;}
      .flow strong {display:block; color:#D6AE52; font-size:.78rem; font-weight:600; letter-spacing:.04em;}
      .flow span {font-size:.85rem; color:#A9A59C;}
      .operator {font-size:1.55rem; font-weight:600; text-align:center; padding-top:1.1rem; color:#A9A59C;}
      .model-strip {display:flex; align-items:center; justify-content:center; gap:.75rem; flex-wrap:wrap;
                    padding:.9rem 1rem; margin:.4rem 0 1.4rem; border:1px solid rgba(244,240,230,.10);
                    border-radius:12px; background:#292824;}
      .model-step {font-size:.82rem; font-weight:600; color:#F4F0E6; letter-spacing:.02em;}
      .model-step.activity {background:rgba(116,122,61,.34); color:#F4F0E6; padding:.28rem .5rem; border-radius:6px;}
      .model-step.mobility {color:#D6AE52;}
      .model-step.mismatch, .model-step.legacy {background:rgba(122,38,58,.58); color:#F4F0E6;
                                                padding:.28rem .5rem; border-radius:6px;}
      .model-step.fifa {color:#D6AE52;}
      .model-op {color:#A9A59C; font-size:1.05rem; font-weight:600;}
      .finding {border-top:3px solid #7A263A;}
      .why {border:1px solid rgba(38,37,33,.10); background:#F4F0E6; color:#262521;
            border-radius:12px; padding:1rem 1.15rem; height:auto;}
      .why b, .why strong {color:#262521;}
      div[data-testid="stMetric"] {border:1px solid rgba(38,37,33,.10); border-radius:12px;
                                   padding:.82rem 1rem; background:#F4F0E6; color:#262521;
                                   min-height:0; height:auto; box-shadow:none;}
      div[data-testid="stMetric"] [data-testid="stMetricLabel"],
      div[data-testid="stMetric"] [data-testid="stMetricLabel"] p {color:rgba(38,37,33,.68) !important; font-weight:600;}
      div[data-testid="stMetric"] [data-testid="stMetricValue"],
      div[data-testid="stMetric"] [data-testid="stMetricValue"] > div {color:#262521 !important; font-weight:700;}
      div[data-testid="stMetric"] [data-testid="stMetricDelta"],
      div[data-testid="stMetric"] [data-testid="stMetricDelta"] > div,
      div[data-testid="stMetric"] [data-testid="stMetricDelta"] svg {color:#747A3D !important; fill:#747A3D !important;}
      div[data-testid="stDataFrame"] {border:1px solid rgba(244,240,230,.10); border-radius:12px; overflow:hidden;}
      .section-note {color:#A9A59C; margin-top:-.55rem; margin-bottom:1rem;}
      button[kind="primary"], button[data-testid="stBaseButton-primary"] {background:#7A263A !important;
        color:#F4F0E6 !important; border:1px solid #7A263A !important; box-shadow:none !important;}
      button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover {background:#5C1D2C !important;
        border-color:#5C1D2C !important;}
      button[kind="secondary"], button[data-testid="stBaseButton-secondary"], [data-testid="stDownloadButton"] button {
        background:#292824 !important; color:#F4F0E6 !important; border:1px solid #747A3D !important; box-shadow:none !important;}
      button[kind="secondary"]:hover, button[data-testid="stBaseButton-secondary"]:hover,
      [data-testid="stDownloadButton"] button:hover {border-color:#D6AE52 !important; color:#F4F0E6 !important;}
      button[data-baseweb="tab"] {color:#A9A59C !important; font-weight:600;}
      button[data-baseweb="tab"][aria-selected="true"] {color:#F4F0E6 !important;}
      [data-baseweb="tab-highlight"] {background-color:#7A263A !important;}
      div[data-baseweb="select"] > div, div[data-baseweb="input"], [data-baseweb="base-input"] {
        background:#292824 !important; border-color:rgba(169,165,156,.45) !important; color:#F4F0E6 !important;}
      [data-testid="stAlert"] {background:rgba(116,122,61,.18) !important;
                               border:1px solid #747A3D !important; color:#F4F0E6 !important;}
      [data-testid="stAlert"] p, [data-testid="stAlert"] div {color:#F4F0E6 !important;}
      [data-testid="stExpander"] {border-color:rgba(244,240,230,.10) !important; background:#292824;}
      [data-testid="stHorizontalBlock"] {gap:1rem;}
      @media (max-width: 768px) {
        .block-container {padding:1rem .75rem 2rem;}
        h1 {font-size:2.6rem !important;}
        h2 {font-size:1.65rem !important; padding-top:2.1rem !important;}
        .subtitle {font-size:1.15rem;}
        .tagline {font-size:1rem;}
        .big-number {font-size:1.45rem; overflow-wrap:anywhere;}
        .flow {min-height:auto; padding:.7rem .35rem;}
        .model-strip {justify-content:flex-start; gap:.55rem;}
        .stage-label {margin-top:2.5rem;}
      }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_data():
    frame = pd.read_csv(CSV, dtype={"GEOID": "string"})
    with GEOJSON.open(encoding="utf-8") as handle:
        geography = json.load(handle)
    for feature in geography["features"]:
        feature["properties"]["GEOID"] = str(feature["properties"]["GEOID"])
    frame["selector"] = frame["tract_name"] + " · " + frame["GEOID"]
    frame["baseline_rank"] = frame["legacy_priority"].rank(method="min", ascending=False)
    core_fields = ["population", "population_density", "median_income", "no_vehicle_pct"]
    frame["data_completeness_pct"] = frame[core_fields].notna().sum(axis=1) / len(core_fields) * 100
    return frame, geography


def fmt(value, pattern=".1f", unavailable="Unavailable"):
    return format(value, pattern) if pd.notna(value) else unavailable


def style_dark_chart(figure):
    """Apply the shared charcoal visual system without changing chart data."""
    figure.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "#F4F0E6", "family": "Inter, ui-sans-serif, system-ui, sans-serif"},
        legend={"font": {"color": "#F4F0E6"}},
        hoverlabel={"bgcolor": "#F4F0E6", "bordercolor": "#A9A59C", "font": {"color": "#262521"}},
    )
    figure.update_xaxes(color="#A9A59C", gridcolor="rgba(169,165,156,.18)", zerolinecolor="rgba(169,165,156,.28)")
    figure.update_yaxes(color="#A9A59C", gridcolor="rgba(169,165,156,.18)", zerolinecolor="rgba(169,165,156,.28)")
    return figure


def tract_explanation(row):
    if pd.isna(row["mismatch_score"]):
        return "This tract lacks a complete mobility signal, so the model does not assign a diagnostic priority."
    if row["mismatch_score"] >= 75 and row["fifa_relevance"] >= 65:
        return "High activity relative to mobility produces a large mismatch signal, while strong FIFA relevance makes it especially timely to examine."
    if row["mismatch_score"] >= 75:
        return "High activity relative to mobility produces a large mismatch signal, although FIFA relevance is more moderate."
    if row["fifa_relevance"] >= 75 and row["mismatch_score"] > 0:
        return "This tract has a moderate mismatch but ranks higher because its FIFA relevance is strong."
    if row["mismatch_score"] > 0:
        return "Activity exceeds modeled mobility capacity, creating a positive—but comparatively moderate—mismatch signal."
    return "Modeled mobility capacity meets or exceeds activity, so this tract has no positive mismatch signal."


def normalize_scenario(raw_gap, frame):
    if pd.isna(raw_gap):
        return float("nan")
    low, high = frame["mismatch_severity_raw"].quantile([0.02, 0.98])
    return max(0.0, min(100.0, (raw_gap - low) / (high - low) * 100))


def scenario_values(row, improvement, frame):
    mobility = min(100, row["mobility_score"] + improvement) if pd.notna(row["mobility_score"]) else float("nan")
    raw_gap = max(row["activity_score"] - mobility, 0) if pd.notna(mobility) else float("nan")
    mismatch = normalize_scenario(raw_gap, frame)
    priority = mismatch * row["fifa_relevance"] / 100
    rank = 1 + int((frame.drop(index=row.name)["legacy_priority"] > priority).sum()) if pd.notna(priority) else None
    return mobility, mismatch, priority, rank


def sensitivity_results(frame):
    results = {}
    for miles in (10, 15, 20):
        nrg_score = (100 * (1 - frame["distance_to_nrg_miles"] / miles)).clip(lower=0, upper=100)
        fifa_score = 0.70 * nrg_score + 0.30 * frame["transit_supply_score"]
        priority_score = frame["mismatch_score"] * fifa_score / 100
        results[miles] = {"fifa": fifa_score, "priority": priority_score,
                          "rank": priority_score.rank(method="min", ascending=False)}
    return results


def intervention_category(row, frame):
    """Screening suggestion only; does not alter any analytical score."""
    mobility_median = frame["mobility_score"].median()
    activity_q75 = frame["activity_score"].quantile(0.75)
    no_vehicle_q75 = frame["no_vehicle_pct"].quantile(0.75)
    transit_median = frame["transit_supply_score"].median()
    if row["distance_to_nrg_miles"] <= 3 and row["mismatch_score"] > 0:
        return "First / Last Mile Access Review"
    if row["no_vehicle_pct"] >= no_vehicle_q75 and row["mobility_score"] < mobility_median:
        return "Transit Service Gap Review"
    if row["activity_score"] >= activity_q75 and row["mobility_score"] < mobility_median:
        return "Mobility Capacity Study"
    if row["fifa_relevance"] >= frame["fifa_relevance"].quantile(0.75) and row["transit_supply_score"] <= transit_median:
        return "Shuttle / Transfer Evaluation"
    return "Pedestrian Connectivity Review"


if not CSV.exists() or not GEOJSON.exists():
    st.error("Processed files are missing. Run `python prepare_data.py` from the project root.")
    st.stop()
try:
    df, geojson = load_data()
except Exception as exc:
    st.error(f"Unable to load processed data: {exc}")
    st.stop()

selector_options = df.sort_values("tract_name")["selector"].tolist()
if "selected_tract" not in st.session_state:
    st.session_state.selected_tract = df.nlargest(1, "legacy_priority").iloc[0]["selector"]
df["suggested_intervention_category"] = df.apply(lambda row: intervention_category(row, df), axis=1)
leader = df.nlargest(1, "legacy_priority").iloc[0]
positive_mismatches = df.loc[df["mismatch_score"] > 0, "mismatch_score"]
legacy_mismatch_threshold = positive_mismatches.median()
legacy_fifa_threshold = df["fifa_relevance"].quantile(0.75)
high_mismatch = df["mismatch_score"] >= legacy_mismatch_threshold
strong_fifa = df["fifa_relevance"] >= legacy_fifa_threshold
legacy_opportunity = high_mismatch & strong_fifa

# HERO
st.markdown('<div class="eyebrow">Houston urban decision support</div>', unsafe_allow_html=True)
st.title("CorridorIQ")
st.markdown('<div class="subtitle">Houston Urban DNA for FIFA 2026</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="tagline">Find where urban intensity and mobility are out of alignment — and where FIFA 2026 creates a timely opportunity to act.</div>',
    unsafe_allow_html=True,
)
st.markdown('<div class="badge">Track 4 — High Intensity Corridors &amp; Future Growth Districts</div>', unsafe_allow_html=True)
st.write(
    "Most urban dashboards show where indicators are high or low. CorridorIQ focuses on where they conflict. "
    "It combines a tract-level mismatch diagnostic with FIFA relevance to surface areas that may deserve closer planning attention."
)

analysis_mode = st.radio("Analysis Mode", ["Citywide Analysis", "FIFA Legacy Mode"], horizontal=True)
legacy_mode = analysis_mode == "FIFA Legacy Mode"
if st.session_state.get("last_analysis_mode") != analysis_mode:
    st.session_state.scenario_preset = "Moderate Mobility Improvement (+15)" if legacy_mode else "Baseline"
    if legacy_mode:
        st.session_state.scenario_tract = leader["selector"]
    st.session_state.last_analysis_mode = analysis_mode
if legacy_mode:
    st.markdown("## Where can event-driven mobility investment create lasting value?")
    st.markdown('<div class="subtitle">CorridorIQ identifies places where FIFA/event relevance overlaps with existing activity–mobility mismatches.</div>', unsafe_allow_html=True)
    st.write("A mega-event creates a temporary window for infrastructure investment. CorridorIQ helps distinguish locations that are merely close to event activity from locations where event-driven investment also aligns with an existing community mobility need.")
    lm1, lm2, lm3 = st.columns(3)
    lm1.markdown('<div class="flow"><strong>COMMUNITY NEED</strong><br>Existing Activity–Mobility mismatch</div>', unsafe_allow_html=True)
    lm2.markdown('<div class="flow"><strong>EVENT OPPORTUNITY</strong><br>FIFA relevance</div>', unsafe_allow_html=True)
    lm3.markdown('<div class="flow"><strong>LEGACY OPPORTUNITY</strong><br>Where both conditions overlap</div>', unsafe_allow_html=True)

# GUIDED DEMO MODE
if "guided_demo" not in st.session_state:
    st.session_state.guided_demo = False
guide_label = "Close guided demo" if st.session_state.guided_demo else "▶ Start 60-second guided demo"
if st.button(guide_label, type="primary", key="guide_toggle"):
    st.session_state.guided_demo = not st.session_state.guided_demo
    st.rerun()
if st.session_state.guided_demo:
    with st.container(border=True):
        st.markdown('<div class="eyebrow">60-second guided demo</div>', unsafe_allow_html=True)
        if legacy_mode:
            st.write("**Decision:** Where can event-driven mobility investment support FIFA access while also addressing an existing community mismatch?")
        guide_step = st.radio("Demo stage", ["1 · The mismatch is the signal", "2 · Add the FIFA lens",
            "3 · Test an intervention", "4 · Check robustness"], horizontal=True, label_visibility="collapsed")
        if guide_step.startswith("1"):
            g1, g2, g3 = st.columns(3)
            g1.metric("Activity", f"{leader['activity_score']:.1f}")
            g2.metric("Mobility", f"{leader['mobility_score']:.1f}")
            g3.metric("Mismatch", f"{leader['mismatch_score']:.1f}")
            st.write(f"{leader['tract_name']} sits far above the balance line: urban activity intensity substantially exceeds its mobility score. See the Urban Opportunity Matrix below.")
        elif guide_step.startswith("2"):
            g1, op_a, g2, op_b, g3 = st.columns([1, .25, 1, .25, 1])
            g1.metric("Mismatch", f"{leader['mismatch_score']:.1f}")
            op_a.markdown('<div class="operator">×</div>', unsafe_allow_html=True)
            g2.metric("FIFA Relevance", f"{leader['fifa_relevance']:.1f}")
            op_b.markdown('<div class="operator">=</div>', unsafe_allow_html=True)
            g3.metric("Legacy Priority", f"{leader['legacy_priority']:.1f}")
            st.caption(f"Distance to NRG: {leader['distance_to_nrg_miles']:.2f} miles")
            st.write("A mismatch alone does not determine priority. FIFA relevance identifies which mismatches may be especially timely during World Cup planning; it is not measured visitor demand.")
        elif guide_step.startswith("3"):
            gm, gmis, gp, gr = scenario_values(leader, 15, df)
            baseline_rank = int(leader["baseline_rank"])
            guide_scenario = pd.DataFrame({"Measure": ["Mobility", "Mismatch", "Legacy Priority", "Rank"],
                "Baseline": [f"{leader['mobility_score']:.1f}", f"{leader['mismatch_score']:.1f}",
                             f"{leader['legacy_priority']:.1f}", f"#{baseline_rank}"],
                "Scenario (+15)": [f"{gm:.1f}", f"{gmis:.1f}", f"{gp:.1f}", f"#{gr}"]})
            st.dataframe(guide_scenario, hide_index=True, width="stretch")
            st.warning("Illustrative planning scenario — not a forecast.")
            if legacy_mode:
                st.caption(f"Potential intervention category: {leader['suggested_intervention_category']} — a screening suggestion, not an engineering recommendation.")
            if gmis == leader["mismatch_score"]:
                st.write("Mobility improves, but this tract's normalized mismatch remains at the model ceiling, so its Legacy Priority and rank do not change. This is an honest consequence of applying the existing normalization consistently.")
            else:
                st.write("As the mobility indicator improves, the diagnostic mismatch changes. The scenario demonstrates how CorridorIQ can be used to explore planning tradeoffs.")
        else:
            guide_sensitivity = sensitivity_results(df)
            rank_cols = st.columns(3)
            for column, miles in zip(rank_cols, (10, 15, 20)):
                rank = guide_sensitivity[miles]["rank"].loc[leader.name]
                column.metric(f"{miles}-mile assumption", f"Rank #{int(rank)}")
            guide_sets = [set(df.loc[guide_sensitivity[m]["priority"].nlargest(10).index, "GEOID"]) for m in (10, 15, 20)]
            overlap = len(set.intersection(*guide_sets))
            st.metric("Top-10 overlap", f"{overlap} of 10 tracts")
            st.write("CorridorIQ tests multiple proximity assumptions so planners can see whether the priority signal depends heavily on a single modeling choice. This is prototype sensitivity analysis, not statistical validation.")
            st.info("Explore the map yourself → Scroll to the Houston decision surface below.")

# MODEL FLOW
st.markdown('<div class="stage-label">Overview</div>', unsafe_allow_html=True)
st.markdown("### The mismatch is the signal")
st.markdown(
    '''<div class="model-strip">
    <span class="model-step activity">Activity</span><span class="model-op">−</span>
    <span class="model-step mobility">Mobility</span><span class="model-op">→</span>
    <span class="model-step mismatch">Mismatch</span><span class="model-op">×</span>
    <span class="model-step fifa">FIFA Relevance</span><span class="model-op">→</span>
    <span class="model-step legacy">Legacy Opportunity</span>
    </div>''',
    unsafe_allow_html=True,
)

# HERO INSIGHT
st.markdown("## Where should planners look first?")
left, right = st.columns([1.7, 1])
left.markdown(
    f'''<div class="card hero-card"><div class="card-label">Highest Legacy Priority</div>
    <div class="big-number">{leader["tract_name"]}</div><div>GEOID {leader["GEOID"]}</div><br>
    <b>{leader["tract_name"].replace("; Harris County; Texas", "")} rises to the top because it combines a severe
    activity–mobility mismatch ({leader["mismatch_score"]:.1f}) with high FIFA relevance ({leader["fifa_relevance"]:.1f})
    just {leader["distance_to_nrg_miles"]:.2f} miles from NRG.</b></div>''', unsafe_allow_html=True,
)
r1, r2 = right.columns(2)
r1.metric("Legacy Priority", f"{leader['legacy_priority']:.1f}")
r2.metric("Mismatch", f"{leader['mismatch_score']:.1f}")
r1.metric("FIFA Relevance", f"{leader['fifa_relevance']:.1f}")
r2.metric("Distance to NRG", f"{leader['distance_to_nrg_miles']:.2f} mi")
if st.button("Explore this tract →", type="primary"):
    st.session_state.selected_tract = leader["selector"]

# KPIS
valid_priorities = df["legacy_priority"].dropna()
high_priority_count = (len(valid_priorities) + 3) // 4
st.markdown("## County snapshot")
k1, k2, k3, k4 = st.columns(4)
k1.metric("Tracts Analyzed", f"{len(df):,}")
k2.metric("High-Priority Tracts", f"{high_priority_count:,}", help="Top quartile by Legacy Priority rank")
k3.metric("Highest Legacy Priority", f"{valid_priorities.max():.1f}")
k4.metric("Median Mismatch Score", f"{df['mismatch_score'].median():.1f}")

# MAP
st.markdown("## Houston decision surface")
st.markdown('<div class="section-note">Switch the planning lens or focus on the top quartile. Scores remain continuous and unchanged.</div>', unsafe_allow_html=True)
mc1, mc2 = st.columns([2, 1])
map_choices = {"Legacy Priority": "legacy_priority", "Mismatch Score": "mismatch_score",
               "FIFA Relevance": "fifa_relevance", "Activity Score": "activity_score", "Mobility Score": "mobility_score"}
map_label = mc1.radio("Map metric", list(map_choices), horizontal=True)
priority_only = mc2.toggle("Show only highest-priority tracts", value=False)
map_field = map_choices[map_label]
plot_df = df.dropna(subset=[map_field]).copy()
if priority_only:
    top_ids = set(df.nlargest(high_priority_count, "legacy_priority")["GEOID"])
    plot_df = plot_df[plot_df["GEOID"].isin(top_ids)]
plot_df["distance_display"] = plot_df["distance_to_nrg_miles"].map(lambda x: f"{x:.2f} mi")
fig = px.choropleth_map(
    plot_df, geojson=geojson, locations="GEOID", featureidkey="properties.GEOID", color=map_field,
    color_continuous_scale=[[0, "#F4F0E6"], [.38, "#D6AE52"], [.68, "#A4674D"], [1, "#7A263A"]],
    range_color=(0, 100), map_style="carto-positron", center={"lat": 29.72, "lon": -95.38}, zoom=9.25, opacity=.80,
    hover_name="tract_name", hover_data={"GEOID": False, "corridor_type": True, "legacy_priority": ":.1f",
        "mismatch_score": ":.1f", "fifa_relevance": ":.1f", "activity_score": ":.1f",
        "mobility_score": ":.1f", "distance_display": True},
    labels={map_field: map_label, "corridor_type": "Corridor Type", "legacy_priority": "Legacy Priority",
        "mismatch_score": "Mismatch", "fifa_relevance": "FIFA Relevance", "activity_score": "Activity",
        "mobility_score": "Mobility", "distance_display": "Distance to NRG"},
)
fig.add_trace(go.Scattermap(lat=[NRG_LAT], lon=[NRG_LON], mode="markers+text", text=["NRG Stadium"],
    textposition="top center", marker={"size": 15, "color": "#D6AE52"}, hovertemplate="<b>NRG Stadium</b><extra></extra>", name="NRG Stadium"))
if legacy_mode:
    event_anchors = [
        ("Houston Stadium / NRG", 29.6847, -95.4107), ("Stadium Park / Astrodome", 29.6858, -95.4074),
        ("Texas Medical Center", 29.7108, -95.3975), ("Museum District", 29.7257, -95.3905),
        ("Midtown", 29.7410, -95.3760), ("Downtown", 29.7604, -95.3698),
        ("EaDo / Fan Festival area", 29.7520, -95.3550),
    ]
    fig.add_trace(go.Scattermap(lat=[item[1] for item in event_anchors], lon=[item[2] for item in event_anchors],
        mode="lines+markers", text=[item[0] for item in event_anchors],
        marker={"size": 9, "color": "#D6AE52"}, line={"width": 4, "color": "#D6AE52"},
        hovertemplate="<b>%{text}</b><br>Event-network reference point<extra>FIFA Event Mobility Spine</extra>",
        name="FIFA Event Mobility Spine"))
fig.update_layout(height=650, margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=False,
                  coloraxis_colorbar={"title": map_label, "thickness": 14})
st.plotly_chart(fig, width="stretch")
if legacy_mode:
    st.caption("FIFA Event Mobility Spine: manually defined event-network reference points using well-known local anchors. This is a planning reference—not measured visitor movement.")

    # FIFA LEGACY DECISION WORKFLOW
    st.markdown("## Legacy Opportunity Matrix")
    st.markdown('<div class="section-note">The strongest legacy candidates combine an existing mobility mismatch with high event relevance.</div>', unsafe_allow_html=True)
    legacy_points = df.dropna(subset=["fifa_relevance", "mismatch_score", "activity_score"]).copy()
    legacy_matrix = px.scatter(legacy_points, x="fifa_relevance", y="mismatch_score", size="activity_score",
        color="legacy_priority", size_max=24, opacity=.70,
        color_continuous_scale=[[0, "#F4F0E6"], [.45, "#747A3D"], [.72, "#D6AE52"], [1, "#7A263A"]],
        hover_name="tract_name", hover_data={"fifa_relevance": ":.1f", "mismatch_score": ":.1f",
            "activity_score": ":.1f", "legacy_priority": ":.1f", "distance_to_nrg_miles": ":.2f",
            "suggested_intervention_category": True},
        labels={"fifa_relevance": "FIFA Relevance", "mismatch_score": "Mismatch Score",
            "activity_score": "Activity", "legacy_priority": "Legacy Priority",
            "distance_to_nrg_miles": "Distance to NRG", "suggested_intervention_category": "Potential Intervention"})
    legacy_matrix.add_vline(x=legacy_fifa_threshold, line_dash="dash", line_color="#A9A59C")
    legacy_matrix.add_hline(y=legacy_mismatch_threshold, line_dash="dash", line_color="#A9A59C")
    quadrant_style = {"showarrow": False, "bgcolor": "#F4F0E6", "bordercolor": "#A9A59C",
                      "font": {"size": 11, "color": "#262521"}}
    legacy_matrix.add_annotation(x=18, y=88, text="LONG-TERM<br>COMMUNITY NEED", **quadrant_style)
    legacy_matrix.add_annotation(x=82, y=88, text="LEGACY<br>OPPORTUNITY", **quadrant_style)
    legacy_matrix.add_annotation(x=82, y=8, text="EVENT-RELEVANT /<br>LOWER EXISTING MISMATCH", **quadrant_style)
    legacy_matrix.add_annotation(x=18, y=8, text="LOWER IMMEDIATE<br>PRIORITY", **quadrant_style)
    legacy_matrix.add_trace(go.Scatter(x=[leader["fifa_relevance"]], y=[leader["mismatch_score"]], mode="markers",
        marker={"size": 23, "color": "rgba(0,0,0,0)", "line": {"color": "#7A263A", "width": 3}},
        name="Highest Legacy Priority", hovertemplate=f"<b>{leader['tract_name']}</b><extra>Highest Legacy Priority</extra>"))
    legacy_matrix.update_xaxes(range=[0, 100]); legacy_matrix.update_yaxes(range=[0, 100])
    legacy_matrix.update_layout(height=610, margin={"r": 20, "t": 20, "l": 20, "b": 20},
                                coloraxis_colorbar={"title": "Legacy Priority"})
    style_dark_chart(legacy_matrix)
    st.plotly_chart(legacy_matrix, width="stretch")

    bs1, bs2, bs3 = st.columns(3)
    bs1.markdown('<div class="card"><div class="card-label">FIFA RELEVANCE ANSWERS</div><b>Is this location connected to the event opportunity?</b></div>', unsafe_allow_html=True)
    bs2.markdown('<div class="card"><div class="card-label">MISMATCH SCORE ANSWERS</div><b>Does this location show an underlying urban mobility imbalance?</b></div>', unsafe_allow_html=True)
    bs3.markdown('<div class="card"><div class="card-label">LEGACY PRIORITY ANSWERS</div><b>Where do those two conditions overlap?</b></div>', unsafe_allow_html=True)

    st.markdown("### Decision funnel")
    fu1, ar1, fu2, ar2, fu3, ar3, fu4 = st.columns([1, .25, 1, .25, 1, .25, 1])
    fu1.metric("All Tracts", f"{len(df):,}")
    ar1.markdown('<div class="operator">→</div>', unsafe_allow_html=True)
    fu2.metric("High Mismatch", f"{int(high_mismatch.sum()):,}")
    ar2.markdown('<div class="operator">+</div>', unsafe_allow_html=True)
    fu3.metric("Strong FIFA Relevance", f"{int(strong_fifa.sum()):,}")
    ar3.markdown('<div class="operator">→</div>', unsafe_allow_html=True)
    fu4.metric("Legacy Opportunity Areas", f"{int(legacy_opportunity.sum()):,}")
    with st.expander("How the Legacy Opportunity threshold works"):
        st.write(f"High Mismatch means a score at or above {legacy_mismatch_threshold:.1f}, the median among tracts with a positive mismatch. The countywide 75th percentile is zero, so using it would incorrectly label zero-mismatch tracts as high need.")
        st.write(f"Strong FIFA Relevance means a score at or above {legacy_fifa_threshold:.1f}, the countywide 75th percentile. Legacy Opportunity Areas meet both conditions. Scores themselves are unchanged.")

    flagship = df.loc[df["GEOID"] == "48201314301"].iloc[0]
    st.markdown("### Why this matters: Tract 3143.01")
    fc1, fc2 = st.columns([1.5, 1])
    fc1.markdown(f'''<div class="card hero-card"><div class="card-label">Flagship case study</div>
        <div class="big-number">{flagship["tract_name"]}</div>
        Proximity alone tells planners this tract is close to event activity. CorridorIQ adds community context:
        its activity–mobility mismatch is also among the strongest in the dataset.<br><br>
        <b>This makes it a candidate for closer evaluation where an event-related mobility investment could potentially serve both visitors and residents.</b>
        </div>''', unsafe_allow_html=True)
    fm1, fm2 = fc2.columns(2)
    fm1.metric("Distance to NRG", f"{flagship['distance_to_nrg_miles']:.2f} mi")
    fm2.metric("Activity", f"{flagship['activity_score']:.1f}")
    fm1.metric("Mobility", f"{flagship['mobility_score']:.1f}")
    fm2.metric("Mismatch", f"{flagship['mismatch_score']:.1f}")
    fm1.metric("FIFA Relevance", f"{flagship['fifa_relevance']:.1f}")
    fm2.metric("Legacy Priority", f"{flagship['legacy_priority']:.1f}")
    st.caption(f"Potential intervention category: {flagship['suggested_intervention_category']}. These categories are screening suggestions, not engineering recommendations.")
    if st.button("Test this opportunity in Scenario Lab →", key="legacy_scenario"):
        st.session_state.scenario_tract = flagship["selector"]
        st.session_state.scenario_preset = "Moderate Mobility Improvement (+15)"
        st.session_state.selected_tract = flagship["selector"]
        st.success("Loaded Tract 3143.01 and the +15 example into Scenario Lab below.")

# OPPORTUNITY MATRIX
st.markdown('<div class="stage-label">Diagnose</div>', unsafe_allow_html=True)
st.markdown("## Urban Opportunity Matrix")
st.markdown('<div class="section-note">Why is it a mismatch? The diagonal marks equal Activity and Mobility scores.</div>', unsafe_allow_html=True)
st.write("CorridorIQ focuses on the distance between urban intensity and mobility conditions. Tracts farther above the balance line exhibit larger diagnostic mismatch signals.")
matrix_df = df.dropna(subset=["mobility_score", "activity_score", "fifa_relevance", "legacy_priority"]).copy()
matrix = px.scatter(
    matrix_df, x="mobility_score", y="activity_score", size="fifa_relevance", color="legacy_priority",
    size_max=18, opacity=.46,
    color_continuous_scale=[[0, "#A9A59C"], [.42, "#747A3D"], [.72, "#D6AE52"], [1, "#7A263A"]],
    hover_name="tract_name", hover_data={"activity_score": ":.1f", "mobility_score": ":.1f",
        "mismatch_score": ":.1f", "fifa_relevance": ":.1f", "legacy_priority": ":.1f",
        "distance_to_nrg_miles": ":.2f", "corridor_type": True},
    labels={"mobility_score": "Mobility Score", "activity_score": "Activity Score",
        "legacy_priority": "Legacy Priority", "fifa_relevance": "FIFA Relevance",
        "mismatch_score": "Mismatch", "distance_to_nrg_miles": "Distance to NRG",
        "corridor_type": "Corridor Type"},
)
matrix.add_trace(go.Scatter(x=[0, 100], y=[0, 100], mode="lines", line={"color": "#A9A59C", "dash": "dash", "width": 2},
                            name="Balance line", hovertemplate="Activity = Mobility<extra>Balance line</extra>"))
matrix.add_trace(go.Scatter(x=[leader["mobility_score"]], y=[leader["activity_score"]], mode="markers",
    marker={"size": 22, "color": "rgba(0,0,0,0)", "line": {"color": "#7A263A", "width": 3}},
    name="Highest Legacy Priority", hovertemplate=f"<b>{leader['tract_name']}</b><extra>Highest Legacy Priority</extra>"))
matrix.add_annotation(x=leader["mobility_score"], y=leader["activity_score"], text=leader["tract_name"].split(";")[0],
                      showarrow=True, arrowhead=2, ax=55, ay=-35, bgcolor="#F4F0E6", bordercolor="#A9A59C",
                      font={"color": "#262521"})
matrix.add_annotation(x=72, y=68, text="Balance line", showarrow=False, font={"color": "#A9A59C"}, textangle=-38)
matrix.update_xaxes(range=[0, 100], constrain="domain")
matrix.update_yaxes(range=[0, 100], scaleanchor="x", scaleratio=1)
matrix.update_layout(height=650, margin={"r": 20, "t": 25, "l": 20, "b": 20},
                     legend={"orientation": "h", "y": 1.04, "x": 0}, coloraxis_colorbar={"title": "Legacy Priority"})
style_dark_chart(matrix)
st.plotly_chart(matrix, width="stretch")
st.caption("Bubble size represents FIFA Relevance. Points near the diagonal are relatively balanced under the prototype indicators; this is not a measure of congestion.")

positive_gap = df["activity_score"] > df["mobility_score"]
valid_gap_count = int(df[["activity_score", "mobility_score"]].dropna().shape[0])
positive_gap_count = int(positive_gap.sum())
quartile_size = (int(df["mismatch_score"].notna().sum()) + 3) // 4
top_mismatch_ids = set(df.nlargest(quartile_size, "mismatch_score")["GEOID"])
top_fifa_ids = set(df.nlargest(quartile_size, "fifa_relevance")["GEOID"])
joint_top_count = len(top_mismatch_ids & top_fifa_ids)
near_high_count = int(((df["GEOID"].isin(top_mismatch_ids)) & (df["distance_to_nrg_miles"] <= 5)).sum())
o1, o2, o3 = st.columns(3)
o1.metric("Activity exceeds Mobility", f"{positive_gap_count} tracts", f"{positive_gap_count / valid_gap_count * 100:.1f}% of complete tracts", delta_color="off")
o2.metric("Top-quartile overlap", f"{joint_top_count} tracts", "Mismatch + FIFA relevance", delta_color="off")
o3.metric("High mismatch near NRG", f"{near_high_count} tracts", "Top-quartile mismatch within 5 mi", delta_color="off")

# URBAN DNA HEATMAP
st.markdown("## Urban DNA Fingerprints")
st.write("Each row represents a tract's Urban DNA — the combination of economic, activity, mobility, mismatch, and FIFA relevance signals that produces its priority profile.")
st.write("Two tracts can achieve similar Legacy Priority values for very different reasons.")
heat_fields = ["economic_score", "activity_score", "mobility_score", "mismatch_score", "fifa_relevance", "legacy_priority"]
heat_labels = ["Economic", "Activity", "Mobility", "Mismatch", "FIFA Relevance", "Legacy Priority"]
heat_df = df.nlargest(15, "legacy_priority").set_index("tract_name")[heat_fields]
heatmap = go.Figure(go.Heatmap(z=heat_df.values, x=heat_labels, y=[name.split("; Harris")[0] for name in heat_df.index],
    zmin=0, zmax=100, colorscale=[[0, "#F4F0E6"], [.38, "#D6AE52"], [.68, "#747A3D"], [1, "#5C1D2C"]],
    text=heat_df.values, texttemplate="%{text:.1f}", hovertemplate="<b>%{y}</b><br>%{x}: %{z:.1f}<extra></extra>",
    colorbar={"title": "Score"}))
heatmap.update_layout(height=590, margin={"r": 25, "t": 15, "l": 20, "b": 20},
                      xaxis={"side": "top"}, yaxis={"autorange": "reversed"})
heatmap.update_traces(textfont={"shadow": "auto"})
style_dark_chart(heatmap)
st.plotly_chart(heatmap, width="stretch")

# FINDINGS
st.markdown("## What CorridorIQ surfaced")
finding_specs = [
    ("48201314301", "Closest high-severity mismatch", lambda r: f"{r['distance_to_nrg_miles']:.2f} mi from NRG",
     lambda r: f"Activity {r['activity_score']:.1f} vs. Mobility {r['mobility_score']:.1f}",
     "A severe activity–mobility mismatch sits immediately beside the FIFA venue."),
    ("48201421402", "Exceptional density, limited stop count", lambda r: f"{r['population_density']:,.0f} people / sq. mi.",
     lambda r: f"{int(r['transit_stops'])} mapped stops · Mismatch {r['mismatch_score']:.1f}",
     "Extreme density can outpace the mobility-capacity signal even where some transit is present."),
    ("48201314004", "Timeliness changes the ranking", lambda r: f"FIFA relevance {r['fifa_relevance']:.1f}",
     lambda r: f"{r['no_vehicle_pct']:.1f}% no-vehicle · {r['distance_to_nrg_miles']:.2f} mi",
     "A moderate mismatch becomes more timely because this tract is exceptionally close to NRG."),
]
finding_cols = st.columns(3)
for column, (geoid, headline, metric1, metric2, interpretation) in zip(finding_cols, finding_specs):
    row = df.loc[df["GEOID"] == geoid].iloc[0]
    column.markdown(
        f'''<div class="card finding"><div class="card-label">{row["tract_name"].replace("; Harris County; Texas", "")}</div>
        <h4>{headline}</h4><b>{metric1(row)}</b><br><span>{metric2(row)}</span><hr>
        <span>{interpretation}</span></div>''', unsafe_allow_html=True,
    )

# WATCHLIST
st.markdown("## FIFA Legacy Watchlist" if legacy_mode else "## Priority Watchlist")
if legacy_mode:
    st.caption("Leading screening candidates that meet both the High Mismatch and Strong FIFA Relevance criteria.")
    watch_source = df.loc[legacy_opportunity].sort_values("legacy_priority", ascending=False).copy()
    watch = watch_source.head(10).copy()
    watch.insert(0, "Rank", range(1, len(watch) + 1))
    watch = watch[["Rank", "tract_name", "corridor_type", "mismatch_score", "fifa_relevance", "legacy_priority",
                   "no_vehicle_pct", "data_completeness_pct", "suggested_intervention_category"]]
    watch.columns = ["Rank", "Tract", "Corridor Type", "Mismatch", "FIFA Relevance", "Legacy Opportunity / Priority",
                     "No-Vehicle %", "Data Completeness", "Potential Intervention Category"]
else:
    st.caption("The ten highest-priority areas under the prototype scoring framework—not claims about the ‘best investments.’")
    watch_source = df.sort_values("legacy_priority", ascending=False).copy()
    watch = watch_source.head(10).copy()
    watch.insert(0, "Rank", range(1, len(watch) + 1))
    watch = watch[["Rank", "tract_name", "corridor_type", "mismatch_score", "fifa_relevance", "legacy_priority", "distance_to_nrg_miles"]]
    watch.columns = ["Rank", "Tract", "Corridor Type", "Mismatch", "FIFA Relevance", "Legacy Priority", "Distance to NRG"]
for col in ["Mismatch", "FIFA Relevance", "Legacy Priority", "Distance to NRG"]:
    if col in watch:
        watch[col] = watch[col].round(1)
st.dataframe(watch, hide_index=True, width="stretch", column_config={
    "Legacy Priority": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.1f"),
    "Legacy Opportunity / Priority": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.1f"),
    "Mismatch": st.column_config.NumberColumn(format="%.1f"), "FIFA Relevance": st.column_config.NumberColumn(format="%.1f"),
    "Distance to NRG": st.column_config.NumberColumn(format="%.1f mi"),
    "No-Vehicle %": st.column_config.NumberColumn(format="%.1f%%"),
    "Data Completeness": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%.0f%%")})
if legacy_mode:
    st.caption("Potential intervention categories are planning-screening suggestions, not engineering recommendations.")
download_columns = ["GEOID", "tract_name", "economic_score", "activity_score", "mobility_score",
                    "mismatch_score", "fifa_relevance", "legacy_priority", "corridor_type",
                    "data_completeness_pct"]
ranked_download = watch_source[[*download_columns, "distance_to_nrg_miles", "suggested_intervention_category"]]
download_label = "Download FIFA Legacy Watchlist" if legacy_mode else "Download Priority Watchlist"
download_name = "corridoriq_fifa_legacy_watchlist.csv" if legacy_mode else "corridoriq_ranked_results.csv"
st.download_button(download_label, ranked_download.to_csv(index=False).encode("utf-8"), download_name, "text/csv")

# PRODUCT TABS
st.markdown('<div class="stage-label">Decide</div>', unsafe_allow_html=True)
st.markdown("## Explore decisions")
explore_tab, scenario_tab, strategy_tab, compare_tab, robustness_tab = st.tabs(
    ["Explore", "Scenario Lab", "Strategy Simulator", "Compare Corridors", "Robustness"])

with explore_tab:
    choice = st.selectbox("Select a tract", selector_options, key="selected_tract")
    tract = df.loc[df["selector"] == choice].iloc[0]
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("Corridor Type", tract["corridor_type"])
    e2.metric("Legacy Priority", fmt(tract["legacy_priority"]))
    e3.metric("Mismatch", fmt(tract["mismatch_score"]))
    e4.metric("FIFA Relevance", fmt(tract["fifa_relevance"]))
    st.markdown("#### Urban DNA Profile")
    chart_data = pd.DataFrame({"Dimension": ["Economic", "Activity", "Mobility", "Mismatch", "FIFA Relevance"],
        "Score": [tract["economic_score"], tract["activity_score"], tract["mobility_score"],
                  tract["mismatch_score"], tract["fifa_relevance"]]})
    bar = px.bar(chart_data, x="Score", y="Dimension", orientation="h", range_x=[0, 100], text_auto=".1f",
                 color="Dimension", color_discrete_map={"Economic": "#A9A59C", "Activity": "#747A3D",
                     "Mobility": "#747A3D", "Mismatch": "#7A263A", "FIFA Relevance": "#D6AE52"})
    bar.update_layout(height=330, showlegend=False, margin={"r": 15, "t": 10, "l": 10, "b": 10})
    style_dark_chart(bar)
    st.plotly_chart(bar, width="stretch")
    st.markdown(f'<div class="why"><div class="card-label">Why this tract is flagged</div><b>{tract_explanation(tract)}</b><br><br>{tract["priority_reason"]}</div>', unsafe_allow_html=True)

with scenario_tab:
    st.subheader("Scenario Lab")
    st.write("What happens to the diagnostic priority signal if mobility conditions improve?")
    st.warning("Illustrative planning scenario — not a forecast of real-world outcomes.")
    scenario_select_args = {"key": "scenario_tract"}
    if "scenario_tract" not in st.session_state:
        scenario_select_args["index"] = selector_options.index(st.session_state.selected_tract)
    scenario_selector = st.selectbox("Census tract", selector_options, **scenario_select_args)
    scenario_tract = df.loc[df["selector"] == scenario_selector].iloc[0]
    b1, b2, b3, b4, b5, b6 = st.columns(6)
    b1.metric("Activity", fmt(scenario_tract["activity_score"]))
    b2.metric("Mobility", fmt(scenario_tract["mobility_score"]))
    b3.metric("Mismatch", fmt(scenario_tract["mismatch_score"]))
    b4.metric("FIFA Relevance", fmt(scenario_tract["fifa_relevance"]))
    b5.metric("Legacy Priority", fmt(scenario_tract["legacy_priority"]))
    b6.metric("Current Rank", f"#{int(scenario_tract['baseline_rank'])}" if pd.notna(scenario_tract["baseline_rank"]) else "N/A")
    scenario_choice = st.selectbox("Scenario", ["Baseline", "Moderate Mobility Improvement (+15)",
        "Strong Mobility Improvement (+30)", "Custom"], key="scenario_preset")
    if scenario_choice == "Custom":
        improvement = st.slider("Custom mobility improvement", 0, 30, 10)
    else:
        improvement = {"Baseline": 0, "Moderate Mobility Improvement (+15)": 15,
                       "Strong Mobility Improvement (+30)": 30}[scenario_choice]
    current_mobility = scenario_tract["mobility_score"]
    scenario_mobility = min(100, current_mobility + improvement) if pd.notna(current_mobility) else float("nan")
    scenario_gap = max(scenario_tract["activity_score"] - scenario_mobility, 0) if pd.notna(scenario_mobility) else float("nan")
    scenario_mismatch = normalize_scenario(scenario_gap, df)
    scenario_priority = scenario_mismatch * scenario_tract["fifa_relevance"] / 100
    baseline_rank = int(scenario_tract["baseline_rank"]) if pd.notna(scenario_tract["baseline_rank"]) else None
    scenario_rank = 1 + int((df.drop(index=scenario_tract.name)["legacy_priority"] > scenario_priority).sum()) if pd.notna(scenario_priority) else None
    current_col, scenario_col = st.columns(2)
    with current_col:
        st.markdown("#### CURRENT")
        a, b, c, d = st.columns(4)
        a.metric("Mobility", fmt(current_mobility)); b.metric("Mismatch", fmt(scenario_tract["mismatch_score"]))
        c.metric("Legacy Priority", fmt(scenario_tract["legacy_priority"])); d.metric("Rank", f"#{baseline_rank}" if baseline_rank else "N/A")
    with scenario_col:
        st.markdown("#### SCENARIO")
        a, b, c, d = st.columns(4)
        a.metric("Mobility", fmt(scenario_mobility)); b.metric("Mismatch", fmt(scenario_mismatch))
        c.metric("Legacy Priority", fmt(scenario_priority)); d.metric("Rank", f"#{scenario_rank}" if scenario_rank else "N/A")
    scenario_chart = pd.DataFrame({"Metric": ["Mobility", "Mismatch", "Legacy Priority"] * 2,
        "Score": [current_mobility, scenario_tract["mismatch_score"], scenario_tract["legacy_priority"], scenario_mobility, scenario_mismatch, scenario_priority],
        "State": ["Baseline"] * 3 + ["Scenario"] * 3})
    scenario_fig = px.bar(scenario_chart, x="Metric", y="Score", color="State", barmode="group", range_y=[0, 100],
                          color_discrete_map={"Baseline": "#A9A59C", "Scenario": "#747A3D"}, text_auto=".1f")
    scenario_fig.update_layout(height=380, margin={"r": 10, "t": 15, "l": 10, "b": 10})
    style_dark_chart(scenario_fig)
    st.plotly_chart(scenario_fig, width="stretch")
    if improvement == 0:
        scenario_sentence = "The baseline preset leaves mobility, mismatch, FIFA relevance, and diagnostic priority unchanged."
    else:
        scenario_sentence = ("Under this illustrative scenario, mobility improves while the diagnostic mismatch falls. "
                             "FIFA relevance remains unchanged, so Legacy Priority also changes.")
    st.success(f"Priority rank changes from #{baseline_rank} to #{scenario_rank}. {scenario_sentence}")
    st.caption("This control demonstrates how the prioritization framework responds when one underlying condition changes.")

with strategy_tab:
    st.subheader("Strategy Simulator")
    st.write("Test how a consistent mobility-score intervention changes the diagnostic picture across a portfolio of tracts.")
    st.warning("Illustrative planning scenario — not a forecast.")
    sc1, sc2 = st.columns(2)
    strategy = sc1.selectbox("Targeting strategy", ["FIFA Corridor Focus", "Equity First", "Highest Mismatch", "Custom / selected tracts"])
    intensity = sc2.radio("Intervention intensity", ["Low (+10)", "Medium (+20)", "High (+30)"], horizontal=True)
    improvement_points = {"Low (+10)": 10, "Medium (+20)": 20, "High (+30)": 30}[intensity]
    strategy_target_count = int(legacy_opportunity.sum())
    if strategy == "FIFA Corridor Focus":
        targeted_ids = set(df.loc[legacy_opportunity, "GEOID"])
        strategy_note = "Targets tracts where High Mismatch overlaps Strong FIFA Relevance."
    elif strategy == "Equity First":
        targeted_ids = set(df.loc[high_mismatch].nlargest(strategy_target_count, "no_vehicle_pct")["GEOID"])
        strategy_note = "Targets high-mismatch tracts with the largest no-vehicle household shares."
    elif strategy == "Highest Mismatch":
        targeted_ids = set(df.nlargest(strategy_target_count, "mismatch_score")["GEOID"])
        strategy_note = "Targets the highest Mismatch Scores, independent of event relevance."
    else:
        default_custom = df.loc[legacy_opportunity].nlargest(5, "legacy_priority")["selector"].tolist()
        custom_choices = st.multiselect("Selected tracts", selector_options, default=default_custom)
        targeted_ids = set(df.loc[df["selector"].isin(custom_choices), "GEOID"])
        strategy_note = "Targets only the tracts selected above."
    st.caption(strategy_note)

    target_mask = df["GEOID"].isin(targeted_ids)
    if not target_mask.any():
        st.warning("Select at least one tract to generate a custom strategy scenario.")
    scenario_city = df.copy()
    scenario_city["scenario_mobility"] = scenario_city["mobility_score"]
    scenario_city.loc[target_mask, "scenario_mobility"] = (
        scenario_city.loc[target_mask, "mobility_score"] + improvement_points).clip(upper=100)
    scenario_city["scenario_mismatch"] = scenario_city["mismatch_score"]
    scenario_raw = (scenario_city.loc[target_mask, "activity_score"] -
                    scenario_city.loc[target_mask, "scenario_mobility"]).clip(lower=0)
    mismatch_low, mismatch_high = df["mismatch_severity_raw"].quantile([0.02, 0.98])
    scenario_city.loc[target_mask, "scenario_mismatch"] = (
        (scenario_raw - mismatch_low) / (mismatch_high - mismatch_low) * 100).clip(lower=0, upper=100)
    scenario_city["scenario_priority"] = scenario_city["scenario_mismatch"] * scenario_city["fifa_relevance"] / 100
    scenario_city["mismatch_change"] = scenario_city["mismatch_score"] - scenario_city["scenario_mismatch"]

    baseline_high = df["mismatch_score"] >= legacy_mismatch_threshold
    scenario_high = scenario_city["scenario_mismatch"] >= legacy_mismatch_threshold
    baseline_high_count, scenario_high_count = int(baseline_high.sum()), int(scenario_high.sum())
    baseline_high_pop = df.loc[baseline_high, "population"].sum()
    scenario_high_pop = scenario_city.loc[scenario_high, "population"].sum()
    target_before_avg = df.loc[target_mask, "mismatch_score"].mean()
    target_after_avg = scenario_city.loc[target_mask, "scenario_mismatch"].mean()
    target_no_vehicle = df.loc[target_mask, "no_vehicle_households"].sum()
    legacy_before = int(legacy_opportunity.sum())
    legacy_after = int(((scenario_city["scenario_mismatch"] >= legacy_mismatch_threshold) & strong_fifa).sum())

    st.markdown("#### Citywide model-derived outcomes")
    st.caption(f"{int(target_mask.sum())} targeted tracts · {improvement_points} mobility-score points")
    cm1, cm2, cm3, cm4, cm5 = st.columns(5)
    cm1.metric("High-Mismatch Tracts", f"{scenario_high_count}", f"from {baseline_high_count}", delta_color="off")
    cm2.metric("Population in High-Mismatch Tracts", f"{scenario_high_pop:,.0f}", f"from {baseline_high_pop:,.0f}", delta_color="off")
    cm3.metric("Avg. Targeted Mismatch", fmt(target_after_avg), f"from {fmt(target_before_avg)}", delta_color="off")
    cm4.metric("No-Vehicle Households Targeted", f"{target_no_vehicle:,.0f}")
    cm5.metric("Legacy Opportunity Tracts", f"{legacy_after}", f"from {legacy_before}", delta_color="off")

    st.markdown("#### Baseline / Scenario / Change map")
    strategy_map_view = st.radio("Map view", ["Baseline", "Scenario", "Change"], horizontal=True, key="strategy_map_view")
    if strategy_map_view == "Baseline":
        strategy_field, strategy_label = "mismatch_score", "Baseline Mismatch"
        strategy_scale, strategy_range = [[0, "#F4F0E6"], [.45, "#D6AE52"], [1, "#7A263A"]], (0, 100)
    elif strategy_map_view == "Scenario":
        strategy_field, strategy_label = "scenario_mismatch", "Scenario Mismatch"
        strategy_scale, strategy_range = [[0, "#F4F0E6"], [.45, "#D6AE52"], [1, "#7A263A"]], (0, 100)
    else:
        strategy_field, strategy_label = "mismatch_change", "Mismatch Reduction"
        strategy_scale = [[0, "#F4F0E6"], [1, "#747A3D"]]
        strategy_range = (0, max(1, scenario_city["mismatch_change"].max()))
    strategy_map = px.choropleth_map(scenario_city.dropna(subset=[strategy_field]), geojson=geojson,
        locations="GEOID", featureidkey="properties.GEOID", color=strategy_field,
        color_continuous_scale=strategy_scale, range_color=strategy_range, map_style="carto-positron",
        center={"lat": 29.72, "lon": -95.38}, zoom=8.8, opacity=.80, hover_name="tract_name",
        hover_data={"mismatch_score": ":.1f", "scenario_mismatch": ":.1f", "mismatch_change": ":.1f",
                    "scenario_mobility": ":.1f", "fifa_relevance": ":.1f"},
        labels={strategy_field: strategy_label, "mismatch_score": "Baseline Mismatch",
                "scenario_mismatch": "Scenario Mismatch", "mismatch_change": "Change",
                "scenario_mobility": "Scenario Mobility", "fifa_relevance": "FIFA Relevance"})
    strategy_map.add_trace(go.Scattermap(lat=[NRG_LAT], lon=[NRG_LON], mode="markers+text", text=["NRG Stadium"],
        textposition="top center", marker={"size": 13, "color": "#D6AE52"},
        hovertemplate="<b>NRG Stadium</b><extra></extra>", name="NRG Stadium"))
    strategy_map.update_layout(height=560, margin={"r": 0, "t": 0, "l": 0, "b": 0}, showlegend=False,
                               coloraxis_colorbar={"title": strategy_label})
    st.plotly_chart(strategy_map, width="stretch")
    st.caption("Change displays baseline Mismatch minus scenario Mismatch. Untargeted tracts remain unchanged.")

    st.markdown("#### Illustrative implementation pathway")
    pathway = []
    for year, phase, fraction in [(2026, "Baseline", 0), (2027, "Phase 1", .33),
                                  (2028, "Phase 2", .66), (2030, "Full modeled scenario", 1)]:
        phase_mobility = (df.loc[target_mask, "mobility_score"] + improvement_points * fraction).clip(upper=100)
        phase_raw = (df.loc[target_mask, "activity_score"] - phase_mobility).clip(lower=0)
        phase_mismatch = ((phase_raw - mismatch_low) / (mismatch_high - mismatch_low) * 100).clip(0, 100)
        pathway.append({"Year": year, "Phase": phase, "Average Targeted Mismatch": phase_mismatch.mean()})
    pathway_df = pd.DataFrame(pathway)
    timeline = px.line(pathway_df, x="Year", y="Average Targeted Mismatch", markers=True, text="Phase",
                       range_y=[0, 100], color_discrete_sequence=["#747A3D"])
    timeline.update_traces(textposition="top center", line={"width": 4}, marker={"size": 10})
    timeline.update_traces(hovertemplate="<b>%{text}</b><br>Year: %{x}<br>Average targeted mismatch: %{y:.1f}<extra></extra>")
    timeline.update_layout(height=360, margin={"r": 20, "t": 30, "l": 20, "b": 20},
                           xaxis={"tickmode": "array", "tickvals": [2026, 2027, 2028, 2030]})
    style_dark_chart(timeline)
    st.plotly_chart(timeline, width="stretch")
    st.warning("Illustrative implementation pathway — not a forecast.")

with compare_tab:
    st.subheader("Compare Corridors")
    ca, cb = st.columns(2)
    choice_a = ca.selectbox("Tract A", selector_options, index=selector_options.index(leader["selector"]))
    choice_b = cb.selectbox("Tract B", selector_options, index=min(1, len(selector_options) - 1))
    tract_a = df.loc[df["selector"] == choice_a].iloc[0]
    tract_b = df.loc[df["selector"] == choice_b].iloc[0]
    if choice_a == choice_b:
        st.warning("Choose two different tracts to make the comparison meaningful.")
    comparison_details = pd.DataFrame([
        {"Measure": "Population", "Tract A": f"{tract_a['population']:,.0f}", "Tract B": f"{tract_b['population']:,.0f}"},
        {"Measure": "Population Density", "Tract A": f"{tract_a['population_density']:,.0f} / sq. mi.", "Tract B": f"{tract_b['population_density']:,.0f} / sq. mi."},
        {"Measure": "Median Household Income", "Tract A": f"${tract_a['median_income']:,.0f}" if pd.notna(tract_a["median_income"]) else "Unavailable",
         "Tract B": f"${tract_b['median_income']:,.0f}" if pd.notna(tract_b["median_income"]) else "Unavailable"},
        {"Measure": "No-Vehicle %", "Tract A": fmt(tract_a["no_vehicle_pct"]) + "%" if pd.notna(tract_a["no_vehicle_pct"]) else "Unavailable",
         "Tract B": fmt(tract_b["no_vehicle_pct"]) + "%" if pd.notna(tract_b["no_vehicle_pct"]) else "Unavailable"},
        {"Measure": "Economic Score", "Tract A": fmt(tract_a["economic_score"]), "Tract B": fmt(tract_b["economic_score"])},
        {"Measure": "Activity Score", "Tract A": fmt(tract_a["activity_score"]), "Tract B": fmt(tract_b["activity_score"])},
        {"Measure": "Mobility Score", "Tract A": fmt(tract_a["mobility_score"]), "Tract B": fmt(tract_b["mobility_score"])},
        {"Measure": "Mismatch Score", "Tract A": fmt(tract_a["mismatch_score"]), "Tract B": fmt(tract_b["mismatch_score"])},
        {"Measure": "FIFA Relevance", "Tract A": fmt(tract_a["fifa_relevance"]), "Tract B": fmt(tract_b["fifa_relevance"])},
        {"Measure": "Legacy Priority", "Tract A": fmt(tract_a["legacy_priority"]), "Tract B": fmt(tract_b["legacy_priority"])},
        {"Measure": "Distance to NRG", "Tract A": fmt(tract_a["distance_to_nrg_miles"], ".2f") + " mi",
         "Tract B": fmt(tract_b["distance_to_nrg_miles"], ".2f") + " mi"},
        {"Measure": "Corridor Type", "Tract A": tract_a["corridor_type"], "Tract B": tract_b["corridor_type"]},
    ])
    st.dataframe(comparison_details, hide_index=True, width="stretch")
    dimensions = ["Economic", "Activity", "Mobility", "Mismatch", "FIFA Relevance", "Legacy Priority"]
    fields = ["economic_score", "activity_score", "mobility_score", "mismatch_score", "fifa_relevance", "legacy_priority"]
    comparison = pd.DataFrame({"Dimension": dimensions * 2,
        "Score": [tract_a[x] for x in fields] + [tract_b[x] for x in fields],
        "Tract": ["Tract A"] * 6 + ["Tract B"] * 6})
    comparison_fig = px.bar(comparison, x="Dimension", y="Score", color="Tract", barmode="group", range_y=[0, 100],
                            color_discrete_map={"Tract A": "#747A3D", "Tract B": "#7A263A"}, text_auto=".1f")
    comparison_fig.update_layout(height=420, margin={"r": 10, "t": 20, "l": 10, "b": 10})
    style_dark_chart(comparison_fig)
    st.plotly_chart(comparison_fig, width="stretch")
    if abs(tract_a["activity_score"] - tract_b["activity_score"]) <= 10:
        sentence = (f"These tracts have similar activity intensity, but {'Tract A' if tract_a['mismatch_score'] > tract_b['mismatch_score'] else 'Tract B'} "
                    "has the larger mobility mismatch.")
    elif tract_a["mismatch_score"] < tract_b["mismatch_score"] and tract_a["legacy_priority"] >= tract_b["legacy_priority"]:
        sentence = "Tract A has a lower mismatch but ranks similarly or higher because its FIFA relevance is stronger."
    elif tract_b["mismatch_score"] < tract_a["mismatch_score"] and tract_b["legacy_priority"] >= tract_a["legacy_priority"]:
        sentence = "Tract B has a lower mismatch but ranks similarly or higher because its FIFA relevance is stronger."
    else:
        winner = "Tract A" if tract_a["legacy_priority"] > tract_b["legacy_priority"] else "Tract B"
        sentence = f"{winner} has the higher Legacy Priority because the combined mismatch and FIFA-relevance signal is stronger."
    st.info(sentence + " Comparison mode helps planners understand why two corridors with similar urban intensity can receive different priority scores.")

with robustness_tab:
    st.subheader("How robust is this result?")
    st.write("Prototype sensitivity analysis tests whether the selected tract's priority depends strongly on the NRG distance assumption. Saved scores are not overwritten.")

    st.markdown("#### Data completeness")
    core_labels = {"population": "Population", "population_density": "Population density",
                   "median_income": "Median household income", "no_vehicle_pct": "No-vehicle percentage"}
    missing_inputs = [label for field, label in core_labels.items() if pd.isna(tract[field])]
    dc1, dc2 = st.columns([1, 2])
    dc1.metric("Data completeness", f"{tract['data_completeness_pct']:.0f}%")
    dc2.markdown("**Missing input:** " + ", ".join(missing_inputs) if missing_inputs else "**All four core inputs are available.**")
    st.caption("Completeness counts available population, population density, median income, and no-vehicle percentage. Missing values are not imputed.")

    st.markdown("#### FIFA relevance sensitivity")
    cutoff = st.radio("NRG proximity cutoff", [10, 15, 20], index=2, horizontal=True,
                      format_func=lambda value: f"{value} miles")
    sensitivity = {}
    for miles in (10, 15, 20):
        nrg_score = (100 * (1 - df["distance_to_nrg_miles"] / miles)).clip(lower=0, upper=100)
        fifa_score = 0.70 * nrg_score + 0.30 * df["transit_supply_score"]
        priority_score = df["mismatch_score"] * fifa_score / 100
        sensitivity[miles] = {"fifa": fifa_score, "priority": priority_score,
                              "rank": priority_score.rank(method="min", ascending=False)}
    selected_fifa = sensitivity[cutoff]["fifa"].loc[tract.name]
    selected_priority = sensitivity[cutoff]["priority"].loc[tract.name]
    st.info(f"Under the {cutoff}-mile assumption, this tract's FIFA Relevance is {selected_fifa:.1f} and Legacy Priority is {selected_priority:.1f}.")
    rank_values = []
    rank_cols = st.columns(3)
    for column, miles in zip(rank_cols, (10, 15, 20)):
        rank_value = sensitivity[miles]["rank"].loc[tract.name]
        rank_values.append(int(rank_value) if pd.notna(rank_value) else None)
        column.metric(f"{miles}-mile assumption", f"Rank #{int(rank_value)}" if pd.notna(rank_value) else "Unavailable")
    available_ranks = [rank for rank in rank_values if rank is not None]
    rank_range = max(available_ranks) - min(available_ranks) if available_ranks else None
    if rank_range is None:
        stability = "Unavailable"
    elif rank_range <= 5:
        stability = "Stable"
    elif rank_range <= 15:
        stability = "Moderately sensitive"
    else:
        stability = "Sensitive"
    st.metric("Rank stability", stability, f"{rank_range} rank positions" if rank_range is not None else None,
              delta_color="off")

    top_sets = [set(df.loc[sensitivity[miles]["priority"].nlargest(10).index, "GEOID"]) for miles in (10, 15, 20)]
    common_top10 = len(set.intersection(*top_sets))
    st.success(f"{common_top10} of the top 10 priority tracts remain in the top 10 across all three FIFA proximity assumptions.")
    st.caption("The sensitivity calculation preserves the MVP formula: 70% linear NRG proximity plus 30% transit supply, followed by Mismatch × FIFA Relevance / 100.")

    with st.expander("Why sensitivity testing matters"):
        st.write("The FIFA relevance score requires an assumption about how quickly event relevance declines with distance from NRG Stadium. CorridorIQ tests multiple reasonable proximity assumptions rather than relying on one setting.")
        st.write("If the same corridors remain highly ranked under several assumptions, the priority signal is less dependent on the exact distance parameter.")

    st.markdown("#### Countywide score distribution")
    hist = px.histogram(df, x="legacy_priority", nbins=25, color_discrete_sequence=["#7A263A"],
                        labels={"legacy_priority": "Legacy Priority"})
    hist.update_layout(height=340, showlegend=False, margin={"r": 10, "t": 15, "l": 10, "b": 10})
    style_dark_chart(hist)
    st.plotly_chart(hist, width="stretch")
    st.caption("The zero-heavy distribution is a real model result: most tracts do not have a positive activity–mobility gap. It is not adjusted for visual effect.")

# METHODOLOGY / SOURCES / LIMITATIONS
st.markdown("## Methodology, sources, and limitations")
with st.expander("How CorridorIQ works"):
    st.markdown("""
    1. Census tract indicators are normalized from 0–100 using robust min-max scaling.
    2. Activity is compared with mobility capacity; only positive activity-minus-mobility gaps create mismatch.
    3. FIFA relevance combines NRG proximity and locally available transit accessibility.
    4. `Legacy Priority = Mismatch Score × FIFA Relevance / 100`.

    **Legacy Priority is a prioritization index, not a prediction.** Detailed parcel-level land use, employment density,
    METRO service frequency, hotels, permits, and event-day demand are planned extensions rather than MVP dependencies.
    """)
with st.expander("Data sources"):
    st.markdown("""
    - U.S. Census Bureau 2024 ACS 5-Year Estimates: B01003 Total Population, B19013 Median Household Income, B08201 Vehicle Availability
    - U.S. Census Bureau 2024 TIGER/Line census tracts
    - Houston METRO GTFS stop locations already available locally
    - NRG Stadium approximate coordinates: 29.6847, -95.4107
    """)
with st.expander("Limitations and future work"):
    st.markdown("""
    Tract averages conceal within-tract variation. Stop density does not represent frequency, reliability, capacity, or
    travel time. FIFA relevance is an MVP planning rule, not event-demand modeling. ACS sampling uncertainty is not modeled.
    Scenarios are illustrative rather than causal forecasts. Planned extensions include validated land use, jobs, service
    frequency, hotels, permits, pedestrian access, and event-day demand.
    """)
