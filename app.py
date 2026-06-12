import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="PayNow-UPI · SME Financial Efficiency",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── LIGHT PALETTE ─────────────────────────────────────────────────────────────
BG      = "#FAFAF7"
BG1     = "#FFFFFF"
BG2     = "#F4F3EE"
BORDER  = "#E5E3DC"
BORDER2 = "#D1CFC5"
PURPLE  = "#6B5FD4"
PURPLEL = "#8B7FE8"
TEAL    = "#0D9488"
GREEN   = "#059669"
CORAL   = "#DC4848"
AMBER   = "#B45309"
BLUE    = "#2563EB"
T1      = "#1A1A2E"
T2      = "#374151"
T3      = "#6B7280"
T4      = "#9CA3AF"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"], * {{
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}}
section.main > div {{ padding-top: 0 !important; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
header[data-testid="stHeader"] {{ display: none !important; }}
div[data-testid="stDecoration"] {{ display: none !important; }}
section[data-testid="stSidebar"] {{ display: none !important; }}
div[data-testid="collapsedControl"] {{ display: none !important; }}
div[data-testid="stAppViewContainer"] {{ background: {BG} !important; }}
div[data-baseweb="tab-list"] {{
    background: {BG1} !important;
    border-bottom: 1px solid {BORDER} !important;
    padding: 0 2.5rem !important;
    gap: 0 !important;
    position: sticky !important; top: 0 !important; z-index: 999 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
}}
button[data-baseweb="tab"] {{
    background: transparent !important;
    color: {T3} !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 15px 20px !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    transition: all .15s !important;
}}
button[data-baseweb="tab"]:hover {{ color: {T2} !important; }}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: {PURPLE} !important;
    border-bottom: 2px solid {PURPLE} !important;
    background: transparent !important;
}}
div[data-baseweb="tab-panel"] {{ padding: 0 !important; background: {BG} !important; }}
div[data-baseweb="tab-highlight"] {{ display: none !important; }}
.stPlotlyChart {{ border-radius: 12px; overflow: hidden; }}
.stMultiSelect span[data-baseweb="tag"] {{ background: {PURPLE} !important; }}
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

def base(h=300):
    return dict(
        paper_bgcolor=BG1, plot_bgcolor=BG1,
        font=dict(family="Inter, sans-serif", color=T3, size=12),
        margin=dict(l=12, r=12, t=42, b=12), height=h,
        xaxis=dict(showgrid=False, tickfont=dict(size=11, color=T4),
                   linecolor=BORDER, zeroline=False),
        yaxis=dict(gridcolor=BG2, tickfont=dict(size=11, color=T4),
                   linecolor=BORDER, zeroline=False),
        legend=dict(font=dict(size=11, color=T2), bgcolor="rgba(0,0,0,0)",
                    orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hoverlabel=dict(bgcolor=BG1, bordercolor=BORDER2,
                        font=dict(size=12, color=T1, family="Inter")),
    )

PAD = "padding: 36px 52px 52px;"

def h1(text): return f'<div style="font-family:Syne,sans-serif;font-size:26px;font-weight:700;color:{T1};margin-bottom:4px;">{text}</div>'
def sub(text): return f'<div style="font-size:13px;color:{T3};margin-bottom:28px;">{text}</div>'
def sec_label(text, color=T3): return f'<div style="font-size:11px;font-weight:600;letter-spacing:.07em;text-transform:uppercase;color:{color};margin-bottom:12px;margin-top:4px;">{text}</div>'

def kpi_html(label, val, vsub, pill_text="", pill_color=GREEN):
    pill = f'<span style="display:inline-block;background:rgba(5,150,105,0.1);color:{pill_color};font-size:10px;font-weight:700;padding:3px 9px;border-radius:20px;margin-top:6px;">{pill_text}</span>' if pill_text else ""
    return f"""<div style="background:{BG1};border:1px solid {BORDER};border-radius:12px;padding:18px 20px;height:100%;">
      <div style="font-size:10px;color:{T4};font-weight:600;text-transform:uppercase;letter-spacing:.07em;margin-bottom:8px;">{label}</div>
      <div style="font-family:Syne,sans-serif;font-size:24px;font-weight:700;color:{T1};line-height:1;margin-bottom:4px;">{val}</div>
      <div style="font-size:11px;color:{T4};">{vsub}</div>{pill}</div>"""

def info_block(title, desc, color=PURPLE):
    return f"""<div style="border-left:3px solid {color};background:{BG1};border-radius:0 10px 10px 0;padding:12px 16px;margin-bottom:9px;">
      <div style="font-size:13px;font-weight:600;color:{T1};margin-bottom:3px;">{title}</div>
      <div style="font-size:12px;color:{T3};line-height:1.55;">{desc}</div></div>"""

def hyp_html(code, title, stat):
    return f"""<div style="display:flex;align-items:flex-start;gap:14px;background:{BG1};border:1px solid {BORDER};border-radius:12px;padding:16px 18px;margin-bottom:10px;">
      <span style="font-family:Syne,sans-serif;font-size:13px;font-weight:700;color:{PURPLE};min-width:28px;">{code}</span>
      <div style="flex:1;">
        <div style="font-size:14px;font-weight:500;color:{T1};margin-bottom:4px;">{title}</div>
        <div style="font-size:12px;color:{T4};">{stat}</div>
      </div>
      <span style="background:rgba(5,150,105,0.1);color:{GREEN};font-size:11px;font-weight:700;padding:4px 12px;border-radius:20px;white-space:nowrap;">Supported ✔</span>
    </div>"""

def gap_bar(label, pct, color, note, bold=False):
    fw = "700" if bold else "400"
    lc = CORAL if bold else T2
    nc = CORAL if bold else GREEN
    return f"""<div style="margin-bottom:16px;">
      <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px;">
        <span style="font-weight:{fw};color:{lc};">{label}</span>
        <span style="font-weight:700;color:{nc};">{note}</span>
      </div>
      <div style="height:10px;background:{BG2};border-radius:5px;overflow:hidden;">
        <div style="width:{pct}%;height:100%;background:{color};border-radius:5px;"></div>
      </div></div>"""

def tl_item(yr, title, desc, color=T4, is_launch=False):
    yrc = CORAL if is_launch else T4
    tc  = CORAL if is_launch else T1
    bdr = f"3px solid {CORAL}" if is_launch else f"1px solid {BORDER}"
    bg  = "background:rgba(220,72,72,0.04);" if is_launch else ""
    return f"""<div style="border-left:{bdr};padding:12px 16px;margin-bottom:14px;border-radius:0 10px 10px 0;{bg}">
      <div style="font-size:11px;color:{yrc};font-weight:600;margin-bottom:3px;">{yr}</div>
      <div style="font-size:13px;font-weight:600;color:{tc};margin-bottom:4px;">{title}</div>
      <div style="font-size:12px;color:{T3};line-height:1.6;">{desc}</div></div>"""

def coef_card(name, val, stat, note, color=BLUE):
    return f"""<div style="background:{BG1};border:1px solid {BORDER};border-left:3px solid {color};border-radius:0 10px 10px 0;padding:14px 16px;margin-bottom:10px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
        <span style="font-size:12px;font-weight:600;color:{T3};">{name}</span>
        <span style="font-family:Syne,sans-serif;font-size:20px;font-weight:700;color:{color};">{val}</span>
      </div>
      <div style="font-size:11px;color:{T4};margin-bottom:3px;">{stat}</div>
      <div style="font-size:12px;color:{T2};">{note}</div></div>"""

# ── HERO ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:linear-gradient(135deg,#F8F7FF 0%,#EEF2FF 50%,#F0FDF4 100%);
            padding:52px 52px 44px;border-bottom:1px solid {BORDER};">
  <div style="display:inline-block;background:rgba(107,95,212,0.1);border:1px solid rgba(107,95,212,0.25);
              color:{PURPLE};font-size:11px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
              padding:5px 14px;border-radius:20px;margin-bottom:18px;">
    IBR Final Report · SP Jain MGB Class of 2025
  </div>
  <div style="font-family:Syne,sans-serif;font-size:clamp(26px,3vw,42px);font-weight:800;color:{T1};line-height:1.2;margin-bottom:14px;">
    Impact of <span style="color:{PURPLE};">PayNow-UPI</span> on<br>SME Financial Efficiency
  </div>
  <div style="font-size:15px;color:{T2};max-width:640px;line-height:1.75;margin-bottom:26px;">
    A Singapore–India corridor study examining transaction speed, cost reduction, transparency,
    and digital readiness — 6-year secondary dataset (2019–2024) · 15 A/A+-grade sources · OLS bivariate regression.
  </div>
  <div style="font-size:13px;color:{T3};display:flex;flex-wrap:wrap;gap:6px 18px;">
    <span><strong style="color:{T2};">Parinita Jain</strong></span>
    <span>MS25DBM004</span>
    <span>MGB Class of 2025</span>
    <span>SP Jain School of Global Management</span>
    <span>Mentor: Mr S. Vittal · Reviewer: Ms Farah Naaz</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── STAT STRIP ────────────────────────────────────────────────────────────────
stats = [
    ("+202.6%", "SME Efficiency Change",    "0.263 → 0.796 index",      GREEN),
    ("82.9%",   "Cost Reduction",           "6.4% → 1.1% of deal value", TEAL),
    ("3.5 days","Days Saved / Txn",         "SWIFT T+2-5 → ~4 minutes",  T1),
    ("~42 days","Working Capital Freed",    "Per year · 12 payments",    AMBER),
    ("USD 25K", "Annual Saving",            "For a USD 500K SME",        BLUE),
    ("+36.1%",  "Digital Readiness Growth", "vs 159-199% infrastructure",CORAL),
]
cols = st.columns(6)
for col, (val, lbl, vsub, color) in zip(cols, stats):
    with col:
        st.markdown(f"""
        <div style="padding:18px 16px;background:{BG1};border-right:1px solid {BORDER};border-bottom:1px solid {BORDER};">
          <div style="font-size:10px;color:{T4};font-weight:600;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px;">{lbl}</div>
          <div style="font-family:Syne,sans-serif;font-size:22px;font-weight:700;color:{color};line-height:1;">{val}</div>
          <div style="font-size:11px;color:{T4};margin-top:3px;">{vsub}</div>
        </div>""", unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tabs = st.tabs(["📊  Overview","📈  Trends","⚖️  SWIFT vs PayNow","🔢  Regression","🔍  Readiness Gap","📅  Milestones"])

# ════════════════════════════ TAB 1 — OVERVIEW ═══════════════════════════════
with tabs[0]:
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
    st.markdown(h1("Research Overview"), unsafe_allow_html=True)
    st.markdown(sub("Natural pre/post experiment · PayNow-UPI launch February 2023 · 15 A/A+-grade sources"), unsafe_allow_html=True)

    c1,c2,c3 = st.columns(3)
    for col, (lbl, val, vsub, pill, pc) in zip([c1,c2,c3,c1,c2,c3],[
        ("SME Financial Efficiency", "+202.6%", "Pre avg 0.263 → post avg 0.796", "Largest change", GREEN),
        ("Transaction Cost",         "−82.9%",  "6.4% → 1.1% · meets SDG 10.c target", "Below SDG target", GREEN),
        ("Settlement Speed",         "3.5 days","Saved per txn vs SWIFT T+2–T+5", "~4 min post-launch", GREEN),
        ("Working Capital Freed",    "~42 days","Annual · 3.5 days × 12 payments", "Per year", AMBER),
        ("Annual Net Saving",        "~USD 25K","Direct margin gain · USD 500K SME", "Intensive margin", BLUE),
        ("Digital Readiness",        "+36.1%",  "vs 159–199% infra improvement", "Binding constraint", CORAL),
    ]):
        with col:
            st.markdown(kpi_html(lbl,val,vsub,pill,pc), unsafe_allow_html=True)
            st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # FinEff trend
    fig1 = go.Figure()
    fig1.add_vrect(x0=2022.9, x1=2024.15, fillcolor="rgba(107,95,212,0.06)", line_width=0,
                   annotation_text="Post-launch", annotation_position="top right",
                   annotation_font=dict(size=11, color=PURPLE))
    fig1.add_trace(go.Scatter(
        x=df["Year"], y=df["FinEff"], mode="lines+markers",
        line=dict(color=PURPLE, width=3),
        marker=dict(size=9, color=PURPLE, line=dict(color=BG1, width=2)),
        fill="tozeroy", fillcolor="rgba(107,95,212,0.07)",
        hovertemplate="<b>%{x}</b><br>SME FinEff Index: <b>%{y:.3f}</b><extra></extra>",
    ))
    l1 = base(260); l1["yaxis"]["range"] = [0,1]
    l1["title"] = dict(text="SME Financial Efficiency Index — 2019 to 2024", font=dict(size=13,color=T2), x=0.01)
    fig1.update_layout(**l1, showlegend=False)
    st.plotly_chart(fig1, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig2 = go.Figure(go.Bar(
            x=df["Year"], y=df["Cost"],
            marker_color=[CORAL if y<2023 else TEAL for y in df["Year"]],
            marker_cornerradius=6,
            hovertemplate="<b>%{x}</b><br>Cost: %{y:.2f}% of deal value<extra></extra>",
        ))
        fig2.add_hline(y=3, line_dash="dash", line_color=AMBER, line_width=1.2,
                       annotation_text="SDG 10.c target (≤3%)",
                       annotation_font=dict(size=10,color=AMBER))
        l2 = base(250); l2["yaxis"]["ticksuffix"]="%" ; l2["yaxis"]["range"]=[0,8.5]
        l2["title"] = dict(text="Transaction cost (% of deal value)", font=dict(size=13,color=T2), x=0.01)
        fig2.update_layout(**l2, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    with c2:
        fig3 = go.Figure()
        for name, col, vals, dash in [
            ("Transparency",    BLUE,  df["Transparency"], "solid"),
            ("Interoperability",AMBER, df["Interop"],      "dot"),
            ("Digital Readiness",CORAL,df["DigReady"],     "longdash"),
        ]:
            fig3.add_trace(go.Scatter(x=df["Year"], y=vals, name=name,
                line=dict(color=col, width=2.5, dash=dash), mode="lines+markers",
                marker=dict(size=7, color=col, line=dict(color=BG1,width=1.5)),
                hovertemplate=f"<b>%{{x}}</b><br>{name}: %{{y:.2f}}<extra></extra>"))
        l3 = base(250); l3["yaxis"]["range"]=[0,1]
        l3["title"] = dict(text="Infrastructure indices vs digital readiness", font=dict(size=13,color=T2), x=0.01)
        fig3.update_layout(**l3)
        st.plotly_chart(fig3, use_container_width=True)

    c3, c4 = st.columns(2)
    pie_labels = ["Correspondent fees","FX spread","KYC/AML","Reconciliation"]
    with c3:
        fig4 = go.Figure(go.Pie(
            labels=pie_labels, values=[3.00,1.75,0.65,0.40], hole=0.58,
            marker_colors=[CORAL,"#FB923C",AMBER,"#E879F9"],
            textfont=dict(size=11), hovertemplate="%{label}: <b>%{value:.2f}%</b><extra></extra>",
        ))
        l4 = base(260); l4["title"]=dict(text="SWIFT cost breakdown (~6.5% total)",font=dict(size=13,color=T2),x=0.01)
        fig4.update_layout(**l4, showlegend=True,
            annotations=[dict(text="SWIFT<br><b>6.5%</b>",x=0.5,y=0.5,font=dict(size=13,color=T1),showarrow=False)])
        st.plotly_chart(fig4, use_container_width=True)

    with c4:
        fig5 = go.Figure(go.Pie(
            labels=pie_labels, values=[0.05,0.75,0.25,0.05], hole=0.58,
            marker_colors=[GREEN,TEAL,BLUE,PURPLE],
            textfont=dict(size=11), hovertemplate="%{label}: <b>%{value:.2f}%</b><extra></extra>",
        ))
        l5 = base(260); l5["title"]=dict(text="PayNow-UPI cost breakdown (~1.1% total)",font=dict(size=13,color=T2),x=0.01)
        fig5.update_layout(**l5, showlegend=True,
            annotations=[dict(text="PayNow<br><b>1.1%</b>",x=0.5,y=0.5,font=dict(size=13,color=T1),showarrow=False)])
        st.plotly_chart(fig5, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════ TAB 2 — TRENDS ════════════════════════════════
with tabs[1]:
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
    st.markdown(h1("Variable Trends & UPI Growth"), unsafe_allow_html=True)
    st.markdown(sub("Select variables · hover for exact values · dashed line = PayNow-UPI launch Feb 2023"), unsafe_allow_html=True)

    opts = st.multiselect("Variables to display",
        ["FinEff Index","Speed (days saved)","Transaction Cost %","Transparency","Interoperability","Digital Readiness"],
        default=["FinEff Index","Transaction Cost %","Digital Readiness"])

    smap = {
        "FinEff Index":       (df["FinEff"],       PURPLE, "solid"),
        "Speed (days saved)": (df["Speed"],        GREEN,  "solid"),
        "Transaction Cost %": (df["Cost"],         CORAL,  "dash"),
        "Transparency":       (df["Transparency"], BLUE,   "solid"),
        "Interoperability":   (df["Interop"],      AMBER,  "dot"),
        "Digital Readiness":  (df["DigReady"],     TEAL,   "longdash"),
    }
    fig6 = go.Figure()
    fig6.add_vline(x=2023, line_dash="dash", line_color=CORAL, line_width=1.5, opacity=0.6,
                   annotation_text="PayNow-UPI launch (Feb 2023)",
                   annotation_position="top left", annotation_font=dict(size=11,color=CORAL))
    for name in opts:
        v,c,d = smap[name]
        fig6.add_trace(go.Scatter(x=df["Year"], y=v, name=name,
            line=dict(color=c,width=2.5,dash=d), mode="lines+markers",
            marker=dict(size=8,color=c,line=dict(color=BG1,width=2)),
            hovertemplate=f"<b>%{{x}}</b><br>{name}: %{{y:.3f}}<extra></extra>"))
    l6 = base(360); l6["title"]=dict(text="All variables — 2019 to 2024",font=dict(size=14,color=T2),x=0.01)
    fig6.update_layout(**l6)
    st.plotly_chart(fig6, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig7 = go.Figure(go.Bar(
            x=["2016","2018","2020","2022","Jun'23","Oct'24"], y=[0.0001,0.3,2.2,7.0,9.3,15.5],
            marker_color=["#E5E3DC","#D1CFC5","#9CA3AF",GREEN,TEAL,BLUE],
            marker_cornerradius=6,
            text=["~0","0.3B","2.2B","7.0B","9.3B","15.5B"], textposition="outside",
            textfont=dict(size=11,color=T3),
            hovertemplate="<b>%{x}</b><br>%{y:.2f}B txns/month<extra></extra>"))
        l7 = base(280); l7["yaxis"]["ticksuffix"]="B"
        l7["title"]=dict(text="India UPI monthly transaction volume",font=dict(size=13,color=T2),x=0.01)
        fig7.update_layout(**l7, showlegend=False)
        st.plotly_chart(fig7, use_container_width=True)

    with c2:
        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(
            x=[2016,2018,2020,2022,2023,2024], y=[1,4,20,40,49,49],
            line=dict(color=PURPLE,width=3), fill="tozeroy",
            fillcolor="rgba(107,95,212,0.08)", mode="lines+markers",
            marker=dict(size=8,color=PURPLE,line=dict(color=BG1,width=2)),
            hovertemplate="<b>%{x}</b><br>India global RTP share: %{y}%<extra></extra>"))
        l8 = base(280); l8["yaxis"]["ticksuffix"]="%"; l8["yaxis"]["range"]=[0,60]
        l8["title"]=dict(text="India's share of global real-time payment volume",font=dict(size=13,color=T2),x=0.01)
        fig8.update_layout(**l8, showlegend=False)
        st.plotly_chart(fig8, use_container_width=True)

    fig9 = go.Figure()
    mlabels = ["FinEff Index","Cost (%)","Transparency","Interoperability","Dig. Readiness"]
    fig9.add_trace(go.Bar(name="Pre-launch avg 2019–22", x=mlabels, y=[0.263,6.425,0.270,0.218,0.368],
        marker_color=BG2, marker_cornerradius=5,
        marker_line=dict(color=BORDER2,width=1),
        hovertemplate="Pre-launch — %{x}: %{y:.3f}<extra></extra>"))
    fig9.add_trace(go.Bar(name="Post-launch avg 2023–24", x=mlabels, y=[0.796,1.100,0.700,0.650,0.500],
        marker_color=PURPLE, marker_cornerradius=5,
        hovertemplate="Post-launch — %{x}: %{y:.3f}<extra></extra>"))
    l9 = base(280); l9["title"]=dict(text="Pre vs post-launch averages across all variables",font=dict(size=13,color=T2),x=0.01)
    fig9.update_layout(**l9, barmode="group")
    st.plotly_chart(fig9, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════ TAB 3 — COMPARE ═══════════════════════════════
with tabs[2]:
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
    st.markdown(h1("SWIFT vs PayNow-UPI"), unsafe_allow_html=True)
    st.markdown(sub("BIS (2021) four-friction framework: cost, speed, transparency, access · Source: BIS 2021, World Bank 2023, MAS 2023, J.P. Morgan 2025"), unsafe_allow_html=True)

    rows = [
        ("Settlement speed",             "T+2 to T+5 days (avg 3.5 days)",    "~4 minutes (~0.003 days)"),
        ("Total transaction cost",       "6.1–6.8% of deal value",             "1.0–1.2% of deal value"),
        ("Correspondent fees",           "2.5–3.5% of deal value",             "0.0–0.1%"),
        ("FX spread",                    "1.5–2.0%",                           "0.7–0.8%"),
        ("KYC / AML compliance",         "0.5–0.8% — external, manual",        "0.2–0.3% — built-in to rail"),
        ("Reconciliation overhead",      "0.3–0.5% — manual back-office",      "0.0–0.1% — ISO 20022 STP"),
        ("Annual working capital lock-up","~42 days per year",                  "~0.03 days per year"),
        ("Min viable invoice",           "> USD 5,000 (fixed cost penalty)",    "Any value — near-zero marginal cost"),
        ("Settlement transparency",      "Fragmented — no real-time tracking",  "Real-time · ISO 20022 structured"),
        ("Onboarding",                   "Correspondent banking relationship",  "VPA-based · KYC/AML built in"),
        ("SME B2B scalability",          "Low — fixed cost disadvantages SMEs","High (pending INR cap increase)"),
        ("SDG 10.c compliance (≤3%)",    "No — 6.5%, exceeds by 2.2×",         "Yes — 1.1%, 64% below target"),
    ]
    tbl = f'<div style="background:{BG1};border:1px solid {BORDER};border-radius:14px;overflow:hidden;margin-bottom:24px;">'
    tbl += f'<table style="width:100%;border-collapse:collapse;">'
    tbl += f'<thead><tr style="border-bottom:2px solid {BORDER2};background:{BG2};">'
    tbl += f'<th style="padding:12px 16px;font-size:11px;color:{T3};font-weight:600;text-transform:uppercase;letter-spacing:.05em;text-align:left;">Dimension</th>'
    tbl += f'<th style="padding:12px 16px;font-size:11px;color:{CORAL};font-weight:600;text-transform:uppercase;letter-spacing:.05em;text-align:left;">⛔ SWIFT</th>'
    tbl += f'<th style="padding:12px 16px;font-size:11px;color:{GREEN};font-weight:600;text-transform:uppercase;letter-spacing:.05em;text-align:left;">✅ PayNow-UPI</th>'
    tbl += '</tr></thead><tbody>'
    for i,(dim,sw,pn) in enumerate(rows):
        bg = BG2 if i%2==0 else BG1
        tbl += f'<tr style="background:{bg};">'
        tbl += f'<td style="padding:11px 16px;font-size:13px;color:{T2};">{dim}</td>'
        tbl += f'<td style="padding:11px 16px;font-size:13px;color:{CORAL};font-weight:500;">{sw}</td>'
        tbl += f'<td style="padding:11px 16px;font-size:13px;color:{GREEN};font-weight:500;">{pn}</td>'
        tbl += '</tr>'
    tbl += '</tbody></table></div>'
    st.markdown(tbl, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig10 = go.Figure()
        cats = ["Speed","Cost reduction","Transparency","Interoperability","SME Access"]
        fig10.add_trace(go.Scatterpolar(r=[10,20,25,22,30]+[10], theta=cats+[cats[0]],
            fill="toself", name="SWIFT", line=dict(color=CORAL),
            fillcolor="rgba(220,72,72,0.07)"))
        fig10.add_trace(go.Scatterpolar(r=[99,83,75,65,70]+[99], theta=cats+[cats[0]],
            fill="toself", name="PayNow-UPI", line=dict(color=GREEN),
            fillcolor="rgba(5,150,105,0.07)"))
        fig10.update_layout(
            polar=dict(bgcolor=BG1,
                radialaxis=dict(range=[0,110],gridcolor=BORDER,tickfont=dict(size=9,color=T4)),
                angularaxis=dict(gridcolor=BORDER,tickfont=dict(size=11,color=T2))),
            paper_bgcolor=BG1, height=320, showlegend=True,
            font=dict(family="Inter",color=T3),
            legend=dict(bgcolor="rgba(0,0,0,0)",font_size=12,font_color=T2),
            title=dict(text="Capability radar (0–100 scale)",font=dict(size=13,color=T2),x=0.01),
            margin=dict(l=50,r=50,t=50,b=10))
        st.plotly_chart(fig10, use_container_width=True)

    with c2:
        fig11 = go.Figure(go.Waterfall(
            orientation="v", measure=["absolute","relative","relative","relative","relative","total"],
            x=["SWIFT total","Corresp. fees","FX spread","KYC/AML","Reconciliation","PayNow-UPI"],
            y=[6.50,-2.95,-0.975,-0.425,-0.35,0],
            connector=dict(line=dict(color=BORDER2)),
            decreasing=dict(marker=dict(color=GREEN)),
            increasing=dict(marker=dict(color=CORAL)),
            totals=dict(marker=dict(color=PURPLE)),
            hovertemplate="%{x}: %{y:.3f}%<extra></extra>"))
        l11 = base(320); l11["yaxis"]["ticksuffix"]="%"
        l11["title"]=dict(text="Cost waterfall: SWIFT → PayNow-UPI",font=dict(size=13,color=T2),x=0.01)
        fig11.update_layout(**l11, showlegend=False)
        st.plotly_chart(fig11, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════ TAB 4 — REGRESSION ════════════════════════════
with tabs[3]:
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
    st.markdown(h1("OLS Regression Results"), unsafe_allow_html=True)
    st.markdown(sub("Bivariate OLS · n=6 · df=4 · Python scipy.stats.linregress · *** p<0.001 · * p<0.05"), unsafe_allow_html=True)

    c1, c2 = st.columns([3,2])
    with c1:
        fig12 = go.Figure(go.Bar(
            y=["Transaction speed","Transaction cost","Transparency","Interoperability","Digital readiness"],
            x=[0.9968,0.9969,0.9879,0.9882,0.8190], orientation="h",
            marker_color=[BLUE,BLUE,BLUE,BLUE,CORAL], marker_cornerradius=5,
            text=["R²=0.9968","R²=0.9969","R²=0.9879","R²=0.9882","R²=0.819"],
            textposition="inside", textfont=dict(color="white",size=12),
            hovertemplate="<b>%{y}</b><br>R² = %{x:.4f}<extra></extra>"))
        l12 = base(280)
        l12["xaxis"] = dict(range=[0.75,1.02],gridcolor=BG2,tickfont=dict(size=11,color=T4))
        l12["yaxis"] = dict(showgrid=False,tickfont=dict(size=12,color=T2))
        l12["title"]=dict(text="R² by predictor — blue=infrastructure · red=digital readiness",font=dict(size=13,color=T2),x=0.01)
        fig12.update_layout(**l12, showlegend=False)
        st.plotly_chart(fig12, use_container_width=True)

        fig13 = go.Figure()
        fig13.add_trace(go.Scatter(
            x=df["DigReady"], y=df["FinEff"], mode="markers+text",
            text=[str(y) for y in df["Year"]], textposition="top center",
            textfont=dict(size=10,color=T3),
            marker=dict(size=14,
                color=[BG2,BG2,BG2,BG2,PURPLE,PURPLEL],
                line=dict(color=[BORDER2,BORDER2,BORDER2,BORDER2,PURPLE,PURPLEL],width=2)),
            hovertemplate="<b>%{text}</b><br>DigReady: %{x:.2f}<br>FinEff: %{y:.3f}<extra></extra>"))
        xr = np.linspace(0.30,0.55,50)
        fig13.add_trace(go.Scatter(x=xr, y=0.14880+0.31076*xr, mode="lines",
            line=dict(color=PURPLE,dash="dash",width=1.5), hoverinfo="skip"))
        l13 = base(260)
        l13["xaxis"]["title"]=dict(text="Digital Readiness Index",font=dict(size=12,color=T3))
        l13["yaxis"]["title"]=dict(text="FinEff Index",font=dict(size=12,color=T3))
        l13["title"]=dict(text="Scatter: digital readiness vs efficiency (pre=grey · post=purple)",font=dict(size=13,color=T2),x=0.01)
        fig13.update_layout(**l13, showlegend=False)
        st.plotly_chart(fig13, use_container_width=True)

    with c2:
        st.markdown(sec_label("Regression Coefficients"), unsafe_allow_html=True)
        for name,val,stat,note,color in [
            ("β₁ Transaction Speed","+0.152","R²=0.9968 · p<0.001 ***","Each day saved → +0.152 FinEff",BLUE),
            ("β₂ Transaction Cost","−0.100","R²=0.9969 · p<0.001 ***","Highest R² of all variables",TEAL),
            ("β₃ Transparency","+1.217","R²=0.9879 · p<0.001 ***","ISO 20022 STP effect",BLUE),
            ("β₄ Interoperability","+1.210","R²=0.9882 · p<0.001 ***","Near-identical to transparency",BLUE),
            ("β₅ Digital Readiness","+3.237","R²=0.8190 · p=0.013 *","Largest coeff · lowest R² · gap",CORAL),
            ("Parsimony Model R²","0.9984","Speed + DigReady · adj-R²=0.9973","99.73% variance explained",AMBER),
        ]:
            st.markdown(coef_card(name,val,stat,note,color), unsafe_allow_html=True)

    st.markdown(f"<br>{sec_label('Hypothesis Scorecard — all four supported')}", unsafe_allow_html=True)
    for code,title,stat in [
        ("H1","Faster settlement speed → higher SME financial efficiency","β₁=+0.152 · R²=0.997 · p<0.001 · 3.5 days saved/txn · WC freed ~42 days/yr · FinEff +202.6%"),
        ("H2","Lower transaction cost → higher SME financial efficiency","β₂=−0.100 · R²=0.997 · p<0.001 · cost −82.9% · ~USD 25K/yr saving · meets SDG 10.c"),
        ("H3","Greater transparency & interoperability → higher efficiency","β₃=+1.217 · β₄=+1.210 · R²≈0.988 · p<0.001 · Transparency +159.3% · Interop +198.9%"),
        ("H4","Digital readiness mediates the infrastructure–efficiency relationship","β₅=+3.237 · R²=0.819 · p=0.013 · readiness +36.1% vs infra +159–199% · interaction β₆=−0.286"),
    ]:
        st.markdown(hyp_html(code,title,stat), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════ TAB 5 — GAP ═══════════════════════════════════
with tabs[4]:
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
    st.markdown(h1("The Digital Readiness Gap"), unsafe_allow_html=True)
    st.markdown(sub('"Infrastructure Without Readiness Is a Road Without Drivers" — Jain 2025 · Source: Frontiers 2021, PwC 2024'), unsafe_allow_html=True)

    st.markdown(f'<div style="background:{BG1};border:1px solid {BORDER};border-radius:14px;padding:24px 28px;margin-bottom:24px;">', unsafe_allow_html=True)
    st.markdown(sec_label("Relative improvement (%) — 2019 to 2024"), unsafe_allow_html=True)
    for lbl,pct,col,note,bold in [
        ("Transaction speed (0 → 3.497 days saved)",100,GREEN,"Max improvement",False),
        ("Transaction cost reduction",83,TEAL,"−82.9%",False),
        ("Payment transparency index",100,BLUE,"+159.3%",False),
        ("Technical interoperability index",100,PURPLE,"+198.9%",False),
        ("SME digital readiness ← THE BINDING CONSTRAINT",36,CORAL,"+36.1% only",True),
    ]:
        st.markdown(gap_bar(lbl,pct,col,note,bold), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        fig14 = go.Figure(go.Scatterpolar(
            r=[100,83,80,100,36]+[100],
            theta=["Speed","Cost","Transparency","Interoperability","Digital Readiness"]+["Speed"],
            fill="toself", line=dict(color=PURPLE),
            fillcolor="rgba(107,95,212,0.1)",
            hovertemplate="%{theta}: %{r}%<extra></extra>"))
        fig14.update_layout(
            polar=dict(bgcolor=BG1,
                radialaxis=dict(range=[0,110],gridcolor=BORDER,tickfont=dict(size=9,color=T4)),
                angularaxis=dict(gridcolor=BORDER,tickfont=dict(size=11,color=T2))),
            paper_bgcolor=BG1, height=300, showlegend=False,
            font=dict(family="Inter",color=T3),
            title=dict(text="Relative improvement — readiness gap visible",font=dict(size=13,color=T2),x=0.01),
            margin=dict(l=50,r=50,t=50,b=10))
        st.plotly_chart(fig14, use_container_width=True)

    with c2:
        fig15 = go.Figure()
        fig15.add_trace(go.Scatter(x=df["Year"], y=df["DigReady"], name="Actual readiness",
            line=dict(color=CORAL,width=3), mode="lines+markers",
            marker=dict(size=8,color=CORAL,line=dict(color=BG1,width=2)),
            hovertemplate="<b>%{x}</b><br>Digital Readiness: %{y:.2f}<extra></extra>"))
        fig15.add_trace(go.Scatter(x=[2024,2025,2026], y=[0.52,0.61,0.70],
            name="Projected (if policy acts)",
            line=dict(color=AMBER,width=2,dash="dash"), mode="lines+markers",
            marker=dict(size=7,symbol="diamond",color=AMBER,line=dict(color=BG1,width=2)),
            hovertemplate="<b>%{x}</b><br>Projected: %{y:.2f}<extra></extra>"))
        l15 = base(300); l15["yaxis"]["range"]=[0.2,0.8]
        l15["title"]=dict(text="Digital readiness trend & policy projection",font=dict(size=13,color=T2),x=0.01)
        fig15.update_layout(**l15)
        st.plotly_chart(fig15, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown(sec_label("✅ Boon — efficiency gains",GREEN), unsafe_allow_html=True)
        for t,d in [
            ("~80% cost reduction","~USD 25K/year saving · direct net margin improvement · SDG 10.c compliant"),
            ("42 working capital days freed annually","3.5 days × 12 payments · enables JIT procurement"),
            ("Credit history generation","Every txn creates verifiable financial record — enables SME credit access"),
            ("Levels the playing field","Fixed-cost SWIFT penalty reversed — small invoices now economical"),
            ("Intensive margin effect","Enables more txns, not just cheaper ones: weekly vs monthly B2B payments"),
            ("GDP contribution","Digital formalisation → estimated +6% India GDP contribution"),
        ]:
            st.markdown(info_block(t,d,GREEN), unsafe_allow_html=True)

    with c4:
        st.markdown(sec_label("⚠️ Bane — risks to manage",CORAL), unsafe_allow_html=True)
        for t,d in [
            ("INR 60,000/day transaction cap","Hard cap limits B2B applicability — most SME invoices exceed SGD 1,000"),
            ("Payment irreversibility","No recall mechanism · asymmetric fraud risk · real-time = no undo"),
            ("Digital literacy gaps","Rural/low-tech SMEs excluded — Frontiers (2021) TAM framework confirmed"),
            ("Systemic concentration risk","BIS (2023): single-point failure could disrupt entire SG-India corridor"),
            ("FX spread remains (0.7–0.8%)","Not fully eliminated — persistent structural friction"),
            ("Policy negotiation lag","Cap increase requires bilateral MAS-RBI agreement — not technical"),
        ]:
            st.markdown(info_block(t,d,CORAL), unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════ TAB 6 — MILESTONES ════════════════════════════
with tabs[5]:
    st.markdown(f'<div style="{PAD}">', unsafe_allow_html=True)
    st.markdown(h1("Key Milestones & Sources"), unsafe_allow_html=True)
    st.markdown(sub("From demonetisation (2016) through PayNow-UPI launch (Feb 2023) to global expansion (2024)"), unsafe_allow_html=True)

    c1, c2 = st.columns([3,2])
    with c1:
        st.markdown(sec_label("Timeline"), unsafe_allow_html=True)
        st.markdown(tl_item("2016","Demonetisation & UPI launch","86% of Indian currency withdrawn 8 Nov 2016. UPI launched by NPCI April 2016 — 93,000 txns in first month. Digital volumes +43% in Nov-Dec 2016. Critical behavioural foundation for PayNow-UPI.",PURPLE), unsafe_allow_html=True)
        st.markdown(tl_item("2017","PayNow launched in Singapore","MAS launches real-time domestic payment system. Adopted by nearly all banking customers by 2022. Foundation of Singapore-side corridor rails.",BLUE), unsafe_allow_html=True)
        st.markdown(tl_item("2020","COVID-19 accelerates digital adoption","UPI hits ~2.2B transactions/month. India ~20% of global real-time payment volume. Contactless payments normalised. FinEff baseline: 0.248.",GREEN), unsafe_allow_html=True)
        st.markdown(tl_item("2021","BIS & OMFIF framework papers","BIS (2021) defines four cross-border frictions: cost, speed, transparency, access. OMFIF identifies ISO 20022 as reconciliation enabler. Conceptual backbone of this study.",AMBER), unsafe_allow_html=True)
        st.markdown(tl_item("2022","UPI reaches 7B transactions/month · India ~40% of global RTP","RuPay credit card on UPI. Merchant QR rollout. Pre-launch FinEff index: 0.276. PayNow-UPI infrastructure finalised.",TEAL), unsafe_allow_html=True)
        st.markdown(tl_item("Feb 2023","★ PayNow-UPI cross-border linkage launched","MAS + RBI connect two domestic rails. ~4 minute settlement. ~80% cost reduction vs SWIFT. First bilateral cross-border real-time system at scale. FinEff jumps 0.276 → 0.776 by year-end.",CORAL,True), unsafe_allow_html=True)
        st.markdown(tl_item("Jun 2023","UPI: 9.3B txns/month · India ~49% of global RTP","India surpasses all countries in real-time payment volume. UPI live in Singapore, UAE, France, Mauritius. Cross-border SME adoption begins.",GREEN), unsafe_allow_html=True)
        st.markdown(tl_item("2024","UPI expands to 7 countries · 15.5B transactions/month","India-UAE (60,000+ merchants). India-France (Eiffel Tower, Feb 2024). FY2024-25: 228.3B annual txns. FinEff index: 0.816.",PURPLE), unsafe_allow_html=True)

    with c2:
        fig16 = go.Figure(go.Pie(
            labels=["Liquidity efficiency (40%)","Cost efficiency (40%)","Adoption proxy (20%)"],
            values=[40,40,20], hole=0.58,
            marker_colors=[PURPLE,GREEN,AMBER],
            textfont=dict(size=11), hovertemplate="%{label}<extra></extra>"))
        l16 = base(240); l16["title"]=dict(text="FinEff Index composition weights",font=dict(size=13,color=T2),x=0.01)
        fig16.update_layout(**l16, showlegend=True,
            annotations=[dict(text="FinEff<br>Index",x=0.5,y=0.5,font=dict(size=12,color=T1),showarrow=False)])
        st.plotly_chart(fig16, use_container_width=True)

        fig17 = go.Figure(go.Pie(
            labels=["Central banks/regulators (4)","Industry reports (4)","Multilateral institutions (3)","Academic journals (3)","Think tanks (1)"],
            values=[4,4,3,3,1], hole=0.55,
            marker_colors=[BLUE,GREEN,PURPLE,AMBER,"#F97316"],
            textfont=dict(size=11), hovertemplate="%{label}: %{value} papers<extra></extra>"))
        l17 = base(240); l17["title"]=dict(text="15 sources by institution type",font=dict(size=13,color=T2),x=0.01)
        fig17.update_layout(**l17, showlegend=True,
            annotations=[dict(text="15<br>sources",x=0.5,y=0.5,font=dict(size=12,color=T1),showarrow=False)])
        st.plotly_chart(fig17, use_container_width=True)

        st.markdown(f'<div style="margin-top:8px;">{sec_label("All 15 A/A+-grade sources")}', unsafe_allow_html=True)
        src_html = "".join(f'<span style="display:inline-block;background:{BG2};border:1px solid {BORDER};color:{T3};font-size:11px;padding:4px 10px;border-radius:20px;margin:3px;">{s}</span>'
                          for s in ["BIS 2021","BIS 2023","IMF 2025","MAS 2023","RBI 2024","World Bank 2023","PwC 2024","OMFIF 2021","MDPI 2024","ResearchGate 2024","Frontiers 2021","Jain 2025","Forbes/LKY 2023","Academic 2025","J.P. Morgan 2025"])
        st.markdown(src_html+"</div>", unsafe_allow_html=True)

        st.markdown(f'<hr style="border:none;border-top:1px solid {BORDER};margin:20px 0;">', unsafe_allow_html=True)
        st.markdown(sec_label("Principal Findings (Chapter 5)"), unsafe_allow_html=True)
        for t,d,c in [
            ("Finding 1: Infrastructure confirmed","All 4 infra variables R²>0.98 · p<0.001 — substantive, measurable improvements.",BLUE),
            ("Finding 2: Digital Preparedness Gap is binding","Readiness +36.1% vs infra +159–199% — highest-leverage policy opportunity.",CORAL),
            ("Finding 3: Pre-PayNow baseline matters","2016 demonetisation → UPI ecosystem = strategic context enabling corridor success.",TEAL),
            ("Finding 4: SMEs benefit disproportionately","Intensive margin: small invoices now economical — reversal of decades of inequality.",GREEN),
            ("Finding 5: Risks must be proactively managed","INR cap, fraud irreversibility, literacy gaps — boon for prepared, bane for others.",AMBER),
        ]:
            st.markdown(info_block(t,d,c), unsafe_allow_html=True)

    st.markdown(f'<div style="margin-top:32px;padding-top:20px;border-top:1px solid {BORDER};text-align:center;font-size:12px;color:{T4};">'
                f'Parinita Jain &nbsp;·&nbsp; MS25DBM004 &nbsp;·&nbsp; MGB Class of 2025 &nbsp;·&nbsp; SP Jain School of Global Management &nbsp;·&nbsp; IBR Final Report 2025'
                f'</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
