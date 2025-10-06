#!/usr/bin/env python3
"""
Test script to diagnose Streamlit Cloud deployment issues.
Run this to identify what's causing the deployment failure.
"""

import sys
import os
import traceback

def test_environment():
    """Test the Python environment and paths."""
    print("=== ENVIRONMENT TEST ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Python path: {sys.path[:3]}")
    print()

def test_dependencies():
    """Test all required dependencies."""
    print("=== DEPENDENCIES TEST ===")
    dependencies = [
        'pandas', 'numpy', 'plotly', 'streamlit', 
        'sklearn', 'scipy', 'psutil'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"OK {dep}: OK")
        except ImportError as e:
            print(f"FAILED {dep}: FAILED - {e}")
    print()

def test_file_structure():
    """Test file structure and data files."""
    print("=== FILE STRUCTURE TEST ===")
    
    # Check current directory files
    print("Files in current directory:")
    for f in os.listdir('.'):
        if os.path.isfile(f):
            print(f"  OK {f}")
    
    print("\nDirectories:")
    for d in os.listdir('.'):
        if os.path.isdir(d):
            print(f"  OK {d}/")
    
    # Check data directory
    print("\nData directory contents:")
    if os.path.exists('data'):
        for f in os.listdir('data'):
            if f.endswith('.csv'):
                print(f"  OK {f}")
    else:
        print("  FAILED data/ directory not found!")
    print()

def test_imports():
    """Test the specific imports used in streamlit_app.py."""
    print("=== IMPORT TEST ===")
    
    try:
        print("Testing: from src.business_logic import analyzer")
        from src.business_logic import analyzer
        print("OK Business logic import: SUCCESS")
        
        print("Testing: analyzer.get_automaker_list()")
        automakers = analyzer.get_automaker_list()
        print(f"OK Data access: SUCCESS - Found {len(automakers)} automakers")
        
        print("Testing: analyzer.get_sales_summary()")
        sales = analyzer.get_sales_summary()
        print(f"OK Sales data: SUCCESS - Shape: {sales.shape}")
        
    except Exception as e:
        print(f"FAILED Import test: FAILED")
        print(f"Error: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
    print()

def test_streamlit_import():
    """Test Streamlit-specific imports."""
    print("=== STREAMLIT IMPORT TEST ===")
    
    try:
        import streamlit as st
        print("OK Streamlit import: SUCCESS")
        
        # Test if we can import the app
        print("Testing: import streamlit_app")
        import streamlit_app
        print("OK Streamlit app import: SUCCESS")
        
    except Exception as e:
        print(f"FAILED Streamlit test: FAILED")
        print(f"Error: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
    print()

def main():
    """Run all tests."""
    print("STREAMLIT CLOUD DIAGNOSTIC TEST")
    print("=" * 50)
    
    test_environment()
    test_dependencies()
    test_file_structure()
    test_imports()
    test_streamlit_import()
    
    print("=" * 50)
    print("DIAGNOSTIC COMPLETE")
    print("If all tests pass, the issue might be in Streamlit Cloud configuration.")
    print("Check the Streamlit Cloud logs for more specific error details.")

if __name__ == "__main__":
    main()
