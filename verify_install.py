#!/usr/bin/env python3
"""
Simple verification script for the network analysis package
"""

def test_import():
    """Test importing the conn_ratio module"""
    try:
        from network_analysis_package import conn_ratio
        print("SUCCESS: Imported conn_ratio module")
        return True
    except ImportError as e:
        print(f"ERROR: Failed to import conn_ratio module: {e}")
        return False

def test_function_exists():
    """Test that key functions exist in the module"""
    try:
        from network_analysis_package import conn_ratio
        # Check if key functions exist
        if hasattr(conn_ratio, 'analyze_connection_ratios'):
            print("SUCCESS: analyze_connection_ratios function exists")
            return True
        else:
            print("ERROR: analyze_connection_ratios function not found")
            return False
    except ImportError as e:
        print(f"ERROR: Failed to import conn_ratio module: {e}")
        return False

if __name__ == "__main__":
    print("Verifying network analysis package installation...")
    print("=" * 50)
    
    import_success = test_import()
    function_success = test_function_exists()
    
    print("=" * 50)
    if import_success and function_success:
        print("All tests passed! The package is ready to use.")
    else:
        print("Some tests failed. Please check the errors above.")