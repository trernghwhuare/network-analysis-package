#!/usr/bin/env python3
"""
Direct test of the conn_ratio module
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Try to import and test the conn_ratio module
try:
    from network_analysis_package import conn_ratio
    print("Successfully imported conn_ratio")
    
    # Check if module has the expected functions
    print("Module functions:")
    functions = [attr for attr in dir(conn_ratio) if callable(getattr(conn_ratio, attr)) and not attr.startswith("_")]
    for func in functions:
        print(f"  - {func}")
        
    print("\nModule has analyze_connection_ratios:", hasattr(conn_ratio, 'analyze_connection_ratios'))
    print("Module has main:", hasattr(conn_ratio, 'main'))
    
except Exception as e:
    print(f"Error importing conn_ratio: {e}")
    import traceback
    traceback.print_exc()