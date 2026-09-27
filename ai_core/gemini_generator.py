"""
ai_core/gemini_generator.py
Wraps the Google Gemini API to turn structured legal-document inputs
into a full, formatted legal document as text.
"""
import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL_NAME


class GeminiDocumentGenerator:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise RuntimeError(
                "GEMINI_API_KEY is not set. Add it to your .env file."
            )
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    def generate_document(self, document_type: str, parties: str, terms: str, dates: str) -> str:
        """
        Build a structured prompt from the user's inputs and ask Gemini
        to draft a complete legal document.
        """
        prompt = (
            f"Generate a comprehensive legal document titled '{document_type}'.\n"
            f"Involved parties: {parties}\n"
            f"Effective Date: {dates}\n"
            f"Terms and conditions: {terms}\n"
            "Ensure a formal legal structure with numbered sections and clauses "
            "(e.g. Services, Term and Termination, Payment, Confidentiality, "
            "Governing Law, Entire Agreement, Severability, Signatures). "
            "Use plain, unambiguous legal language suitable for the stated "
            "document type and do not include any commentary outside the "
            "document itself."
        )
        response = self.model.generate_content(prompt)
        return response.text
