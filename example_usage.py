#!/usr/bin/env python3
"""
Example usage of the network analysis package.

This script demonstrates how to use the network analysis package with real or sample data.
"""

import os
import json
import pandas as pd
from network_analysis_package import conn_ratio, analysis

def create_sample_data():
    """Create sample network data for demonstration."""
    # Create input_data directory for input files
    os.makedirs("input_data", exist_ok=True)
    
    # Sample network statistics - simulating real data from network analysis
    networks_data = [
        {
            "network_name": "Sample_Network_1",
            "syn_ee_contacts": 15000,
            "syn_ei_contacts": 12000,
            "syn_ie_contacts": 10000,
            "syn_ii_contacts": 8000,
            "ele_ee_conductances": 2500,
            "ele_ii_conductances": 2000,
            "correlation": 0.85
        },
        {
            "network_name": "Sample_Network_2",
            "syn_ee_contacts": 18000,
            "syn_ei_contacts": 15000,
            "syn_ie_contacts": 12000,
            "syn_ii_contacts": 10000,
            "ele_ee_conductances": 3000,
            "ele_ii_conductances": 2500,
            "correlation": 0.90
        }
    ]
    
    filenames = []
    for data in networks_data:
        filename = f"input_data/{data['network_name']}_connection_stats.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        filenames.append(filename)
        print(f"Created: {filename}")
    
    return filenames

def run_complete_analysis():
    """Run a complete analysis workflow."""
    print("Network Analysis Package - Example Usage")
    print("=" * 50)
    
    # Create sample data
    json_files = create_sample_data()
    
    # Create output directory for plots
    os.makedirs("output_plots", exist_ok=True)
    
    # 1. Run connection ratio analysis
    print("\n1. Running Connection Ratio Analysis...")
    conn_results = conn_ratio.analyze_connection_ratios(
        json_files=json_files,
        plots_dir="output_plots"
    )
    
    # Display results
    print("Connection Ratio Analysis Results:")
    for network, ratios in conn_results.items():
        print(f"  {network}:")
        for ratio_name, ratio_value in ratios.items():
            print(f"    {ratio_name}: {ratio_value:.4f}")
    
    # 2. Prepare data for standard analysis
    print("\n2. Preparing data for Standard Analysis...")
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
    
    # 3. Run standard analysis
    print("\n3. Running Standard Analysis...")
    analysis.plot_connection_type_violins(df, outpath="output_plots/connection_violins.png")
    analysis.plot_clustered_heatmap(df, outpath="output_plots/clustermap.png")
    analysis.plot_combined_heatmaps(df, outpath="output_plots/combined_heatmaps.png")
    analysis.plot_ei_scatter_with_stacked(df, outpath="output_plots/ei_stacked.png")
    
    print("\nAnalysis complete!")
    print("Check the 'output_plots' directory for generated visualizations.")

def main():
    """Main function."""
    run_complete_analysis()

if __name__ == "__main__":
    main()