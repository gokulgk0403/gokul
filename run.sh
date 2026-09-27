#!/usr/bin/env bash
# Launches both the FastAPI backend and Streamlit frontend.
set -e

echo "Starting FastAPI backend on :8000 ..."
uvicorn legalEaseAPI.main:app --reload --port 8000 &
BACKEND_PID=$!

sleep 2

echo "Starting Streamlit frontend on :8501 ..."
streamlit run frontend/app.py

kill $BACKEND_PID
