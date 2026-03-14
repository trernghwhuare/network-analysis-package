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
    """Run standard analysis using proper population-level data workflow."""
    print("\nRunning Standard Analysis (Population-Level Data)...")
    try:
        # Import the new standard analysis runner
        from run_standard_analysis import run_all_standard_analyses
        
        # First ensure we have population data
        from generate_population_data import generate_analysis_out_data
        if not generate_analysis_out_data():
            print("Failed to generate population data for standard analysis.")
            return False
        
        # Run standard analysis on all datasets
        success = run_all_standard_analyses(indir="analysis_out", outdir="output_plots")
        
        if success:
            print("  ✓ Standard analysis completed successfully!")
            print("  Check output_plots/ for network-specific violin plots and heatmaps")
        else:
            print("  ✗ Standard analysis failed")
            
        return success
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
        print("Check the 'output_plots' directory for generated visualizations:")
        print("  • Network-specific regression plots (from connection ratio analysis)")
        print("  • Network-specific violin plots (from standard analysis)")
        print("  • Network-specific clustermaps (from standard analysis)")
        print("  • Network-specific combined heatmaps (from standard analysis)")
        print("  • Network-specific E/I scatter plots (from standard analysis)")
    else:
        print("\nSome analyses failed. Please check the error messages above.")


if __name__ == "__main__":
    main()