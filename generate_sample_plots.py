#!/usr/bin/env python3
"""
Generate sample plots for documentation purposes.

This script creates sample plots that can be used in the README.md file
to showcase the capabilities of the network analysis package.
"""

import os
import json
import numpy as np
import pandas as pd
from network_analysis_package import conn_ratio, analysis

def create_sample_data():
    """Create sample network data for demonstration."""
    # Create analysis_out directory
    os.makedirs("analysis_out", exist_ok=True)
    os.makedirs("plots", exist_ok=True)
    os.makedirs("docs/images", exist_ok=True)
    
    # Sample network statistics - simulating real data from network analysis
    networks_data = [
        {
            "network_name": "CTC_max_plus_network",
            "syn_ee_contacts": 18000,
            "syn_ei_contacts": 15000,
            "syn_ie_contacts": 12000,
            "syn_ii_contacts": 10000,
            "ele_ee_conductances": 3000,
            "ele_ii_conductances": 2500,
            "correlation": 0.87
        },
        {
            "network_name": "CTC_optimus_plus_network",
            "syn_ee_contacts": 16000,
            "syn_ei_contacts": 14000,
            "syn_ie_contacts": 11000,
            "syn_ii_contacts": 9000,
            "ele_ee_conductances": 2800,
            "ele_ii_conductances": 2200,
            "correlation": 0.82
        },
        {
            "network_name": "M2M1S1_max_plus_network",
            "syn_ee_contacts": 20000,
            "syn_ei_contacts": 17000,
            "syn_ie_contacts": 14000,
            "syn_ii_contacts": 12000,
            "ele_ee_conductances": 3500,
            "ele_ii_conductances": 3000,
            "correlation": 0.91
        },
        {
            "network_name": "M2M1S1_optimus_plus_network",
            "syn_ee_contacts": 19000,
            "syn_ei_contacts": 16000,
            "syn_ie_contacts": 13000,
            "syn_ii_contacts": 11000,
            "ele_ee_conductances": 3200,
            "ele_ii_conductances": 2800,
            "correlation": 0.88
        }
    ]
    
    filenames = []
    for data in networks_data:
        filename = f"analysis_out/{data['network_name']}_connection_stats.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        filenames.append(filename)
    
    return filenames

def generate_sample_plots():
    """Generate sample plots for documentation."""
    print("Generating sample plots for documentation...")
    
    # Create sample data
    json_files = create_sample_data()
    
    # Run connection ratio analysis
    print("Running connection ratio analysis...")
    conn_ratio_results = conn_ratio.analyze_connection_ratios(json_files, plots_dir="plots")
    
    # Create DataFrame for standard analysis
    data_records = []
    for filename in json_files:
        with open(filename, 'r') as f:
            data = json.load(f)
            record = {
                'network': data['network_name'],
                'syn_ee_contacts': data['syn_ee_contacts'],
                'syn_ei_contacts': data['syn_ei_contacts'],
                'syn_ie_contacts': data['syn_ie_contacts'],
                'syn_ii_contacts': data['syn_ii_contacts'],
                'ele_ee_conductances': data['ele_ee_conductances'],
                'ele_ii_conductances': data['ele_ii_conductances'],
                'correlation': data['correlation']
            }
            data_records.append(record)
    
    df = pd.DataFrame(data_records)
    df.set_index('network', inplace=True)
    
    # Run standard analysis
    print("Running standard analysis...")
    analysis.plot_connection_type_violins(df, outpath="plots/sample_violins.png")
    analysis.plot_clustered_heatmap(df, outpath="plots/sample_clustermap.png")
    analysis.plot_combined_heatmaps(df, outpath="plots/sample_combined_heatmaps.png")
    analysis.plot_ei_scatter_with_stacked(df, outpath="plots/sample_ei_stacked.png")
    
    print("Sample plots generated successfully!")
    print("Check the 'plots' directory for the generated plots.")
    print("\nTo use these in documentation:")
    print("1. Copy the plots to docs/images/")
    print("2. Rename them to match the references in README.md")

if __name__ == "__main__":
    generate_sample_plots()