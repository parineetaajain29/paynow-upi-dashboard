import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="PayNow-UPI · SME Financial Efficiency",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@600&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; }
html, body, [class*="css"], .stMarkdown, p, div { font-family: 'Inter', sans-serif !important; }
[data-testid="stAppViewContainer"] { background: #0f0f13; min-height: 100vh; }
[data-testid="stHeader"] { display: none; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }
button[data-baseweb="tab"] { font-family: 'Inter', sans-serif !important; font-size: 14px !important; font-weight: 500 !important; color: #888 !important; background: transparent !important; border: none !important; padding: 14px 24px !important; }
button[data-baseweb="tab"][aria-selected="true"] { color: #fff !important; border-bottom: 2px solid #7c6fcd !important; }
[data-testid="stTabs"] { background: #18181f; border-bottom: 1px solid #2a2a35; position: sticky; top: 0; z-index: 100; }
[role="tablist"] { padding: 0 2rem; }
.stPlotlyChart { border-radius: 16px; overflow: hidden; }

/* hero */
.hero { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 56px 60px 48px; border-bottom: 1px solid #2a2a35; }
.hero-tag { display: inline-block; background: rgba(124,111,205,0.2); border: 1px solid rgba(124,111,205,0.4); color: #a89fe8; font-size: 12px; font-weight: 600; letter-spacing: .08em; text-transform: uppercase; padding: 5px 14px; border-radius: 20px; margin-bottom: 18px; }
.hero-title { font-family: 'Playfair Display', serif !important; font-size: 42px; font-weight: 600; color: #fff; line-height: 1.2; margin-bottom: 14px; }
.hero-sub { font-size: 16px; color: #8892a4; max-width: 700px; line-height: 1.7; margin-bottom: 28px; }
.hero-meta { font-size: 13px; color: #556; }
.hero-meta span { color: #a89fe8; }

/* stat strip */
.stat-strip { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0; border-bottom: 1px solid #2a2a35; }
.stat-box { padding: 24px 28px; border-right: 1px solid #2a2a35; background: #13131a; }
.stat-box:last-child { border-right: none; }
.stat-label { font-size: 11px; color: #555; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; margin-bottom: 8px; }
.stat-val { font-size: 26px; font-weight: 700; color: #fff; line-height: 1; }
.stat-sub { font-size: 11px; color: #666; margin-top: 5px; }
.stat-pill { display: inline-block; font-size: 11px; font-weight: 700; padding: 3px 9px; border-radius: 20px; margin-top: 6px; }
.up   { background: rgba(52,211,153,0.15); color: #34d399; }
.down { background: rgba(251,113,133,0.15); color: #fb7185; }
.neu  { background: rgba(124,111,205,0.15); color: #a89fe8; }

/* page wrapper */
.page { padding: 40px 60px; }
.section-title { font-family: 'Playfair Display', serif !important; font-size: 28px; font-weight: 600; color: #fff; margin-bottom: 6px; }
.section-sub { font-size: 14px; color: #666; margin-bottom: 32px; }

/* cards */
.card { background: #18181f; border: 1px solid #2a2a35; border-radius: 16px; padding: 24px 28px; }
.card-title { font-size: 13px; font-weight: 600; color: #aaa; text-transform: uppercase; letter-spacing: .06em; margin-bottom: 16px; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }
.grid3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 24px; }

/* compare table */
.ct { width: 100%; border-collapse: collapse; }
.ct thead tr { border-bottom: 2px solid #2a2a35; }
.ct th { padding: 12px 16px; font-size: 12px; color: #666; font-weight: 600; text-transform: uppercase; letter-spacing: .05em; text-align: left; }
.ct td { padding: 13px 16px; font-size: 13px; border-bottom: 1px solid #1e1e28; }
.ct tr:hover td { background: #1c1c26; }
.ct .dim { color: #888; }
.ct .bad  { color: #fb7185; font-weight: 500; }
.ct .good { color: #34d399; font-weight: 500; }

/* hypothesis */
.hyp { background: #18181f; border: 1px solid #2a2a35; border-radius: 12px; padding: 16px 20px; margin-bottom: 10px; display: flex; align-items: flex-start; gap: 16px; transition: border-color .2s; }
.hyp:hover { border-color: #7c6fcd; }
.hyp-code { font-size: 13px; font-weight: 700; color: #a89fe8; min-width: 28px; padding-top: 1px; }
.hyp-main { flex: 1; }
.hyp-title { font-size: 14px; font-weight: 500; color: #e2e8f0; }
.hyp-stat  { font-size: 12px; color: #555; margin-top: 4px; }
.ok-badge  { background: rgba(52,211,153,0.15); color: #34d399; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 20px; white-space: nowrap; }

/* gap bars */
.gb { margin-bottom: 18px; }
.gb-top { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 7px; }
.gb-label { color: #ccc; font-weight: 500; }
.gb-track { height: 12px; background: #1e1e28; border-radius: 6px; overflow: hidden; }
.gb-fill  { height: 100%; border-radius: 6px; }

/* timeline */
.tl { position: relative; padding-left: 28px; }
.tl::before { content:''; position:absolute; left:8px; top:0; bottom:0; width:1px; background:#2a2a35; }
.tl-item { position: relative; padding: 0 0 28px 20px; }
.tl-item::before { content:''; position:absolute; left:-20px; top:4px; width:10px; height:10px; border-radius:50%; border:2px solid #2a2a35; }
.tl-yr   { font-size:12px; color:#666; font-weight:600; margin-bottom:4px; }
.tl-title { font-size:14px; font-weight:600; color:#e2e8f0; margin-bottom:4px; }
.tl-desc  { font-size:13px; color:#666; line-height:1.6; }
.tl-launch::before { border-color:#fb7185 !important; background:#fb7185; }
.tl-launch .tl-yr { color:#fb7185; }
.tl-launch .tl-title { color:#fb7185; }

/* source tags */
.src { display:inline-block; background:#1e1e28; border:1px solid #2a2a35; color:#666; font-size:11px; padding:4px 10px; border-radius:20px; margin:3px; }

/* info blocks */
.info-block { background:#18181f; border-left: 3px solid #7c6fcd; border-radius:0 12px 12px 0; padding:16px 20px; margin-bottom:12px; }
.info-block h4 { font-size:14px; font-weight:600; color:#e2e8f0; margin:0 0 6px; }
.info-block p  { font-size:13px; color:#888; margin:0; line-height:1.6; }
.info-block.teal { border-left-color:#2dd4bf; }
.info-block.coral { border-left-color:#fb7185; }
.info-block.amber { border-left-color:#fbbf24; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────
YEARS = [2019, 2020, 2021, 2022, 2023, 2024]
df = pd.DataFrame({
    "Year":         YEARS,
    "FinEff":       [0.260, 0.248, 0.268, 0.276, 0.776, 0.816],
    "Speed":        [0.000, 0.000, 0.000, 0.000, 3.497, 3.497],
    "Cost":         [6.50,  6.80,  6.30,  6.10,  1.20,  1.00],
    "Transparency": [0.25,  0.25,  0.28,  0.30,  0.65,  0.75],
    "Interop":      [0.20,  0.20,  0.22,  0.25,  0.60,  0.70],
    "DigReady":     [0.32,  0.35,  0.38,  0.42,  0.48,  0.52],
})

def dark_fig(height=300):
    return dict(
        paper_bgcolor="#18181f", plot_bgcolor="#18181f",
        font=dict(family="Inter, sans-serif", color="#888", size=12),
        margin=dict(l=10, r=10, t=40, b=10), height=height,
        xaxis=dict(showgrid=False, tickfont=dict(size=11, color="#666"), color="#555", zeroline=False),
        yaxis=dict(gridcolor="#1e1e28", tickfont=dict(size=11, color="#666"), color="#555", zeroline=False),
        legend=dict(font=dict(size=11, color="#888"), bgcolor="rgba(0,0,0,0)",
                    orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hoverlabel=dict(bgcolor="#1e1e28", font_size=12, bordercolor="#3a3a4a", font_color="#e2e8f0"),
    )

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">IBR Final Report · MGB Class of 2025</div>
  <div class="hero-title">Impact of PayNow-UPI on<br>SME Financial Efficiency</div>
  <div class="hero-sub">A cross-border real-time digital payment systems study examining transaction speed, cost reduction, liquidity, and digital readiness across the Singapore–India corridor (2019–2024).</div>
  <div class="hero-meta">Parinita Jain &nbsp;·&nbsp; <span>MS25DBM004</span> &nbsp;·&nbsp; SP Jain School of Global Management &nbsp;·&nbsp; Mentor: Mr S. Vittal</div>
</div>
""", unsafe_allow_html=True)

# ── STAT STRIP ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-strip">
  <div class="stat-box">
    <div class="stat-label">SME Efficiency Change</div>
    <div class="stat-val">+202.6%</div>
    <div class="stat-pill up">Post-launch</div>
  </div>
  <div class="stat-box">
    <div class="stat-label">Cost Reduction</div>
    <div class="stat-val">82.9%</div>
    <div class="stat-sub">6.4% → 1.1% of deal value</div>
  </div>
  <div class="stat-box">
    <div class="stat-label">Days Saved / Txn</div>
    <div class="stat-val">3.5 days</div>
    <div class="stat-sub">SWIFT avg → ~4 minutes</div>
  </div>
  <div class="stat-box">
    <div class="stat-label">Working Capital Freed</div>
    <div class="stat-val">~42 days</div>
    <div class="stat-sub">Per year, 12 monthly payments</div>
  </div>
  <div class="stat-box">
    <div class="stat-label">Annual Saving</div>
    <div class="stat-val">USD 25K</div>
    <div class="stat-sub">For a USD 500K SME</div>
  </div>
  <div class="stat-box">
    <div class="stat-label">Digital Readiness Growth</div>
    <div class="stat-val">+36.1%</div>
    <div class="stat-pill down">Binding constraint</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊  Overview",
    "📈  Trends & UPI Growth",
    "⚖️  SWIFT vs PayNow-UPI",
    "🔢  Regression & Hypotheses",
    "🔍  Digital Readiness Gap",
    "📅  Milestones & Sources",
])

# ══════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Research overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Six-year secondary dataset (2019–2024) · PayNow-UPI launch: February 2023</div>', unsafe_allow_html=True)

    # main efficiency chart
    fig_eff = go.Figure()
    fig_eff.add_vrect(x0=2022.85, x1=2024.15, fillcolor="rgba(124,111,205,0.07)",
                      line_width=0, annotation_text="Post-launch period",
                      annotation_position="top right",
                      annotation_font=dict(size=11, color="#7c6fcd"))
    fig_eff.add_trace(go.Scatter(
        x=df["Year"], y=df["FinEff"], name="SME FinEff Index",
        line=dict(color="#7c6fcd", width=3),
        mode="lines+markers",
        marker=dict(size=9, color="#7c6fcd", line=dict(color="#0f0f13", width=2)),
        fill="tozeroy", fillcolor="rgba(124,111,205,0.08)",
        hovertemplate="<b>%{x}</b><br>SME Financial Efficiency: %{y:.3f}<extra></extra>",
    ))
    layout = dark_fig(300)
    layout["yaxis"]["range"] = [0, 1]
    layout["title"] = dict(text="SME Financial Efficiency Index — 2019 to 2024", font=dict(size=14, color="#ccc"), x=0.01)
    fig_eff.update_layout(**layout, showlegend=False)
    st.plotly_chart(fig_eff, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        fig_cost = go.Figure()
        fig_cost.add_trace(go.Bar(
            x=df["Year"], y=df["Cost"],
            marker_color=["#fb7185" if y < 2023 else "#34d399" for y in df["Year"]],
            marker_cornerradius=8,
            hovertemplate="<b>%{x}</b><br>Transaction cost: %{y:.2f}%<extra></extra>",
        ))
        fig_cost.add_hline(y=3, line_dash="dash", line_color="#fbbf24", line_width=1,
                           annotation_text="SDG 10.c target (3%)",
                           annotation_font=dict(size=10, color="#fbbf24"))
        layout2 = dark_fig(260)
        layout2["yaxis"]["ticksuffix"] = "%"
        layout2["yaxis"]["range"] = [0, 8.5]
        layout2["title"] = dict(text="Transaction cost (% of deal value)", font=dict(size=13, color="#ccc"), x=0.01)
        fig_cost.update_layout(**layout2, showlegend=False)
        st.plotly_chart(fig_cost, use_container_width=True)

    with col2:
        fig_ti = go.Figure()
        fig_ti.add_trace(go.Scatter(x=df["Year"], y=df["Transparency"], name="Transparency",
            line=dict(color="#38bdf8", width=2.5), mode="lines+markers",
            marker=dict(size=7, line=dict(color="#0f0f13", width=1.5)),
            hovertemplate="<b>%{x}</b><br>Transparency: %{y:.2f}<extra></extra>"))
        fig_ti.add_trace(go.Scatter(x=df["Year"], y=df["Interop"], name="Interoperability",
            line=dict(color="#fbbf24", width=2.5, dash="dot"), mode="lines+markers",
            marker=dict(size=7, line=dict(color="#0f0f13", width=1.5)),
            hovertemplate="<b>%{x}</b><br>Interoperability: %{y:.2f}<extra></extra>"))
        fig_ti.add_trace(go.Scatter(x=df["Year"], y=df["DigReady"], name="Digital Readiness",
            line=dict(color="#fb7185", width=2.5, dash="longdash"), mode="lines+markers",
            marker=dict(size=7, line=dict(color="#0f0f13", width=1.5)),
            hovertemplate="<b>%{x}</b><br>Digital Readiness: %{y:.2f}<extra></extra>"))
        layout3 = dark_fig(260)
        layout3["yaxis"]["range"] = [0, 1]
        layout3["title"] = dict(text="Infrastructure indices vs digital readiness", font=dict(size=13, color="#ccc"), x=0.01)
        fig_ti.update_layout(**layout3)
        st.plotly_chart(fig_ti, use_container_width=True)

    # cost decomposition pie
    col3, col4 = st.columns(2)
    with col3:
        labels = ["Correspondent fees","FX spread","KYC/AML","Reconciliation"]
        swift_vals  = [3.00, 1.75, 0.65, 0.40]
        fig_pie1 = go.Figure(go.Pie(
            labels=labels, values=swift_vals,
            hole=0.55,
            marker_colors=["#fb7185","#f97316","#fbbf24","#e879f9"],
            hovertemplate="%{label}: %{value:.2f}%<extra></extra>",
            textfont=dict(size=12, color="#fff"),
        ))
        fig_pie1.update_layout(**dark_fig(260),
            title=dict(text="SWIFT cost breakdown (avg 6.5% total)", font=dict(size=13, color="#ccc"), x=0.01),
            showlegend=True,
            annotations=[dict(text="SWIFT<br><b>~6.5%</b>", x=0.5, y=0.5, font=dict(size=13, color="#fff"), showarrow=False)])
        st.plotly_chart(fig_pie1, use_container_width=True)

    with col4:
        paynow_vals = [0.05, 0.75, 0.25, 0.05]
        fig_pie2 = go.Figure(go.Pie(
            labels=labels, values=paynow_vals,
            hole=0.55,
            marker_colors=["#34d399","#2dd4bf","#38bdf8","#818cf8"],
            hovertemplate="%{label}: %{value:.2f}%<extra></extra>",
            textfont=dict(size=12, color="#fff"),
        ))
        fig_pie2.update_layout(**dark_fig(260),
            title=dict(text="PayNow-UPI cost breakdown (avg 1.1% total)", font=dict(size=13, color="#ccc"), x=0.01),
            showlegend=True,
            annotations=[dict(text="PayNow<br><b>~1.1%</b>", x=0.5, y=0.5, font=dict(size=13, color="#fff"), showarrow=False)])
        st.plotly_chart(fig_pie2, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 2 — TRENDS
# ══════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Variable trends & UPI growth</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Toggle which variables to display · hover over any data point for exact values</div>', unsafe_allow_html=True)

    selected = st.multiselect("Select variables",
        ["FinEff Index","Speed (days saved)","Transaction Cost %","Transparency","Interoperability","Digital Readiness"],
        default=["FinEff Index","Transaction Cost %","Digital Readiness"],
    )
    series_map = {
        "FinEff Index":         (df["FinEff"],        "#7c6fcd","solid"),
        "Speed (days saved)":   (df["Speed"],         "#34d399","solid"),
        "Transaction Cost %":   (df["Cost"],          "#fb7185","dash"),
        "Transparency":         (df["Transparency"],  "#38bdf8","solid"),
        "Interoperability":     (df["Interop"],       "#fbbf24","dot"),
        "Digital Readiness":    (df["DigReady"],      "#f97316","longdash"),
    }
    fig_all = go.Figure()
    fig_all.add_vline(x=2023, line_dash="dash", line_color="#fb7185", line_width=1.5, opacity=0.6,
                      annotation_text="PayNow-UPI launch (Feb 2023)",
                      annotation_position="top", annotation_font=dict(size=11, color="#fb7185"))
    for name in selected:
        vals, col, dash = series_map[name]
        fig_all.add_trace(go.Scatter(
            x=df["Year"], y=vals, name=name,
            line=dict(color=col, width=2.5, dash=dash),
            mode="lines+markers",
            marker=dict(size=8, color=col, line=dict(color="#0f0f13", width=2)),
            hovertemplate=f"<b>%{{x}}</b><br>{name}: %{{y:.3f}}<extra></extra>",
        ))
    layout_all = dark_fig(380)
    layout_all["title"] = dict(text="All variables — 2019 to 2024", font=dict(size=14, color="#ccc"), x=0.01)
    fig_all.update_layout(**layout_all)
    st.plotly_chart(fig_all, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        upi_labels = ["2016","2018","2020","2022","Jun 2023","Oct 2024"]
        upi_vals   = [0.0001, 0.3, 2.2, 7.0, 9.3, 15.5]
        upi_colors = ["#3a3a4a","#4a4a5a","#6b7280","#34d399","#2dd4bf","#38bdf8"]
        fig_upi = go.Figure(go.Bar(
            x=upi_labels, y=upi_vals, marker_color=upi_colors, marker_cornerradius=8,
            text=[f"{v}B" for v in upi_vals], textposition="outside",
            textfont=dict(size=11, color="#888"),
            hovertemplate="<b>%{x}</b><br>%{y:.2f}B transactions/month<extra></extra>",
        ))
        layout_upi = dark_fig(300)
        layout_upi["yaxis"]["ticksuffix"] = "B"
        layout_upi["title"] = dict(text="India UPI — monthly volume growth", font=dict(size=13, color="#ccc"), x=0.01)
        fig_upi.update_layout(**layout_upi, showlegend=False)
        st.plotly_chart(fig_upi, use_container_width=True)

    with col2:
        # India global RTP share
        fig_share = go.Figure()
        years_share = [2016, 2018, 2020, 2022, 2023, 2024]
        share_vals  = [1, 4, 20, 40, 49, 49]
        fig_share.add_trace(go.Scatter(
            x=years_share, y=share_vals, name="India RTP share",
            line=dict(color="#7c6fcd", width=3),
            fill="tozeroy", fillcolor="rgba(124,111,205,0.1)",
            mode="lines+markers", marker=dict(size=8, color="#7c6fcd", line=dict(color="#0f0f13", width=2)),
            hovertemplate="<b>%{x}</b><br>India's global RTP share: %{y}%<extra></extra>",
        ))
        layout_share = dark_fig(300)
        layout_share["yaxis"]["ticksuffix"] = "%"
        layout_share["yaxis"]["range"] = [0, 60]
        layout_share["title"] = dict(text="India's share of global real-time payment volume", font=dict(size=13, color="#ccc"), x=0.01)
        fig_share.update_layout(**layout_share, showlegend=False)
        st.plotly_chart(fig_share, use_container_width=True)

    # Pre vs post grouped bar
    metrics_pre  = [0.263, 6.425, 0.270, 0.218, 0.368]
    metrics_post = [0.796, 1.100, 0.700, 0.650, 0.500]
    metric_labels = ["FinEff Index","Cost (%)","Transparency","Interoperability","Dig. Readiness"]
    fig_grouped = go.Figure()
    fig_grouped.add_trace(go.Bar(name="Pre-launch avg (2019–2022)", x=metric_labels, y=metrics_pre,
        marker_color="#3a3a5a", marker_cornerradius=6,
        hovertemplate="Pre-launch — %{x}: %{y:.3f}<extra></extra>"))
    fig_grouped.add_trace(go.Bar(name="Post-launch avg (2023–2024)", x=metric_labels, y=metrics_post,
        marker_color="#7c6fcd", marker_cornerradius=6,
        hovertemplate="Post-launch — %{x}: %{y:.3f}<extra></extra>"))
    layout_grouped = dark_fig(300)
    layout_grouped["title"] = dict(text="Pre vs post-launch averages across all variables", font=dict(size=13, color="#ccc"), x=0.01)
    fig_grouped.update_layout(**layout_grouped, barmode="group")
    st.plotly_chart(fig_grouped, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 3 — COMPARE
# ══════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">SWIFT vs PayNow-UPI</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Structural comparison across every efficiency dimension · Source: BIS 2021, World Bank 2023, MAS 2023</div>', unsafe_allow_html=True)

    rows = [
        ("Settlement speed",             "T+2 to T+5 days (avg 3.5 days)",    "~4 minutes (~0.003 days)"),
        ("Total transaction cost",       "6.1–6.8% of deal value",             "1.0–1.2% of deal value"),
        ("Correspondent / network fees", "2.5–3.5% of deal value",             "0.0–0.1%"),
        ("FX spread",                    "1.5–2.0%",                           "0.7–0.8%"),
        ("KYC / AML compliance",         "0.5–0.8%",                           "0.2–0.3% (built-in)"),
        ("Reconciliation overhead",      "0.3–0.5% (manual)",                  "0.0–0.1% (ISO 20022 STP)"),
        ("Annual working capital lock-up","~42 days",                          "~0.03 days"),
        ("Minimum viable invoice",       "> USD 5,000",                        "Any value (near-zero marginal cost)"),
        ("Onboarding requirement",       "Correspondent banking relationship",  "VPA-based · KYC/AML built-in"),
        ("Transparency / tracking",      "Fragmented · no end-to-end status",   "Real-time · ISO 20022 structured"),
        ("Reconciliation method",        "Manual · back-office heavy",          "Automated · straight-through processing"),
        ("SME B2B scalability",          "Low · high fixed cost per txn",       "High (pending cap increase to >INR 60K)"),
    ]
    st.markdown("""
    <div class="card">
    <table class="ct">
      <thead><tr><th>Dimension</th><th>⛔ SWIFT / Correspondent banking</th><th>✅ PayNow-UPI Real-time</th></tr></thead>
      <tbody>""" +
    "".join(f"<tr><td class='dim'>{r[0]}</td><td class='bad'>{r[1]}</td><td class='good'>{r[2]}</td></tr>" for r in rows) +
    "</tbody></table></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        # radar
        cats = ["Speed","Cost<br>reduction","Transparency","Interoperability","Access"]
        swift_radar  = [10, 20, 25, 22, 30]
        paynow_radar = [99, 83, 75, 65, 70]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=swift_radar+[swift_radar[0]], theta=cats+[cats[0]],
            fill="toself", name="SWIFT", line_color="#fb7185", fillcolor="rgba(251,113,133,0.1)"))
        fig_radar.add_trace(go.Scatterpolar(r=paynow_radar+[paynow_radar[0]], theta=cats+[cats[0]],
            fill="toself", name="PayNow-UPI", line_color="#34d399", fillcolor="rgba(52,211,153,0.1)"))
        fig_radar.update_layout(
            polar=dict(bgcolor="#18181f",
                radialaxis=dict(visible=True, range=[0,110], gridcolor="#2a2a35",
                                tickfont=dict(size=9, color="#555")),
                angularaxis=dict(gridcolor="#2a2a35", tickfont=dict(size=11, color="#888"))),
            paper_bgcolor="#18181f", height=320, showlegend=True,
            font=dict(family="Inter, sans-serif", color="#888"),
            legend=dict(bgcolor="rgba(0,0,0,0)", font_size=12),
            title=dict(text="Capability comparison (0–100 scale)", font=dict(size=13, color="#ccc"), x=0.01),
            margin=dict(l=50, r=50, t=50, b=10),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with col2:
        # waterfall savings
        fig_wf = go.Figure(go.Waterfall(
            orientation="v",
            measure=["absolute","relative","relative","relative","relative","total"],
            x=["SWIFT total","Corresp. fees","FX spread","KYC/AML","Reconciliation","PayNow-UPI total"],
            y=[6.50, -2.95, -0.975, -0.425, -0.35, 0],
            connector=dict(line=dict(color="#3a3a4a")),
            decreasing=dict(marker_color="#34d399"),
            increasing=dict(marker_color="#fb7185"),
            totals=dict(marker_color="#7c6fcd"),
            hovertemplate="%{x}: %{y:.2f}%<extra></extra>",
        ))
        layout_wf = dark_fig(320)
        layout_wf["yaxis"]["ticksuffix"] = "%"
        layout_wf["title"] = dict(text="Cost waterfall — SWIFT → PayNow-UPI (% of deal value)", font=dict(size=13, color="#ccc"), x=0.01)
        fig_wf.update_layout(**layout_wf, showlegend=False)
        st.plotly_chart(fig_wf, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 4 — REGRESSION
# ══════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">OLS regression results</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Bivariate OLS · n=6 · df=4 · all p-values < 0.05 · Python scipy.stats.linregress</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        r2_vars = ["Transaction speed","Transaction cost","Transparency","Interoperability","Digital readiness"]
        r2_vals = [0.9968, 0.9969, 0.9879, 0.9882, 0.8190]
        r2_cols = ["#38bdf8","#38bdf8","#38bdf8","#38bdf8","#fb7185"]
        fig_r2 = go.Figure(go.Bar(
            y=r2_vars, x=r2_vals, orientation="h",
            marker_color=r2_cols, marker_cornerradius=6,
            text=[f"R² = {v:.4f}" for v in r2_vals],
            textposition="inside", textfont=dict(color="white", size=12, family="Inter"),
            hovertemplate="<b>%{y}</b><br>R² = %{x:.4f}<extra></extra>",
        ))
        layout_r2 = dark_fig(300)
        layout_r2["xaxis"] = dict(range=[0.75,1.02], gridcolor="#1e1e28", tickfont=dict(size=11,color="#666"))
        layout_r2["yaxis"] = dict(showgrid=False, tickfont=dict(size=12,color="#ccc"))
        layout_r2["title"] = dict(text="R² by predictor — infrastructure (blue) vs digital readiness (red)", font=dict(size=13,color="#ccc"), x=0.01)
        fig_r2.update_layout(**layout_r2, showlegend=False)
        st.plotly_chart(fig_r2, use_container_width=True)

        # scatter: FinEff vs DigReady
        fig_sc = go.Figure()
        fig_sc.add_trace(go.Scatter(
            x=df["DigReady"], y=df["FinEff"],
            mode="markers+text",
            text=[str(y) for y in df["Year"]],
            textposition="top center", textfont=dict(size=10, color="#888"),
            marker=dict(size=14, color=["#3a3a5a","#3a3a5a","#3a3a5a","#3a3a5a","#7c6fcd","#7c6fcd"],
                        line=dict(color="#0f0f13", width=2)),
            hovertemplate="<b>%{text}</b><br>DigReady: %{x:.2f}<br>FinEff: %{y:.3f}<extra></extra>",
        ))
        x_line = np.linspace(0.30, 0.55, 50)
        y_line = 0.14880 + 0.31076 * x_line
        fig_sc.add_trace(go.Scatter(x=x_line, y=y_line, mode="lines",
            line=dict(color="#7c6fcd", dash="dash", width=1.5), name="Fit line",
            hoverinfo="skip"))
        layout_sc = dark_fig(280)
        layout_sc["xaxis"]["title"] = dict(text="Digital Readiness Index", font=dict(size=12,color="#666"))
        layout_sc["yaxis"]["title"] = dict(text="FinEff Index", font=dict(size=12,color="#666"))
        layout_sc["title"] = dict(text="Scatter: Digital readiness vs SME efficiency", font=dict(size=13,color="#ccc"), x=0.01)
        fig_sc.update_layout(**layout_sc, showlegend=False)
        st.plotly_chart(fig_sc, use_container_width=True)

    with col2:
        st.markdown("""
        <div style="margin-top:8px;">
        <div class="info-block"><h4>β₁ Transaction Speed</h4><p>+0.152 · R²=0.997 · p&lt;0.001<br>Each day saved → +0.152 in FinEff index</p></div>
        <div class="info-block teal"><h4>β₂ Transaction Cost</h4><p>−0.100 · R²=0.997 · p&lt;0.001<br>Highest R² of all variables</p></div>
        <div class="info-block"><h4>β₃ Transparency</h4><p>+1.217 · R²=0.988 · p&lt;0.001<br>ISO 20022 STP effect</p></div>
        <div class="info-block teal"><h4>β₄ Interoperability</h4><p>+1.210 · R²=0.988 · p&lt;0.001<br>Near-identical to transparency</p></div>
        <div class="info-block coral"><h4>β₅ Digital Readiness</h4><p>+3.237 · R²=0.819 · p=0.013<br>Largest coefficient · lowest R² · binding constraint</p></div>
        <div class="info-block amber"><h4>Parsimony model</h4><p>Speed + DigReady → adj-R²=0.9973<br>Explains 99.73% of variance in FinEff</p></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-sub" style="font-size:15px;color:#ccc;font-weight:600;">Hypothesis scorecard — all four supported</div>', unsafe_allow_html=True)
    hyps = [
        ("H1","Faster settlement is positively associated with SME financial efficiency",
         "β₁=+0.152 · R²=0.9968 · p<0.001 · 3.497 days saved per txn · annual working capital freed: ~42 days · FinEff +202.6%"),
        ("H2","Lower transaction cost is positively associated with SME financial efficiency",
         "β₂=−0.100 · R²=0.9969 · p<0.001 · cost reduced 82.9% post-launch · ~USD 25K/year saving for USD 500K SME"),
        ("H3","Greater transparency & interoperability are positively associated with SME financial efficiency",
         "β₃=+1.217 · β₄=+1.210 · R²≈0.988 · p<0.001 · Transparency +159.3% · Interop +198.9% post-launch"),
        ("H4","SME digital readiness mediates the infrastructure–efficiency relationship",
         "β₅=+3.237 · R²=0.819 · p=0.013 · readiness +36.1% vs infrastructure +159–199% · interaction β₆=−0.286 confirmed"),
    ]
    for code, title, stat in hyps:
        st.markdown(f"""<div class="hyp">
            <span class="hyp-code">{code}</span>
            <div class="hyp-main">
                <div class="hyp-title">{title}</div>
                <div class="hyp-stat">{stat}</div>
            </div>
            <span class="ok-badge">Supported ✔</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 5 — GAP
# ══════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">The digital readiness gap</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Infrastructure improved 4–6× faster than SME organisational readiness · Source: Frontiers 2021, PwC 2024, Jain 2025</div>', unsafe_allow_html=True)

    gap_items = [
        ("Transaction speed (0 → 3.5 days saved)",        100, "#34d399", "Max improvement"),
        ("Transaction cost reduction",                      83,  "#2dd4bf", "−82.9%"),
        ("Payment transparency index",                     100,  "#38bdf8", "+159.3%"),
        ("Technical interoperability index",               100,  "#818cf8", "+198.9%"),
        ("SME digital readiness ← binding constraint",     36,  "#fb7185", "+36.1% only"),
    ]
    for label, pct, col, note in gap_items:
        is_key = "binding" in label
        lw = "700" if is_key else "400"
        lc = "#fb7185" if is_key else "#ccc"
        nc = "#fb7185" if is_key else "#34d399"
        st.markdown(f"""
        <div class="gb">
          <div class="gb-top">
            <span style="font-weight:{lw};color:{lc};">{label}</span>
            <span style="font-weight:700;color:{nc};">{note}</span>
          </div>
          <div class="gb-track"><div class="gb-fill" style="width:{pct}%;background:{col};"></div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        # radar
        cats = ["Speed","Cost","Transparency","Interoperability","Digital<br>Readiness"]
        vals_norm = [100, 83, 80, 100, 36]
        fig_rad = go.Figure(go.Scatterpolar(
            r=vals_norm + [vals_norm[0]], theta=cats + [cats[0]],
            fill="toself", line_color="#7c6fcd", fillcolor="rgba(124,111,205,0.12)",
            hovertemplate="%{theta}: %{r}%<extra></extra>",
        ))
        fig_rad.update_layout(
            polar=dict(bgcolor="#18181f",
                radialaxis=dict(range=[0,110], gridcolor="#2a2a35", tickfont=dict(size=9,color="#555")),
                angularaxis=dict(gridcolor="#2a2a35", tickfont=dict(size=11,color="#aaa"))),
            paper_bgcolor="#18181f", height=320, showlegend=False,
            font=dict(family="Inter, sans-serif"),
            title=dict(text="Relative improvement (%) — readiness gap clearly visible", font=dict(size=13,color="#ccc"), x=0.01),
            margin=dict(l=60,r=60,t=50,b=10),
        )
        st.plotly_chart(fig_rad, use_container_width=True)

    with col2:
        # DigReady trend with projection
        dr_actual = [0.32, 0.35, 0.38, 0.42, 0.48, 0.52]
        fig_dr = go.Figure()
        fig_dr.add_trace(go.Scatter(
            x=df["Year"], y=dr_actual, name="Actual readiness",
            line=dict(color="#fb7185", width=3), mode="lines+markers",
            marker=dict(size=8, line=dict(color="#0f0f13", width=2)),
            hovertemplate="<b>%{x}</b><br>Digital readiness: %{y:.2f}<extra></extra>",
        ))
        fig_dr.add_trace(go.Scatter(
            x=[2024,2025,2026], y=[0.52,0.60,0.68], name="Projected (if policy acts)",
            line=dict(color="#fbbf24", width=2, dash="dash"), mode="lines+markers",
            marker=dict(size=7, symbol="diamond", line=dict(color="#0f0f13", width=2)),
            hovertemplate="<b>%{x}</b><br>Projected readiness: %{y:.2f}<extra></extra>",
        ))
        layout_dr = dark_fig(320)
        layout_dr["yaxis"]["range"] = [0.2, 0.8]
        layout_dr["title"] = dict(text="Digital readiness trend & policy projection", font=dict(size=13,color="#ccc"), x=0.01)
        fig_dr.update_layout(**layout_dr)
        st.plotly_chart(fig_dr, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<p style="font-size:15px;font-weight:600;color:#34d399;margin-bottom:14px;">✅ Boon — efficiency gains</p>', unsafe_allow_html=True)
        boons = [
            ("~80% cost reduction", "~USD 25K/year saving for a USD 500K SME"),
            ("42 working capital days freed", "Per year, based on 12 monthly supplier payments"),
            ("Credit history generation", "Digital payment data enables SME working capital credit"),
            ("Just-in-time procurement", "Near-zero marginal cost enables frequent, low-value txns"),
            ("Levels the playing field", "Fixed-cost SWIFT disadvantage for SMEs eliminated"),
            ("GDP contribution", "Digital formalisation → estimated +6% India GDP contribution"),
        ]
        for title, desc in boons:
            st.markdown(f'<div class="info-block teal"><h4>{title}</h4><p>{desc}</p></div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<p style="font-size:15px;font-weight:600;color:#fb7185;margin-bottom:14px;">⚠️ Bane — risks to manage</p>', unsafe_allow_html=True)
        banes = [
            ("INR 60,000/day cap", "Limits B2B invoice settlement — most SME B2B invoices exceed this"),
            ("Payment irreversibility", "Real-time = no recall mechanism · asymmetric fraud risk"),
            ("Digital literacy gaps", "Rural and low-tech SMEs excluded · urban adoption skew"),
            ("Systemic concentration risk", "Single infrastructure failure disrupts entire corridor"),
            ("FX spread remains", "0.7–0.8% still applicable · not fully eliminated"),
            ("Policy negotiation lag", "Cap increase requires bilateral MAS-RBI agreement"),
        ]
        for title, desc in banes:
            st.markdown(f'<div class="info-block coral"><h4>{title}</h4><p>{desc}</p></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════
# TAB 6 — MILESTONES
# ══════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="page">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Key milestones & sources</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">From demonetisation (2016) to the cross-border corridor (2023) and beyond</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([3,2])
    with col1:
        milestones = [
            (2016,"#818cf8",False,"Demonetisation & UPI launch",
             "86% of Indian currency withdrawn overnight on 8 Nov 2016. UPI launched by NPCI in April 2016 — 93,000 transactions in first month. Digital transaction volumes surged 43% in Nov-Dec 2016."),
            (2017,"#38bdf8",False,"PayNow launched in Singapore",
             "MAS launches real-time domestic payment system. Adopted by nearly all banking customers in Singapore by 2022. Foundation of the corridor's Singapore-side rails."),
            (2020,"#34d399",False,"COVID accelerates digital adoption",
             "UPI hits ~2.2 billion transactions/month. Contactless payments normalised across India. India = ~20% of global real-time payment volume."),
            (2021,"#fbbf24",False,"BIS & OMFIF framework papers published",
             "BIS (2021) defines four cross-border frictions: cost, speed, transparency, access. OMFIF identifies ISO 20022 as the reconciliation enabler for SMEs."),
            (2022,"#2dd4bf",False,"UPI reaches 7B transactions/month",
             "India = ~40% of global real-time payment volume. RuPay credit card on UPI launched. Merchant QR rollout accelerates. Pre-launch FinEff index: 0.276."),
            (2023,"#fb7185",True,"★ PayNow-UPI cross-border linkage launched (Feb 2023)",
             "MAS + RBI connect two domestic rails. Near-instant settlement (~4 min). ~80% cost reduction vs SWIFT. This study's natural experiment start point. FinEff index jumps to 0.776 by year-end."),
            (2023,"#34d399",False,"UPI: 9.3B transactions/month (June 2023)",
             "India = ~49% of global real-time payment volume. SME FinEff index rises from 0.276 to 0.776. UPI expands to Singapore, UAE, France, Mauritius."),
            (2024,"#818cf8",False,"UPI expands to 7 countries; 15.5B/month",
             "India-UAE linkage (July 2024, 60,000+ merchants). India-France (Feb 2024, Eiffel Tower launch). FY 2024-25: 228.3 billion annual transactions. SME FinEff index: 0.816."),
        ]
        st.markdown('<div class="tl">', unsafe_allow_html=True)
        for yr, col, is_launch, title, desc in milestones:
            cls = "tl-item tl-launch" if is_launch else "tl-item"
            border = f"border-left:3px solid {col};" if is_launch else f"border-left:1px solid #2a2a35;"
            st.markdown(f"""
            <div class="{cls}" style="{border}padding-left:16px;margin-bottom:20px;border-radius:0 8px 8px 0;">
              <div class="tl-yr">{yr}</div>
              <div class="tl-title">{title}</div>
              <div class="tl-desc">{desc}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        # research scope pie
        fig_scope = go.Figure(go.Pie(
            labels=["Liquidity efficiency (40%)","Cost efficiency (40%)","Adoption proxy (20%)"],
            values=[40,40,20],
            hole=0.6,
            marker_colors=["#7c6fcd","#34d399","#fbbf24"],
            textfont=dict(size=12),
            hovertemplate="%{label}<extra></extra>",
        ))
        fig_scope.update_layout(**dark_fig(240),
            title=dict(text="FinEff Index composition weights", font=dict(size=13,color="#ccc"), x=0.01),
            showlegend=True,
            annotations=[dict(text="FinEff<br>Index", x=0.5, y=0.5, font=dict(size=12,color="#fff"), showarrow=False)])
        st.plotly_chart(fig_scope, use_container_width=True)

        # sources donut by institution type
        fig_src = go.Figure(go.Pie(
            labels=["Multilateral institutions","Central banks & regulators","Industry reports","Academic journals","Think tanks"],
            values=[3,4,4,3,1],
            hole=0.55,
            marker_colors=["#818cf8","#38bdf8","#34d399","#fbbf24","#f97316"],
            textfont=dict(size=11),
            hovertemplate="%{label}: %{value} papers<extra></extra>",
        ))
        fig_src.update_layout(**dark_fig(240),
            title=dict(text="15 sources by institution type", font=dict(size=13,color="#ccc"), x=0.01),
            showlegend=True,
            annotations=[dict(text="15<br>sources", x=0.5, y=0.5, font=dict(size=12,color="#fff"), showarrow=False)])
        st.plotly_chart(fig_src, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<p style="font-size:12px;color:#555;font-weight:600;margin-bottom:8px;">ALL 15 SOURCES</p>', unsafe_allow_html=True)
        sources = ["BIS 2021","BIS 2023","IMF 2025","MAS 2023","RBI 2024","World Bank 2023",
                   "PwC 2024","OMFIF 2021","MDPI 2024","ResearchGate 2024","Frontiers 2021",
                   "Jain 2025","Forbes/LKY 2023","Academic 2025","J.P. Morgan 2025"]
        st.markdown("".join(f'<span class="src">{s}</span>' for s in sources), unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center;padding:24px;border-top:1px solid #2a2a35;color:#444;font-size:12px;">
      Parinita Jain &nbsp;·&nbsp; MS25DBM004 &nbsp;·&nbsp; MGB Class of 2025 &nbsp;·&nbsp;
      SP Jain School of Global Management &nbsp;·&nbsp; IBR Final Report
    </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
