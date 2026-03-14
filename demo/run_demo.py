#!/usr/bin/env python3
"""
Connection Ratio Analysis Demo

This script demonstrates how the connection ratio analysis works with real data.
"""

import json
import os
import sys

# Add parent directory to path to import the package
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

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

def run_analysis():
    """Run the connection ratio analysis on sample data."""
    print("Connection Ratio Analysis Demonstration")
    print("=" * 50)
    
    # Create sample data
    filenames = create_sample_data()
    
    # Import and run analysis
    try:
        from network_analysis_package import conn_ratio
        
        print("\nRunning connection ratio analysis...")
        results = conn_ratio.analyze_connection_ratios(filenames, plots_dir="plots")
        
        # Display results
        print("\nAnalysis Results:")
        print("-" * 30)
        for network, ratios in results.items():
            print(f"\nNetwork: {network}")
            for ratio_name, ratio_value in ratios.items():
                if isinstance(ratio_value, (int, float)) and not (isinstance(ratio_value, float) and str(ratio_value).lower() in ['inf', '-inf', 'nan']):
                    print(f"  {ratio_name}: {ratio_value:.6f}")
                else:
                    print(f"  {ratio_name}: {ratio_value}")
        
        print("\nGenerated plots in 'plots' directory:")
        if os.path.exists("plots"):
            for file in os.listdir("plots"):
                print(f"  - {file}")
        else:
            print("  No plots directory found")
            
        print("\nTry running the full demo workflow with:")
        print("  cd .. && python demo_workflow.py")
        
    except ImportError as e:
        print(f"Error importing conn_ratio module: {e}")
        print("Make sure you're running this from the correct directory")
    except Exception as e:
        print(f"Error running analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_analysis()