#!/usr/bin/env python3
"""
Test script for connection ratio analysis
"""

import os
import sys
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the conn_ratio module
try:
    from network_analysis_package import conn_ratio
    print("Successfully imported conn_ratio module")
except ImportError as e:
    print(f"Failed to import conn_ratio module: {e}")
    sys.exit(1)

# Create test data directory
os.makedirs("analysis_out", exist_ok=True)

# Create sample data
sample_data = {
    "network_name": "test_network",
    "syn_ee_contacts": 10000,
    "syn_ei_contacts": 8000,
    "syn_ie_contacts": 7000,
    "syn_ii_contacts": 6000,
    "ele_ee_conductances": 1500,
    "ele_ii_conductances": 1200,
    "correlation": 0.75
}

# Write sample data
with open("analysis_out/test_network_connection_stats.json", "w") as f:
    json.dump(sample_data, f, indent=2)

print("Created sample data file")

# Test the analyze_connection_ratios function
try:
    results = conn_ratio.analyze_connection_ratios(
        ["analysis_out/test_network_connection_stats.json"],
        plots_dir="plots"
    )
    print("Analysis completed successfully")
    print("Results:", results)
except Exception as e:
    print(f"Error during analysis: {e}")
    import traceback
    traceback.print_exc()