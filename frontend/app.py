"""
frontend/app.py
Streamlit UI for LegalEase.

Run with:
    streamlit run frontend/app.py
(with the FastAPI backend already running on BACKEND_URL)
"""
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import requests

from config import APP_TITLE, APP_TAGLINE, LOGO_PATH, BACKEND_URL
from ai_core.generator import sanitize_text, format_docx, format_pdf, format_html_preview

st.set_page_config(page_title=APP_TITLE, layout="centered")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if os.path.exists(LOGO_PATH):
        st.image(LOGO_PATH, use_container_width=True)
    else:
        st.markdown(f"<h1 style='text-align:center;'>{APP_TITLE}</h1>", unsafe_allow_html=True)

st.markdown(
    f"<h2 style='text-align: center;'>{APP_TAGLINE}</h2>",
    unsafe_allow_html=True,
)

document_type = st.text_input("Document Type (Ex: Agreement, Contract, NDA)")
parties = st.text_area("Parties Involved")
terms = st.text_area("Terms & Conditions (Use semicolons for bullet points)")
dates = st.text_input("Effective Date")

if "generated_text" not in st.session_state:
    st.session_state.generated_text = ""
if "show_edit" not in st.session_state:
    st.session_state.show_edit = False

if st.button("Generate Document"):
    if not (document_type and parties and terms and dates):
        st.warning("Please fill in all fields before generating.")
    else:
        with st.spinner("Generating your document..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "dates": dates,
                    },
                    timeout=60,
                )
                response.raise_for_status()
                st.session_state.generated_text = sanitize_text(response.json()["document"])
                st.success("Document Generated Successfully!")
            except Exception as exc:
                st.error(f"Failed to generate document: {exc}")

if st.session_state.generated_text:
    styled_html = format_html_preview(st.session_state.generated_text)
    st.markdown(
        f"<div style='background:#111;color:#eee;padding:16px;border-radius:8px;"
        f"max-height:400px;overflow-y:auto;'>{styled_html}</div>",
        unsafe_allow_html=True,
    )

    if st.button("Click to Edit Document"):
        st.session_state.show_edit = not st.session_state.show_edit

    if st.session_state.show_edit:
        edited_text = st.text_area(
            "Edit Document Below:", st.session_state.generated_text, height=300
        )
        st.session_state.generated_text = edited_text

    safe_name = document_type.replace(" ", "_").lower() or "document"

    st.download_button(
        "Download as .TXT",
        data=st.session_state.generated_text,
        file_name=f"{safe_name}.txt",
    )
    st.download_button(
        "Download as .DOCX",
        data=format_docx(st.session_state.generated_text, document_type, parties, terms, dates),
        file_name=f"{safe_name}.docx",
    )
    st.download_button(
        "Download as .PDF",
        data=format_pdf(st.session_state.generated_text, document_type, terms),
        file_name=f"{safe_name}.pdf",
    )
else:
    st.info("Click 'Generate Document' to start")
