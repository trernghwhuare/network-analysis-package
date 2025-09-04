#!/usr/bin/env python3
"""
Test script to verify that both modules in the network_analysis_package can be imported and used.
"""

def test_imports():
    """Test importing both modules from the package."""
    try:
        from network_analysis_package import conn_ratio
        print("SUCCESS: Imported conn_ratio module")
    except ImportError as e:
        print(f"ERROR: Failed to import conn_ratio module: {e}")
        return False
    
    try:
        from network_analysis_package import analysis
        print("SUCCESS: Imported analysis module")
    except ImportError as e:
        print(f"ERROR: Failed to import analysis module: {e}")
        return False
    
    return True


def test_functions():
    """Test that key functions exist in both modules."""
    try:
        from network_analysis_package import conn_ratio, analysis
        
        # Check conn_ratio functions
        conn_functions = ['analyze_connection_ratios', 'main']
        for func in conn_functions:
            if hasattr(conn_ratio, func):
                print(f"SUCCESS: conn_ratio.{func} function exists")
            else:
                print(f"ERROR: conn_ratio.{func} function not found")
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
                print(f"SUCCESS: analysis.{func} function exists")
            else:
                print(f"ERROR: analysis.{func} function not found")
                return False
                
        return True
    except ImportError as e:
        print(f"ERROR: Failed to import modules: {e}")
        return False


if __name__ == "__main__":
    print("Testing network_analysis_package...")
    print("=" * 50)
    
    import_success = test_imports()
    function_success = test_functions()
    
    print("=" * 50)
    if import_success and function_success:
        print("All tests passed! The package is ready to use.")
    else:
        print("Some tests failed. Please check the errors above.")