"""
The old Streamlit app (ai-resume-ats.streamlit.app) used to live here.
The project is now a Next.js site, so this tiny page just sends visitors there.

Streamlit Cloud still runs this file, so the old link keeps working.
Vercel ignores it.
"""

import streamlit as st
import streamlit.components.v1 as components

NEW_URL = "https://ai-resume-ats.vercel.app"

st.set_page_config(page_title="AI Resume ATS has moved", page_icon="📄", layout="centered")

st.markdown(
    f"""
    <div style="text-align:center;padding:4rem 1rem">
      <h1>AI Resume ATS has a new home ✨</h1>
      <p style="font-size:1.1rem;opacity:.8">
        Faster, with AI rewrites, interview prep, cover letters and version tracking.
      </p>
      <p>Taking you there now…</p>
    </div>
    """,
    unsafe_allow_html=True,
)
st.link_button("Open the new AI Resume ATS →", NEW_URL, type="primary", use_container_width=True)

# Try to redirect automatically (some browsers block this, so the button stays as a backup).
components.html(f"<script>window.top.location.href = '{NEW_URL}';</script>", height=0)
