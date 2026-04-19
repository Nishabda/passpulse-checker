import streamlit as st
import hashlib
import requests
import secrets
import string
import math
import re

st.set_page_config(
    page_title="PassPulse — Password Strength Checker",
    page_icon="🔐",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Syne:wght@400;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0a0a0f;
    color: #e8e8f0;
    font-family: 'Syne', sans-serif;
}
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,255,180,0.07), transparent),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(80,0,255,0.05), transparent),
        #0a0a0f;
}
[data-testid="stMain"] { padding: 0 1rem; }

#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #00ffb4; border-radius: 2px; }

.hero { text-align: center; padding: 2rem 0 1.2rem; }
.hero-tag {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.25em;
    color: #00ffb4;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-size: clamp(2.2rem, 8vw, 3.2rem);
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, #ffffff 0%, #00ffb4 60%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-size: clamp(0.7rem, 2.5vw, 0.9rem);
    color: #6b7280;
    margin-top: 0.5rem;
    font-family: 'Share Tech Mono', monospace;
}

.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.4rem 1.6rem;
    margin: 0.8rem 0;
}
.card-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: #00ffb4;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}

.bar-wrap {
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
    margin: 0.5rem 0 0.3rem;
}
.bar-fill { height: 100%; border-radius: 999px; }

.score-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.28rem 0.85rem;
    border-radius: 999px;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    font-family: 'Share Tech Mono', monospace;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 0.7rem;
    margin: 0.8rem 0;
}
@media (max-width: 480px) {
    .metric-grid { grid-template-columns: 1fr 1fr; gap: 0.5rem; }
}
.metric-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 0.9rem 0.6rem;
    text-align: center;
}
.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.58rem;
    color: #6b7280;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
}
.metric-value {
    font-size: clamp(0.95rem, 3vw, 1.2rem);
    font-weight: 700;
    color: #e8e8f0;
    word-break: break-word;
}

.check-item {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.3rem 0;
    font-size: clamp(0.75rem, 2.5vw, 0.85rem);
    font-family: 'Share Tech Mono', monospace;
}
.check-dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }

.suggestion {
    background: rgba(251,191,36,0.07);
    border-left: 3px solid #fbbf24;
    border-radius: 0 8px 8px 0;
    padding: 0.5rem 0.75rem;
    margin: 0.35rem 0;
    font-size: clamp(0.75rem, 2.5vw, 0.83rem);
    color: #fcd34d;
    font-family: 'Share Tech Mono', monospace;
    line-height: 1.5;
}

.breach-safe {
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.3);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    color: #34d399;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.83rem;
    margin-top: 0.7rem;
    line-height: 1.5;
}
.breach-danger {
    background: rgba(248,113,113,0.08);
    border: 1px solid rgba(248,113,113,0.3);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    color: #f87171;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.83rem;
    margin-top: 0.7rem;
    line-height: 1.5;
}

.gen-box {
    background: rgba(0,0,0,0.4);
    border: 1px solid #00ffb4;
    border-radius: 10px;
    padding: 1rem 1.1rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: clamp(0.85rem, 2.5vw, 1rem);
    color: #00ffb4;
    letter-spacing: 0.04em;
    word-break: break-all;
    text-align: center;
    margin: 0.8rem 0 0.4rem;
    line-height: 1.6;
}

.tip-box {
    background: rgba(139,92,246,0.08);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 10px;
    padding: 0.75rem 1rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.78rem;
    color: #a78bfa;
    margin-top: 0.5rem;
    line-height: 1.5;
}

.empty-state {
    text-align: center;
    padding: 2.5rem 1rem;
    color: #2d3748;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem;
    line-height: 2;
}
.empty-icon { font-size: 2.5rem; margin-bottom: 0.5rem; }

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent);
    margin: 1.2rem 0;
}

/* Streamlit overrides */
[data-testid="stTextInput"] > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
    caret-color: #00ffb4;
    width: 100% !important;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #00ffb4 !important;
    box-shadow: 0 0 0 2px rgba(0,255,180,0.12) !important;
    outline: none !important;
}
/* Hide the default streamlit eye toggle on password field */
[data-testid="stTextInput"] button {
    display: none !important;
}

[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #00ffb4, #06b6d4) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1.4rem !important;
    width: 100% !important;
    transition: opacity 0.2s !important;
}
[data-testid="stButton"] > button:hover { opacity: 0.85 !important; }

[data-testid="stCheckbox"] > label {
    color: #9ca3af !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.82rem !important;
}
[data-testid="stCheckbox"] input:checked + div {
    background: #00ffb4 !important;
    border-color: #00ffb4 !important;
}

[data-testid="stSlider"] > div > div > div > div {
    background: #00ffb4 !important;
}

.stAlert { border-radius: 10px !important; font-family: 'Share Tech Mono', monospace !important; }

[data-testid="stColumn"] { padding: 0 0.25rem !important; }
</style>
""", unsafe_allow_html=True)


# ── Core Logic ─────────────────────────────────────────────────────────────────

COMMON_PASSWORDS = {
    "password", "123456", "password1", "qwerty", "abc123", "letmein",
    "monkey", "master", "dragon", "111111", "baseball", "iloveyou",
    "trustno1", "sunshine", "princess", "welcome", "shadow", "superman",
    "michael", "football", "batman", "admin", "login", "passw0rd",
    "p@ssword", "p@ssw0rd", "pa$$word", "pass123", "test123",
    "qwerty123", "1q2w3e4r", "12345678", "1234567890", "password123",
    "admin123", "root", "toor", "qwertyuiop", "asdfghjkl",
}

KEYBOARD_WALKS = [
    "qwerty", "asdf", "zxcv", "qazwsx", "1qaz", "2wsx",
    "qweasd", "asdfgh", "zxcvbn", "123456", "098765",
    "qwertyuiop", "asdfghjkl",
]

LEET_MAP = str.maketrans("@4310$!5|", "aaeiossil")


def normalize(pwd):
    return pwd.lower().translate(LEET_MAP)


def calculate_entropy(pwd):
    pool = 0
    if re.search(r"[a-z]", pwd): pool += 26
    if re.search(r"[A-Z]", pwd): pool += 26
    if re.search(r"\d", pwd):    pool += 10
    if re.search(r"[^a-zA-Z0-9]", pwd): pool += 32
    return 0.0 if pool == 0 else len(pwd) * math.log2(pool)


def crack_time_display(entropy):
    seconds = (2 ** entropy) / 1e10
    if seconds < 1:           return "< 1 second ⚡"
    if seconds < 60:          return f"{int(seconds)} seconds"
    if seconds < 3600:        return f"{int(seconds/60)} minutes"
    if seconds < 86400:       return f"{int(seconds/3600)} hours"
    if seconds < 2592000:     return f"{int(seconds/86400)} days"
    if seconds < 31536000:    return f"{int(seconds/2592000)} months"
    years = seconds / 31536000
    if years < 1000:          return f"{int(years)} years"
    if years < 1_000_000:     return f"{years/1000:.1f}K years"
    return "centuries+ 🛡️"


def check_hibp(password):
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        resp = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers={"User-Agent": "PassPulse-Checker"},
            timeout=6,
        )
        if resp.status_code != 200:
            return False, -1
        for line in resp.text.splitlines():
            h, count = line.split(":")
            if h == suffix:
                return True, int(count)
        return False, 0
    except Exception:
        return False, -1


def analyze_password(pwd):
    if not pwd:
        return {}
    norm = normalize(pwd)

    has_upper   = bool(re.search(r"[A-Z]", pwd))
    has_lower   = bool(re.search(r"[a-z]", pwd))
    has_digit   = bool(re.search(r"\d", pwd))
    has_special = bool(re.search(r"[^a-zA-Z0-9]", pwd))
    is_common   = norm in COMMON_PASSWORDS or pwd.lower() in COMMON_PASSWORDS
    has_walk    = any(w in norm for w in KEYBOARD_WALKS)
    has_repeats = bool(re.search(r"(.)\1{2,}", pwd))
    has_seq     = bool(re.search(r"(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi)", norm))
    has_date    = bool(re.search(r"(19|20)\d{2}|(\d{2}[\/\-\.]\d{2}[\/\-\.]\d{2,4})", pwd))
    e           = calculate_entropy(pwd)
    pool        = (26 if has_lower else 0) + (26 if has_upper else 0) + (10 if has_digit else 0) + (32 if has_special else 0)

    score = 0
    if len(pwd) >= 8:  score += 10
    if len(pwd) >= 12: score += 10
    if len(pwd) >= 16: score += 10
    if len(pwd) >= 20: score += 5
    if has_upper:      score += 10
    if has_lower:      score += 10
    if has_digit:      score += 10
    if has_special:    score += 15
    if e >= 50:        score += 10
    if e >= 70:        score += 10
    if e >= 90:        score += 5
    if is_common:      score -= 40
    if has_walk:       score -= 15
    if has_repeats:    score -= 10
    if has_seq:        score -= 8
    if has_date:       score -= 5
    if len(pwd) < 8:   score -= 20
    score = max(0, min(100, score))

    if score < 20:   grade, color = "💀 Critically Weak", "#ef4444"
    elif score < 40: grade, color = "⚠️ Weak",            "#f97316"
    elif score < 60: grade, color = "🔶 Fair",            "#eab308"
    elif score < 80: grade, color = "✅ Strong",          "#22c55e"
    else:            grade, color = "🛡️ Fortress",        "#00ffb4"

    suggestions = []
    if len(pwd) < 12:  suggestions.append("→ Use at least 12 characters (16+ is ideal)")
    if not has_upper:  suggestions.append("→ Add uppercase letters (A–Z)")
    if not has_lower:  suggestions.append("→ Add lowercase letters (a–z)")
    if not has_digit:  suggestions.append("→ Include numbers (0–9)")
    if not has_special:suggestions.append("→ Add special characters like !@#$%^&*")
    if is_common:      suggestions.append("→ This is a well-known password — change it immediately!")
    if has_walk:       suggestions.append("→ Avoid keyboard patterns like 'qwerty' or '12345'")
    if has_repeats:    suggestions.append("→ Avoid repeated characters like 'aaa' or '111'")
    if has_seq:        suggestions.append("→ Avoid sequential patterns like 'abc' or '123'")
    if has_date:       suggestions.append("→ Avoid dates — they are easy to guess")
    if not suggestions:suggestions.append("✓ No obvious weaknesses detected. Great password!")

    return dict(
        length=len(pwd), has_upper=has_upper, has_lower=has_lower,
        has_digit=has_digit, has_special=has_special, is_common=is_common,
        has_walk=has_walk, has_repeats=has_repeats, has_seq=has_seq,
        has_date=has_date, entropy=e, crack_time=crack_time_display(e),
        pool=pool, score=score, grade=grade, color=color, suggestions=suggestions,
    )


def generate_password(length=20, use_upper=True, use_digits=True, use_special=True):
    lower   = string.ascii_lowercase
    upper   = string.ascii_uppercase
    digits  = string.digits
    special = "!@#$%^&*()-_=+[]{}|;:,.<>?"
    pool    = lower
    req     = [secrets.choice(lower)]
    if use_upper:   pool += upper;   req.append(secrets.choice(upper))
    if use_digits:  pool += digits;  req.append(secrets.choice(digits))
    if use_special: pool += special; req.append(secrets.choice(special))
    rest = [secrets.choice(pool) for _ in range(length - len(req))]
    all_chars = req + rest
    secrets.SystemRandom().shuffle(all_chars)
    return "".join(all_chars)


# ── UI ─────────────────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero">
    <div class="hero-tag">// security tool v1.0</div>
    <div class="hero-title">PassPulse</div>
    <div class="hero-sub">Real-time analysis · Breach detection · Entropy scoring</div>
</div>
""", unsafe_allow_html=True)

# ── Password Input ─────────────────────────────────────────────────────────────
st.markdown('<div class="card"><div class="card-title">// enter your password</div>', unsafe_allow_html=True)

show_pw = st.session_state.get("show_pw", False)
password = st.text_input(
    "Password",
    type="default" if show_pw else "password",
    placeholder="Type your password here...",
    label_visibility="collapsed",
    key="pw_input",
)

toggle_label = "🙈 Hide Password" if show_pw else "👁 Show Password"
if st.button(toggle_label, key="toggle_btn"):
    st.session_state["show_pw"] = not show_pw
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# ── Analysis ───────────────────────────────────────────────────────────────────
if password:
    d = analyze_password(password)

    # Strength bar
    st.markdown(f"""
    <div class="card">
        <div class="card-title">// strength</div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem; flex-wrap:wrap; gap:0.4rem;">
            <span class="score-badge" style="background:{d['color']}22; color:{d['color']}; border:1px solid {d['color']}55;">{d['grade']}</span>
            <span style="font-family:'Share Tech Mono',monospace; font-size:0.88rem; color:{d['color']}; font-weight:700;">{d['score']} / 100</span>
        </div>
        <div class="bar-wrap">
            <div class="bar-fill" style="width:{d['score']}%; background:linear-gradient(90deg,{d['color']},{d['color']}99);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    crack_color = "#f87171" if d['score'] < 40 else "#34d399"
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-box">
            <div class="metric-label">Entropy</div>
            <div class="metric-value" style="color:#00ffb4;">{d['entropy']:.1f} bits</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Crack Time</div>
            <div class="metric-value" style="color:{crack_color}; font-size:clamp(0.78rem,2.2vw,1rem);">{d['crack_time']}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Length</div>
            <div class="metric-value">{d['length']} chars</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Char Pool</div>
            <div class="metric-value" style="color:#00ffb4;">{d['pool']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Checklist
    checks = [
        (d["length"] >= 12,  f"Length ≥ 12  ({d['length']} chars)"),
        (d["has_upper"],      "Uppercase letters (A–Z)"),
        (d["has_lower"],      "Lowercase letters (a–z)"),
        (d["has_digit"],      "Numbers (0–9)"),
        (d["has_special"],    "Special characters (!@#$...)"),
        (not d["is_common"],  "Not a common password"),
        (not d["has_walk"],   "No keyboard walk patterns"),
        (not d["has_repeats"],"No repeated characters"),
        (not d["has_seq"],    "No sequential patterns"),
        (not d["has_date"],   "No date patterns"),
    ]
    items = "".join(
        f'<div class="check-item"><div class="check-dot" style="background:{"#34d399" if ok else "#f87171"};"></div>'
        f'<span style="color:{"#34d399" if ok else "#f87171"};">{"✓" if ok else "✗"} {label}</span></div>'
        for ok, label in checks
    )
    st.markdown(f'<div class="card"><div class="card-title">// checklist</div>{items}</div>', unsafe_allow_html=True)

    # Suggestions
    if d["suggestions"]:
        suggs = "".join(f'<div class="suggestion">{s}</div>' for s in d["suggestions"])
        st.markdown(f'<div class="card"><div class="card-title">// recommendations</div>{suggs}</div>', unsafe_allow_html=True)

    # Breach Check
    st.markdown("""
    <div class="card">
        <div class="card-title">// data breach check</div>
        <div style="font-family:'Share Tech Mono',monospace; font-size:0.72rem; color:#4b5563; margin-bottom:0.9rem; line-height:1.6;">
            🔒 Privacy-safe — only a 5-character hash prefix is sent to Have I Been Pwned.<br>
            Your actual password never leaves your device.
        </div>
    """, unsafe_allow_html=True)

    if st.button("🔍 Check Against Data Breaches", key="breach_btn"):
        with st.spinner("Checking against 900M+ breached passwords..."):
            pwned, count = check_hibp(password)
        if count == -1:
            st.warning("⚡ Could not reach the HIBP API. Check your internet connection.")
        elif pwned:
            st.markdown(f'<div class="breach-danger">🚨 PWNED! Found in <strong>{count:,}</strong> data breach(es).<br>Stop using this password immediately.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="breach-safe">✅ Not found in any known data breaches.<br>This password has not been publicly exposed.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state">
        <div class="empty-icon">🔐</div>
        Type a password above to see your full analysis<br>
        <span style="font-size:0.7rem; color:#1f2937;">strength · entropy · crack time · breach check</span>
    </div>
    """, unsafe_allow_html=True)

# ── Generator ──────────────────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown('<div class="card"><div class="card-title">// password generator</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    use_upper   = st.checkbox("Uppercase", value=True)
with col2:
    use_digits  = st.checkbox("Numbers",   value=True)
with col3:
    use_special = st.checkbox("Symbols",   value=True)

pw_length = st.slider("Password Length", min_value=8, max_value=64, value=20, step=1)

if st.button("⚡ Generate Strong Password", key="gen_btn"):
    st.session_state["gen_pw"] = generate_password(pw_length, use_upper, use_digits, use_special)

if "gen_pw" in st.session_state:
    gen_pw   = st.session_state["gen_pw"]
    gen_data = analyze_password(gen_pw)
    st.markdown(f'<div class="gen-box">{gen_pw}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align:center; font-family:'Share Tech Mono',monospace; font-size:0.75rem; color:#4b5563; margin-bottom:0.5rem;">
        <span style="color:{gen_data['color']};">{gen_data['grade']}</span>
        &nbsp;·&nbsp; {gen_data['entropy']:.0f} bits
        &nbsp;·&nbsp; {gen_data['crack_time']}
    </div>
    <div class="tip-box">
        💡 <strong>Tip:</strong> Copy this password and store it in a password manager like Bitwarden or 1Password.
        Never save passwords in notes or messages.
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:1.8rem 0 0.8rem; font-family:'Share Tech Mono',monospace; font-size:0.6rem; color:#1f2937; letter-spacing:0.12em;">
    PASSPULSE · BUILT WITH PYTHON + STREAMLIT · YOUR PASSWORDS ARE NEVER STORED OR TRANSMITTED
</div>
""", unsafe_allow_html=True)
