"""
ai_core/generator.py
Core formatting utilities: turns raw AI-generated text into
polished .docx / .pdf output, an HTML preview, and provides
text sanitization.
"""
import io
import re

from docx import Document
from docx.shared import Inches, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from fpdf import FPDF

from config import LOGO_PATH, FOOTER_TEXT


def sanitize_text(text: str) -> str:
    """Remove special/typographic characters that break clean formatting."""
    if not text:
        return ""
    replacements = {
        "\u2018": "'", "\u2019": "'",
        "\u201c": '"', "\u201d": '"',
        "\u2013": "-", "\u2014": "-",
        "\u2026": "...",
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    text = text.replace("#", "").replace("*", "")
    return text.strip()


def _split_terms(terms: str):
    return [t.strip() for t in terms.split(";") if t.strip()]


def format_docx(text: str, doc_type: str, parties: str = "", terms: str = "", dates: str = "") -> bytes:
    """Build a branded, formatted Word document from generated text."""
    doc = Document()

    # Logo on the title page (best-effort; skipped if the file is missing)
    try:
        doc.add_picture(LOGO_PATH, width=Inches(1.5))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    except Exception:
        pass

    title = doc.add_heading(doc_type, level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for para in sanitize_text(text).split("\n"):
        if para.strip():
            p = doc.add_paragraph(para.strip())
            p.style.font.size = Pt(11)

    # Auto-generated terms table
    term_list = _split_terms(terms)
    if term_list:
        doc.add_heading("Summary of Terms", level=2)
        table = doc.add_table(rows=1, cols=1)
        table.style = "Light Grid Accent 1"
        table.rows[0].cells[0].text = "Term"
        for t in term_list:
            row = table.add_row()
            row.cells[0].text = t

    footer = doc.sections[0].footer
    footer.paragraphs[0].text = FOOTER_TEXT
    footer.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()


class _BrandedPDF(FPDF):
    def header(self):
        try:
            self.image(LOGO_PATH, x=(self.w - 30) / 2, y=8, w=30)
            self.ln(20)
        except Exception:
            self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, FOOTER_TEXT, align="C")


def format_pdf(text: str, doc_type: str, terms: str = "") -> bytes:
    """Build a branded PDF with header/footer and bullet-style terms."""
    pdf = _BrandedPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.multi_cell(0, 10, doc_type, align="C")
    pdf.ln(4)

    pdf.set_font("Helvetica", size=11)
    for para in sanitize_text(text).split("\n"):
        if para.strip():
            pdf.multi_cell(0, 7, para.strip())
            pdf.ln(1)

    term_list = _split_terms(terms)
    if term_list:
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Summary of Terms", ln=True)
        pdf.set_font("Helvetica", size=11)
        for t in term_list:
            pdf.multi_cell(0, 7, f"- {t}")

    return bytes(pdf.output(dest="S"))


def format_html_preview(text: str) -> str:
    """Convert generated text into styled HTML for an inline preview."""
    clean = sanitize_text(text)
    paragraphs = [p.strip() for p in clean.split("\n") if p.strip()]
    html_paragraphs = "".join(f"<p style='margin:0 0 10px 0;'>{p}</p>" for p in paragraphs)
    return html_paragraphs
