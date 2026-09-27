"""
config.py - Central configuration for LegalEase
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API key (set this in your .env file)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Model to use for generation
GEMINI_MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-pro")

# Backend URL the Streamlit frontend talks to
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Branding
APP_TITLE = "LegalEase"
APP_TAGLINE = "AI Legal Document Generator"
LOGO_PATH = os.path.join(os.path.dirname(__file__), "Image", "Logo.png")
FOOTER_TEXT = "LegalEase Inc. | contact@legalease.com | All Rights Reserved."
