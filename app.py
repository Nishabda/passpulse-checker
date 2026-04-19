import streamlit as st
import hashlib
import requests
import secrets
import string
import math
import re

st.set_page_config(
    page_title="PassPulse",
    page_icon="🔐",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body,
[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="block-container"] {
    background-color: #0d0d0d !important;
    color: #ededed;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 14px;
    line-height: 1.6;
}

[data-testid="stMain"] > div { padding-top: 0 !important; }
[data-testid="block-container"] { padding: 0 1.5rem 3rem !important; max-width: 640px !important; }

#MainMenu, footer, header,
[data-testid="stDecoration"],
[data-testid="stToolbar"] { display: none !important; visibility: hidden !important; }

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-thumb { background: #2a2a2a; border-radius: 99px; }

/* ── Typography ── */
.pp-wordmark {
    font-size: 13px;
    font-weight: 600;
    color: #ededed;
    letter-spacing: -0.01em;
}
.pp-wordmark span { color: #5b6af0; }

.pp-headline {
    font-size: clamp(28px, 6vw, 40px);
    font-weight: 600;
    letter-spacing: -0.03em;
    line-height: 1.15;
    color: #ffffff;
}
.pp-sub {
    font-size: 13px;
    color: #777;
    margin-top: 6px;
    letter-spacing: 0.01em;
}

/* ── Layout ── */
.pp-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 0;
    border-bottom: 1px solid #1e1e1e;
    margin-bottom: 40px;
    position: sticky;
    top: 0;
    background: #0d0d0d;
    z-index: 100;
}
.pp-badge {
    font-size: 11px;
    font-weight: 500;
    color: #666;
    background: #181818;
    border: 1px solid #2a2a2a;
    border-radius: 99px;
    padding: 3px 10px;
    letter-spacing: 0.02em;
    position: relative;
    cursor: pointer;
    user-select: none;
}
.pp-badge .pp-tooltip { opacity: 0; pointer-events: none; transform: translateY(-4px); }
.pp-badge.open .pp-tooltip { opacity: 1; pointer-events: auto; transform: translateY(0); }
.pp-tooltip {
    position: absolute;
    top: calc(100% + 10px);
    right: 0;
    background: #161616;
    border: 1px solid #2a2a2a;
    border-radius: 10px;
    padding: 12px 14px;
    width: 230px;
    transition: opacity 0.2s ease, transform 0.2s ease;
    z-index: 999;
    text-align: left;
}
.pp-tooltip-row {
    display: flex;
    align-items: flex-start;
    gap: 8px;
    padding: 5px 0;
    border-bottom: 1px solid #1e1e1e;
    font-size: 12px;
    color: #888;
    line-height: 1.5;
}
.pp-tooltip-row:last-child { border-bottom: none; }
.pp-tooltip-icon { font-size: 12px; flex-shrink: 0; margin-top: 1px; }
.pp-tooltip a { color: #5b6af0; text-decoration: none; }
.pp-tooltip a:hover { text-decoration: underline; }

.pp-section { margin-bottom: 10px; }

.pp-label {
    font-size: 11px;
    font-weight: 500;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 10px;
}

/* ── Input ── */
[data-testid="stTextInput"] > div > div > input {
    background: #111 !important;
    border: 1px solid #222 !important;
    border-radius: 10px !important;
    color: #ededed !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 15px !important;
    font-weight: 400 !important;
    padding: 12px 16px !important;
    width: 100% !important;
    transition: border-color 0.15s ease !important;
    caret-color: #5b6af0;
    letter-spacing: 0.02em;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #2d2d2d !important;
    box-shadow: 0 0 0 3px rgba(91,106,240,0.08) !important;
    outline: none !important;
}
[data-testid="stTextInput"] > div > div > input::placeholder { color: #333 !important; }
[data-testid="stTextInput"] button { display: none !important; }
[data-testid="stTextInput"] label { display: none !important; }

/* ── Strength bar ── */
.pp-bar-track {
    height: 3px;
    background: #1a1a1a;
    border-radius: 99px;
    overflow: hidden;
    margin: 16px 0 6px;
}
.pp-bar-fill {
    height: 100%;
    border-radius: 99px;
    transition: width 0.4s cubic-bezier(.4,0,.2,1);
}

/* ── Score row ── */
.pp-score-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
}
.pp-grade {
    font-size: 13px;
    font-weight: 500;
}
.pp-score-num {
    font-size: 12px;
    color: #444;
    font-variant-numeric: tabular-nums;
}

/* ── Stat grid ── */
.pp-stats {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 8px;
    margin: 24px 0;
}
.pp-stat {
    background: #111;
    border: 1px solid #1c1c1c;
    border-radius: 10px;
    padding: 14px 16px;
}
.pp-stat-label {
    font-size: 11px;
    color: #444;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 5px;
}
.pp-stat-value {
    font-size: 18px;
    font-weight: 600;
    color: #ededed;
    letter-spacing: -0.02em;
    line-height: 1.2;
    word-break: break-word;
}

/* ── Divider ── */
.pp-divider {
    height: 1px;
    background: #1a1a1a;
    margin: 28px 0;
}

/* ── Checklist ── */
.pp-checks { display: flex; flex-direction: column; gap: 2px; }
.pp-check {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 7px 0;
    border-bottom: 1px solid #141414;
    font-size: 13px;
}
.pp-check:last-child { border-bottom: none; }
.pp-check-icon {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 10px;
    flex-shrink: 0;
    font-weight: 700;
}
.pp-check-pass { background: rgba(52,211,153,0.1); color: #34d399; }
.pp-check-fail { background: rgba(239,68,68,0.1); color: #ef4444; }
.pp-check-text-pass { color: #ccc; }
.pp-check-text-fail { color: #777; }

/* ── Suggestions ── */
.pp-suggestions { display: flex; flex-direction: column; gap: 6px; margin-top: 4px; }
.pp-suggestion {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 10px 12px;
    background: #111;
    border: 1px solid #1c1c1c;
    border-radius: 8px;
    font-size: 13px;
    color: #aaa;
    line-height: 1.5;
}
.pp-suggestion-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #f59e0b;
    flex-shrink: 0;
    margin-top: 6px;
}
.pp-suggestion-ok { color: #34d399; }
.pp-suggestion-dot-ok { background: #34d399; }

/* ── Breach ── */
.pp-breach {
    padding: 14px 16px;
    border-radius: 10px;
    font-size: 13px;
    line-height: 1.6;
    margin-top: 12px;
}
.pp-breach-safe {
    background: rgba(52,211,153,0.05);
    border: 1px solid rgba(52,211,153,0.15);
    color: #6ee7b7;
}
.pp-breach-danger {
    background: rgba(239,68,68,0.05);
    border: 1px solid rgba(239,68,68,0.15);
    color: #fca5a5;
}
.pp-breach-note {
    font-size: 12px;
    color: #333;
    margin-bottom: 14px;
    line-height: 1.6;
}

/* ── Generator ── */
.pp-gen-output {
    background: #111;
    border: 1px solid #222;
    border-radius: 10px;
    padding: 16px;
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 14px;
    color: #ededed;
    word-break: break-all;
    line-height: 1.7;
    margin: 14px 0 8px;
    letter-spacing: 0.03em;
}
.pp-gen-meta {
    font-size: 12px;
    color: #333;
    margin-top: 6px;
}
.pp-gen-meta span { color: #555; }

/* ── Copy button ── */
.pp-copy-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin: 14px 0 8px;
}
.pp-gen-output-inline {
    background: #111;
    border: 1px solid #222;
    border-radius: 10px;
    padding: 14px 16px;
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 14px;
    color: #ededed;
    word-break: break-all;
    line-height: 1.7;
    letter-spacing: 0.03em;
    flex: 1;
}
.pp-copy-btn {
    background: #181818;
    border: 1px solid #2a2a2a;
    border-radius: 8px;
    color: #888;
    font-family: 'Inter', sans-serif;
    font-size: 12px;
    font-weight: 500;
    padding: 8px 14px;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.15s;
    flex-shrink: 0;
}
.pp-copy-btn:hover { background: #222; color: #ccc; border-color: #333; }
.pp-copy-btn.copied { color: #34d399; border-color: rgba(52,211,153,0.3); background: rgba(52,211,153,0.05); }

/* ── History ── */
.pp-history { display: flex; flex-direction: column; gap: 6px; }
.pp-history-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 14px;
    background: #111;
    border: 1px solid #1c1c1c;
    border-radius: 8px;
    gap: 12px;
}
.pp-history-pw {
    font-family: 'SF Mono', 'Fira Code', monospace;
    font-size: 13px;
    color: #ccc;
    word-break: break-all;
    flex: 1;
    letter-spacing: 0.02em;
}
.pp-history-meta {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-shrink: 0;
}
.pp-history-grade {
    font-size: 11px;
    font-weight: 500;
    white-space: nowrap;
}
.pp-history-score {
    font-size: 11px;
    color: #444;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
}
.pp-history-empty {
    font-size: 13px;
    color: #333;
    text-align: center;
    padding: 20px 0;
}

/* ── Buttons ── */
[data-testid="stButton"] > button {
    background: #181818 !important;
    color: #ccc !important;
    border: 1px solid #252525 !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    padding: 9px 16px !important;
    width: 100% !important;
    transition: background 0.15s, border-color 0.15s, color 0.15s !important;
    letter-spacing: 0.01em !important;
    cursor: pointer !important;
}
[data-testid="stButton"] > button:hover {
    background: #1f1f1f !important;
    border-color: #333 !important;
    color: #ededed !important;
}

/* Primary button variant via key */
[data-testid="stButton"]:has(button[kind="primary"]) > button,
div[data-testid="stButton"] > button.primary {
    background: #5b6af0 !important;
    color: #fff !important;
    border-color: transparent !important;
}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label {
    color: #666 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 400 !important;
    gap: 8px !important;
}
[data-testid="stCheckbox"] input:checked ~ div svg { color: #5b6af0 !important; }

/* ── Slider ── */
[data-testid="stSlider"] label {
    color: #444 !important;
    font-size: 12px !important;
    font-family: 'Inter', sans-serif !important;
}
[data-testid="stSlider"] [data-baseweb="slider"] div[role="slider"] {
    background: #5b6af0 !important;
    border-color: #5b6af0 !important;
}
[data-testid="stSlider"] div[data-testid="stTickBarMin"],
[data-testid="stSlider"] div[data-testid="stTickBarMax"] {
    color: #333 !important;
    font-size: 11px !important;
}

/* ── Empty state ── */
.pp-empty {
    text-align: center;
    padding: 48px 24px;
}
.pp-empty-icon {
    font-size: 32px;
    margin-bottom: 12px;
    opacity: 0.3;
}
.pp-empty-text { font-size: 14px; color: #2a2a2a; }

/* ── Footer ── */
.pp-footer {
    text-align: center;
    padding: 32px 0 8px;
    font-size: 11px;
    color: #222;
    letter-spacing: 0.05em;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #444 !important; }

/* ── Info box ── */
.pp-info {
    background: #111;
    border: 1px solid #1c1c1c;
    border-radius: 8px;
    padding: 10px 14px;
    font-size: 12px;
    color: #444;
    line-height: 1.6;
    margin-top: 8px;
}

/* ── Toggle button special style ── */
.pp-toggle { margin-top: 8px; }
</style>
""", unsafe_allow_html=True)


# ── Logic ──────────────────────────────────────────────────────────────────────

COMMON = {
    "password","123456","password1","qwerty","abc123","letmein","monkey",
    "master","dragon","111111","baseball","iloveyou","trustno1","sunshine",
    "princess","welcome","shadow","superman","michael","football","batman",
    "admin","login","passw0rd","p@ssword","p@ssw0rd","pa$$word","pass123",
    "test123","qwerty123","1q2w3e4r","12345678","1234567890","password123",
    "admin123","root","toor","qwertyuiop","asdfghjkl","zxcvbnm","000000",
    "654321","123123","666666","888888","1234567","12345","1234","123",
}
WALKS = ["qwerty","asdf","zxcv","qazwsx","1qaz","2wsx","qweasd",
         "asdfgh","zxcvbn","123456","098765","qwertyuiop","asdfghjkl"]
LEET  = str.maketrans("@4310$!5|", "aaeiossil")

def norm(p): return p.lower().translate(LEET)

def entropy(p):
    pool = sum([26 if re.search(r"[a-z]",p) else 0,
                26 if re.search(r"[A-Z]",p) else 0,
                10 if re.search(r"\d",p)    else 0,
                32 if re.search(r"[^a-zA-Z0-9]",p) else 0])
    return 0.0 if pool == 0 else len(p) * math.log2(pool)

def crack_time(e):
    s = (2**e) / 1e10
    if s < 1:         return "< 1 second"
    if s < 60:        return f"{int(s)} sec"
    if s < 3600:      return f"{int(s/60)} min"
    if s < 86400:     return f"{int(s/3600)} hrs"
    if s < 2592000:   return f"{int(s/86400)} days"
    if s < 31536000:  return f"{int(s/2592000)} months"
    y = s / 31536000
    if y < 1000:      return f"{int(y)} years"
    if y < 1_000_000: return f"{y/1000:.0f}K years"
    return "Centuries"

def check_hibp(pwd):
    h = hashlib.sha1(pwd.encode()).hexdigest().upper()
    pre, suf = h[:5], h[5:]
    try:
        r = requests.get(f"https://api.pwnedpasswords.com/range/{pre}",
                         headers={"User-Agent": "PassPulse"}, timeout=6)
        if r.status_code != 200: return False, -1
        for line in r.text.splitlines():
            hh, c = line.split(":")
            if hh == suf: return True, int(c)
        return False, 0
    except: return False, -1

def analyze(pwd):
    if not pwd: return {}
    n     = norm(pwd)
    hasU  = bool(re.search(r"[A-Z]", pwd))
    hasL  = bool(re.search(r"[a-z]", pwd))
    hasD  = bool(re.search(r"\d", pwd))
    hasS  = bool(re.search(r"[^a-zA-Z0-9]", pwd))
    isCom = n in COMMON or pwd.lower() in COMMON
    hasW  = any(w in n for w in WALKS)
    hasR  = bool(re.search(r"(.)\1{2,}", pwd))
    hasSq = bool(re.search(r"(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def)", n))
    hasDt = bool(re.search(r"(19|20)\d{2}", pwd))
    e     = entropy(pwd)
    pool  = (26 if hasL else 0)+(26 if hasU else 0)+(10 if hasD else 0)+(32 if hasS else 0)

    sc = 0
    if len(pwd)>=8:  sc+=10
    if len(pwd)>=12: sc+=10
    if len(pwd)>=16: sc+=10
    if len(pwd)>=20: sc+=5
    if hasU: sc+=10
    if hasL: sc+=10
    if hasD: sc+=10
    if hasS: sc+=15
    if e>=50: sc+=10
    if e>=70: sc+=10
    if e>=90: sc+=5
    if isCom: sc-=40
    if hasW:  sc-=15
    if hasR:  sc-=10
    if hasSq: sc-=8
    if hasDt: sc-=5
    if len(pwd)<8: sc-=20
    sc = max(0, min(100, sc))

    if   sc < 20: grade, color, bar = "Critically Weak", "#ef4444", "#ef4444"
    elif sc < 40: grade, color, bar = "Weak",            "#f97316", "#f97316"
    elif sc < 60: grade, color, bar = "Fair",            "#eab308", "#eab308"
    elif sc < 80: grade, color, bar = "Strong",          "#22c55e", "#22c55e"
    else:         grade, color, bar = "Very Strong",     "#5b6af0", "#5b6af0"

    sugg = []
    if len(pwd)<12: sugg.append("Use at least 12 characters — 16 or more is ideal")
    if not hasU:    sugg.append("Add uppercase letters (A–Z)")
    if not hasL:    sugg.append("Add lowercase letters (a–z)")
    if not hasD:    sugg.append("Include at least one number (0–9)")
    if not hasS:    sugg.append("Add a special character like ! @ # $ % ^ & *")
    if isCom:       sugg.append("This is a very common password — change it now")
    if hasW:        sugg.append("Avoid keyboard patterns like qwerty or 12345")
    if hasR:        sugg.append("Remove repeated characters like aaa or 111")
    if hasSq:       sugg.append("Avoid sequences like abc or 123")
    if hasDt:       sugg.append("Avoid using dates — they are easy to guess")
    if not sugg:    sugg.append("No weaknesses detected. This is a strong password.")

    checks = [
        (len(pwd)>=12, f"Length — {len(pwd)} characters"),
        (hasU,  "Uppercase letters"),
        (hasL,  "Lowercase letters"),
        (hasD,  "Numbers"),
        (hasS,  "Special characters"),
        (not isCom, "Not a common password"),
        (not hasW,  "No keyboard patterns"),
        (not hasR,  "No repeated characters"),
        (not hasSq, "No sequential patterns"),
        (not hasDt, "No date patterns"),
    ]

    return dict(len=len(pwd), hasU=hasU, hasL=hasL, hasD=hasD, hasS=hasS,
                isCom=isCom, hasW=hasW, hasR=hasR, hasSq=hasSq, hasDt=hasDt,
                e=e, crack=crack_time(e), pool=pool, score=sc,
                grade=grade, color=color, bar=bar, sugg=sugg, checks=checks)

def gen_password(length=20, upper=True, digits=True, special=True):
    lo = string.ascii_lowercase
    up = string.ascii_uppercase
    di = string.digits
    sp = "!@#$%^&*()-_=+[]|;:,.<>?"
    pool, req = lo, [secrets.choice(lo)]
    if upper:   pool+=up; req.append(secrets.choice(up))
    if digits:  pool+=di; req.append(secrets.choice(di))
    if special: pool+=sp; req.append(secrets.choice(sp))
    rest = [secrets.choice(pool) for _ in range(length-len(req))]
    out  = req+rest
    secrets.SystemRandom().shuffle(out)
    return "".join(out)


# ── UI ─────────────────────────────────────────────────────────────────────────

# Top bar
st.markdown("""
<div class="pp-topbar">
    <div class="pp-wordmark" onclick="window.scrollTo({top:0,behavior:'smooth'});" style="cursor:pointer;">Pass<span>Pulse</span></div>
    <div class="pp-badge" id="pp-badge" onclick="toggleTooltip(event)">
        Password Checker
        <div class="pp-tooltip" id="pp-tooltip">
            <div class="pp-tooltip-row">
                <span class="pp-tooltip-icon">🔒</span>
                <span>Your passwords are never stored or transmitted in full</span>
            </div>
            <div class="pp-tooltip-row">
                <span class="pp-tooltip-icon">⚡</span>
                <span>Real-time strength analysis powered by entropy scoring</span>
            </div>
            <div class="pp-tooltip-row">
                <span class="pp-tooltip-icon">👤</span>
                <span>Built by Nishabda Shrestha</span>
            </div>
            <div class="pp-tooltip-row">
                <span class="pp-tooltip-icon">🐙</span>
                <span><a href="https://github.com/Nishabda" target="_blank" onclick="event.stopPropagation()">github.com/Nishabda</a></span>
            </div>
        </div>
    </div>
</div>
<script>
function toggleTooltip(e) {
    e.stopPropagation();
    document.getElementById('pp-badge').classList.toggle('open');
}
document.addEventListener('click', function() {
    document.getElementById('pp-badge').classList.remove('open');
});
</script>
""", unsafe_allow_html=True)

# Headline
st.markdown("""
<div style="margin-bottom: 36px;">
    <div class="pp-headline">How strong is<br>your password?</div>
    <div class="pp-sub">Real-time analysis, breach detection, and a score out of 100.</div>
</div>
""", unsafe_allow_html=True)

# ── Input ──
show = st.session_state.get("show", False)
password = st.text_input(
    "pw",
    type="default" if show else "password",
    placeholder="Enter your password",
    label_visibility="collapsed",
    key="pw",
)

col_a, col_b = st.columns([1, 1])
with col_a:
    if st.button("🙈 Hide" if show else "👁  Show", key="tog"):
        st.session_state["show"] = not show
        st.rerun()

st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)

# ── Results ──
if password:
    d = analyze(password)

    # Score + bar
    st.markdown(f"""
    <div class="pp-score-row">
        <span class="pp-grade" style="color:{d['color']};">{d['grade']}</span>
        <span class="pp-score-num">{d['score']} / 100</span>
    </div>
    <div class="pp-bar-track">
        <div class="pp-bar-fill" style="width:{d['score']}%; background:{d['bar']};"></div>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    cc = "#ef4444" if d['score'] < 40 else ("#eab308" if d['score'] < 60 else "#22c55e")
    st.markdown(f"""
    <div class="pp-stats">
        <div class="pp-stat">
            <div class="pp-stat-label">Entropy</div>
            <div class="pp-stat-value" style="color:#5b6af0;">{d['e']:.0f} bits</div>
        </div>
        <div class="pp-stat">
            <div class="pp-stat-label">Crack Time</div>
            <div class="pp-stat-value" style="color:{cc}; font-size:clamp(13px,3vw,18px);">{d['crack']}</div>
        </div>
        <div class="pp-stat">
            <div class="pp-stat-label">Length</div>
            <div class="pp-stat-value">{d['len']}</div>
        </div>
        <div class="pp-stat">
            <div class="pp-stat-label">Character pool</div>
            <div class="pp-stat-value">{d['pool']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)

    # Checklist
    st.markdown('<div class="pp-label">Checklist</div>', unsafe_allow_html=True)
    items = ""
    for ok, label in d["checks"]:
        ic  = "pp-check-pass" if ok else "pp-check-fail"
        tc  = "pp-check-text-pass" if ok else "pp-check-text-fail"
        sym = "✓" if ok else "✕"
        items += f'<div class="pp-check"><div class="pp-check-icon {ic}">{sym}</div><span class="{tc}">{label}</span></div>'
    st.markdown(f'<div class="pp-checks">{items}</div>', unsafe_allow_html=True)

    st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)

    # Suggestions
    st.markdown('<div class="pp-label">Suggestions</div>', unsafe_allow_html=True)
    suggs = ""
    all_good = len(d["sugg"]) == 1 and "No weaknesses" in d["sugg"][0]
    for s in d["sugg"]:
        dot_cls  = "pp-suggestion-dot-ok" if all_good else "pp-suggestion-dot"
        text_cls = "pp-suggestion-ok"     if all_good else ""
        suggs += f'<div class="pp-suggestion"><div class="pp-suggestion-dot {dot_cls}"></div><span class="{text_cls}">{s}</span></div>'
    st.markdown(f'<div class="pp-suggestions">{suggs}</div>', unsafe_allow_html=True)

    st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)

    # Breach check
    st.markdown('<div class="pp-label">Data Breach Check</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="pp-breach-note">
        Checks against 900M+ compromised passwords via Have I Been Pwned.<br>
        Only a 5-character hash prefix is sent — your password never leaves your device.
    </div>
    """, unsafe_allow_html=True)

    if st.button("Check for breaches →", key="breach"):
        with st.spinner("Checking..."):
            pwned, count = check_hibp(password)
        if count == -1:
            st.warning("Could not reach the API. Check your connection.")
        elif pwned:
            st.markdown(f'<div class="pp-breach pp-breach-danger">Found in <strong>{count:,} data breaches.</strong> Stop using this password immediately.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="pp-breach pp-breach-safe">Not found in any known breaches. You\'re clear.</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="pp-empty">
        <div class="pp-empty-icon">🔐</div>
        <div class="pp-empty-text">Enter a password above to see your analysis</div>
    </div>
    """, unsafe_allow_html=True)

# ── Generator ──
st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="pp-label">Password Generator</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: use_upper   = st.checkbox("Uppercase", value=True)
with c2: use_digits  = st.checkbox("Numbers",   value=True)
with c3: use_special = st.checkbox("Symbols",   value=True)

pw_len = st.slider("Length", min_value=8, max_value=64, value=20, step=1, label_visibility="collapsed")
st.markdown(f'<div class="pp-gen-meta" style="margin-bottom:10px;">Length: <span>{pw_len} characters</span></div>', unsafe_allow_html=True)

if st.button("Generate password", key="gen"):
    new_pw = gen_password(pw_len, use_upper, use_digits, use_special)
    st.session_state["gpw"] = new_pw
    # Add to history (max 5, no duplicates)
    if "history" not in st.session_state:
        st.session_state["history"] = []
    if new_pw not in [h["pw"] for h in st.session_state["history"]]:
        gd_new = analyze(new_pw)
        st.session_state["history"].insert(0, {
            "pw":    new_pw,
            "grade": gd_new["grade"],
            "color": gd_new["color"],
            "score": gd_new["score"],
        })
        st.session_state["history"] = st.session_state["history"][:5]

if "gpw" in st.session_state:
    gd = analyze(st.session_state["gpw"])
    gpw = st.session_state["gpw"]

    # Copy button via HTML + JS
    st.markdown(f"""
    <div class="pp-copy-wrap">
        <div class="pp-gen-output-inline" id="gen-pw-text">{gpw}</div>
        <button class="pp-copy-btn" id="copy-btn" onclick="
            navigator.clipboard.writeText('{gpw}').then(() => {{
                this.textContent = '✓ Copied';
                this.classList.add('copied');
                setTimeout(() => {{
                    this.textContent = 'Copy';
                    this.classList.remove('copied');
                }}, 2000);
            }});
        ">Copy</button>
    </div>
    """, unsafe_allow_html=True)

    if gd:
        st.markdown(f"""
        <div class="pp-gen-meta">
            <span style="color:{gd['color']};">{gd['grade']}</span>
            &nbsp;·&nbsp; {gd['e']:.0f} bits entropy
            &nbsp;·&nbsp; Crack time: {gd['crack']}
        </div>
        <div class="pp-info" style="margin-top:10px;">
            Save this in a password manager like <strong style="color:#666;">Bitwarden</strong> or <strong style="color:#666;">1Password</strong>. Never store passwords in notes or messages.
        </div>
        """, unsafe_allow_html=True)

# ── History ──
st.markdown('<div class="pp-divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="pp-label">Generated History</div>', unsafe_allow_html=True)

history = st.session_state.get("history", [])
if not history:
    st.markdown('<div class="pp-history-empty">No passwords generated yet</div>', unsafe_allow_html=True)
else:
    rows = ""
    for h in history:
        rows += f"""
        <div class="pp-history-row">
            <div class="pp-history-pw">{h['pw']}</div>
            <div class="pp-history-meta">
                <span class="pp-history-grade" style="color:{h['color']};">{h['grade']}</span>
                <span class="pp-history-score">{h['score']}/100</span>
            </div>
        </div>"""
    st.markdown(f'<div class="pp-history">{rows}</div>', unsafe_allow_html=True)

    if st.button("Clear history", key="clear_hist"):
        st.session_state["history"] = []
        st.rerun()

# Footer
st.markdown("""
<div class="pp-footer">
    PASSPULSE &nbsp;·&nbsp; YOUR PASSWORDS ARE NEVER STORED OR SENT IN FULL
</div>
""", unsafe_allow_html=True)
