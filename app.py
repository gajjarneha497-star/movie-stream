import streamlit as st
import pandas as pd
import json
import base64
import random
from datetime import datetime
from pathlib import Path

# ────────────────────────────────────────────────
# CONFIG & PATHS
# ────────────────────────────────────────────────
DATA_DIR    = Path(".")
USERS_FILE  = DATA_DIR / "users.json"
MOVIES_FILE = DATA_DIR / "movies.csv"
POSTER_DIR  = DATA_DIR
PARTY_FILE  = DATA_DIR / "parties.json"
POSTER_DIR.mkdir(exist_ok=True)

# ────────────────────────────────────────────────
# CUSTOM CSS — Dark Navy + Neon Cyan + Animations
# ────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700;800&display=swap');

html, body, .stApp {
    background: #07102a !important;
    color: #e2e8f0 !important;
    font-family: 'Poppins', 'Segoe UI', sans-serif !important;
}
.stApp::before {
    content: '';
    position: fixed; inset: 0;
    background:
        radial-gradient(ellipse 80% 40% at 20% 10%, #00e5ff0d 0%, transparent 60%),
        radial-gradient(ellipse 60% 30% at 80% 80%, #1a479e0d 0%, transparent 60%);
    pointer-events: none; z-index: 0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.2rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0a1830 0%,#07102a 100%) !important;
    border-right: 1px solid #1a3060 !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
.sidebar-logo {
    font-size: 22px; font-weight: 800; color: #00e5ff !important;
    text-shadow: 0 0 18px #00e5ff88, 0 0 40px #00e5ff33;
    padding: 8px 0 4px; letter-spacing: 1px;
}

/* ── Buttons ── */
div[data-testid="stButton"] > button {
    border-radius: 8px !important; font-weight: 600 !important;
    transition: all 0.25s cubic-bezier(.34,1.56,.64,1) !important;
    width: 100% !important;
}
div[data-testid="stButton"] > button[kind="primary"] {
    background: linear-gradient(135deg,#00e5ff,#00aacc) !important;
    color: #07102a !important; border: none !important;
    box-shadow: 0 0 12px #00e5ff55 !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    box-shadow: 0 0 24px #00e5ffaa, 0 4px 16px #00000066 !important;
    transform: translateY(-2px) scale(1.02) !important;
}
div[data-testid="stButton"] > button:not([kind="primary"]) {
    background: #0d1e3a !important; color: #cbd5e1 !important;
    border: 1.5px solid #1a3060 !important;
}
div[data-testid="stButton"] > button:not([kind="primary"]):hover {
    border-color: #00e5ff !important; color: #00e5ff !important;
    box-shadow: 0 0 10px #00e5ff33 !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs ── */
div[data-testid="stTextInput"] input {
    background: #0d1e3a !important; border: 1.5px solid #1a3060 !important;
    border-radius: 8px !important; color: #fff !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #00e5ff !important; box-shadow: 0 0 8px #00e5ff44 !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: #0d1e3a !important; border: 1.5px solid #1a3060 !important;
    border-radius: 8px !important; color: #fff !important;
}

/* ── Tabs ── */
div[data-testid="stTabs"] [role="tab"] {
    background: #0d1e3a !important; color: #8899bb !important;
    border-radius: 8px 8px 0 0 !important; font-weight: 600 !important;
}
div[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: #1a3060 !important; color: #00e5ff !important;
    box-shadow: 0 0 8px #00e5ff33 !important;
}

/* ── Hero ── */
.hero-banner {
    background: linear-gradient(135deg,#0a1830 0%,#0d2040 50%,#0a1830 100%);
    border: 1px solid #1a3060; border-radius: 16px;
    padding: 26px 30px; margin-bottom: 22px;
    position: relative; overflow: hidden;
    animation: heroFade .6s ease forwards;
}
.hero-banner::before {
    content:''; position:absolute; top:-80px; right:-80px;
    width:280px; height:280px;
    background:radial-gradient(circle,#00e5ff14 0%,transparent 70%);
}
@keyframes heroFade { from{opacity:0;transform:translateY(-14px);} to{opacity:1;transform:none;} }
.hero-title {
    font-size:27px; font-weight:800; color:#00e5ff;
    text-shadow:0 0 18px #00e5ff88; margin:0 0 5px;
}
.hero-sub { color:#8899bb; font-size:13px; margin-bottom:14px; }
.badge-row { display:flex; gap:8px; flex-wrap:wrap; }
.badge {
    padding:5px 13px; border-radius:20px; font-size:11px; font-weight:700;
    background:#0d1e3a; border:1.5px solid #00e5ff; color:#00e5ff;
    box-shadow:0 0 8px #00e5ff33;
    animation:badgePop .5s ease forwards; opacity:0;
}
.badge:nth-child(1){animation-delay:.15s;} .badge:nth-child(2){animation-delay:.3s;}
.badge:nth-child(3){animation-delay:.45s;} .badge:nth-child(4){animation-delay:.6s;}
@keyframes badgePop { from{opacity:0;transform:scale(.7);} to{opacity:1;transform:scale(1);} }

/* ── Stats ── */
.stat-card {
    background:#0d1e3a; border:1.5px solid #00e5ff44;
    border-radius:12px; padding:16px 10px; text-align:center;
    box-shadow:0 0 14px #00e5ff1a;
    animation:cardPop .45s ease forwards; opacity:0;
}
.stat-number { font-size:28px; font-weight:800; color:#00e5ff; text-shadow:0 0 10px #00e5ff88; }
.stat-label  { font-size:11px; color:#8899bb; margin-top:2px; }

/* ── Section title ── */
.section-title {
    font-size:17px; font-weight:700; color:#00e5ff;
    text-shadow:0 0 10px #00e5ff55; margin:20px 0 12px;
    display:flex; align-items:center; gap:9px;
}
.section-title::before {
    content:''; width:4px; height:20px; background:#00e5ff;
    border-radius:2px; box-shadow:0 0 8px #00e5ff88; display:inline-block;
}

/* ── Movie card ── */
.movie-card {
    background:#0d1e3a; border-radius:14px; padding:12px;
    border:1px solid #1a3060; margin-bottom:14px;
    transition:all .3s cubic-bezier(.34,1.56,.64,1);
    animation:cardPop .45s ease forwards; opacity:0;
}
.movie-card:hover {
    border-color:#00e5ff;
    box-shadow:0 0 20px #00e5ff33, 0 8px 32px #00000088;
    transform:translateY(-4px);
}
@keyframes cardPop { from{opacity:0;transform:scale(.88) translateY(16px);} to{opacity:1;transform:none;} }

/* ── Neon divider ── */
.neon-divider {
    height:2px; margin:18px 0;
    background:linear-gradient(90deg,transparent,#00e5ff44,#00e5ff,#00e5ff44,transparent);
    border:none; border-radius:2px;
}

/* ── Trailer box ── */
.trailer-wrap {
    background:#0d1e3a; border:2px solid #00e5ff; border-radius:14px;
    padding:18px; box-shadow:0 0 28px #00e5ff33;
    animation:popIn .4s cubic-bezier(.34,1.56,.64,1) forwards;
}
@keyframes popIn { from{transform:scale(.9);opacity:0;} to{transform:scale(1);opacity:1;} }
.trailer-title { color:#00e5ff; font-size:16px; font-weight:700; margin-bottom:12px; text-shadow:0 0 10px #00e5ff66; }

/* ── AI panel ── */
.ai-panel {
    background:linear-gradient(135deg,#0d1a3a,#0a1428);
    border:1.5px solid #4f46e566; border-radius:14px;
    padding:18px 22px; margin-bottom:20px;
    animation:slideUp .5s ease forwards;
}
@keyframes slideUp { from{opacity:0;transform:translateY(20px);} to{opacity:1;transform:none;} }
.ai-tag {
    display:inline-block; background:linear-gradient(135deg,#7c3aed,#4f46e5);
    color:#fff; border-radius:8px; padding:3px 12px;
    font-size:11px; font-weight:700; box-shadow:0 0 10px #7c3aed66;
}
.ai-chip {
    background:#0d1e3a; border:1px solid #4f46e566;
    border-radius:12px; padding:14px 10px; text-align:center;
    animation:chipPop .4s ease forwards; opacity:0; margin-bottom:10px;
}
@keyframes chipPop { from{opacity:0;transform:scale(.8) translateY(8px);} to{opacity:1;transform:none;} }

/* ── Watch party ── */
.party-panel {
    background:linear-gradient(135deg,#0d2040,#0a1830);
    border:1.5px solid #00e5ff33; border-radius:14px;
    padding:18px 22px; margin-bottom:20px;
    position:relative; overflow:hidden;
    animation:slideUp .55s ease forwards;
}
.party-panel::after { content:'🎉'; position:absolute; right:18px; top:12px; font-size:50px; opacity:.1; }
.party-code {
    font-size:30px; font-weight:900; color:#00e5ff; letter-spacing:8px;
    text-shadow:0 0 20px #00e5ffaa; text-align:center; padding:12px 0;
}
.member-pill {
    display:inline-flex; align-items:center; gap:6px;
    background:#0d1e3a; border:1px solid #1a3060;
    border-radius:20px; padding:3px 12px; font-size:11px; color:#00e5ff; margin:3px;
}
.online-dot { width:7px; height:7px; border-radius:50%; background:#22c55e; box-shadow:0 0 6px #22c55e; display:inline-block; }

/* ── Offline panel ── */
.offline-panel {
    background:linear-gradient(135deg,#071a0a,#0a2010);
    border:1.5px solid #22c55e33; border-radius:14px;
    padding:18px 22px; margin-bottom:20px;
    animation:slideUp .6s ease forwards;
}


st.markdown("""
<div class="voice-box">
    <span class="voice-mic">🎙️</span>
    <div class="voice-label">Voice Search — type or speak a movie name / genre</div>
    <div style="color:#8899bb;font-size:11px;margin-top:3px;">Smart filter: searches title AND genre instantly</div>
</div>""", unsafe_allow_html=True)
""", unsafe_allow_html=True)
st.markdown("""
<div class="voice-box">
    <span class="voice-mic">🎙️</span>
    <div class="voice-label">Voice Search</div>
    <button onclick="startVoice()" style="background:linear-gradient(135deg,#00e5ff,#00aacc);
        border:none;border-radius:8px;padding:8px 22px;color:#07102a;
        font-weight:700;font-size:14px;cursor:pointer;margin-top:8px;">
        🎙️ Speak Now
    </button>
</div>
<script>
function startVoice() {
    if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
        alert('Taro browser voice search support nathi karto. Chrome use karo.');
        return;
    }
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'hi-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.start();
    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        const inputs = window.parent.document.querySelectorAll('input[type=text]');
        if (inputs.length > 0) {
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(inputs[0], transcript);
            inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
        }
    };
    recognition.onerror = function(event) {
        alert('Voice error: ' + event.error);
    };
}
</script>
""", unsafe_allow_html=True)

# ────────────────────────────────────────────────
# DATA HELPERS
# ────────────────────────────────────────────────
def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE) as f: return json.load(f)
    return {}

def save_users(u):
    with open(USERS_FILE,"w") as f: json.dump(u, f, indent=2)

def load_parties():
    if PARTY_FILE.exists():
        with open(PARTY_FILE) as f: return json.load(f)
    return {}

def save_parties(p):
    with open(PARTY_FILE,"w") as f: json.dump(p, f, indent=2)

def load_movies():
    if MOVIES_FILE.exists():
        return pd.read_csv(MOVIES_FILE)
    data = {
        "movie_id":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
        "title":["Tare Zameen Par","Dangal","Bahubali","KGF","Pushpa",
                 "Shiddat","Satyaprem Ki Katha","Total Dhamal",
                 "Munja","Zootopia","Housefull 4","12 Fail","Snow White","Lion King","Bigil","Master"],
        "genre":["Drama","Drama","Action","Action","Action",
                 "Romance","Romance","Comedy","Horror","Animation","Comedy","Biopic","Family","Fantasy","Sports","Action"],
        "rating":[8.4,8.3,8.1,8.2,8.0,7.5,7.6,8.0,9.1,8.0,8.1,7.2,9.1,9.0,8.3,9.3],
        
        "poster":["tare zameen par.png","Dangal.png","bahubali.png","KGF.png","Pushpa.png",
          "shiddat.png","satyaprem ki katha.png","totaldhamal.png",
          "Munjya.png","Zootopia.png","Housefull4.png","12fail.png",
          "SnowWhite.png","LionKing.png","Bigil.png","Master.png"],
        "trailer":[
            "https://www.youtube.com/watch?v=XLUBcZQSZ70",#tare zameen par 1
            "https://www.youtube.com/watch?v=_x-YLGv9u1g",#dangal 2
            "https://www.youtube.com/watch?v=q2aENKR59w4",#bahubali 3
            "https://www.youtube.com/watch?v=q2aENKR59w4",#kgf 4
            "https://www.youtube.com/watch?v=INKMPPhPAPY",#pushpa 5
            "https://www.youtube.com/watch?v=FYfjV31tE3o",#shiddat 6
            "https://www.youtube.com/watch?v=8EPJiFfWRfw",#satyaprem ki katha 7
            "https://www.youtube.com/watch?v=fo9EhcwQXcM",#total dhamal 8
            "https://www.youtube.com/watch?v=8X3uF80H5LU",#munjya 9
            "https://www.youtube.com/watch?v=LzMyLV2pwws",#zootopia 10
            "https://www.youtube.com/watch?v=gcHH34cEl3Y",#housefull 4  11
            "https://www.youtube.com/watch?v=afEJYg0tyJ4",#12 fail  12
            "https://www.youtube.com/watch?v=aehhDN8p6Ws",#snow white 13
            "https://www.youtube.com/watch?v=mTy2Khuv_1s",#lion king 14
            "https://www.youtube.com/watch?v=Co6UqFUGJqU",  #bigil 15
             "https://www.youtube.com/watch?v=Zi9ciWeJ3fg",  #master 16
          
        ],
    }
    return pd.DataFrame(data)

def get_poster_b64(filename):
    p = POSTER_DIR / filename
    if p.exists():
        with open(p,"rb") as f: return base64.b64encode(f.read()).decode()
    return None

def remove_from_watchlist(title, users):
    if title in st.session_state.watchlist:
        st.session_state.watchlist.remove(title)
    users[st.session_state.username]["watchlist"] = st.session_state.watchlist
    save_users(users)

def add_download(username, title, users):
    if "downloads" not in users[username]: users[username]["downloads"] = []
    if title not in users[username]["downloads"]: users[username]["downloads"].append(title)
    save_users(users)

def remove_download(username, title, users):
    if "downloads" in users[username] and title in users[username]["downloads"]:
        users[username]["downloads"].remove(title)
    save_users(users)

# ── 🤖 AI Recommendations ──────────────────────
def ai_recommendations(username, movies_df, users):
    wl = users.get(username, {}).get("watchlist", [])
    if not wl:
        return movies_df.nlargest(4, "rating")
    watched = movies_df[movies_df["title"].isin(wl)]
    if watched.empty:
        return movies_df.nlargest(4, "rating")
    top_genre = watched["genre"].value_counts().index[0]
    recs = movies_df[(movies_df["genre"]==top_genre) & (~movies_df["title"].isin(wl))]
    if len(recs) < 4:
        extras = movies_df[~movies_df["title"].isin(wl)]
        recs = pd.concat([recs, extras]).drop_duplicates().head(4)
    return recs.head(4)

# ── 🎉 Watch Party ──────────────────────────────
def create_party(host, movie_title):
    code = str(random.randint(100000, 999999))
    parties = load_parties()
    parties[code] = {"host":host,"movie":movie_title,
                     "members":[host],"created":str(datetime.now())}
    save_parties(parties); return code

def join_party(code, username):
    parties = load_parties()
    if code in parties:
        if username not in parties[code]["members"]:
            parties[code]["members"].append(username)
        save_parties(parties)
        return parties[code]
    return None

# ────────────────────────────────────────────────
# SESSION STATE
# ────────────────────────────────────────────────
DEFAULTS = {"logged_in":False,"username":None,"watchlist":[],
            "voice_query":"","party_code":None,"active_tab":"🎬 Movies"}
for k,v in DEFAULTS.items():
    if k not in st.session_state: st.session_state[k] = v

movies = load_movies()
users  = load_users()

# ────────────────────────────────────────────────
# SIDEBAR
# ────────────────────────────────────────────────
st.sidebar.markdown('<div class="sidebar-logo">🎬 Movie Stream</div>', unsafe_allow_html=True)

if not st.session_state.logged_in:
    t1, t2 = st.sidebar.tabs(["Login","Register"])
    with t1:
        u = st.text_input("Username", key="lu")
        p = st.text_input("Password", type="password", key="lp")
        if st.button("Login", key="do_login", type="primary"):
            if u in users and users[u]["password"] == p:
                st.session_state.logged_in = True
                st.session_state.username  = u
                st.session_state.watchlist = users[u].get("watchlist",[])
                st.rerun()
            else:
                st.error("Invalid credentials")
    with t2:
        nu = st.text_input("New Username", key="ru")
        np = st.text_input("New Password", type="password", key="rp")
        if st.button("Create Account", key="do_reg", type="primary"):
            if nu and np:
                if nu in users: st.error("Username taken")
                else:
                    users[nu] = {"password":np,"watchlist":[],
                                 "downloads":[],"created":str(datetime.now())}
                    save_users(users); st.success("Account created! Login now.")
            else: st.error("Fill both fields")
else:
    st.sidebar.markdown(f"**Logged in as:** `{st.session_state.username}`")
    for tab in ["🎬 Movies","🤖 AI Picks","🎉 Watch Party","💾 Downloads"]:
        if st.sidebar.button(tab, key=f"nav_{tab}"):
            st.session_state.active_tab = tab; st.rerun()

    st.sidebar.markdown("---")
    with st.sidebar.expander("📋 My Watchlist", expanded=True):
        if st.session_state.watchlist:
            for title in list(st.session_state.watchlist):
                c1,c2 = st.columns([3,1])
                with c1:
                    if st.button(f"▶ {title}", key=f"wlp_{title}"):
                        row = movies[movies["title"]==title]
                        if not row.empty:
                            st.session_state["playing"] = row.iloc[0].to_dict()
                            st.rerun()
                with c2:
                    if st.button("🗑", key=f"wlr_{title}"):
                        remove_from_watchlist(title, users); st.rerun()
        else:
            st.caption("Your watchlist is empty.")
    st.sidebar.markdown("---")
    if st.sidebar.button("Logout"):
        for k,v in DEFAULTS.items(): st.session_state[k] = v
        st.rerun()

# ────────────────────────────────────────────────
# NOT LOGGED IN
# ────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("""
    <div class="hero-banner">
        <div class="hero-title">🎬 Movie Stream</div>
        <div class="hero-sub">India's Next-Gen OTT Platform</div>
        <div class="badge-row">
            <span class="badge">🤖 AI Recommendations</span>
            <span class="badge">🎉 Live Watch Parties</span>
            <span class="badge">🎙️ Voice Search</span>
            <span class="badge">💾 Offline Downloads</span>
        </div>
    </div>""", unsafe_allow_html=True)
    st.info("👈 Login from the sidebar to start streaming.")
    st.stop()

# ────────────────────────────────────────────────
# HERO + STATS
# ────────────────────────────────────────────────
st.markdown(f"""
<div class="hero-banner">
    <div class="hero-title">🎬 Movie Stream</div>
    <div class="hero-sub">Welcome back, <b style="color:#00e5ff">{st.session_state.username}</b> — What are you watching today?</div>
    <div class="badge-row">
        <span class="badge">🤖 AI Picks</span>
        <span class="badge">🎉 Watch Party</span>
        <span class="badge">🎙️ Voice Search</span>
        <span class="badge">💾 Offline Mode</span>
    </div>
</div>""", unsafe_allow_html=True)

user_data  = users.get(st.session_state.username, {})
user_dls   = user_data.get("downloads", [])
c1,c2,c3,c4 = st.columns(4)
for col,(num,lbl) in zip([c1,c2,c3,c4],[
    (str(len(movies)),"Movies"),
    (str(len(set(movies["genre"]))),"Genres"),
    (str(len(st.session_state.watchlist)),"Watchlist"),
    (str(len(user_dls)),"Downloads"),
]):
    col.markdown(f'<div class="stat-card"><div class="stat-number">{num}</div>'
                 f'<div class="stat-label">{lbl}</div></div>', unsafe_allow_html=True)

st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════
# TAB: 🎬 MOVIES
# ════════════════════════════════════════════════
if st.session_state.active_tab == "🎬 Movies":

    # ── 🎙️ Voice Search UI ──────────────────────
    st.markdown("""
    <div class="voice-box">
        <span class="voice-mic">🎙️</span>
        <div class="voice-label">Voice Search — type or speak a movie name / genre</div>
        <div style="color:#8899bb;font-size:11px;margin-top:3px;">Smart filter: searches title AND genre instantly</div>
    </div>""", unsafe_allow_html=True)

    sc1, sc2 = st.columns([4,1])
    with sc1:
        voice_q = st.text_input("🎙️ Search", value=st.session_state.voice_query,
                                placeholder="e.g. 'action', 'romance', 'Dangal'…",
                                label_visibility="collapsed", key="vsearch")
    with sc2:
        if st.button("🔍 Search", key="do_search", type="primary"):
            st.session_state.voice_query = voice_q; st.rerun()
    if st.session_state.voice_query:
        if st.button("✕ Clear Search", key="clr_srch"):
            st.session_state.voice_query = ""; st.rerun()

    # ── Genre chips ──────────────────────────────
    genres_all = ["All"] + sorted(movies["genre"].unique().tolist())
    if "genre_sel" not in st.session_state: st.session_state.genre_sel = "All"
    gcols = st.columns(len(genres_all))
    for i,g in enumerate(genres_all):
        with gcols[i]:
            if st.button(g, key=f"g_{g}",
                         type="primary" if st.session_state.genre_sel==g else "secondary"):
                st.session_state.genre_sel = g; st.rerun()

    # ── Filter ───────────────────────────────────
    filtered = movies.copy()
    q = st.session_state.voice_query.strip().lower()
    if q:
        filtered = filtered[
            filtered["title"].str.lower().str.contains(q, na=False) |
            filtered["genre"].str.lower().str.contains(q, na=False)
        ]
    if st.session_state.genre_sel != "All":
        filtered = filtered[filtered["genre"]==st.session_state.genre_sel]

    # ── Grid ─────────────────────────────────────
    st.markdown(f'<div class="section-title">🎬 Movies — {len(filtered)} results</div>',
                unsafe_allow_html=True)

    EMOJI = {"Action":"⚔️","Romance":"💕","Comedy":"😂","Drama":"🎭",
             "Horror":"👻","Animation":"✨"}

    if filtered.empty:
        st.warning("No movies found. Try a different search or genre.")
    else:
        cols5 = st.columns(5)
        for idx, (_, row) in enumerate(filtered.iterrows()):
            with cols5[idx % 5]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)

                # Poster
                b64 = get_poster_b64(row["poster"])
                if b64:
                    st.markdown(
                        f'<img src="data:image/png;base64,{b64}" style="width:100%;'
                        f'border-radius:10px;aspect-ratio:2/3;object-fit:cover;">',
                        unsafe_allow_html=True)
                else:
                    em = EMOJI.get(row["genre"],"🎬")
                    st.markdown(
                        f'<div style="width:100%;aspect-ratio:2/3;'
                        f'background:linear-gradient(135deg,#0d1e3a,#1a3060);'
                        f'border-radius:10px;display:flex;align-items:center;'
                        f'justify-content:center;font-size:52px;">{em}</div>',
                        unsafe_allow_html=True)

                # Downloaded badge
                if row["title"] in user_dls:
                    st.markdown('<div style="color:#22c55e;font-size:10px;'
                                'font-weight:700;text-align:right;margin:3px 0;">✅ Downloaded</div>',
                                unsafe_allow_html=True)

                st.markdown(
                    f'<div style="font-weight:700;font-size:12px;margin:5px 0 2px;'
                    f'white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{row["title"]}</div>'
                    f'<div style="display:flex;justify-content:space-between;margin-bottom:7px;">'
                    f'<span style="color:#ffcc00;font-size:11px;font-weight:700;">★ {row["rating"]}</span>'
                    f'<span style="font-size:9px;color:#8899bb;background:#1a3060;'
                    f'padding:2px 7px;border-radius:10px;">{row["genre"]}</span>'
                    f'</div>', unsafe_allow_html=True)

                # Buttons
                if st.button("▶ Play Trailer", key=f"tr_{row['movie_id']}", type="primary"):
                    st.session_state["playing"] = row.to_dict(); st.rerun()

                in_wl = row["title"] in st.session_state.watchlist
                if in_wl:
                    if st.button("🗑 Watchlist", key=f"rm_{row['movie_id']}"):
                        remove_from_watchlist(row["title"], users); st.rerun()
                else:
                    if st.button("＋ Watchlist", key=f"add_{row['movie_id']}"):
                        st.session_state.watchlist.append(row["title"])
                        users[st.session_state.username]["watchlist"] = st.session_state.watchlist
                        save_users(users); st.rerun()

                if row["title"] in user_dls:
                    if st.button("🗑 Remove DL", key=f"rmd_{row['movie_id']}"):
                        remove_download(st.session_state.username, row["title"], users)
                        st.rerun()
                else:
                    if st.button("💾 Download", key=f"dl_{row['movie_id']}"):
                        add_download(st.session_state.username, row["title"], users)
                        st.success(f"'{row['title']}' saved offline!"); st.rerun()

                st.markdown('</div>', unsafe_allow_html=True)

    # ── Trailer Player ────────────────────────────
    if "playing" in st.session_state:
        movie = st.session_state["playing"]
        st.markdown('<div class="neon-divider"></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="trailer-wrap"><div class="trailer-title">'
                    f'🎬 {movie["title"]} — Official Trailer</div></div>',
                    unsafe_allow_html=True)
        st.video(movie["trailer"])
        if st.button("✕ Close Player", key="close_pl", type="primary"):
            del st.session_state["playing"]; st.rerun()

# ════════════════════════════════════════════════
# TAB: 🤖 AI PICKS
# ════════════════════════════════════════════════
elif st.session_state.active_tab == "🤖 AI Picks":
    st.markdown("""
    <div class="ai-panel">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:6px;">
            <span class="ai-tag">🤖 AI Engine</span>
            <span style="font-size:16px;font-weight:700;">Personalised Movie Recommendations</span>
        </div>
        <div style="color:#8899bb;font-size:12px;">
            Our AI studies your watchlist and viewing patterns to find your next favourite film.
        </div>
    </div>""", unsafe_allow_html=True)

    recs = ai_recommendations(st.session_state.username, movies, users)
    st.markdown('<div class="section-title">🤖 Picked Just For You</div>', unsafe_allow_html=True)

    rcols = st.columns(4)
    for i, (_, row) in enumerate(recs.iterrows()):
        em = EMOJI.get(row["genre"],"🎬") if 'EMOJI' in dir() else "🎬"
        with rcols[i % 4]:
            st.markdown(f"""
            <div class="ai-chip" style="animation-delay:{i*0.12}s;">
                <div style="font-size:34px;margin-bottom:7px;">{em}</div>
                <div style="font-weight:700;font-size:12px;color:#e2e8f0;">{row['title']}</div>
                <div style="font-size:10px;color:#8899bb;margin:3px 0;">★ {row['rating']} · {row['genre']}</div>
            </div>""", unsafe_allow_html=True)
            b64 = get_poster_b64(row["poster"])
            if b64:
                st.markdown(f'<img src="data:image/png;base64,{b64}" style="width:100%;'
                            f'border-radius:10px;margin:6px 0;aspect-ratio:2/3;object-fit:cover;">',
                            unsafe_allow_html=True)
            if st.button("▶ Watch Trailer", key=f"ai_tr_{row['movie_id']}", type="primary"):
                st.session_state["playing"] = row.to_dict()
                st.session_state.active_tab = "🎬 Movies"; st.rerun()
            if row["title"] not in st.session_state.watchlist:
                if st.button("＋ Watchlist", key=f"ai_wl_{row['movie_id']}"):
                    st.session_state.watchlist.append(row["title"])
                    users[st.session_state.username]["watchlist"] = st.session_state.watchlist
                    save_users(users); st.rerun()

    # AI Insight
    wl = users.get(st.session_state.username,{}).get("watchlist",[])
    if wl:
        w_genres = movies[movies["title"].isin(wl)]["genre"].value_counts()
        if not w_genres.empty:
            top = w_genres.index[0]
            st.markdown(f"""
            <div style="background:#0d1a3a;border:1px solid #4f46e544;border-radius:10px;
                        padding:14px 18px;margin-top:16px;font-size:12px;color:#8899bb;">
                🤖 <b style="color:#7c3aed">AI Insight:</b>
                You love <b style="color:#e2e8f0">{top}</b> movies most.
                Recommendations built from <b style="color:#e2e8f0">{len(wl)}</b> watchlist item(s).
            </div>""", unsafe_allow_html=True)
    else:
        st.info("💡 Add movies to your watchlist — the AI learns your taste from it!")

# ════════════════════════════════════════════════
# TAB: 🎉 WATCH PARTY
# ════════════════════════════════════════════════
elif st.session_state.active_tab == "🎉 Watch Party":
    st.markdown("""
    <div class="party-panel">
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:4px;">
            <span style="font-size:28px;">🎉</span>
            <div>
                <div style="font-size:17px;font-weight:700;color:#00e5ff;">Live Watch Party</div>
                <div style="font-size:12px;color:#8899bb;">
                    Watch movies together with friends — share a 6-digit code & sync up in real time!
                </div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    pt1, pt2 = st.tabs(["🆕 Create Party","🔗 Join Party"])

    with pt1:
        st.markdown("**Choose a movie for your Watch Party:**")
        chosen = st.selectbox("Select Movie", movies["title"].tolist(), key="party_movie")
        if st.button("🎉 Create Watch Party", key="create_pty", type="primary"):
            code = create_party(st.session_state.username, chosen)
            st.session_state.party_code = code; st.rerun()

        if st.session_state.party_code:
            party = load_parties().get(st.session_state.party_code, {})
            if party:
                st.markdown(f"""
                <div class="party-panel" style="margin-top:14px;">
                    <div style="font-size:12px;color:#8899bb;margin-bottom:4px;">
                        🎬 Watching: <b style="color:#fff">{party.get('movie','')}</b>
                    </div>
                    <div style="font-size:12px;color:#8899bb;margin-bottom:2px;">Share this code with friends:</div>
                    <div class="party-code">{st.session_state.party_code}</div>
                    <div style="font-size:11px;color:#8899bb;margin:8px 0 4px;">Members online:</div>
                    {"".join(f'<span class="member-pill"><span class="online-dot"></span>{m}</span>'
                             for m in party.get("members",[]))}
                </div>""", unsafe_allow_html=True)

                mrow = movies[movies["title"]==party.get("movie","")]
                if not mrow.empty:
                    if st.button("▶ Start Watching Together", key="pty_watch", type="primary"):
                        st.session_state["playing"] = mrow.iloc[0].to_dict()
                        st.session_state.active_tab = "🎬 Movies"; st.rerun()
                if st.button("✕ End Party", key="end_pty"):
                    parties = load_parties()
                    parties.pop(st.session_state.party_code, None)
                    save_parties(parties)
                    st.session_state.party_code = None; st.rerun()

    with pt2:
        st.markdown("**Enter the 6-digit party code from your friend:**")
        jcode = st.text_input("Party Code", placeholder="e.g. 482910", key="jcode")
        if st.button("🔗 Join Party", key="do_join", type="primary"):
            if jcode:
                result = join_party(jcode, st.session_state.username)
                if result:
                    st.session_state.party_code = jcode
                    st.success(f"✅ Joined! Watching **{result['movie']}** with {len(result['members'])} member(s)")
                    st.rerun()
                else:
                    st.error("Party not found. Check the code.")
            else:
                st.error("Enter a party code first.")

        if st.session_state.party_code:
            party = load_parties().get(st.session_state.party_code, {})
            if party:
                st.markdown(f"""
                <div class="party-panel" style="margin-top:12px;">
                    <div style="font-size:12px;color:#8899bb;margin-bottom:6px;">
                        🎬 <b style="color:#fff">{party.get('movie','')}</b>
                        &nbsp;·&nbsp; Host: <b style="color:#00e5ff">{party.get('host','')}</b>
                    </div>
                    {"".join(f'<span class="member-pill"><span class="online-dot"></span>{m}</span>'
                             for m in party.get("members",[]))}
                </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════
# TAB: 💾 DOWNLOADS
# ════════════════════════════════════════════════
elif st.session_state.active_tab == "💾 Downloads":
    st.markdown("""
    <div class="offline-panel">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <span style="font-size:28px;">💾</span>
            <div>
                <div style="font-size:17px;font-weight:700;color:#22c55e;">Offline Downloads</div>
                <div style="font-size:12px;color:#8899bb;">Download movies — watch without internet, anytime.</div>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)

    user_downloads = users.get(st.session_state.username, {}).get("downloads", [])
    if not user_downloads:
        st.markdown("""
        <div style="text-align:center;padding:48px 20px;color:#8899bb;">
            <div style="font-size:52px;margin-bottom:12px;">💾</div>
            <div style="font-size:15px;font-weight:600;color:#e2e8f0;margin-bottom:5px;">No Downloads Yet</div>
            <div style="font-size:12px;">Go to 🎬 Movies and click 💾 Download on any movie.</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="section-title">💾 Downloaded — {len(user_downloads)} movies</div>',
                    unsafe_allow_html=True)
        dl_cols = st.columns(5)
        for i, title in enumerate(user_downloads):
            row_df = movies[movies["title"]==title]
            if row_df.empty: continue
            row = row_df.iloc[0]
            with dl_cols[i % 5]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                b64 = get_poster_b64(row["poster"])
                em = {"Action":"⚔️","Romance":"💕","Comedy":"😂",
                      "Drama":"🎭","Horror":"👻","Animation":"✨"}.get(row["genre"],"🎬")
                if b64:
                    st.markdown(f'<img src="data:image/png;base64,{b64}" style="width:100%;'
                                f'border-radius:10px;aspect-ratio:2/3;object-fit:cover;">',
                                unsafe_allow_html=True)
                else:
                    st.markdown(f'<div style="width:100%;aspect-ratio:2/3;'
                                f'background:linear-gradient(135deg,#071a0a,#0a2010);'
                                f'border-radius:10px;display:flex;align-items:center;'
                                f'justify-content:center;font-size:52px;">{em}</div>',
                                unsafe_allow_html=True)
                st.markdown(f'<div style="font-weight:700;font-size:12px;margin:5px 0 2px;">{row["title"]}</div>'
                            f'<div style="color:#22c55e;font-size:10px;font-weight:700;margin-bottom:6px;">'
                            f'✅ Available Offline</div>', unsafe_allow_html=True)
                if st.button("▶ Watch Now", key=f"dl_play_{i}", type="primary"):
                    st.session_state["playing"] = row.to_dict()
                    st.session_state.active_tab = "🎬 Movies"; st.rerun()
                if st.button("🗑 Remove", key=f"dl_rm_{i}"):
                    remove_download(st.session_state.username, title, users); st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
