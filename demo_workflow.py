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
    # Create input_data directory for input files
    os.makedirs("input_data", exist_ok=True)
    
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
    
    print("Creating sample data files...")
    for data in networks_data:
        filename = f"input_data/{data['network_name']}_connection_stats.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"  Created: {filename}")


def run_connection_ratio_analysis():
    """Run connection ratio analysis on sample data."""
    print("\nRunning Connection Ratio Analysis...")
    try:
        from network_analysis_package import conn_ratio
        import glob
        
        # Find all JSON files in input_data directory
        json_files = glob.glob("input_data/*_connection_stats.json")
        
        if not json_files:
            print("No JSON files found in input_data/")
            return False
        
        # Run analysis
        results = conn_ratio.analyze_connection_ratios(
            json_files=json_files,
            plots_dir="output_plots"
        )
        
        print("Connection Ratio Analysis Results:")
        for network, ratios in results.items():
            print(f"  {network}:")
            for ratio_name, ratio_value in ratios.items():
                if isinstance(ratio_value, (int, float)) and not (isinstance(ratio_value, float) and str(ratio_value).lower() in ['inf', '-inf', 'nan']):
                    print(f"    {ratio_name}: {ratio_value:.4f}")
                else:
                    print(f"    {ratio_name}: {ratio_value}")
                
        return True
    except Exception as e:
        print(f"Error running connection ratio analysis: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_standard_analysis():
    """Run standard analysis on sample data."""
    print("\nRunning Standard Analysis...")
    try:
        from network_analysis_package import analysis
        import pandas as pd
        import glob
        import json
        
        # Find all JSON files in input_data directory
        json_files = glob.glob("input_data/*_connection_stats.json")
        
        if not json_files:
            print("No JSON files found in input_data/")
            return False
            
        # Load data into DataFrame
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
        
        # Create output directory for plots
        os.makedirs("output_plots", exist_ok=True)
        
        # Run analysis functions
        analysis.plot_connection_type_violins(df, outpath="output_plots/connection_violins.png")
        print("  Created connection violins plot")
        
        analysis.plot_clustered_heatmap(df, outpath="output_plots/clustermap.png")
        print("  Created clustered heatmap")
        
        analysis.plot_combined_heatmaps(df, outpath="output_plots/combined_heatmaps.png")
        print("  Created combined heatmaps")
        
        analysis.plot_ei_scatter_with_stacked(df, outpath="output_plots/ei_stacked.png")
        print("  Created E/I scatter with stacked bars")
        
        return True
    except Exception as e:
        print(f"Error running standard analysis: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main demo workflow function."""
    print("Network Analysis Package - Demo Workflow")
    print("=" * 50)
    
    # Step 1: Create sample data
    create_sample_data()
    
    # Step 2: Run connection ratio analysis
    conn_ratio_success = run_connection_ratio_analysis()
    
    # Step 3: Run standard analysis
    standard_analysis_success = run_standard_analysis()
    
    # Summary
    print("\n" + "=" * 50)
    print("Demo Workflow Summary:")
    print(f"  Connection Ratio Analysis: {'✓ Success' if conn_ratio_success else '✗ Failed'}")
    print(f"  Standard Analysis: {'✓ Success' if standard_analysis_success else '✗ Failed'}")
    
    if conn_ratio_success and standard_analysis_success:
        print("\nAll analyses completed successfully!")
        print("Check the 'output_plots' directory for generated visualizations.")
    else:
        print("\nSome analyses failed. Please check the error messages above.")


if __name__ == "__main__":
    main()