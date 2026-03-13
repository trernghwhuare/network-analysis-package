#!/usr/bin/env python3
"""
Simple demonstration script to show that the network analysis package is working.
"""

import os
import json
import pandas as pd

def create_test_data():
    """Create test data for demonstration."""
    # Create input_data directory for input files
    os.makedirs("input_data", exist_ok=True)
    
    # Create sample network data
    network_data = {
        "network_name": "demo_network",
        "syn_ee_contacts": 15000,
        "syn_ei_contacts": 12000,
        "syn_ie_contacts": 10000,
        "syn_ii_contacts": 8000,
        "ele_ee_conductances": 2500,
        "ele_ii_conductances": 2000,
        "correlation": 0.85
    }
    
    # Save as JSON
    with open("input_data/demo_network_connection_stats.json", "w") as f:
        json.dump(network_data, f, indent=2)
    
    print("✓ Created sample network data")

def test_conn_ratio_analysis():
    """Test connection ratio analysis."""
    try:
        from network_analysis_package import conn_ratio
        
        # Run analysis
        results = conn_ratio.analyze_connection_ratios(
            json_files=["input_data/demo_network_connection_stats.json"],
            plots_dir="output_plots"
        )
        
        print("✓ Connection ratio analysis completed")
        print("  Results:")
        for network, ratios in results.items():
            print(f"    {network}:")
            for ratio_name, ratio_value in ratios.items():
                print(f"      {ratio_name}: {ratio_value:.4f}")
                
        return True
    except Exception as e:
        print(f"✗ Connection ratio analysis failed: {e}")
        return False

def test_standard_analysis():
    """Test standard analysis."""
    try:
        from network_analysis_package import analysis
        import glob
        
        # Create a simple DataFrame for testing
        data = {
            'network': ['demo_network'],
            'syn_ee_contacts': [15000],
            'syn_ei_contacts': [12000],
            'syn_ie_contacts': [10000],
            'syn_ii_contacts': [8000],
            'ele_ee_conductances': [2500],
            'ele_ii_conductances': [2000]
        }
        
        df = pd.DataFrame(data)
        df.set_index('network', inplace=True)
        
        # Test plotting functions
        analysis.plot_connection_type_violins(df, outpath="output_plots/test_violins.png")
        print("✓ Standard analysis (violin plots) completed")
        
        analysis.plot_clustered_heatmap(df, outpath="output_plots/test_clustermap.png")
        print("✓ Standard analysis (clustered heatmap) completed")
        
        analysis.plot_combined_heatmaps(df, outpath="output_plots/test_combined.png")
        print("✓ Standard analysis (combined heatmaps) completed")
        
        analysis.plot_ei_scatter_with_stacked(df, outpath="output_plots/test_ei_stacked.png")
        print("✓ Standard analysis (E/I scatter) completed")
        
        return True
    except Exception as e:
        print(f"✗ Standard analysis failed: {e}")
        return False

def main():
    """Main function."""
    print("Network Analysis Package - Demo")
    print("=" * 40)
    
    # Create test data
    create_test_data()
    
    # Test connection ratio analysis
    print("\n1. Testing Connection Ratio Analysis:")
    conn_ratio_success = test_conn_ratio_analysis()
    
    # Test standard analysis
    print("\n2. Testing Standard Analysis:")
    standard_analysis_success = test_standard_analysis()
    
    # Summary
    print("\n" + "=" * 40)
    if conn_ratio_success and standard_analysis_success:
        print("All tests passed! The package is working correctly.")
        print("Check the 'output_plots' directory for generated visualizations.")
    else:
        print("Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()