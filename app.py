import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="PayNow-UPI IBR Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── muted colour palette ──────────────────────────────────────────────────────
C_PURPLE  = "#8884c8"
C_TEAL    = "#5DCAA5"
C_CORAL   = "#c97b6a"
C_BLUE    = "#6aabb7"
C_AMBER   = "#b99a5e"
C_GREEN   = "#8aab6a"
C_LIGHT   = "#f5f4f0"
C_BORDER  = "#dddbd3"

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_family="sans-serif",
    font_color="#444",
    margin=dict(l=10, r=10, t=30, b=10),
    xaxis=dict(showgrid=False, tickfont_size=11),
    legend=dict(font_size=11, bgcolor="rgba(0,0,0,0)"),
    hoverlabel=dict(bgcolor="white", font_size=12),
)
Y_DEFAULT = dict(gridcolor="#ebebeb", tickfont_size=11)

# ── data ──────────────────────────────────────────────────────────────────────
YEARS = [2019, 2020, 2021, 2022, 2023, 2024]

df = pd.DataFrame({
    "Year":          YEARS,
    "FinEff":        [0.260, 0.248, 0.268, 0.276, 0.776, 0.816],
    "Speed":         [0.000, 0.000, 0.000, 0.000, 3.497, 3.497],
    "Cost":          [6.50,  6.80,  6.30,  6.10,  1.20,  1.00],
    "Transparency":  [0.25,  0.25,  0.28,  0.30,  0.65,  0.75],
    "Interop":       [0.20,  0.20,  0.22,  0.25,  0.60,  0.70],
    "DigReady":      [0.32,  0.35,  0.38,  0.42,  0.48,  0.52],
})

UPI_LABELS = ["2016", "2018", "2020", "2022", "2023", "2024"]
UPI_VOL    = [0.0001, 0.3, 2.2, 7.0, 9.3, 15.5]
UPI_COLORS = ["#d3d1c7","#b4b2a9","#888780","#5DCAA5","#4aac8a","#1D9E75"]

COST_CATS   = ["Correspondent fees","FX spread","Compliance/KYC","Reconciliation"]
COST_SWIFT  = [3.00, 1.75, 0.65, 0.40]
COST_PAYNOW = [0.05, 0.75, 0.25, 0.05]

R2_VARS  = ["Transaction speed","Transaction cost","Transparency","Interoperability","Digital readiness"]
R2_VALS  = [0.9968, 0.9969, 0.9879, 0.9882, 0.8190]
R2_COLS  = [C_BLUE]*4 + [C_CORAL]

HYPOTHESES = [
    ("H1","Faster settlement → higher SME efficiency",
     "β₁=+0.152 · R²=0.997 · p<0.001 · 3.5 days saved"),
    ("H2","Lower cost → higher SME efficiency",
     "β₂=−0.100 · R²=0.997 · p<0.001 · cost −82.9%"),
    ("H3","Greater transparency & interoperability → higher efficiency",
     "β₃=+1.217 · β₄=+1.210 · R²≈0.988 · p<0.001"),
    ("H4","Digital readiness mediates infrastructure–efficiency link",
     "β₅=+3.237 · R²=0.819 · p=0.013 · readiness +36.1%"),
]

MILESTONES = [
    (2016, C_PURPLE, "Demonetisation & UPI launch",
     "86% of Indian currency withdrawn overnight. UPI launched by NPCI — 93,000 transactions in first month."),
    (2017, C_BLUE,   "PayNow launched in Singapore",
     "MAS launches real-time domestic payment system; adopted by nearly all banking customers by 2022."),
    (2020, C_TEAL,   "COVID accelerates digital adoption",
     "UPI hits ~2.2 billion transactions/month. Contactless payments normalised across India."),
    (2021, C_AMBER,  "BIS & OMFIF framework papers",
     "BIS (2021) defines four cross-border frictions. OMFIF identifies ISO 20022 as reconciliation enabler."),
    (2022, C_GREEN,  "UPI reaches 7B transactions/month",
     "India = ~40% of global real-time payment volume. RuPay credit card on UPI launched."),
    (2023, C_CORAL,  "★ PayNow-UPI cross-border linkage launched (Feb 2023)",
     "MAS + RBI connect two domestic rails. Near-instant settlement, ~80% cost reduction vs SWIFT."),
    (2023, C_TEAL,   "UPI: 9.3B transactions/month (June 2023)",
     "India = ~49% of global real-time payment volume. SME FinEff index rises from 0.276 to 0.776."),
    (2024, C_PURPLE, "UPI expands to 7 countries; 15.5B/month",
     "India-UAE & India-France linkages launched. FY 2024-25: 228.3B annual transactions."),
]

SOURCES = [
    "BIS 2021","BIS 2023","IMF 2025","MAS 2023","RBI 2024",
    "World Bank 2023","PwC 2024","OMFIF 2021","MDPI 2024",
    "ResearchGate 2024","Frontiers 2021","Journal 2025",
    "Forbes/LKY 2023","Academic 2025","J.P. Morgan 2025",
]

# ── custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #faf9f6; }
[data-testid="stHeader"] { background: transparent; }
.metric-card {
    background: #f0efe9;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    margin-bottom: 2px;
}
.metric-label { font-size: 12px; color: #888; margin-bottom: 4px; }
.metric-value { font-size: 22px; font-weight: 600; color: #2c2c2a; }
.metric-sub   { font-size: 11px; color: #aaa; margin-top: 2px; }
.tag-up   { background: #EAF3DE; color: #3B6D11; font-size: 11px;
             font-weight: 600; padding: 2px 8px; border-radius: 4px; }
.tag-down { background: #FAECE7; color: #993C1D; font-size: 11px;
             font-weight: 600; padding: 2px 8px; border-radius: 4px; }
.section-title { font-size: 15px; font-weight: 600; color: #2c2c2a;
                 margin-bottom: 2px; margin-top: 4px; }
.section-sub   { font-size: 12px; color: #888; margin-bottom: 12px; }
.compare-cell-bad  { color: #993C1D; font-weight: 500; }
.compare-cell-good { color: #0F6E56; font-weight: 500; }
.hyp-badge { background: #EAF3DE; color: #3B6D11; font-size: 12px;
              font-weight: 600; padding: 3px 10px; border-radius: 5px; }
.tl-dot { display: inline-block; width: 10px; height: 10px;
          border-radius: 50%; margin-right: 6px; vertical-align: middle; }
.src-tag { display: inline-block; background: #f0efe9; color: #666;
           font-size: 12px; padding: 3px 9px; border-radius: 5px; margin: 3px; }
.launch-badge { background: #FAECE7; color: #993C1D; font-size: 12px;
                font-weight: 600; padding: 3px 10px; border-radius: 5px; }
div[data-testid="stHorizontalBlock"] { gap: 10px; }
</style>
""", unsafe_allow_html=True)

# ── header ────────────────────────────────────────────────────────────────────
st.markdown("## PayNow-UPI & SME Financial Efficiency")
st.markdown(
    "<p style='color:#888;font-size:13px;margin-top:-10px;margin-bottom:20px;'>"
    "Singapore–India cross-border payment linkage · 2019–2024 · "
    "Individual Business Research — Parinita Jain · MS25DBM004 · MGB'25</p>",
    unsafe_allow_html=True,
)

# ── tabs ──────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📊 Overview",
    "📈 Trends",
    "⚖️ SWIFT vs PayNow-UPI",
    "🔢 Regression",
    "🔍 Digital readiness gap",
    "📅 Key milestones",
])

# ════════════════════════════════════════════════════════════════════════
# TAB 1 — OVERVIEW
# ════════════════════════════════════════════════════════════════════════
with tabs[0]:
    metrics = [
        ("SME financial efficiency","<span class='tag-up'>+202.6%</span>","Pre → post launch"),
        ("Transaction cost reduction","82.9%","6.4% → 1.1% of deal value"),
        ("Days saved per transaction","3.5 days","SWIFT avg → ~4 minutes"),
        ("Annual working capital freed","~42 days","For 12 monthly payments"),
        ("Annual saving (USD 500K SME)","~USD 25K","Direct margin improvement"),
        ("SME digital readiness growth","<span class='tag-down'>+36.1%</span>","vs 159–199% infrastructure"),
    ]
    cols = st.columns(3)
    for i, (lbl, val, sub) in enumerate(metrics):
        with cols[i % 3]:
            st.markdown(
                f"<div class='metric-card'>"
                f"<div class='metric-label'>{lbl}</div>"
                f"<div class='metric-value'>{val}</div>"
                f"<div class='metric-sub'>{sub}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # efficiency trend
    st.markdown("<div class='section-title'>SME financial efficiency index — 2019 to 2024</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Composite index (0–1); vertical line marks PayNow-UPI launch, Feb 2023</div>", unsafe_allow_html=True)

    fig_eff = go.Figure()
    fig_eff.add_vline(x=2023, line_dash="dash", line_color=C_CORAL, line_width=1.2, opacity=0.5)
    fig_eff.add_annotation(x=2023.05, y=0.9, text="Launch", showarrow=False,
                           font=dict(size=10, color=C_CORAL), xanchor="left")
    fig_eff.add_trace(go.Scatter(
        x=df["Year"], y=df["FinEff"],
        mode="lines+markers",
        name="FinEff index",
        line=dict(color=C_PURPLE, width=2.5),
        marker=dict(size=7, color=C_PURPLE),
        fill="tozeroy", fillcolor="rgba(136,132,200,0.07)",
    ))
    fig_eff.update_layout(**PLOT_LAYOUT, height=240, showlegend=False,
                          yaxis=dict(range=[0, 1], **Y_DEFAULT))
    st.plotly_chart(fig_eff, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-title'>Transaction cost (% of deal value)</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-sub'>Pre-launch 6.1–6.8%, post-launch 1.0–1.2%</div>", unsafe_allow_html=True)
        bar_colors = [C_CORAL if y < 2023 else C_TEAL for y in df["Year"]]
        fig_cost = go.Figure(go.Bar(
            x=df["Year"], y=df["Cost"],
            marker_color=bar_colors, marker_cornerradius=4,
        ))
        fig_cost.update_layout(**PLOT_LAYOUT, height=220, showlegend=False,
                               yaxis=dict(range=[0, 8], ticksuffix="%", **Y_DEFAULT))
        st.plotly_chart(fig_cost, use_container_width=True)

    with c2:
        st.markdown("<div class='section-title'>Transparency & interoperability indices</div>", unsafe_allow_html=True)
        st.markdown("<div class='section-sub'>Both rose ~160–200% post-launch</div>", unsafe_allow_html=True)
        fig_ti = go.Figure()
        fig_ti.add_trace(go.Scatter(x=df["Year"], y=df["Transparency"],
            name="Transparency", line=dict(color=C_BLUE, width=2),
            mode="lines+markers", marker_size=5))
        fig_ti.add_trace(go.Scatter(x=df["Year"], y=df["Interop"],
            name="Interoperability", line=dict(color=C_AMBER, width=2, dash="dot"),
            mode="lines+markers", marker_size=5))
        fig_ti.update_layout(**PLOT_LAYOUT, height=220, yaxis=dict(range=[0, 1], **Y_DEFAULT))
        st.plotly_chart(fig_ti, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 2 — TRENDS
# ════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown("<div class='section-title'>All six variables — 2019–2024</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Infrastructure variables on primary axis; cost (%) note: values are higher than 0–1 indices</div>", unsafe_allow_html=True)

    fig_all = go.Figure()
    fig_all.add_vline(x=2023, line_dash="dash", line_color=C_CORAL, line_width=1, opacity=0.5)
    series = [
        ("FinEff",       "FinEff index",       C_PURPLE, "solid",   df["FinEff"]),
        ("Speed",        "Speed (days saved)", C_TEAL,   "solid",   df["Speed"]),
        ("Cost",         "Cost % deal val",    C_CORAL,  "dash",    df["Cost"]),
        ("Transparency", "Transparency",       C_BLUE,   "solid",   df["Transparency"]),
        ("Interop",      "Interoperability",   C_AMBER,  "dot",     df["Interop"]),
        ("DigReady",     "Digital readiness",  C_GREEN,  "longdash",df["DigReady"]),
    ]
    for _, name, col, dash, vals in series:
        fig_all.add_trace(go.Scatter(
            x=df["Year"], y=vals, name=name,
            line=dict(color=col, width=2, dash=dash),
            mode="lines+markers", marker_size=5,
        ))
    fig_all.update_layout(**PLOT_LAYOUT, height=350, yaxis=Y_DEFAULT)
    st.plotly_chart(fig_all, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>India UPI transaction volume — monthly (billions)</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Explosive growth following demonetisation 2016; PayNow-UPI cross-border linkage Feb 2023</div>", unsafe_allow_html=True)

    fig_upi = go.Figure(go.Bar(
        x=UPI_LABELS, y=UPI_VOL,
        marker_color=UPI_COLORS, marker_cornerradius=4,
        text=[f"{v}B" for v in UPI_VOL], textposition="outside",
        textfont=dict(size=11, color="#888"),
    ))
    fig_upi.update_layout(**PLOT_LAYOUT, height=250, showlegend=False,
                          yaxis=dict(ticksuffix="B", **Y_DEFAULT))
    st.plotly_chart(fig_upi, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 3 — COMPARE
# ════════════════════════════════════════════════════════════════════════
with tabs[2]:
    compare_data = [
        ("Settlement speed",           "T+2 to T+5 days",          "~4 minutes"),
        ("Transaction cost",           "6.1–6.8% of deal value",   "1.0–1.2% of deal value"),
        ("Transparency",               "Fragmented, manual",        "ISO 20022, real-time STP"),
        ("Reconciliation",             "Manual, back-office heavy", "Automated (STP)"),
        ("Correspondent fees",         "2.5–3.5% of deal value",   "0.0–0.1%"),
        ("FX spread",                  "1.5–2.0%",                  "0.7–0.8%"),
        ("Min viable invoice",         "> USD 5,000",               "Any value (near-zero marginal cost)"),
        ("Annual working capital lock-up","~42 days",               "~0.03 days"),
    ]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<p style='font-size:14px;font-weight:600;color:#993C1D;margin-bottom:10px;'>SWIFT / correspondent banking</p>", unsafe_allow_html=True)
        for dim, swift_val, _ in compare_data:
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;padding:7px 0;"
                f"border-bottom:0.5px solid {C_BORDER};font-size:13px;'>"
                f"<span style='color:#888;'>{dim}</span>"
                f"<span class='compare-cell-bad'>{swift_val}</span></div>",
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown("<p style='font-size:14px;font-weight:600;color:#0F6E56;margin-bottom:10px;'>PayNow-UPI real-time linkage</p>", unsafe_allow_html=True)
        for dim, _, pn_val in compare_data:
            st.markdown(
                f"<div style='display:flex;justify-content:space-between;padding:7px 0;"
                f"border-bottom:0.5px solid {C_BORDER};font-size:13px;'>"
                f"<span style='color:#888;'>{dim}</span>"
                f"<span class='compare-cell-good'>{pn_val}</span></div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Cost decomposition — SWIFT vs PayNow-UPI</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>All figures in % of deal value. Source: World Bank 2023, J.P. Morgan 2025, MAS 2023</div>", unsafe_allow_html=True)

    fig_decomp = go.Figure()
    fig_decomp.add_trace(go.Bar(name="SWIFT", x=COST_CATS, y=COST_SWIFT,
                                marker_color=C_CORAL, marker_cornerradius=3))
    fig_decomp.add_trace(go.Bar(name="PayNow-UPI", x=COST_CATS, y=COST_PAYNOW,
                                marker_color=C_TEAL, marker_cornerradius=3))
    fig_decomp.update_layout(**PLOT_LAYOUT, height=280, barmode="group",
                             yaxis=dict(ticksuffix="%", **Y_DEFAULT))
    st.plotly_chart(fig_decomp, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 4 — REGRESSION
# ════════════════════════════════════════════════════════════════════════
with tabs[3]:
    reg_metrics = [
        ("β₁ Transaction speed",  "+0.152", "R²=0.997, p<0.001"),
        ("β₂ Transaction cost",   "−0.100", "R²=0.997, p<0.001"),
        ("β₃ Transparency",       "+1.217", "R²=0.988, p<0.001"),
        ("β₄ Interoperability",   "+1.210", "R²=0.988, p<0.001"),
        ("β₅ Digital readiness",  "+3.237", "R²=0.819, p=0.013"),
        ("Parsimony model R²",    "0.9984", "Speed + DigReady, adj-R²=0.997"),
    ]
    cols = st.columns(3)
    for i, (lbl, val, sub) in enumerate(reg_metrics):
        with cols[i % 3]:
            st.markdown(
                f"<div class='metric-card'>"
                f"<div class='metric-label'>{lbl}</div>"
                f"<div class='metric-value'>{val}</div>"
                f"<div class='metric-sub'>{sub}</div>"
                f"</div>",
                unsafe_allow_html=True,
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>R² by variable</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Infrastructure variables >0.98; digital readiness only 0.819 — the digital preparedness gap in numbers</div>", unsafe_allow_html=True)

    fig_r2 = go.Figure(go.Bar(
        y=R2_VARS, x=R2_VALS, orientation="h",
        marker_color=R2_COLS, marker_cornerradius=3,
        text=[f"{v:.4f}" for v in R2_VALS], textposition="inside",
        textfont=dict(color="white", size=11),
    ))
    fig_r2.update_layout(**PLOT_LAYOUT, height=240, showlegend=False,
                         xaxis=dict(range=[0.75, 1.01], **Y_DEFAULT),
                         yaxis=dict(showgrid=False, tickfont_size=12))
    st.plotly_chart(fig_r2, use_container_width=True)

    st.markdown("<div class='section-title'>Hypothesis scorecard</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>All four hypotheses supported — OLS bivariate regression, n=6, df=4</div>", unsafe_allow_html=True)

    for code, text, stats in HYPOTHESES:
        col_a, col_b, col_c = st.columns([0.06, 0.7, 0.24])
        with col_a:
            st.markdown(f"<p style='font-weight:600;font-size:14px;margin-top:6px;'>{code}</p>",
                        unsafe_allow_html=True)
        with col_b:
            st.markdown(
                f"<p style='font-size:13px;margin-bottom:0;'>{text}</p>"
                f"<p style='font-size:11px;color:#aaa;margin-top:2px;'>{stats}</p>",
                unsafe_allow_html=True,
            )
        with col_c:
            st.markdown(f"<span class='hyp-badge'>Supported ✔</span>", unsafe_allow_html=True)
        st.markdown(f"<hr style='margin:6px 0;border:none;border-top:0.5px solid {C_BORDER};'>",
                    unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════
# TAB 5 — GAP
# ════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("<div class='section-title'>The digital preparedness gap</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Infrastructure improved 4–6× faster than SME organisational readiness. Source: Frontiers 2021, PwC 2024, Jain 2025</div>", unsafe_allow_html=True)

    gap_items = [
        ("Transaction speed (0 → 3.5 days saved)", 100, C_TEAL,  "Max change"),
        ("Transaction cost reduction",               83,  C_TEAL,  "−82.9%"),
        ("Payment transparency index",              100,  C_BLUE,  "+159.3%"),
        ("Technical interoperability index",        100,  C_AMBER, "+198.9%"),
        ("SME digital readiness ← binding constraint",36, C_CORAL, "+36.1%"),
    ]

    for label, pct, col, note in gap_items:
        is_constraint = "binding" in label
        weight = "600" if is_constraint else "400"
        lc = "#2c2c2a" if is_constraint else "#555"
        nc = C_CORAL if is_constraint else "#0F6E56"

        st.markdown(
            f"<div style='display:flex;justify-content:space-between;"
            f"font-size:13px;margin-bottom:4px;'>"
            f"<span style='font-weight:{weight};color:{lc};'>{label}</span>"
            f"<span style='font-weight:600;color:{nc};'>{note}</span></div>",
            unsafe_allow_html=True,
        )
        bar_html = (
            f"<div style='height:10px;background:#ede;border-radius:5px;margin-bottom:12px;'>"
            f"<div style='width:{pct}%;height:100%;border-radius:5px;background:{col};'></div>"
            f"</div>"
        )
        st.markdown(bar_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        st.markdown("<div class='section-title'>Boon factors</div>", unsafe_allow_html=True)
        boons = [
            "80% cost reduction → ~USD 25K/yr saving",
            "42 working capital days freed annually",
            "Credit history generation for SME lending",
            "Just-in-time procurement now viable",
            "Levels playing field vs large corporates",
        ]
        for item in boons:
            st.markdown(
                f"<div style='padding:6px 0;border-bottom:0.5px solid {C_BORDER};"
                f"font-size:13px;color:#555;'>"
                f"<span style='color:{C_TEAL};margin-right:6px;'>✓</span>{item}</div>",
                unsafe_allow_html=True,
            )
    with b2:
        st.markdown("<div class='section-title'>Bane risks</div>", unsafe_allow_html=True)
        banes = [
            "INR 60,000/day cap limits B2B invoices",
            "Payments irreversible — fraud exposure",
            "Digital literacy gaps exclude rural SMEs",
            "Systemic concentration risk at scale",
            "Policy negotiation needed for cap increase",
        ]
        for item in banes:
            st.markdown(
                f"<div style='padding:6px 0;border-bottom:0.5px solid {C_BORDER};"
                f"font-size:13px;color:#555;'>"
                f"<span style='color:{C_CORAL};margin-right:6px;'>⚠</span>{item}</div>",
                unsafe_allow_html=True,
            )

# ════════════════════════════════════════════════════════════════════════
# TAB 6 — TIMELINE
# ════════════════════════════════════════════════════════════════════════
with tabs[5]:
    st.markdown("<div class='section-title'>Key milestones — India digital payments & PayNow-UPI</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>From demonetisation shock to cross-border corridor</div>", unsafe_allow_html=True)

    for yr, col, title, desc in MILESTONES:
        is_launch = "★" in title
        year_style = f"font-weight:700;color:{C_CORAL};" if is_launch else "color:#888;"
        title_style = f"font-weight:600;color:{C_CORAL};" if is_launch else "font-weight:500;color:#2c2c2a;"
        st.markdown(
            f"<div style='display:flex;gap:12px;padding:10px 0;"
            f"border-bottom:0.5px solid {C_BORDER};align-items:flex-start;'>"
            f"<span style='font-size:13px;min-width:36px;{year_style}'>{yr}</span>"
            f"<span class='tl-dot' style='background:{col};margin-top:5px;'></span>"
            f"<div><p style='font-size:13px;margin:0;{title_style}'>{title}</p>"
            f"<p style='font-size:12px;color:#999;margin:2px 0 0;'>{desc}</p></div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>15 A/A+-grade sources · 2020–2025</div>", unsafe_allow_html=True)
    src_html = "".join(f"<span class='src-tag'>{s}</span>" for s in SOURCES)
    st.markdown(f"<div style='margin-top:8px;'>{src_html}</div>", unsafe_allow_html=True)

# ── footer ────────────────────────────────────────────────────────────────────
st.markdown(
    f"<div style='margin-top:2rem;padding-top:1rem;border-top:0.5px solid {C_BORDER};"
    f"font-size:12px;color:#bbb;text-align:center;'>"
    f"Parinita Jain · MS25DBM004 · MGB Class of 2025 · "
    f"SP Jain School of Global Management · IBR Final Report</div>",
    unsafe_allow_html=True,
)
