#!/usr/bin/env python3
"""
Test script to verify that the network analysis package works correctly locally.
"""

import sys
import os

def test_imports():
    """Test importing the package modules."""
    try:
        from network_analysis_package import conn_ratio
        print("✓ Successfully imported conn_ratio module")
    except ImportError as e:
        print(f"✗ Failed to import conn_ratio module: {e}")
        return False
    
    try:
        from network_analysis_package import analysis
        print("✓ Successfully imported analysis module")
    except ImportError as e:
        print(f"✗ Failed to import analysis module: {e}")
        return False
    
    return True

def test_functions():
    """Test that key functions exist."""
    try:
        from network_analysis_package import conn_ratio, analysis
        
        # Check conn_ratio functions
        conn_functions = ['analyze_connection_ratios', 'main']
        for func in conn_functions:
            if hasattr(conn_ratio, func):
                print(f"✓ conn_ratio.{func} function exists")
            else:
                print(f"✗ conn_ratio.{func} function not found")
                return False
        
        # Check analysis functions
        analysis_functions = [
            'plot_connection_type_violins',
            'plot_clustered_heatmap', 
            'plot_combined_heatmaps',
            'plot_ei_scatter_with_stacked'
        ]
        for func in analysis_functions:
            if hasattr(analysis, func):
                print(f"✓ analysis.{func} function exists")
            else:
                print(f"✗ analysis.{func} function not found")
                return False
                
        return True
    except ImportError as e:
        print(f"✗ Failed to import modules: {e}")
        return False

def test_directory_structure():
    """Test that the expected directory structure exists."""
    expected_dirs = ['network_analysis_package', 'analysis_out', 'plots']
    for dir_name in expected_dirs:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name} directory exists")
        else:
            print(f"ℹ {dir_name} directory does not exist (will be created when needed)")
    
    # Check for required files
    required_files = [
        'network_analysis_package/__init__.py',
        'network_analysis_package/conn_ratio.py',
        'network_analysis_package/analysis.py'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} does not exist")
            return False
    
    return True

def main():
    """Main test function."""
    print("Testing network_analysis_package local installation...")
    print("=" * 60)
    
    print("\n1. Testing directory structure...")
    dir_success = test_directory_structure()
    
    print("\n2. Testing module imports...")
    import_success = test_imports()
    
    print("\n3. Testing function availability...")
    function_success = test_functions()
    
    print("\n" + "=" * 60)
    if dir_success and import_success and function_success:
        print("All tests passed! The package is ready to use locally.")
        print("\nTo get started:")
        print("1. Prepare your network data in analysis_out/")
        print("2. Run 'python example_usage.py' for a complete example")
        print("3. Check the plots/ directory for generated visualizations")
    else:
        print("Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()