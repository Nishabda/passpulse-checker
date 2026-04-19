import streamlit as st
import hashlib
import requests
import secrets
import string
import math
import re
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PassPulse — Password Strength Checker",
    page_icon="🔐",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
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
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(0,255,180,0.08), transparent),
        radial-gradient(ellipse 60% 40% at 80% 80%, rgba(80,0,255,0.06), transparent),
        #0a0a0f;
}

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0f; }
::-webkit-scrollbar-thumb { background: #00ffb4; border-radius: 2px; }

/* Hero title */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
}
.hero-tag {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: #00ffb4;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    line-height: 1.05;
    background: linear-gradient(135deg, #ffffff 0%, #00ffb4 60%, #8b5cf6 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.02em;
}
.hero-sub {
    font-size: 0.95rem;
    color: #6b7280;
    margin-top: 0.6rem;
    font-family: 'Share Tech Mono', monospace;
}

/* Card container */
.card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin: 1rem 0;
    backdrop-filter: blur(12px);
}
.card-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.2em;
    color: #00ffb4;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

/* Strength bar */
.bar-wrap {
    background: rgba(255,255,255,0.06);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
    margin: 0.5rem 0 0.3rem;
}
.bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.4s ease, background 0.4s ease;
}

/* Score badge */
.score-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.3rem 0.9rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    font-family: 'Share Tech Mono', monospace;
}

/* Metric row */
.metric-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.8rem;
    margin: 1rem 0;
}
.metric-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: #6b7280;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-size: 1.3rem;
    font-weight: 700;
    color: #e8e8f0;
}
.metric-value.accent { color: #00ffb4; }

/* Checklist */
.check-item {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.35rem 0;
    font-size: 0.88rem;
    color: #9ca3af;
    font-family: 'Share Tech Mono', monospace;
}
.check-item.pass { color: #34d399; }
.check-item.fail { color: #f87171; }
.check-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}
.check-item.pass .check-dot { background: #34d399; }
.check-item.fail .check-dot { background: #f87171; }

/* Suggestions */
.suggestion {
    background: rgba(251,191,36,0.07);
    border-left: 3px solid #fbbf24;
    border-radius: 0 8px 8px 0;
    padding: 0.5rem 0.8rem;
    margin: 0.4rem 0;
    font-size: 0.85rem;
    color: #fcd34d;
    font-family: 'Share Tech Mono', monospace;
}

/* Breach result */
.breach-safe {
    background: rgba(52,211,153,0.08);
    border: 1px solid rgba(52,211,153,0.3);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    color: #34d399;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
}
.breach-danger {
    background: rgba(248,113,113,0.08);
    border: 1px solid rgba(248,113,113,0.3);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    color: #f87171;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
}

/* Generated password box */
.gen-box {
    background: rgba(0,0,0,0.4);
    border: 1px solid #00ffb4;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.1rem;
    color: #00ffb4;
    letter-spacing: 0.05em;
    word-break: break-all;
    text-align: center;
    margin: 0.8rem 0;
}

/* Streamlit widget overrides */
[data-testid="stTextInput"] > div > div > input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 1rem !important;
    padding: 0.7rem 1rem !important;
    caret-color: #00ffb4;
}
[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #00ffb4 !important;
    box-shadow: 0 0 0 2px rgba(0,255,180,0.15) !important;
    outline: none !important;
}

[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #00ffb4, #06b6d4) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.03em !important;
    padding: 0.6rem 1.4rem !important;
    transition: opacity 0.2s !important;
}
[data-testid="stButton"] > button:hover { opacity: 0.85 !important; }

[data-testid="stSlider"] > div { padding: 0; }

.stCheckbox > label { color: #9ca3af !important; font-family: 'Share Tech Mono', monospace !important; font-size: 0.82rem !important; }
.stSelectbox > div > div { background: rgba(255,255,255,0.04) !important; border-color: rgba(255,255,255,0.12) !important; border-radius: 10px !important; }

[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 12px !important;
}

.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Core Logic ────────────────────────────────────────────────────────────────

COMMON_PASSWORDS = {
    "password", "123456", "password1", "qwerty", "abc123", "letmein",
    "monkey", "master", "dragon", "111111", "baseball", "iloveyou",
    "trustno1", "sunshine", "princess", "welcome", "shadow", "superman",
    "michael", "football", "batman", "admin", "login", "passw0rd",
    "p@ssword", "p@ssw0rd", "pa$$word", "pass123", "test123",
    "qwerty123", "1q2w3e4r", "12345678", "1234567890",
}

KEYBOARD_WALKS = [
    "qwerty", "asdf", "zxcv", "qazwsx", "1qaz", "2wsx",
    "qweasd", "asdfgh", "zxcvbn", "123456", "098765",
    "qwertyuiop", "asdfghjkl",
]

LEET_MAP = str.maketrans("@4310$!5|", "aaeiossil")


def normalize_password(pwd: str) -> str:
    return pwd.lower().translate(LEET_MAP)


def calculate_entropy(pwd: str) -> float:
    pool = 0
    if re.search(r"[a-z]", pwd): pool += 26
    if re.search(r"[A-Z]", pwd): pool += 26
    if re.search(r"\d", pwd):    pool += 10
    if re.search(r"[^a-zA-Z0-9]", pwd): pool += 32
    if pool == 0:
        return 0.0
    return len(pwd) * math.log2(pool)


def crack_time_display(entropy: float) -> str:
    """Estimate crack time at 10 billion guesses/sec (modern GPU cluster)."""
    guesses = 2 ** entropy
    seconds = guesses / 1e10
    if seconds < 1:         return "< 1 second"
    if seconds < 60:        return f"{int(seconds)} seconds"
    if seconds < 3600:      return f"{int(seconds/60)} minutes"
    if seconds < 86400:     return f"{int(seconds/3600)} hours"
    if seconds < 2592000:   return f"{int(seconds/86400)} days"
    if seconds < 31536000:  return f"{int(seconds/2592000)} months"
    years = seconds / 31536000
    if years < 1000:        return f"{int(years)} years"
    if years < 1_000_000:   return f"{years/1000:.1f}K years"
    return "centuries+"


def check_hibp(password: str) -> tuple[bool, int]:
    """k-Anonymity: only first 5 chars of SHA1 hash leave your machine."""
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    try:
        resp = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}",
            headers={"User-Agent": "PassPulse-Checker"},
            timeout=5,
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


def analyze_password(pwd: str) -> dict:
    if not pwd:
        return {}

    norm = normalize_password(pwd)
    results = {}

    # Basic checks
    results["length"] = len(pwd)
    results["has_upper"] = bool(re.search(r"[A-Z]", pwd))
    results["has_lower"] = bool(re.search(r"[a-z]", pwd))
    results["has_digit"] = bool(re.search(r"\d", pwd))
    results["has_special"] = bool(re.search(r"[^a-zA-Z0-9]", pwd))
    results["entropy"] = calculate_entropy(pwd)
    results["crack_time"] = crack_time_display(results["entropy"])

    # Pattern detections
    results["is_common"] = norm in COMMON_PASSWORDS or pwd.lower() in COMMON_PASSWORDS
    results["has_keyboard_walk"] = any(walk in norm for walk in KEYBOARD_WALKS)
    results["has_repeats"] = bool(re.search(r"(.)\1{2,}", pwd))
    results["has_sequences"] = bool(
        re.search(r"(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi)", norm)
    )
    results["has_date_pattern"] = bool(
        re.search(r"(19|20)\d{2}|(\d{2}[/\-\.]\d{2}[/\-\.]\d{2,4})", pwd)
    )

    # Scoring (0–100)
    score = 0
    if results["length"] >= 8:  score += 10
    if results["length"] >= 12: score += 10
    if results["length"] >= 16: score += 10
    if results["length"] >= 20: score += 5
    if results["has_upper"]:    score += 10
    if results["has_lower"]:    score += 10
    if results["has_digit"]:    score += 10
    if results["has_special"]:  score += 15

    # Entropy bonus
    if results["entropy"] >= 50:  score += 10
    if results["entropy"] >= 70:  score += 10
    if results["entropy"] >= 90:  score += 5

    # Penalties
    if results["is_common"]:         score -= 40
    if results["has_keyboard_walk"]: score -= 15
    if results["has_repeats"]:       score -= 10
    if results["has_sequences"]:     score -= 8
    if results["has_date_pattern"]:  score -= 5
    if results["length"] < 8:        score -= 20

    results["score"] = max(0, min(100, score))

    # Grade
    s = results["score"]
    if s < 20:   results["grade"] = ("💀 Critically Weak", "#ef4444", 1)
    elif s < 40: results["grade"] = ("⚠️ Weak",            "#f97316", 2)
    elif s < 60: results["grade"] = ("🔶 Fair",            "#eab308", 3)
    elif s < 80: results["grade"] = ("✅ Strong",          "#22c55e", 4)
    else:        results["grade"] = ("🛡️ Fortress",        "#00ffb4", 5)

    # Suggestions
    suggestions = []
    if results["length"] < 12:
        suggestions.append("→ Use at least 12 characters (16+ is ideal)")
    if not results["has_upper"]:
        suggestions.append("→ Add uppercase letters (A–Z)")
    if not results["has_lower"]:
        suggestions.append("→ Add lowercase letters (a–z)")
    if not results["has_digit"]:
        suggestions.append("→ Include numbers (0–9)")
    if not results["has_special"]:
        suggestions.append("→ Add special characters (!@#$%^&*)")
    if results["is_common"]:
        suggestions.append("→ This is a commonly known password — change it immediately")
    if results["has_keyboard_walk"]:
        suggestions.append("→ Avoid keyboard patterns like 'qwerty' or '12345'")
    if results["has_repeats"]:
        suggestions.append("→ Avoid repeated characters like 'aaa' or '111'")
    if results["has_sequences"]:
        suggestions.append("→ Avoid sequential patterns like 'abc' or '123'")
    if results["has_date_pattern"]:
        suggestions.append("→ Avoid dates — they're easy to guess")
    if not suggestions:
        suggestions.append("✓ Excellent password! No obvious weaknesses detected.")
    results["suggestions"] = suggestions

    return results


def generate_password(length=20, use_upper=True, use_digits=True, use_special=True) -> str:
    chars = string.ascii_lowercase
    required = [secrets.choice(string.ascii_lowercase)]
    if use_upper:
        chars += string.ascii_uppercase
        required.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        chars += string.digits
        required.append(secrets.choice(string.digits))
    if use_special:
        special = "!@#$%^&*()-_=+[]{}|;:,.<>?"
        chars += special
        required.append(secrets.choice(special))
    rest = [secrets.choice(chars) for _ in range(length - len(required))]
    all_chars = required + rest
    secrets.SystemRandom().shuffle(all_chars)
    return "".join(all_chars)


# ── UI ────────────────────────────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero">
    <div class="hero-tag">// security tool v1.0</div>
    <div class="hero-title">PassPulse</div>
    <div class="hero-sub">Real-time password analysis · Breach detection · AI-grade scoring</div>
</div>
""", unsafe_allow_html=True)

# Input
st.markdown('<div class="card"><div class="card-title">// enter password</div>', unsafe_allow_html=True)

col_pw, col_show = st.columns([5, 1])
with col_pw:
    show_pw = st.session_state.get("show_pw", False)
    password = st.text_input(
        "Password",
        type="default" if show_pw else "password",
        placeholder="Type your password here...",
        label_visibility="collapsed",
        key="pw_input",
    )
with col_show:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("👁" if not show_pw else "🙈", help="Toggle visibility"):
        st.session_state["show_pw"] = not show_pw
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Analysis
if password:
    data = analyze_password(password)
    grade_label, grade_color, grade_level = data["grade"]
    bar_pct = data["score"]

    # Strength bar
    st.markdown(f"""
    <div class="card">
        <div class="card-title">// strength analysis</div>
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.4rem;">
            <span class="score-badge" style="background:{grade_color}22; color:{grade_color}; border:1px solid {grade_color}55;">
                {grade_label}
            </span>
            <span style="font-family:'Share Tech Mono',monospace; font-size:0.9rem; color:{grade_color}; font-weight:700;">{bar_pct}/100</span>
        </div>
        <div class="bar-wrap">
            <div class="bar-fill" style="width:{bar_pct}%; background:linear-gradient(90deg,{grade_color},{grade_color}aa);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Metrics
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-box">
            <div class="metric-label">Entropy</div>
            <div class="metric-value accent">{data['entropy']:.1f} bits</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Crack Time</div>
            <div class="metric-value" style="font-size:1rem; color:{'#f87171' if data['score']<40 else '#34d399'};">{data['crack_time']}</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Length</div>
            <div class="metric-value">{data['length']} chars</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Character Pool</div>
            <div class="metric-value accent">{sum([26 if data['has_lower'] else 0, 26 if data['has_upper'] else 0, 10 if data['has_digit'] else 0, 32 if data['has_special'] else 0])}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Checklist
    checks = [
        (data["length"] >= 12, f"Length ≥ 12  ({data['length']} chars)"),
        (data["has_upper"],    "Uppercase letters"),
        (data["has_lower"],    "Lowercase letters"),
        (data["has_digit"],    "Numbers"),
        (data["has_special"],  "Special characters"),
        (not data["is_common"],        "Not a common password"),
        (not data["has_keyboard_walk"],"No keyboard walk patterns"),
        (not data["has_repeats"],      "No repeated characters"),
        (not data["has_sequences"],    "No sequential patterns"),
        (not data["has_date_pattern"], "No date patterns"),
    ]

    items_html = ""
    for passed, label in checks:
        cls = "pass" if passed else "fail"
        icon = "✓" if passed else "✗"
        items_html += f'<div class="check-item {cls}"><div class="check-dot"></div>{icon} {label}</div>'

    st.markdown(f"""
    <div class="card">
        <div class="card-title">// criteria checklist</div>
        {items_html}
    </div>
    """, unsafe_allow_html=True)

    # Suggestions
    sugg_html = "".join(f'<div class="suggestion">{s}</div>' for s in data["suggestions"])
    st.markdown(f"""
    <div class="card">
        <div class="card-title">// recommendations</div>
        {sugg_html}
    </div>
    """, unsafe_allow_html=True)

    # Breach Check
    st.markdown('<div class="card"><div class="card-title">// breach check (Have I Been Pwned)</div>', unsafe_allow_html=True)
    st.markdown('<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.75rem;color:#6b7280;margin-bottom:0.8rem;">Your password is never sent — only a 5-char hash prefix leaves your device (k-Anonymity).</p>', unsafe_allow_html=True)

    if st.button("🔍 Check Against Data Breaches"):
        with st.spinner("Querying Have I Been Pwned..."):
            pwned, count = check_hibp(password)

        if count == -1:
            st.warning("⚡ Could not reach the HIBP API. Check your internet connection.")
        elif pwned:
            st.markdown(f'<div class="breach-danger">🚨 PWNED! This password appeared in <strong>{count:,}</strong> data breach(es). Do NOT use it.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="breach-safe">✅ Not found in any known data breaches. You\'re clear.</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div style="text-align:center; padding:2rem; color:#374151; font-family:'Share Tech Mono',monospace; font-size:0.85rem;">
        ↑ Enter a password above to begin analysis
    </div>
    """, unsafe_allow_html=True)

# Divider
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# Password Generator
st.markdown('<div class="card"><div class="card-title">// password generator</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    use_upper   = st.checkbox("Uppercase", value=True)
    use_digits  = st.checkbox("Numbers",   value=True)
with col2:
    use_special = st.checkbox("Symbols",   value=True)
with col3:
    pass

pw_length = st.slider("Length", min_value=8, max_value=64, value=20, step=1)

if st.button("⚡ Generate Strong Password"):
    gen = generate_password(pw_length, use_upper, use_digits, use_special)
    st.session_state["gen_pw"] = gen

if "gen_pw" in st.session_state:
    gen_pw = st.session_state["gen_pw"]
    st.markdown(f'<div class="gen-box">{gen_pw}</div>', unsafe_allow_html=True)

    gen_data = analyze_password(gen_pw)
    if gen_data:
        g_label, g_color, _ = gen_data["grade"]
        st.markdown(f"""
        <div style="display:flex; gap:1rem; font-family:'Share Tech Mono',monospace; font-size:0.8rem; color:#6b7280; justify-content:center; margin-top:0.5rem;">
            <span style="color:{g_color};">{g_label}</span>
            <span>·</span>
            <span>{gen_data['entropy']:.0f} bits entropy</span>
            <span>·</span>
            <span>Crack time: {gen_data['crack_time']}</span>
        </div>
        """, unsafe_allow_html=True)
    st.info("💡 Copy the password above and save it in a password manager.")

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align:center; padding:2rem 0 1rem; font-family:'Share Tech Mono',monospace; font-size:0.65rem; color:#374151; letter-spacing:0.1em;">
    PASSPULSE · BUILT WITH PYTHON + STREAMLIT · NO PASSWORDS ARE STORED OR TRANSMITTED IN FULL
</div>
""", unsafe_allow_html=True)
