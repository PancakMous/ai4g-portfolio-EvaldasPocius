import html

import streamlit as st
from dutch4you_core import process_text

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Dutch4You: understand your Dutch letters",
    page_icon="🇳🇱",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# STYLES
# Palette: paper grey, ink navy, Dutch blue for structure,
# oranje reserved for deadlines and anything time-sensitive.
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Public+Sans:wght@400;500;600;700&display=swap');

:root {
    color-scheme: light;
    --paper: #F6F7F9;
    --card: #FFFFFF;
    --ink: #0F1B2D;
    --muted: #5B6675;
    --line: #DDE1E7;
    --blue: #154273;
    --blue-dark: #0F3357;
    --blue-soft: #E8EEF6;
    --orange: #D9480F;
    --orange-soft: #FFF1E8;
    --green: #1E7B4F;
    --amber: #C98A00;
    --display: 'Bricolage Grotesque', 'Public Sans', system-ui, sans-serif;
}

/* ---------- Base ---------- */

.stApp {
    background: var(--paper);
    color: var(--ink);
}

.stApp, .stApp p, .stApp li, .stApp label, .stApp textarea, .stApp button {
    font-family: 'Public Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
}

.stApp [data-testid="stMarkdownContainer"] p,
.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stCheckbox"] p,
.stApp [data-testid="stCaptionContainer"] {
    color: var(--ink);
}

.block-container {
    max-width: 880px;
    padding-top: 32px;
    padding-bottom: 56px;
}

#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }

/* ---------- Header ---------- */

.brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: var(--display);
    font-weight: 700;
    font-size: 20px;
    letter-spacing: -0.01em;
    color: var(--ink);
}

.flag {
    display: inline-block;
    width: 24px;
    height: 17px;
    border-radius: 2px;
    box-shadow: 0 0 0 1px var(--line);
    background: linear-gradient(#AE1C28 33.33%, #FFFFFF 33.33% 66.66%, #21468B 66.66%);
}

.headline {
    font-family: var(--display);
    font-weight: 800;
    font-size: clamp(34px, 6vw, 52px);
    line-height: 1.05;
    letter-spacing: -0.03em;
    color: var(--ink);
    margin: 40px 0 14px 0;
}

.lede {
    max-width: 56ch;
    color: var(--muted);
    font-size: 17px;
    line-height: 1.6;
    margin-bottom: 30px;
}

/* ---------- Inputs ---------- */

.stApp [data-testid="stWidgetLabel"] p,
.stApp [data-testid="stCaptionContainer"] {
    color: var(--muted);
    font-size: 14px;
    font-weight: 600;
}

[data-baseweb="textarea"] {
    background: var(--card) !important;
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
}

[data-baseweb="textarea"]:focus-within {
    border-color: var(--blue) !important;
    box-shadow: 0 0 0 3px rgba(21, 66, 115, 0.15) !important;
}

.stApp textarea {
    background: var(--card) !important;
    color: var(--ink) !important;
    font-size: 16px !important;
    line-height: 1.65 !important;
}

.hint {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.5;
    margin: 2px 0 14px 0;
}

/* ---------- Buttons ---------- */

[data-testid="stBaseButton-primary"],
button[kind="primary"] {
    height: 48px;
    border-radius: 10px;
    background: var(--blue) !important;
    border: 1px solid var(--blue) !important;
    font-weight: 600;
    font-size: 16px;
    transition: background 0.15s ease;
}

[data-testid="stBaseButton-primary"] p,
button[kind="primary"] p { color: #FFFFFF !important; }

[data-testid="stBaseButton-primary"]:hover,
button[kind="primary"]:hover {
    background: var(--blue-dark) !important;
    border-color: var(--blue-dark) !important;
}

[data-testid="stBaseButton-secondary"],
button[kind="secondary"] {
    height: 48px;
    border-radius: 10px;
    background: var(--card);
    border: 1px solid var(--line);
    color: var(--ink);
    font-weight: 600;
}

[data-testid="stBaseButton-secondary"] p,
button[kind="secondary"] p { color: var(--ink); }

[data-testid="stBaseButton-secondary"]:hover,
button[kind="secondary"]:hover {
    border-color: var(--blue);
}

[data-testid="stBaseButton-secondary"]:hover p,
button[kind="secondary"]:hover p { color: var(--blue); }

.stApp button:focus-visible {
    outline: 3px solid rgba(21, 66, 115, 0.45) !important;
    outline-offset: 2px;
}

/* ---------- To-do panel (the one loud element) ---------- */

.space { height: 24px; }

.st-key-todo {
    background: var(--card);
    border: 1px solid var(--line);
    border-top: 4px solid var(--orange);
    border-radius: 12px;
    padding: 24px 26px;
    animation: rise 0.35s ease-out;
}

@keyframes rise {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: none; }
}

@media (prefers-reduced-motion: reduce) {
    .st-key-todo { animation: none; }
}

@media (min-width: 640px) {
    .st-key-todo [data-testid="stColumn"]:last-child,
    .st-key-todo [data-testid="column"]:last-child {
        border-left: 1px solid var(--line);
        padding-left: 24px;
    }
}

.panel-title {
    font-family: var(--display);
    font-weight: 700;
    font-size: 21px;
    letter-spacing: -0.01em;
    margin-bottom: 10px;
}

.stApp [data-testid="stCheckbox"] label p {
    font-size: 16px;
    font-weight: 500;
    line-height: 1.5;
}

.stApp [data-testid="stCheckbox"] label:has(input:checked) p {
    color: var(--muted);
    text-decoration: line-through;
}

.fact { margin-bottom: 18px; }

.fact-label {
    color: var(--muted);
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 4px;
}

.fact-main {
    font-family: var(--display);
    font-weight: 700;
    font-size: 26px;
    line-height: 1.2;
    letter-spacing: -0.01em;
    color: var(--ink);
}

.fact-main.deadline { color: var(--orange); }

.fact-none {
    color: var(--muted);
    font-size: 15px;
}

.quiet {
    background: var(--card);
    border: 1px dashed var(--line);
    border-radius: 12px;
    padding: 18px 20px;
    color: var(--muted);
    font-size: 15px;
    line-height: 1.6;
}

/* ---------- Translation + explanation ---------- */

.doc {
    border-radius: 12px;
    padding: 20px 22px;
}

.doc.english {
    background: var(--card);
    border: 1px solid var(--line);
}

.doc.original {
    background: var(--blue-soft);
    border: 1px solid #D3DEEC;
}

.doc-label {
    color: var(--muted);
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 10px;
}

.doc-body {
    color: var(--ink);
    font-size: 16px;
    line-height: 1.7;
}

.doc.original .doc-body {
    color: #33465F;
    font-size: 15px;
}

.doc.explain .doc-body { max-width: 68ch; }

/* ---------- Confidence + note ---------- */

.conf {
    display: inline-flex;
    align-items: center;
    gap: 9px;
    font-size: 14px;
    line-height: 1.4;
    color: var(--ink);
}

.conf::before {
    content: "";
    flex: none;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--c);
}

.conf-high { --c: var(--green); }
.conf-medium { --c: var(--amber); }
.conf-low { --c: var(--orange); }

.note {
    background: var(--orange-soft);
    border-left: 4px solid var(--orange);
    border-radius: 8px;
    padding: 14px 16px;
    font-size: 15px;
    line-height: 1.6;
    margin-top: 14px;
    color: var(--ink);
}

.st-key-meta [data-testid="stBaseButton-secondary"],
.st-key-meta button[kind="secondary"] { height: 42px; }

[data-testid="stExpander"] {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 10px;
}

/* ---------- How it works (empty state) ---------- */

.steps {
    display: flex;
    flex-wrap: wrap;
    gap: 24px 32px;
    margin-top: 44px;
}

.step {
    flex: 1 1 210px;
    display: flex;
    gap: 12px;
}

.step-n {
    flex: none;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--blue);
    color: #FFFFFF;
    font-size: 14px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
}

.step-title { font-weight: 700; margin-bottom: 2px; color: var(--ink); }

.step-text {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.5;
}

/* ---------- Footer ---------- */

.site-note {
    max-width: 70ch;
    margin-top: 56px;
    padding-top: 18px;
    border-top: 1px solid var(--line);
    color: var(--muted);
    font-size: 13px;
    line-height: 1.6;
}
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# DATA + HELPERS
# ============================================================

EXAMPLES = {
    "Housing": (
        "U dient uiterlijk 30 september uw documenten in te leveren. "
        "Als u dit niet op tijd doet, kan uw aanvraag vertraging oplopen."
    ),
    "University": (
        "De deadline voor het indienen van uw opdracht is vrijdag 4 oktober "
        "om 23:59 uur. Zorg ervoor dat u de opdracht via Brightspace indient."
    ),
    "Municipality": (
        "U wordt verzocht om vóór 15 oktober een afspraak te maken bij "
        "de gemeente voor het registreren van uw adres."
    ),
    "Bank": (
        "Wij verzoeken u om vóór 1 oktober uw identiteitsbewijs en "
        "bewijs van verblijf aan te leveren."
    ),
}

CONFIDENCE = {
    "high": "High confidence",
    "medium": "Medium confidence. Double-check dates and amounts.",
    "low": "Low confidence. Check the original before you act.",
}


def h(markup: str) -> str:
    """Strip indentation and line breaks so Markdown never turns HTML into a code block."""
    return "".join(line.strip() for line in markup.strip().splitlines())


def render(markup: str) -> None:
    st.markdown(h(markup), unsafe_allow_html=True)


def esc(value) -> str:
    """Escape model output before it goes into HTML, keeping line breaks."""
    return html.escape(str(value)).replace("\n", "<br>")


def as_list(value) -> list:
    if not value:
        return []
    if isinstance(value, (list, tuple)):
        return [str(v).strip() for v in value if str(v).strip()]
    return [str(value).strip()]


def extract(result: dict):
    key_info = result.get("key_info") or {}
    return (
        as_list(key_info.get("deadlines")),
        as_list(key_info.get("amounts")),
        as_list(key_info.get("required_actions")),
    )


def facts_html(label: str, values: list, empty: str, accent: bool = False) -> str:
    if values:
        css = "fact-main deadline" if accent else "fact-main"
        body = "".join(f'<div class="{css}">{esc(v)}</div>' for v in values)
    else:
        body = f'<div class="fact-none">{empty}</div>'
    return f'<div class="fact"><div class="fact-label">{label}</div>{body}</div>'


def keyed_container(key: str, bordered: bool = False):
    """st.container(key=...) needs Streamlit 1.39+. Fall back gracefully on older versions."""
    try:
        return st.container(key=key)
    except TypeError:
        return st.container(border=True) if bordered else st.container()


def centered_columns(spec, **kwargs):
    """vertical_alignment needs Streamlit 1.36+. Fall back gracefully on older versions."""
    try:
        return st.columns(spec, vertical_alignment="center", **kwargs)
    except TypeError:
        return st.columns(spec, **kwargs)


def build_summary(result: dict, source: str) -> str:
    deadlines, amounts, actions = extract(result)
    lines = ["Dutch4You summary", ""]
    if actions:
        lines += ["What you need to do:"] + [f"- {a}" for a in actions] + [""]
    if deadlines:
        lines += ["Deadline:"] + [f"- {d}" for d in deadlines] + [""]
    if amounts:
        lines += ["Amount:"] + [f"- {a}" for a in amounts] + [""]
    lines += [
        "In English:",
        str(result.get("translation", "")),
        "",
        "What this means:",
        str(result.get("explanation", "")),
        "",
        "Dutch original:",
        source,
    ]
    return "\n".join(lines)


# ============================================================
# STATE + CALLBACKS
# ============================================================

st.session_state.setdefault("message", "")
st.session_state.setdefault("result", None)
st.session_state.setdefault("source", "")
st.session_state.setdefault("run_id", 0)


def load_example(name: str) -> None:
    st.session_state.message = EXAMPLES[name]
    st.session_state.result = None


def clear_all() -> None:
    st.session_state.message = ""
    st.session_state.result = None
    st.session_state.source = ""


# ============================================================
# HEADER
# ============================================================

render(
    """
    <div class="brand"><span class="flag"></span>Dutch4You</div>
    <div class="headline" role="heading" aria-level="1">Got a letter in Dutch?</div>
    <div class="lede">
        Paste it below. You get an English translation, a plain explanation,
        and a checklist of what to do and by when.
    </div>
    """
)

# ============================================================
# INPUT
# ============================================================

st.caption("Try an example")
example_cols = st.columns(len(EXAMPLES))
for col, name in zip(example_cols, EXAMPLES):
    with col:
        st.button(
            name,
            key=f"ex_{name}",
            on_click=load_example,
            args=(name,),
            use_container_width=True,
        )

text = st.text_area(
    "Dutch message",
    key="message",
    height=180,
    placeholder="Paste the Dutch text here: an email, letter or notice from your university, landlord, bank or municipality.",
    label_visibility="collapsed",
)

render(
    f"""
    <div class="hint">
        {len(text):,} characters. Remove personal numbers such as your BSN or IBAN before pasting.
    </div>
    """
)

go_col, clear_col = st.columns([3, 1])
with go_col:
    go = st.button("Translate and explain", type="primary", use_container_width=True)
with clear_col:
    st.button("Clear", on_click=clear_all, use_container_width=True)

if go:
    if not text.strip():
        st.warning("Paste a Dutch message first, then select Translate and explain.")
    else:
        with st.spinner("Reading your message…"):
            try:
                st.session_state.result = process_text(text)
                st.session_state.source = text
                st.session_state.run_id += 1
            except Exception as exc:
                st.session_state.result = None
                st.error(
                    "We couldn't read this message. Check your connection and try again. "
                    "If it keeps failing, try a shorter text."
                )
                with st.expander("Technical details"):
                    st.code(str(exc))

# ============================================================
# RESULTS
# ============================================================


def show_result(result: dict, source: str, run_id: int) -> None:
    deadlines, amounts, actions = extract(result)
    translation = result.get("translation") or "No translation available."
    explanation = result.get("explanation") or "No explanation available."

    render('<div class="space"></div>')

    # 1. Translation first (English on top on phones), Dutch original beside it
    english_col, dutch_col = st.columns(2, gap="medium")
    with english_col:
        render(
            f"""
            <div class="doc english">
                <div class="doc-label">In English</div>
                <div class="doc-body">{esc(translation)}</div>
            </div>
            """
        )
    with dutch_col:
        render(
            f"""
            <div class="doc original">
                <div class="doc-label">Dutch original</div>
                <div class="doc-body">{esc(source)}</div>
            </div>
            """
        )

    render('<div style="height:16px"></div>')

    # 2. Plain-language explanation
    render(
        f"""
        <div class="doc english explain">
            <div class="doc-label">What this means</div>
            <div class="doc-body">{esc(explanation)}</div>
        </div>
        """
    )

    render('<div class="space"></div>')

    # 3. What to do, and by when
    if deadlines or amounts or actions:
        with keyed_container("todo", bordered=True):
            left, right = st.columns([3, 2], gap="large")
            with left:
                render('<div class="panel-title">What you need to do</div>')
                if actions:
                    for i, action in enumerate(actions):
                        st.checkbox(action, key=f"action_{run_id}_{i}")
                else:
                    render('<div class="fact-none">No required action found.</div>')
            with right:
                render(facts_html("Deadline", deadlines, "No deadline found", accent=True))
                render(facts_html("Amount", amounts, "No amount found"))
    else:
        render(
            """
            <div class="quiet">
                No deadline, amount or required action found. This message looks
                like information only. Read the translation below to be sure.
            </div>
            """
        )

    render('<div class="space"></div>')

    # 4. Trust signals + save
    confidence = str(result.get("confidence") or "").lower()
    with keyed_container("meta"):
        meta_left, meta_right = centered_columns([3, 1], gap="medium")
        with meta_left:
            if confidence in CONFIDENCE:
                render(f'<span class="conf conf-{confidence}">{CONFIDENCE[confidence]}</span>')
        with meta_right:
            st.download_button(
                "Save summary",
                data=build_summary(result, source),
                file_name="dutch4you-summary.txt",
                mime="text/plain",
                use_container_width=True,
            )

    if result.get("warning"):
        render(f'<div class="note"><strong>Heads-up:</strong> {esc(result["warning"])}</div>')


if st.session_state.result:
    show_result(
        st.session_state.result,
        st.session_state.source,
        st.session_state.run_id,
    )
else:
    render(
        """
        <div class="steps">
            <div class="step">
                <div class="step-n">1</div>
                <div>
                    <div class="step-title">Paste</div>
                    <div class="step-text">Add the Dutch email, letter or notice.</div>
                </div>
            </div>
            <div class="step">
                <div class="step-n">2</div>
                <div>
                    <div class="step-title">Read</div>
                    <div class="step-text">See it in English, with a plain explanation.</div>
                </div>
            </div>
            <div class="step">
                <div class="step-n">3</div>
                <div>
                    <div class="step-title">Act</div>
                    <div class="step-text">Tick off what you need to do before the deadline.</div>
                </div>
            </div>
        </div>
        """
    )

# ============================================================
# FOOTER
# ============================================================

render(
    """
    <div class="site-note">
        Dutch4You uses AI and can make mistakes. For legal, immigration, financial
        or other official decisions, check the original document or contact the sender.
    </div>
    """
)