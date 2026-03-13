#!/usr/bin/env python3
"""
Getting Started Guide for the Network Analysis Package

This script helps new users get started with the network analysis package
by providing a step-by-step guide and interactive setup.
"""

import os
import sys
import json

def print_welcome():
    """Print welcome message and overview."""
    print("=" * 60)
    print("Welcome to the Network Analysis Package!")
    print("=" * 60)
    print("\nThis package provides tools for analyzing neural network structures")
    print("and connection ratios with advanced visualization capabilities.")
    print("\nFeatures include:")
    print("  • Connection type distribution analysis")
    print("  • Correlation analysis between different metrics")
    print("  • Excitatory/Inhibitory (E/I) ratio analysis")
    print("  • Publication-quality visualization generation")
    print("  • Batch processing capabilities")

def check_prerequisites():
    """Check if prerequisites are met."""
    print("\nChecking prerequisites...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 6:
        print(f"✓ Python {sys.version.split()[0]} - Supported")
    else:
        print(f"✗ Python {sys.version.split()[0]} - Version 3.6+ required")
        return False
    
    # Check if required packages are available
    required_packages = ['numpy', 'pandas', 'matplotlib', 'seaborn', 'scipy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} - Available")
        except ImportError:
            print(f"✗ {package} - Not installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nPlease install missing packages with:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def create_sample_data():
    """Create sample data for demonstration."""
    print("\nCreating sample data...")
    
    # Create input_data directory for input files
    os.makedirs("input_data", exist_ok=True)
    
    # Sample network statistics
    sample_networks = [
        {
            "network_name": "Sample_Network_A",
            "syn_ee_contacts": 18000,
            "syn_ei_contacts": 15000,
            "syn_ie_contacts": 12000,
            "syn_ii_contacts": 10000,
            "ele_ee_conductances": 3000,
            "ele_ii_conductances": 2500,
            "correlation": 0.87
        },
        {
            "network_name": "Sample_Network_B",
            "syn_ee_contacts": 16000,
            "syn_ei_contacts": 14000,
            "syn_ie_contacts": 11000,
            "syn_ii_contacts": 9000,
            "ele_ee_conductances": 2800,
            "ele_ii_conductances": 2200,
            "correlation": 0.82
        }
    ]
    
    created_files = []
    for network_data in sample_networks:
        filename = f"input_data/{network_data['network_name']}_connection_stats.json"
        with open(filename, "w") as f:
            json.dump(network_data, f, indent=2)
        created_files.append(filename)
        print(f"✓ Created {filename}")
    
    return created_files

def run_sample_analysis():
    """Run sample analysis on the created data."""
    print("\nRunning sample analysis...")
    
    try:
        # Import and run connection ratio analysis
        from network_analysis_package import conn_ratio
        import glob
        
        # Find all JSON files
        json_files = glob.glob("input_data/*_connection_stats.json")
        
        if not json_files:
            print("No JSON files found in input_data/")
            return False
        
        # Run analysis
        results = conn_ratio.analyze_connection_ratios(
            json_files=json_files,
            plots_dir="output_plots"
        )
        
        print("✓ Connection ratio analysis completed")
        print("\nAnalysis Results:")
        for network, ratios in results.items():
            print(f"  {network}:")
            for ratio_name, ratio_value in ratios.items():
                print(f"    {ratio_name}: {ratio_value:.4f}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error running analysis: {e}")
        return False

def show_next_steps():
    """Show next steps for the user."""
    print("\n" + "=" * 60)
    print("Next Steps")
    print("=" * 60)
    print("\nYou're ready to use the network analysis package!")
    print("\nTo continue exploring:")
    print("1. Run the complete demo workflow:")
    print("   python demo_workflow.py")
    print("\n2. Try the example usage script:")
    print("   python example_usage.py")
    print("\n3. Use the package in your own scripts:")
    print("   from network_analysis_package import conn_ratio, analysis")
    print("\n4. Check the generated plots in the 'output_plots' directory")
    print("\n5. Refer to the documentation:")
    print("   - README.md for general information")
    print("   - ANALYSIS_WORKFLOW.md for detailed usage")
    print("   - HOW_IT_WORKS.md for technical details")

def main():
    """Main function."""
    print_welcome()
    
    # Check prerequisites
    if not check_prerequisites():
        print("\nPlease resolve the issues above before continuing.")
        sys.exit(1)
    
    # Create sample data
    sample_files = create_sample_data()
    
    # Run sample analysis
    if run_sample_analysis():
        print("\n✓ Sample analysis completed successfully!")
    else:
        print("\n✗ Sample analysis failed.")
        sys.exit(1)
    
    # Show next steps
    show_next_steps()
    
    print("\nEnjoy using the Network Analysis Package!")

if __name__ == "__main__":
    main()