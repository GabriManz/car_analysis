import streamlit as st

# Delegate to the new modular app router
try:
	from src.app import main as run_app
except Exception as e:
	st.error(f"Failed to import app router: {e}")
else:
	run_app()
