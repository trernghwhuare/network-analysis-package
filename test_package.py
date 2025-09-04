#!/usr/bin/env python3
"""
Simple test script to check if the package is working correctly.
"""

def test_imports():
    """Test importing the package modules."""
    try:
        from network_analysis_package import conn_ratio
        print("✓ Successfully imported conn_ratio module")
        return True
    except ImportError as e:
        print(f"✗ Failed to import conn_ratio module: {e}")
        return False

def test_functions():
    """Test that key functions exist."""
    try:
        from network_analysis_package import conn_ratio
        
        # Check if main function exists
        if hasattr(conn_ratio, 'main'):
            print("✓ conn_ratio.main function exists")
        else:
            print("✗ conn_ratio.main function not found")
            return False
            
        # Check if analyze_connection_ratios function exists
        if hasattr(conn_ratio, 'analyze_connection_ratios'):
            print("✓ conn_ratio.analyze_connection_ratios function exists")
        else:
            print("✗ conn_ratio.analyze_connection_ratios function not found")
            return False
            
        return True
    except ImportError as e:
        print(f"✗ Failed to import conn_ratio module: {e}")
        return False

if __name__ == "__main__":
    print("Testing network_analysis_package...")
    print("=" * 40)
    
    import_success = test_imports()
    function_success = test_functions()
    
    print("=" * 40)
    if import_success and function_success:
        print("All tests passed! The package is ready to use.")
    else:
        print("Some tests failed. Please check the errors above.")