import streamlit as st
import pandas as pd

# ============================================================
# CITYPULSE — FINAL DASHBOARD
# ============================================================

st.set_page_config(
    page_title="CityPulse | Urban Intelligence",
    page_icon="🌆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# STYLE
# ============================================================

st.markdown("""
<style>
.stApp {
    background: #0b1220;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(135deg, #111827 0%, #172554 55%, #0f172a 100%);
    border: 1px solid #263449;
    border-radius: 22px;
    padding: 26px 30px;
    margin-bottom: 20px;
}

.hero h1 {
    color: #f8fafc;
    font-size: 42px;
    margin: 0;
    letter-spacing: -1px;
}

.hero p {
    color: #94a3b8;
    margin: 6px 0 0 0;
    font-size: 16px;
}

.hero-status {
    color: #22c55e;
    font-weight: 700;
    margin-top: 12px;
    font-size: 13px;
}

.kpi {
    background: #111827;
    border: 1px solid #263449;
    border-radius: 17px;
    padding: 18px 20px;
    min-height: 110px;
}

.kpi-label {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: .5px;
}

.kpi-value {
    color: #f8fafc;
    font-size: 30px;
    font-weight: 800;
    margin-top: 8px;
}

.kpi-note {
    color: #64748b;
    font-size: 12px;
    margin-top: 3px;
}

.panel {
    background: #111827;
    border: 1px solid #263449;
    border-radius: 18px;
    padding: 20px;
}

.panel-title {
    color: #f8fafc;
    font-size: 20px;
    font-weight: 750;
    margin-bottom: 8px;
}

.pulse-score {
    color: #60a5fa;
    font-size: 58px;
    font-weight: 900;
    line-height: 1;
    margin: 10px 0;
}

.pulse-label {
    color: #22c55e;
    font-weight: 800;
    font-size: 13px;
}

.zone {
    background: #0f172a;
    border: 1px solid #263449;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 8px;
}

.zone-name {
    color: #f8fafc;
    font-weight: 800;
    font-size: 17px;
}

.zone-meta {
    color: #94a3b8;
    font-size: 12px;
    margin-top: 3px;
}

.alert {
    background: #1b1712;
    border: 1px solid #7c4a03;
    border-radius: 14px;
    padding: 14px 16px;
    margin-bottom: 8px;
}

.alert-title {
    color: #fbbf24;
    font-weight: 800;
    font-size: 13px;
}

.alert-meta {
    color: #cbd5e1;
    font-size: 12px;
    margin-top: 4px;
}

.footer {
    text-align: center;
    color: #64748b;
    font-size: 12px;
    padding-top: 12px;
}

[data-testid="stMetric"] {
    background: transparent;
}

section[data-testid="stSidebar"] {
    background: #0f172a;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_data():
    zone_data = pd.read_csv("Data/processed/zone_summary.csv")
    anomalies = pd.read_csv("Data/processed/anomalies.csv")

    raw = pd.read_csv(
        "Data/raw/city_data.csv",
        usecols=[
            "timestamp",
            "zone",
            "traffic",
            "aqi",
            "energy",
            "activity",
        ],
    )

    raw["timestamp"] = pd.to_datetime(raw["timestamp"])

    return zone_data, anomalies, raw


zone_data, anomalies, raw = load_data()

TOTAL_RECORDS = len(raw)

anomalies["timestamp"] = pd.to_datetime(anomalies["timestamp"])
anomalies = anomalies.sort_values("timestamp", ascending=False).reset_index(drop=True)

def anomaly_reason(row):
    reasons = []
    if row["traffic"] >= 2500:
        reasons.append("🚗 Traffic Spike")
    if row["aqi"] >= 140:
        reasons.append("🌫️ AQI Spike")
    if row["activity"] >= 2000:
        reasons.append("👥 Activity Surge")
    return " • ".join(reasons) if reasons else "⚠️ Unusual Pattern"

def get_status(score):
    if score >= 70:
        return "Stable"
    elif score >= 50:
        return "Watch"
    return "Attention"

# ============================================================
# CITY PULSE SCORE
# Project-defined index based on traffic, AQI and anomaly levels
# ============================================================

zone_metrics = zone_data.copy()

alert_counts = (
    anomalies.groupby("zone")
    .size()
    .rename("alerts")
    .reset_index()
)

zone_metrics = zone_metrics.merge(
    alert_counts,
    on="zone",
    how="left",
)

zone_metrics["alerts"] = zone_metrics["alerts"].fillna(0)


def normalize(series):
    low = series.min()
    high = series.max()

    if high == low:
        return pd.Series(0.5, index=series.index)

    return (series - low) / (high - low)


traffic_norm = normalize(zone_metrics["avg_traffic"])
aqi_norm = normalize(zone_metrics["avg_aqi"])
alert_norm = normalize(zone_metrics["alerts"])

zone_metrics["pulse_score"] = (
    100
    - traffic_norm * 35
    - aqi_norm * 45
    - alert_norm * 20
).clip(0, 100).round().astype(int)

city_pulse = int(round(zone_metrics["pulse_score"].mean()))

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🌆 CityPulse")
st.sidebar.caption("Urban Intelligence & Big Data Analytics")
st.sidebar.divider()

selected_zone = st.sidebar.selectbox(
    "📍 Zone",
    ["All Zones"] + list(zone_metrics["zone"])
)

metric = st.sidebar.selectbox(
    "📈 Trend Metric",
    ["Traffic", "AQI", "Energy", "Activity"]
)

st.sidebar.divider()
st.sidebar.markdown("### Pipeline")

st.sidebar.success("Data Generation")
st.sidebar.success("PySpark Analytics")
st.sidebar.success("Anomaly Detection")
st.sidebar.success("Dashboard Ready")

st.sidebar.divider()
st.sidebar.caption("Data type: Synthetic historical dataset")
st.sidebar.caption(f"Records: {TOTAL_RECORDS:,}")

# ============================================================
# HERO
# ============================================================

st.markdown("""
<div class="hero">
    <h1>🌆 CityPulse</h1>
    <p>Urban Intelligence & Big Data Analytics</p>
    <div class="hero-status">● ANALYTICS SYSTEM ONLINE</div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FILTER
# ============================================================

if selected_zone == "All Zones":
    selected_zone_data = zone_metrics
    selected_anomalies = anomalies.sort_values("timestamp", ascending=False)
    pulse_value = city_pulse
else:
    selected_zone_data = zone_metrics[
        zone_metrics["zone"] == selected_zone
    ]
    selected_anomalies = anomalies[
        anomalies["zone"] == selected_zone
    ].sort_values("timestamp", ascending=False)
    pulse_value = int(selected_zone_data["pulse_score"].iloc[0])

avg_aqi = selected_zone_data["avg_aqi"].mean()
avg_traffic = selected_zone_data["avg_traffic"].mean()
avg_energy = selected_zone_data["avg_energy"].mean()

# ============================================================
# KPI ROW
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">TOTAL RECORDS</div>
            <div class="kpi-value">{TOTAL_RECORDS:,}</div>
            <div class="kpi-note">City observations</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">MONITORED ZONES</div>
            <div class="kpi-value">{len(selected_zone_data)}</div>
            <div class="kpi-note">Urban areas</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">DETECTED ANOMALIES</div>
            <div class="kpi-value">{len(selected_anomalies):,}</div>
            <div class="kpi-note">Unusual observations</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c4:
    st.markdown(
        f"""
        <div class="kpi">
            <div class="kpi-label">AVERAGE AQI</div>
            <div class="kpi-value">{avg_aqi:.1f}</div>
            <div class="kpi-note">Air quality indicator</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# PULSE + ZONE STATUS
# ============================================================

st.markdown('<div class="panel-title">🧭 City Overview</div>', unsafe_allow_html=True)

left, right = st.columns([1, 2])

with left:
    if pulse_value >= 70:
        pulse_status = "STABLE"
    elif pulse_value >= 50:
        pulse_status = "WATCH"
    else:
        pulse_status = "ATTENTION"

    st.markdown(
        f"""
        <div class="panel">
            <div class="panel-title">City Pulse Index</div>
            <div class="pulse-score">{pulse_value}</div>
            <div class="pulse-label">● {pulse_status}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(pulse_value / 100)

with right:
    st.markdown(
        '<div class="panel"><div class="panel-title">📍 Zone Status</div>',
        unsafe_allow_html=True,
    )

    zone_cols = st.columns(5)

    for i, (_, row) in enumerate(zone_metrics.iterrows()):
        score = int(row["pulse_score"])

        status = get_status(score)

        with zone_cols[i]:
            st.markdown(
                f"""
<div class="zone">
    <div class="zone-name">{row["zone"]}</div>
    <div class="zone-meta">● {status}</div>
    <br>
    <div class="zone-meta">🚗 {row["avg_traffic"]:.0f}</div>
    <div class="zone-meta">🌫️ {row["avg_aqi"]:.0f}</div>
    <div class="zone-meta">⚡ {row["avg_energy"]:.0f}</div>
    <div class="zone-meta">👥 {row["avg_activity"]:.0f}</div>
    <div class="zone-meta">🚨 Alerts: {int(row["alerts"])}</div>
</div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# TREND ANALYSIS
# ============================================================

st.markdown('<div class="panel-title">📈 City Trend</div>', unsafe_allow_html=True)

trend_raw = raw.copy()

if selected_zone != "All Zones":
    trend_raw = trend_raw[
        trend_raw["zone"] == selected_zone
    ]

range_choice = st.selectbox(
    "Time Range",
    ["Last 7 Days", "Last 30 Days", "Last 90 Days", "Full Year"],
    index=1,
)

end_time = trend_raw["timestamp"].max()
range_days = {
    "Last 7 Days": 7,
    "Last 30 Days": 30,
    "Last 90 Days": 90,
    "Full Year": None,
}
days = range_days[range_choice]

if days is not None:
    cutoff = end_time - pd.Timedelta(days=days)
    trend_raw = trend_raw[trend_raw["timestamp"] >= cutoff]

metric_column = {
    "Traffic": "traffic",
    "AQI": "aqi",
    "Energy": "energy",
    "Activity": "activity",
}[metric]

frequency = "6h" if days is not None else "1D"
trend = (
    trend_raw.set_index("timestamp")[metric_column]
    .resample(frequency)
    .mean()
    .dropna()
)

st.markdown(f"**{metric} over time**")
st.line_chart(trend, height=300)
st.caption(f"{range_choice} • {selected_zone}")

# ============================================================
# ALERTS + DETAIL
# ============================================================

left, right = st.columns([1, 1])

with left:
    st.markdown(
        '<div class="panel-title">🚨 Recent City Alerts</div>',
        unsafe_allow_html=True,
    )

    if selected_anomalies.empty:
        st.success("No anomalies detected.")
    else:
        for _, row in selected_anomalies.head(6).iterrows():
            reason = anomaly_reason(row)

            st.markdown(
                f"""
<div class="alert">
    <div class="alert-title">
        🚨 {reason} — {row["zone"]}
    </div>
    <div class="alert-meta">
        🕒 {row["timestamp"]}
    </div>
    <div class="alert-meta">
        🚗 Traffic {row["traffic"]}
        &nbsp; | &nbsp;
        🌫️ AQI {row["aqi"]}
        &nbsp; | &nbsp;
        👥 Activity {row["activity"]}
    </div>
</div>
                """,
                unsafe_allow_html=True,
            )

with right:
    st.markdown(
        '<div class="panel-title">📊 Zone Metrics</div>',
        unsafe_allow_html=True,
    )

    metrics_view = selected_zone_data.copy()
    metrics_view["status"] = metrics_view["pulse_score"].apply(get_status)

    display_columns = [
        "zone",
        "avg_traffic",
        "avg_aqi",
        "avg_energy",
        "avg_activity",
        "alerts",
        "status",
    ]

    st.dataframe(
        metrics_view[display_columns],
        width="stretch",
        hide_index=True,
    )

# ============================================================
# DETAILED ANOMALIES
# ============================================================

with st.expander("📋 View detailed anomaly records"):
    st.dataframe(
        selected_anomalies.head(100),
        width="stretch",
        hide_index=True,
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🌆 CityPulse · Python · PySpark · Pandas · Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
