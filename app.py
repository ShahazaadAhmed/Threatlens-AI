import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Threatlens AI", page_icon="◈", layout="wide",
                   initial_sidebar_state="expanded")

# ═════════════════════════ THEME ═════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
@property --angle { syntax: '<angle>'; initial-value: 0deg; inherits: false; }

:root {
  --line:#2a2e35; --line-hi:#4a505a; --text:#e8eaed; --muted:#8b919b; --silver:#c9ced6;
  --ease:cubic-bezier(.22,.61,.36,1);
}
html, body, [class*="css"] { font-family:'Space Grotesk',sans-serif; }

/* Streamlit paints its own backgrounds on these layers, so clear them */
.stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"], header[data-testid="stHeader"] {
  background: transparent !important;
}
.stApp {
  background:
    radial-gradient(1100px 600px at 88% -8%, rgba(140,146,158,.20), transparent 60%),
    radial-gradient(900px 500px at -8% 108%, rgba(100,106,116,.16), transparent 60%),
    linear-gradient(135deg,#050506 0%,#15171b 38%,#0a0b0d 68%,#1b1e23 100%) !important;
  background-size:100% 100%,100% 100%,300% 300% !important;
  animation: drift 30s ease-in-out infinite alternate;
}
@keyframes drift { from{background-position:0 0,0 0,0% 50%} to{background-position:0 0,0 0,100% 50%} }
.stApp::before {
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background-image:linear-gradient(rgba(255,255,255,.028) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(255,255,255,.028) 1px,transparent 1px);
  background-size:48px 48px;
  mask-image:radial-gradient(ellipse at center,#000 25%,transparent 80%);
}
.block-container { padding-top:1.6rem; padding-bottom:3rem; max-width:1320px; position:relative; z-index:1; }
.block-container > div > div { animation: rise .7s var(--ease) both; }
@keyframes rise { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:none} }

h1,h2,h3 { letter-spacing:-.02em; }
h3 { font-weight:500; color:var(--silver); font-size:1.05rem !important; margin-top:.4rem; }
[data-testid="stCaptionContainer"] { color:var(--muted); }
hr { border-color:var(--line) !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] { background:linear-gradient(180deg,#0a0b0e 0%,#15171b 100%) !important; border-right:1px solid var(--line); }
[data-testid="stSidebar"] [role="radiogroup"] { gap:4px; }
[data-testid="stSidebar"] [role="radiogroup"] label {
  padding:11px 14px; border-radius:9px; border:1px solid transparent; width:100%;
  transition:background .3s var(--ease),border-color .3s var(--ease),transform .3s var(--ease);
}
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background:rgba(255,255,255,.045); transform:translateX(4px); }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
  background:linear-gradient(90deg,rgba(255,255,255,.10),rgba(255,255,255,.02));
  border-color:var(--line-hi); box-shadow:inset 3px 0 0 var(--silver);
}
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display:none; }

/* ── Hero with rotating gradient border ── */
.hero {
  position:relative; border-radius:16px; padding:30px 34px; margin-bottom:22px; overflow:hidden;
  background:linear-gradient(135deg,rgba(30,33,39,.92),rgba(8,9,11,.95));
  border:1px solid transparent;
  --b:conic-gradient(from var(--angle),#1a1c20,#8b919b,#1a1c20 40%,#1a1c20 60%,#c9ced6,#1a1c20);
  background-image:linear-gradient(135deg,#17191d,#08090b),var(--b);
  background-origin:border-box; background-clip:padding-box,border-box;
  animation:spin 9s linear infinite;
}
@keyframes spin { to{--angle:360deg} }
.hero::after { /* scan line */
  content:""; position:absolute; left:0; right:0; height:90px; top:-90px; pointer-events:none;
  background:linear-gradient(180deg,transparent,rgba(255,255,255,.05),transparent);
  animation:scan 7s ease-in-out infinite;
}
@keyframes scan { 0%{top:-90px} 60%,100%{top:110%} }
.hero .mark { font:500 12px 'JetBrains Mono',monospace; color:var(--muted); letter-spacing:.14em; text-transform:uppercase; }
.hero h1 {
  margin:6px 0 4px; font-size:2.5rem; font-weight:700; padding:0;
  background:linear-gradient(90deg,#fff,#7d838d); -webkit-background-clip:text; background-clip:text; color:transparent;
}
.hero p { color:var(--muted); margin:0 0 16px; max-width:60ch; }
.chip {
  display:inline-flex; align-items:center; gap:7px; padding:5px 12px; margin-right:8px; border-radius:99px;
  font:400 12px 'JetBrains Mono',monospace; color:var(--silver);
  background:rgba(255,255,255,.04); border:1px solid var(--line);
}
.dot { width:7px; height:7px; border-radius:50%; background:#e8eaed; animation:ping 2.4s infinite; }
@keyframes ping { 0%{box-shadow:0 0 0 0 rgba(232,234,237,.55)} 70%,100%{box-shadow:0 0 0 9px rgba(232,234,237,0)} }

/* ── Stat cards ── */
.stat {
  position:relative; padding:18px 20px 12px; border-radius:14px; overflow:hidden;
  background:linear-gradient(160deg,rgba(34,38,44,.85),rgba(11,12,15,.9)); border:1px solid var(--line);
  transition:transform .35s var(--ease),border-color .35s var(--ease),box-shadow .35s var(--ease);
}
.stat:hover { transform:translateY(-4px); border-color:var(--line-hi); box-shadow:0 16px 34px rgba(0,0,0,.6),inset 0 1px 0 rgba(255,255,255,.07); }
.stat .lab { color:var(--muted); font-size:.85rem; }
.stat .val { font:500 2rem 'JetBrains Mono',monospace; color:#fff; margin:2px 0; }
.stat .del { font:400 .78rem 'JetBrains Mono',monospace; color:var(--silver); }
.stat svg { display:block; margin-top:8px; width:100%; height:38px; }
.stat svg path.ln { stroke-dasharray:300; stroke-dashoffset:300; animation:draw 1.6s var(--ease) .3s forwards; }
@keyframes draw { to{stroke-dashoffset:0} }

/* ── Panels, feed, pills ── */
.panel { border:1px solid var(--line); border-radius:14px; padding:16px 18px; background:rgba(14,16,19,.7); backdrop-filter:blur(8px); }
.feed { display:flex; gap:12px; padding:11px 8px; border-bottom:1px solid #1d2026; border-radius:8px; transition:background .3s var(--ease),transform .3s var(--ease); }
.feed:last-child { border:0; }
.feed:hover { background:rgba(255,255,255,.035); transform:translateX(4px); }
.feed .t { font:400 .72rem 'JetBrains Mono',monospace; color:var(--muted); white-space:nowrap; padding-top:3px; }
.feed .m { color:var(--text); font-size:.9rem; line-height:1.35; }
.pill { font:500 .68rem 'JetBrains Mono',monospace; padding:2px 9px; border-radius:99px; border:1px solid var(--line-hi); margin-right:6px; }
.pill.hi { background:#e8eaed; color:#0a0b0d; border-color:#e8eaed; }
.pill.md { color:var(--silver); } .pill.lo { color:var(--muted); border-color:var(--line); }
.case { padding:14px 16px; margin-bottom:10px; border-radius:12px; border:1px solid var(--line);
  background:linear-gradient(160deg,rgba(30,33,39,.8),rgba(10,11,14,.9));
  transition:transform .3s var(--ease),border-color .3s var(--ease); }
.case:hover { transform:translateY(-3px); border-color:var(--line-hi); }
.case b { display:block; margin-bottom:4px; } .case span { color:var(--muted); font-size:.82rem; }
.colhead { font:500 .78rem 'JetBrains Mono',monospace; color:var(--muted); letter-spacing:.1em; text-transform:uppercase; margin-bottom:10px; }

/* ── Native widgets ── */
div.stButton > button {
  background:linear-gradient(180deg,#262a30,#14161a); color:var(--text); border:1px solid var(--line-hi);
  border-radius:9px; padding:.6rem 1rem; transition:all .3s var(--ease);
}
div.stButton > button:hover { background:linear-gradient(180deg,#383c43,#1b1e23); border-color:#9aa0aa; color:#fff; transform:translateY(-2px); box-shadow:0 8px 22px rgba(0,0,0,.5); }
div.stButton > button:active { transform:none; }
[data-testid="stTextInput"] input, [data-baseweb="select"] > div {
  background:#0c0d10 !important; border:1px solid var(--line) !important; border-radius:9px !important; color:var(--text) !important;
  font-family:'JetBrains Mono',monospace; transition:border-color .3s var(--ease),box-shadow .3s var(--ease);
}
[data-testid="stTextInput"] input:focus { border-color:var(--silver) !important; box-shadow:0 0 0 3px rgba(201,206,214,.13); }
[data-testid="stDataFrame"], [data-testid="stPlotlyChart"] { border:1px solid var(--line); border-radius:14px; overflow:hidden; background:rgba(10,11,14,.6); transition:border-color .35s var(--ease); }
[data-testid="stDataFrame"]:hover, [data-testid="stPlotlyChart"]:hover { border-color:var(--line-hi); }

@media (prefers-reduced-motion:reduce) { .stApp,.hero,.hero::after,.dot,.block-container>div>div { animation:none !important; } *{transition:none !important;} }
</style>
""", unsafe_allow_html=True)

# ═════════════════════════ DATA ═════════════════════════
NODES = {  # name: (x, y, type, risk 0-100)
    "evil-login.test": (0, 1.2, "Domain", 82), "sample-malware.test": (-.6, -.2, "Domain", 55),
    "198.51.100.24": (-1.5, .5, "IP", 91), "203.0.113.15": (-1.3, -.9, "IP", 22),
    "DEMO_HASH_001": (1.2, .5, "Hash", 88), "DEMO_HASH_002": (2.0, 1.3, "Hash", 61),
    "Loader.Demo": (.6, -.7, "Malware", 94), "Stealer.Demo": (2.3, -.4, "Malware", 79),
    "Operation Graphite": (1.4, -1.6, "Campaign", 85), "Cluster 07": (-.1, -1.6, "Actor", 70),
}
EDGES = [("evil-login.test", "198.51.100.24"), ("evil-login.test", "DEMO_HASH_001"),
         ("sample-malware.test", "198.51.100.24"), ("sample-malware.test", "203.0.113.15"),
         ("DEMO_HASH_001", "Loader.Demo"), ("DEMO_HASH_002", "Stealer.Demo"),
         ("evil-login.test", "DEMO_HASH_002"), ("Loader.Demo", "Operation Graphite"),
         ("Stealer.Demo", "Operation Graphite"), ("Loader.Demo", "Cluster 07"),
         ("sample-malware.test", "Loader.Demo")]
TYPE_COLOR = {"Domain": "#aeb4be", "IP": "#8b919b", "Hash": "#6f7580",
              "Malware": "#ffffff", "Campaign": "#d4d8de", "Actor": "#5b616b"}

def band(score): return "High" if score >= 75 else "Medium" if score >= 40 else "Low"

IND = pd.DataFrame([[n, t, s, band(s), "Graphite-" + str(i % 3 + 1), f"{i + 1}h ago"]
                    for i, (n, (_, _, t, s)) in enumerate(NODES.items())],
                   columns=["Indicator", "Type", "Score", "Risk", "Cluster", "First seen"])

def neighbours(n): return {b if a == n else a for a, b in EDGES if n in (a, b)}

def navigate(target): st.session_state["page"] = target  # NOTE: not named `go`, that is Plotly's alias

# ═════════════════════════ HELPERS ═════════════════════════
def spark(vals):
    w, h, lo, hi = 200, 38, min(vals), max(vals)
    pts = [(i * w / (len(vals) - 1), h - 4 - (v - lo) / ((hi - lo) or 1) * (h - 10)) for i, v in enumerate(vals)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return (f'<svg viewBox="0 0 {w} {h}" preserveAspectRatio="none"><defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs>'
            f'<path d="{d} L{w},{h} L0,{h} Z" fill="url(#g)"/><path class="ln" d="{d}" fill="none" stroke="#c9ced6" stroke-width="1.6"/></svg>')

def stat(label, value, delta, series):
    return f'<div class="stat"><div class="lab">{label}</div><div class="val">{value}</div><div class="del">▲ {delta} this week</div>{spark(series)}</div>'

def base_layout(h):
    return dict(height=h, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="Space Grotesk", color="#c9ced6"), margin=dict(l=16, r=16, t=16, b=16),
                hoverlabel=dict(bgcolor="#14161a", bordercolor="#4a505a", font_color="#e8eaed"))

def graph_fig(selected=None, h=460):
    near = neighbours(selected) | {selected} if selected else set(NODES)
    fig = go.Figure()
    for a, b in EDGES:
        on = a in near and b in near
        fig.add_trace(go.Scatter(x=[NODES[a][0], NODES[b][0]], y=[NODES[a][1], NODES[b][1]], mode="lines",
                                 line=dict(color="#8b919b" if selected and on else "#363b44", width=2.6 if selected and on else 1.6),
                                 hoverinfo="skip", showlegend=False))
    for n, (x, y, t, r) in NODES.items():
        on, c = n in near, TYPE_COLOR[t]
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers", hoverinfo="skip", showlegend=False,
                                 marker=dict(size=26 + r * .45, color=c, opacity=.12 if on else .03)))
        fig.add_trace(go.Scatter(x=[x], y=[y], mode="markers+text", text=[n], textposition="bottom center",
                                 textfont=dict(color="#c9ced6" if on else "#4a505a", size=12),
                                 marker=dict(size=12 + r * .2, color=c, opacity=1 if on else .25, line=dict(color="#0b0c0f", width=3)),
                                 hovertemplate=f"<b>{n}</b><br>{t} · risk {r}<extra></extra>", showlegend=False))
    fig.update_layout(**base_layout(h), xaxis=dict(visible=False, range=[-2.1, 2.8]), yaxis=dict(visible=False, range=[-2, 1.7]))
    return fig

TABLE_CFG = dict(Score=st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d"))

# ═════════════════════════ SIDEBAR ═════════════════════════
PAGES = ["Overview", "Threat Graph", "Indicator Explorer", "Investigations", "Reports"]
with st.sidebar:
    st.markdown("## ◈ Threatlens AI")
    st.caption("Threat intelligence platform")
    st.divider()
    page = st.radio("Navigation", PAGES, key="page", label_visibility="collapsed")
    st.divider()
    st.markdown('<span class="chip"><span class="dot"></span>Simulated data</span>', unsafe_allow_html=True)
    st.caption("Prototype build")

st.markdown(f"""
<div class="hero">
  <div class="mark">◈ Threatlens AI / {page}</div>
  <h1>{page}</h1>
  <p>Explore intelligence. Discover relationships. Investigate threats.</p>
  <span class="chip"><span class="dot"></span>Feeds online</span>
  <span class="chip">1,284 indicators</span><span class="chip">24 clusters</span>
</div>""", unsafe_allow_html=True)

# ═════════════════════════ PAGES ═════════════════════════
if page == "Overview":
    cols = st.columns(4)
    cards = [("Indicators", "1,284", "86", [3, 5, 4, 7, 6, 9, 8, 11]), ("Threat clusters", "24", "3", [2, 2, 3, 3, 4, 4, 5, 6]),
             ("High risk", "37", "5", [4, 3, 5, 4, 7, 6, 8, 9]), ("Investigations", "12", "2", [1, 2, 2, 3, 3, 5, 4, 6])]
    for c, args in zip(cols, cards):
        c.markdown(stat(*args), unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([3, 2])
    with left:
        st.markdown("### Threat intelligence graph")
        st.plotly_chart(graph_fig(), use_container_width=True)
    with right:
        st.markdown("### Risk distribution")
        counts = IND["Risk"].value_counts().reindex(["High", "Medium", "Low"]).fillna(0)
        bar = go.Figure(go.Bar(x=counts.values, y=counts.index, orientation="h",
                               marker=dict(color=["#e8eaed", "#8b919b", "#444a53"], line=dict(width=0)),
                               hovertemplate="%{y}: %{x}<extra></extra>"))
        bar.update_layout(**base_layout(150), xaxis=dict(visible=False), yaxis=dict(autorange="reversed"), bargap=.35)
        st.plotly_chart(bar, use_container_width=True)
        st.markdown("### Live activity")
        st.markdown("""<div class="panel">
<div class="feed"><span class="t">02m</span><span class="m"><span class="pill hi">HIGH</span>198.51.100.24 contacted evil-login.test</span></div>
<div class="feed"><span class="t">14m</span><span class="m"><span class="pill hi">HIGH</span>Loader.Demo linked to Operation Graphite</span></div>
<div class="feed"><span class="t">41m</span><span class="m"><span class="pill md">MED</span>New domain joined Graphite-2 cluster</span></div>
<div class="feed"><span class="t">1h</span><span class="m"><span class="pill lo">LOW</span>203.0.113.15 re-scored after review</span></div>
</div>""", unsafe_allow_html=True)

    st.markdown("### Recent intelligence")
    st.dataframe(IND.sort_values("Score", ascending=False).head(6), hide_index=True,
                 use_container_width=True, column_config=TABLE_CFG)
    b1, b2, _ = st.columns([1, 1, 3])
    b1.button("Explore threat graph", on_click=navigate, args=("Threat Graph",), use_container_width=True)
    b2.button("Search indicators", on_click=navigate, args=("Indicator Explorer",), use_container_width=True)

elif page == "Threat Graph":
    pick = st.selectbox("Focus on an entity", ["Show all"] + list(NODES))
    sel = None if pick == "Show all" else pick
    g, d = st.columns([3, 1.3])
    with g:
        st.plotly_chart(graph_fig(sel, 560), use_container_width=True)
    with d:
        st.markdown("### Details")
        if sel:
            _, _, t, r = NODES[sel]
            links = "".join(f'<div class="feed"><span class="m">{n} <span class="pill lo">{NODES[n][2]}</span></span></div>' for n in sorted(neighbours(sel)))
            st.markdown(f'<div class="panel"><b>{sel}</b><br><span class="pill {"hi" if r >= 75 else "md" if r >= 40 else "lo"}">{band(r).upper()} · {r}</span>'
                        f'<span class="pill lo">{t}</span><div class="colhead" style="margin-top:14px">Connected to</div>{links}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="panel"><span style="color:#8b919b">Pick an entity to highlight its connections and see its details.</span></div>', unsafe_allow_html=True)

elif page == "Indicator Explorer":
    q = st.text_input("Search indicator", placeholder="Enter an IP, domain or file hash")
    res = IND[IND["Indicator"].str.contains(q, case=False, regex=False)] if q else IND
    if q and res.empty:
        st.markdown('<div class="panel">No indicator matches that search. Try part of an IP, domain or hash.</div>', unsafe_allow_html=True)
    else:
        a, b = st.columns([3, 1.4])
        a.dataframe(res.sort_values("Score", ascending=False), hide_index=True, use_container_width=True, column_config=TABLE_CFG)
        top = res.sort_values("Score", ascending=False).iloc[0]
        gauge = go.Figure(go.Indicator(mode="gauge+number", value=int(top["Score"]),
                          number=dict(font=dict(family="JetBrains Mono", color="#fff", size=38)),
                          gauge=dict(axis=dict(range=[0, 100], tickcolor="#4a505a"), bar=dict(color="#e8eaed", thickness=.28),
                                     bgcolor="#14161a", borderwidth=0,
                                     steps=[dict(range=[0, 40], color="#1a1d22"), dict(range=[40, 75], color="#262a30"), dict(range=[75, 100], color="#343941")])))
        gauge.update_layout(**base_layout(230))
        with b:
            st.markdown(f"### {top['Indicator']}")
            st.plotly_chart(gauge, use_container_width=True)

elif page == "Investigations":
    cols = st.columns(3)
    board = {"Open": [("Loader.Demo spread", "3 indicators · Graphite-1"), ("Credential phishing wave", "5 indicators · Graphite-2")],
             "In progress": [("Operation Graphite", "9 indicators · Analyst A"), ("Cluster 07 attribution", "4 indicators · Analyst B")],
             "Closed": [("Stealer.Demo false positive", "Resolved · 2 days ago")]}
    for c, (name, items) in zip(cols, board.items()):
        body = "".join(f'<div class="case"><b>{t}</b><span>{s}</span></div>' for t, s in items)
        c.markdown(f'<div class="colhead">{name} · {len(items)}</div>{body}', unsafe_allow_html=True)

elif page == "Reports":
    cols = st.columns(3)
    for i, (c, (t, s)) in enumerate(zip(cols, [("Weekly threat summary", "New indicators, clusters and risk changes."),
                                               ("Campaign brief", "Entities and links for one campaign."),
                                               ("Indicator export", "High-risk indicators as a table.")])):
        c.markdown(f'<div class="case"><b>{t}</b><span>{s}</span></div>', unsafe_allow_html=True)
        if c.button("Generate report", key=f"rep{i}", use_container_width=True):
            st.toast(f"{t} generation will be added in a later build.")