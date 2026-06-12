import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="PayNow-UPI · SME Financial Efficiency",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Google Fonts + global CSS ─────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stAppViewContainer"] { background: #f7f6f2; }
[data-testid="stHeader"]           { background: transparent; }
[data-testid="stSidebar"]          { background: #1e1e1e; }
[data-testid="stSidebar"] * { color: #e0ddd6 !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 14px; }
[data-testid="stSidebar"] hr { border-color: #333; }

/* metric cards */
.kpi-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 14px; margin-bottom: 24px; }
.kpi { background:#fff; border-radius:14px; padding:18px 20px;
       border:1px solid #eae9e3; transition: box-shadow .2s; }
.kpi:hover { box-shadow: 0 4px 18px rgba(0,0,0,0.07); }
.kpi-label { font-size:12px; color:#999; font-weight:500; letter-spacing:.04em;
             text-transform:uppercase; margin-bottom:8px; }
.kpi-val   { font-size:28px; font-weight:600; color:#1e1e1e; line-height:1; }
.kpi-sub   { font-size:12px; color:#aaa; margin-top:6px; }
.pill-up   { display:inline-block; background:#e8f5e9; color:#2e7d32;
             font-size:12px; font-weight:600; padding:3px 10px;
             border-radius:20px; margin-top:6px; }
.pill-down { display:inline-block; background:#fce8e6; color:#c62828;
             font-size:12px; font-weight:600; padding:3px 10px;
             border-radius:20px; margin-top:6px; }
.pill-neu  { display:inline-block; background:#e3f2fd; color:#1565c0;
             font-size:12px; font-weight:600; padding:3px 10px;
             border-radius:20px; margin-top:6px; }

/* section headers */
.sh { font-family:'DM Serif Display',serif; font-size:22px;
      color:#1e1e1e; margin:4px 0 2px; }
.ss { font-size:13px; color:#999; margin-bottom:16px; }

/* compare table */
.ct { width:100%; border-collapse:collapse; font-size:13px; }
.ct th { text-align:left; padding:10px 14px; font-size:11px; font-weight:600;
         text-transform:uppercase; letter-spacing:.05em; color:#999;
         border-bottom:2px solid #eae9e3; }
.ct td { padding:10px 14px; border-bottom:1px solid #f0efe9; }
.ct tr:hover td { background:#faf9f6; }
.ct .dim { color:#555; }
.ct .bad  { color:#c62828; font-weight:500; }
.ct .good { color:#1b5e20; font-weight:500; }

/* hypothesis */
.hyp { background:#fff; border-radius:12px; border:1px solid #eae9e3;
       padding:14px 18px; margin-bottom:10px; display:flex;
       align-items:flex-start; gap:14px; }
.hyp:hover { box-shadow: 0 3px 14px rgba(0,0,0,0.06); }
.hyp-code { font-weight:700; font-size:14px; color:#1e1e1e; min-width:28px; }
.hyp-body { flex:1; }
.hyp-title { font-size:13px; font-weight:500; color:#1e1e1e; }
.hyp-stat  { font-size:11px; color:#aaa; margin-top:3px; }
.badge-ok  { background:#e8f5e9; color:#2e7d32; font-size:11px; font-weight:600;
             padding:4px 12px; border-radius:20px; white-space:nowrap; }

/* gap bars */
.gb-wrap  { margin-bottom:14px; }
.gb-row   { display:flex; justify-content:space-between; font-size:13px; margin-bottom:5px; }
.gb-track { height:10px; background:#eae9e3; border-radius:6px; overflow:hidden; }
.gb-fill  { height:100%; border-radius:6px; }

/* timeline */
.tl-item { display:flex; gap:14px; padding:12px 0;
           border-bottom:1px solid #eae9e3; align-items:flex-start; }
.tl-item:last-child { border-bottom:none; }
.tl-yr   { font-size:12px; font-weight:600; color:#999; min-width:38px; padding-top:2px; }
.tl-dot  { width:10px; height:10px; border-radius:50%; flex-shrink:0; margin-top:4px; }
.tl-txt  { font-size:13px; font-weight:500; color:#1e1e1e; }
.tl-desc { font-size:12px; color:#aaa; margin-top:2px; }
.tl-launch .tl-yr  { color:#c62828; font-size:13px; }
.tl-launch .tl-txt { color:#c62828; }

/* boon/bane */
.bb-item { padding:8px 0; border-bottom:1px solid #f0efe9;
           font-size:13px; color:#555; display:flex; gap:8px; }
.bb-item:last-child { border-bottom:none; }
.ico-ok  { color:#2e7d32; font-weight:700; }
.ico-bad { color:#c62828; font-weight:700; }

/* source tags */
.src { display:inline-block; background:#f0efe9; color:#777; font-size:11px;
       padding:4px 10px; border-radius:20px; margin:3px; }

/* sidebar nav style fix */
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    padding: 8px 12px; border-radius:8px; cursor:pointer; transition:.15s;
}
section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.07);
}
</style>
""", unsafe_allow_html=True)

# ── data ──────────────────────────────────────────────────────────────────────
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

# ── colours ───────────────────────────────────────────────────────────────────
PURPLE = "#8884c8"; TEAL = "#4aac8a"; CORAL = "#c97b6a"
BLUE   = "#6aabb7"; AMBER = "#b99a5e"; GREEN = "#7aaa5a"

def fig_base(height=260):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_family="DM Sans, sans-serif", font_color="#444",
        margin=dict(l=8, r=8, t=32, b=8), height=height,
        xaxis=dict(showgrid=False, tickfont_size=11, color="#888"),
        yaxis=dict(gridcolor="#eae9e3", tickfont_size=11, color="#888", zeroline=False),
        legend=dict(font_size=11, bgcolor="rgba(0,0,0,0)", orientation="h",
                    yanchor="bottom", y=1.02, xanchor="left", x=0),
        hoverlabel=dict(bgcolor="white", font_size=12, bordercolor="#eae9e3"),
    )

# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 💳 PayNow-UPI")
    st.markdown("<p style='font-size:12px;color:#666;margin-top:-8px;'>IBR Dashboard · MGB'25</p>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigate", [
        "📊  Overview",
        "📈  All trends",
        "⚖️  SWIFT vs PayNow-UPI",
        "🔢  OLS regression",
        "🔍  Digital readiness gap",
        "📅  Key milestones",
    ], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("<p style='font-size:11px;color:#555;'>Parinita Jain<br>MS25DBM004 · MGB Class of 2025<br>SP Jain School of Global Management</p>", unsafe_allow_html=True)

# ── page title ─────────────────────────────────────────────────────────────────
titles = {
    "📊  Overview":            ("Overview", "Six key metrics from the Singapore–India PayNow-UPI study, 2019–2024"),
    "📈  All trends":          ("Variable trends", "All six regression variables plotted across the study period"),
    "⚖️  SWIFT vs PayNow-UPI": ("SWIFT vs PayNow-UPI", "Structural comparison across every efficiency dimension"),
    "🔢  OLS regression":      ("OLS regression results", "Bivariate regression — n=6, df=4; all hypotheses supported"),
    "🔍  Digital readiness gap":("Digital readiness gap", "Infrastructure improved 4–6× faster than SME organisational readiness"),
    "📅  Key milestones":      ("Key milestones", "From demonetisation (2016) to the cross-border corridor (2023–2024)"),
}
ttl, sub = titles[page]
st.markdown(f"<div class='sh'>{ttl}</div><div class='ss'>{sub}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
if "Overview" in page:
# ══════════════════════════════════════════════════════════════════════════════
    kpis = [
        ("SME financial efficiency", "<span class='pill-up'>+202.6% post-launch</span>", "Pre-launch avg 0.263 → 0.796"),
        ("Transaction cost",         "82.9%<br><span style='font-size:14px;color:#999;'>reduction</span>", "6.4% → 1.1% of deal value"),
        ("Days saved per txn",       "3.5 days", "SWIFT T+2–5 → ~4 minutes"),
        ("Working capital freed",    "~42 days/yr", "For 12 monthly supplier payments"),
        ("Annual saving (USD 500K SME)", "~USD 25K", "Direct net margin improvement"),
        ("SME digital readiness",    "<span class='pill-down'>+36.1% only</span>", "vs 159–199% infrastructure improvement"),
    ]
    st.markdown("<div class='kpi-grid'>" + "".join(
        f"<div class='kpi'><div class='kpi-label'>{l}</div>"
        f"<div class='kpi-val'>{v}</div>"
        f"<div class='kpi-sub'>{s}</div></div>"
        for l, v, s in kpis
    ) + "</div>", unsafe_allow_html=True)

    # efficiency trend
    fig = go.Figure()
    fig.add_vrect(x0=2022.85, x1=2024.1, fillcolor="#fce8e6", opacity=0.25, line_width=0, annotation_text="Post-launch", annotation_position="top right", annotation_font_size=11, annotation_font_color="#c62828")
    fig.add_trace(go.Scatter(
        x=df["Year"], y=df["FinEff"], name="SME FinEff index",
        line=dict(color=PURPLE, width=3),
        mode="lines+markers", marker=dict(size=8, color=PURPLE, line=dict(color="white", width=2)),
        fill="tozeroy", fillcolor="rgba(136,132,200,0.08)",
        hovertemplate="<b>%{x}</b><br>FinEff index: %{y:.3f}<extra></extra>",
    ))
    layout = fig_base(260)
    layout["yaxis"]["range"] = [0, 1]
    layout["title"] = dict(text="SME financial efficiency index (2019–2024)", font_size=13, x=0, font_color="#555")
    fig.update_layout(**layout, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig2 = go.Figure(go.Bar(
            x=df["Year"], y=df["Cost"],
            marker_color=[CORAL if y < 2023 else TEAL for y in df["Year"]],
            marker_cornerradius=6,
            hovertemplate="<b>%{x}</b><br>Cost: %{y:.2f}% of deal value<extra></extra>",
        ))
        layout2 = fig_base(220)
        layout2["yaxis"]["ticksuffix"] = "%"
        layout2["yaxis"]["range"] = [0, 8]
        layout2["title"] = dict(text="Transaction cost (% of deal value)", font_size=13, x=0, font_color="#555")
        fig2.update_layout(**layout2, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)
    with c2:
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(x=df["Year"], y=df["Transparency"], name="Transparency",
            line=dict(color=BLUE, width=2.5), mode="lines+markers", marker_size=6,
            hovertemplate="<b>%{x}</b><br>Transparency: %{y:.2f}<extra></extra>"))
        fig3.add_trace(go.Scatter(x=df["Year"], y=df["Interop"], name="Interoperability",
            line=dict(color=AMBER, width=2.5, dash="dot"), mode="lines+markers", marker_size=6,
            hovertemplate="<b>%{x}</b><br>Interoperability: %{y:.2f}<extra></extra>"))
        layout3 = fig_base(220)
        layout3["yaxis"]["range"] = [0, 1]
        layout3["title"] = dict(text="Transparency & interoperability indices", font_size=13, x=0, font_color="#555")
        fig3.update_layout(**layout3)
        st.plotly_chart(fig3, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
elif "trends" in page:
# ══════════════════════════════════════════════════════════════════════════════
    selected = st.multiselect("Select variables to display",
        ["FinEff index", "Speed (days saved)", "Transaction cost %", "Transparency", "Interoperability", "Digital readiness"],
        default=["FinEff index", "Transaction cost %", "Digital readiness"],
    )
    series_map = {
        "FinEff index":        (df["FinEff"],       PURPLE, "solid"),
        "Speed (days saved)":  (df["Speed"],        TEAL,   "solid"),
        "Transaction cost %":  (df["Cost"],         CORAL,  "dash"),
        "Transparency":        (df["Transparency"], BLUE,   "solid"),
        "Interoperability":    (df["Interop"],      AMBER,  "dot"),
        "Digital readiness":   (df["DigReady"],     GREEN,  "longdash"),
    }
    fig = go.Figure()
    fig.add_vline(x=2023, line_dash="dash", line_color=CORAL, line_width=1.5, opacity=0.5,
                  annotation_text="PayNow-UPI launch", annotation_position="top",
                  annotation_font_size=11, annotation_font_color=CORAL)
    for name in selected:
        vals, col, dash = series_map[name]
        fig.update_layout()
        fig.add_trace(go.Scatter(
            x=df["Year"], y=vals, name=name,
            line=dict(color=col, width=2.5, dash=dash),
            mode="lines+markers", marker=dict(size=7, color=col, line=dict(color="white", width=1.5)),
            hovertemplate=f"<b>%{{x}}</b><br>{name}: %{{y:.3f}}<extra></extra>",
        ))
    layout = fig_base(360)
    layout["title"] = dict(text="Variable trends — 2019 to 2024", font_size=13, x=0, font_color="#555")
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)

    # UPI volume
    st.markdown("<div class='ss' style='margin-top:8px;'>India UPI monthly transaction volume (billions)</div>", unsafe_allow_html=True)
    upi_y = ["2016","2018","2020","2022","2023","2024"]
    upi_v = [0.0001, 0.3, 2.2, 7.0, 9.3, 15.5]
    upi_c = ["#d3d1c7","#b4b2a9","#888780","#5DCAA5","#4aac8a","#1D9E75"]
    fig4 = go.Figure(go.Bar(x=upi_y, y=upi_v, marker_color=upi_c, marker_cornerradius=6,
        text=[f"{v}B" for v in upi_v], textposition="outside", textfont=dict(size=11, color="#888"),
        hovertemplate="<b>%{x}</b><br>%{y:.1f}B transactions/month<extra></extra>"))
    layout4 = fig_base(240)
    layout4["yaxis"]["ticksuffix"] = "B"
    layout4["title"] = dict(text="UPI monthly volume — from launch to 2024", font_size=13, x=0, font_color="#555")
    fig4.update_layout(**layout4, showlegend=False)
    st.plotly_chart(fig4, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
elif "SWIFT" in page:
# ══════════════════════════════════════════════════════════════════════════════
    rows = [
        ("Settlement speed",          "T+2 to T+5 days (avg 3.5 days)",    "~4 minutes"),
        ("Transaction cost",          "6.1–6.8% of deal value",             "1.0–1.2% of deal value"),
        ("Transparency",              "Fragmented, manual reconciliation",   "ISO 20022, real-time STP"),
        ("Correspondent fees",        "2.5–3.5% of deal value",             "0.0–0.1%"),
        ("FX spread",                 "1.5–2.0%",                           "0.7–0.8%"),
        ("KYC/AML overhead",          "0.5–0.8%",                           "0.2–0.3%"),
        ("Reconciliation overhead",   "0.3–0.5%",                           "0.0–0.1%"),
        ("Min viable invoice",        "> USD 5,000",                        "Any value (near-zero marginal cost)"),
        ("Annual working capital lock-up","~42 days",                       "~0.03 days"),
        ("Onboarding requirement",    "Correspondent banking relationship",  "VPA-based, KYC/AML built-in"),
    ]
    st.markdown("""
    <table class='ct'>
      <thead><tr><th>Dimension</th><th>SWIFT / correspondent banking</th><th>PayNow-UPI</th></tr></thead>
      <tbody>
    """ + "".join(
        f"<tr><td class='dim'>{r[0]}</td><td class='bad'>{r[1]}</td><td class='good'>{r[2]}</td></tr>"
        for r in rows
    ) + "</tbody></table>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cats   = ["Correspondent fees","FX spread","Compliance / KYC","Reconciliation overhead"]
    swift  = [3.00, 1.75, 0.65, 0.40]
    paynow = [0.05, 0.75, 0.25, 0.05]
    fig = go.Figure()
    fig.add_trace(go.Bar(name="SWIFT", x=cats, y=swift, marker_color=CORAL, marker_cornerradius=5,
        hovertemplate="SWIFT — %{x}: %{y:.2f}%<extra></extra>"))
    fig.add_trace(go.Bar(name="PayNow-UPI", x=cats, y=paynow, marker_color=TEAL, marker_cornerradius=5,
        hovertemplate="PayNow-UPI — %{x}: %{y:.2f}%<extra></extra>"))
    layout = fig_base(280)
    layout["yaxis"]["ticksuffix"] = "%"
    layout["title"] = dict(text="Cost decomposition — SWIFT vs PayNow-UPI (% of deal value)", font_size=13, x=0, font_color="#555")
    fig.update_layout(**layout, barmode="group")
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
elif "regression" in page:
# ══════════════════════════════════════════════════════════════════════════════
    reg_kpis = [
        ("β₁ Transaction speed",  "+0.152", "R²=0.997 · p<0.001"),
        ("β₂ Transaction cost",   "−0.100", "R²=0.997 · p<0.001"),
        ("β₃ Transparency",       "+1.217", "R²=0.988 · p<0.001"),
        ("β₄ Interoperability",   "+1.210", "R²=0.988 · p<0.001"),
        ("β₅ Digital readiness",  "+3.237", "R²=0.819 · p=0.013"),
        ("Parsimony model R²",    "0.9984",  "Speed + DigReady combined"),
    ]
    st.markdown("<div class='kpi-grid'>" + "".join(
        f"<div class='kpi'><div class='kpi-label'>{l}</div>"
        f"<div class='kpi-val'>{v}</div><div class='kpi-sub'>{s}</div></div>"
        for l, v, s in reg_kpis
    ) + "</div>", unsafe_allow_html=True)

    # R² chart — interactive hover
    r2_vars = ["Transaction speed","Transaction cost","Transparency","Interoperability","Digital readiness"]
    r2_vals = [0.9968, 0.9969, 0.9879, 0.9882, 0.8190]
    r2_cols = [BLUE, BLUE, BLUE, BLUE, CORAL]
    fig = go.Figure(go.Bar(
        y=r2_vars, x=r2_vals, orientation="h",
        marker_color=r2_cols, marker_cornerradius=5,
        text=[f"R²={v:.4f}" for v in r2_vals],
        textposition="inside", textfont=dict(color="white", size=12),
        hovertemplate="<b>%{y}</b><br>R² = %{x:.4f}<extra></extra>",
    ))
    layout = fig_base(260)
    layout["xaxis"] = dict(range=[0.75, 1.01], gridcolor="#eae9e3", tickfont_size=11, color="#888")
    layout["yaxis"] = dict(showgrid=False, tickfont_size=12, color="#444")
    layout["title"] = dict(text="R² by predictor — infrastructure (blue) vs readiness (coral)", font_size=13, x=0, font_color="#555")
    fig.update_layout(**layout, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("<div class='ss'>Hypothesis scorecard — all four supported</div>", unsafe_allow_html=True)
    hyps = [
        ("H1","Faster settlement → higher SME financial efficiency","β₁=+0.152 · R²=0.997 · p<0.001 · 3.5 days saved per txn"),
        ("H2","Lower cost → higher SME financial efficiency","β₂=−0.100 · R²=0.997 · p<0.001 · cost fell 82.9%"),
        ("H3","Greater transparency & interoperability → higher efficiency","β₃=+1.217 · β₄=+1.210 · R²≈0.988 · p<0.001"),
        ("H4","SME digital readiness mediates infrastructure–efficiency link","β₅=+3.237 · R²=0.819 · p=0.013 · readiness +36.1%"),
    ]
    for code, title, stat in hyps:
        st.markdown(
            f"<div class='hyp'>"
            f"<span class='hyp-code'>{code}</span>"
            f"<div class='hyp-body'><div class='hyp-title'>{title}</div>"
            f"<div class='hyp-stat'>{stat}</div></div>"
            f"<span class='badge-ok'>Supported ✔</span>"
            f"</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
elif "readiness" in page:
# ══════════════════════════════════════════════════════════════════════════════
    gap_items = [
        ("Transaction speed (0 → 3.5 days saved)", 100, TEAL,   "Max improvement"),
        ("Transaction cost reduction",               83,  TEAL,   "−82.9%"),
        ("Payment transparency index",              100,  BLUE,   "+159.3%"),
        ("Technical interoperability index",        100,  AMBER,  "+198.9%"),
        ("SME digital readiness ← binding constraint", 36, CORAL, "+36.1%"),
    ]
    for label, pct, col, note in gap_items:
        is_key = "binding" in label
        lw = "600" if is_key else "400"
        lc = "#c62828" if is_key else "#444"
        nc = "#c62828" if is_key else "#1b5e20"
        st.markdown(
            f"<div class='gb-wrap'>"
            f"<div class='gb-row'>"
            f"<span style='font-weight:{lw};color:{lc};'>{label}</span>"
            f"<span style='font-weight:600;color:{nc};'>{note}</span></div>"
            f"<div class='gb-track'>"
            f"<div class='gb-fill' style='width:{pct}%;background:{col};'></div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<p style='font-weight:600;font-size:14px;color:#1b5e20;margin-bottom:10px;'>Boon — efficiency gains</p>", unsafe_allow_html=True)
        boons = ["80% cost reduction → ~USD 25K/yr saving", "42 working capital days freed annually",
                 "Credit history generation for SME lending", "Just-in-time procurement now viable",
                 "Levels playing field vs large corporates"]
        for b in boons:
            st.markdown(f"<div class='bb-item'><span class='ico-ok'>✓</span>{b}</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<p style='font-weight:600;font-size:14px;color:#c62828;margin-bottom:10px;'>Bane — risks to manage</p>", unsafe_allow_html=True)
        banes = ["INR 60,000/day cap limits B2B invoices", "Payments irreversible — fraud exposure",
                 "Digital literacy gaps exclude rural SMEs", "Systemic concentration risk at scale",
                 "Policy negotiation needed for cap increase"]
        for b in banes:
            st.markdown(f"<div class='bb-item'><span class='ico-bad'>⚠</span>{b}</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # readiness vs infrastructure radar
    categories = ["Speed<br>improvement","Cost<br>reduction","Transparency","Interoperability","Digital<br>readiness"]
    infra_norm  = [100, 83, 80, 100, 36]   # normalised to max 100
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=infra_norm, theta=categories, fill="toself",
        name="Change achieved (%)", line_color=TEAL, fillcolor="rgba(74,172,138,0.15)",
        hovertemplate="%{theta}: %{r}%<extra></extra>"))
    fig.update_layout(
        polar=dict(bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0,110], gridcolor="#eae9e3", tickfont_size=10),
            angularaxis=dict(gridcolor="#eae9e3")),
        paper_bgcolor="rgba(0,0,0,0)", height=320, showlegend=False,
        font_family="DM Sans, sans-serif",
        title=dict(text="Relative % improvement across all variables (readiness lags clearly)", font_size=13, x=0, font_color="#555"),
    )
    st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
elif "milestones" in page:
# ══════════════════════════════════════════════════════════════════════════════
    milestones = [
        (2016, PURPLE, False, "Demonetisation & UPI launch",
         "86% of Indian currency withdrawn overnight. UPI launched by NPCI — 93,000 txns in first month."),
        (2017, BLUE,   False, "PayNow launched in Singapore",
         "MAS launches real-time domestic payment system; adopted by nearly all banking customers by 2022."),
        (2020, TEAL,   False, "COVID accelerates digital adoption",
         "UPI hits ~2.2B transactions/month. Contactless payments normalised across India."),
        (2021, AMBER,  False, "BIS & OMFIF framework papers",
         "BIS (2021) defines four cross-border frictions. OMFIF identifies ISO 20022 as reconciliation enabler."),
        (2022, GREEN,  False, "UPI reaches 7B transactions/month",
         "India = ~40% of global real-time payment volume. RuPay credit card on UPI launched."),
        (2023, CORAL,  True,  "★ PayNow-UPI cross-border linkage launched",
         "MAS + RBI connect two domestic rails (Feb 2023). Near-instant settlement, ~80% cost reduction vs SWIFT."),
        (2023, TEAL,   False, "UPI: 9.3B transactions/month (June 2023)",
         "India = ~49% of global real-time payment volume. SME FinEff index rises 0.276 → 0.776."),
        (2024, PURPLE, False, "UPI expands to 7 countries; 15.5B/month",
         "India-UAE & India-France linkages launched. FY 2024-25: 228.3B annual transactions."),
    ]
    for yr, col, is_launch, title, desc in milestones:
        cls = "tl-item tl-launch" if is_launch else "tl-item"
        st.markdown(
            f"<div class='{cls}'>"
            f"<span class='tl-yr'>{yr}</span>"
            f"<span class='tl-dot' style='background:{col};'></span>"
            f"<div><div class='tl-txt'>{title}</div>"
            f"<div class='tl-desc'>{desc}</div></div>"
            f"</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px;font-weight:500;color:#555;margin-bottom:8px;'>15 A/A+-grade sources · 2020–2025</p>", unsafe_allow_html=True)
    sources = ["BIS 2021","BIS 2023","IMF 2025","MAS 2023","RBI 2024","World Bank 2023",
               "PwC 2024","OMFIF 2021","MDPI 2024","ResearchGate 2024","Frontiers 2021",
               "Journal 2025","Forbes/LKY 2023","Academic 2025","J.P. Morgan 2025"]
    st.markdown("".join(f"<span class='src'>{s}</span>" for s in sources), unsafe_allow_html=True)
