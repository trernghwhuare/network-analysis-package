#!/usr/bin/env python3
"""
Demonstration of Connection Ratio Analysis

This script shows how the connection ratio analysis works with sample data.
"""

import json
import os
from network_analysis_package import conn_ratio

def create_sample_data():
    """Create sample network data for demonstration."""
    # Create analysis_out directory
    os.makedirs("analysis_out", exist_ok=True)
    
    # Sample network statistics
    sample_stats = {
        "network_name": "Demo_Network",
        "syn_ee_contacts": 15000,
        "syn_ei_contacts": 12000,
        "syn_ie_contacts": 10000,
        "syn_ii_contacts": 8000,
        "ele_ee_conductances": 2500,
        "ele_ii_conductances": 2000,
        "correlation": 0.85
    }
    
    # Write sample data to JSON file
    filename = "analysis_out/demo_network_connection_stats.json"
    with open(filename, "w") as f:
        json.dump(sample_stats, f, indent=2)
    
    print(f"Created sample data file: {filename}")
    return filename

def run_analysis():
    """Run the connection ratio analysis on sample data."""
    print("Connection Ratio Analysis Demonstration")
    print("=" * 40)
    
    # Create sample data
    filename = create_sample_data()
    
    # Run analysis
    print("\nRunning connection ratio analysis...")
    results = conn_ratio.analyze_connection_ratios([filename], plots_dir="plots")
    
    # Display results
    print("\nAnalysis Results:")
    print("-" * 20)
    for network, ratios in results.items():
        print(f"Network: {network}")
        for ratio_name, ratio_value in ratios.items():
            print(f"  {ratio_name}: {ratio_value:.6f}")
    
    print("\nCheck the 'plots' directory for generated visualizations:")
    print("1. {network}_regression.png - Scatter plots with regression lines")
    print("2. {network}_ratio_distributions.png - Distribution histograms")

if __name__ == "__main__":
    run_analysis()