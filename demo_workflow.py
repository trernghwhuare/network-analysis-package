#!/usr/bin/env python3
"""
Demo workflow for the network analysis package.

This script demonstrates the complete workflow of the network analysis package,
including generating sample data, running connection ratio analysis, and running
standard network analysis.
"""

import os
import json
from pathlib import Path

def create_sample_data():
    """Create sample network data for demonstration."""
    # Create analysis_out directory
    os.makedirs("analysis_out", exist_ok=True)
    
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
        }
    ]
    
    filenames = []
    for data in networks_data:
        filename = f"analysis_out/{data['network_name']}_connection_stats.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        filenames.append(filename)
        print(f"Created sample data file: {filename}")
    
    return filenames


def run_connection_ratio_analysis(json_files):
    """Run connection ratio analysis on sample data."""
    print("\n" + "="*50)
    print("RUNNING CONNECTION RATIO ANALYSIS")
    print("="*50)
    
    try:
        from network_analysis_package import conn_ratio
        
        # Run connection ratio analysis
        results = conn_ratio.analyze_connection_ratios(json_files, plots_dir="plots")
        
        # Display results
        print("\nConnection Ratio Analysis Results:")
        print("-" * 40)
        for network, ratios in results.items():
            print(f"\nNetwork: {network}")
            for ratio_name, ratio_value in ratios.items():
                print(f"  {ratio_name}: {ratio_value:.6f}")
        
        return True
    except Exception as e:
        print(f"Error running connection ratio analysis: {e}")
        return False


def run_standard_analysis(json_files):
    """Run standard network analysis on sample data."""
    print("\n" + "="*50)
    print("RUNNING STANDARD NETWORK ANALYSIS")
    print("="*50)
    
    try:
        from network_analysis_package import analysis
        import pandas as pd
        
        # Load data into a DataFrame
        data_records = []
        for filename in json_files:
            with open(filename, 'r') as f:
                data = json.load(f)
                # Flatten the data for DataFrame
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
        
        # Create DataFrame
        df = pd.DataFrame(data_records)
        df.set_index('network', inplace=True)
        
        # Run standard analysis plots
        print("Generating standard analysis plots...")
        analysis.plot_connection_type_violins(df, outpath="plots/connection_violins.png")
        analysis.plot_clustered_heatmap(df, outpath="plots/clustermap.png")
        analysis.plot_combined_heatmaps(df, outpath="plots/combined_heatmaps.png")
        analysis.plot_ei_scatter_with_stacked(df, outpath="plots/ei_stacked.png")
        
        print("Standard analysis plots generated successfully!")
        return True
    except Exception as e:
        print(f"Error running standard analysis: {e}")
        return False


def main():
    """Main demo workflow function."""
    print("Network Analysis Package Demo Workflow")
    print("=" * 50)
    
    # Create sample data
    json_files = create_sample_data()
    
    # Run connection ratio analysis
    conn_ratio_success = run_connection_ratio_analysis(json_files)
    
    # Run standard analysis
    standard_analysis_success = run_standard_analysis(json_files)
    
    # Summary
    print("\n" + "="*50)
    print("DEMO WORKFLOW SUMMARY")
    print("="*50)
    print(f"Connection Ratio Analysis: {'PASSED' if conn_ratio_success else 'FAILED'}")
    print(f"Standard Analysis: {'PASSED' if standard_analysis_success else 'FAILED'}")
    
    if conn_ratio_success and standard_analysis_success:
        print("\nAll analysis completed successfully!")
        print("Check the 'plots' directory for generated visualizations.")
    else:
        print("\nSome analysis steps failed. Please check the error messages above.")


if __name__ == "__main__":
    main()