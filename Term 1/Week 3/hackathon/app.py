"""
Dutch4You - Streamlit app
Run with: streamlit run app.py
"""

import streamlit as st
from dutch4you_core import process_text

st.set_page_config(page_title="Dutch4You", page_icon="🇳🇱")

st.title("🇳🇱 Dutch4You")
st.caption("Paste Dutch text and get an English translation, a plain-language explanation, and the key info you need to act on.")

dutch_text = st.text_area(
    "Paste Dutch text here",
    height=180,
    placeholder="e.g. U dient uiterlijk 30 september uw documenten in te leveren.",
)

submitted = st.button("Translate & Explain", type="primary")

if submitted:
    if not dutch_text.strip():
        st.warning("Paste some Dutch text first.")
    else:
        with st.spinner("Reading your Dutch text..."):
            result = process_text(dutch_text)

        # Low confidence + empty translation means something went wrong
        # (bad input, API error, or the model flagged it as unclear/not Dutch).
        if not result["translation"] and result["warning"]:
            st.error(result["warning"])
        else:
            st.subheader("🇬🇧 Translation")
            st.write(result["translation"])

            st.subheader("🧠 Explanation")
            st.write(result["explanation"])

            key_info = result["key_info"]
            if any(key_info.values()):
                st.subheader("📌 Important information")
                if key_info["deadlines"]:
                    st.markdown("**Deadlines:**")
                    for d in key_info["deadlines"]:
                        st.markdown(f"- {d}")
                if key_info["amounts"]:
                    st.markdown("**Amounts:**")
                    for a in key_info["amounts"]:
                        st.markdown(f"- {a}")
                if key_info["required_actions"]:
                    st.markdown("**Required actions:**")
                    for act in key_info["required_actions"]:
                        st.markdown(f"- {act}")

            if result["warning"]:
                st.warning(f"⚠️ {result['warning']}")

            if result["confidence"] == "low":
                st.caption("⚠️ Low confidence — double check this with an official source or a Dutch speaker before acting on it.")
