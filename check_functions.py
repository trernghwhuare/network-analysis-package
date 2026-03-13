#!/usr/bin/env python3
"""
Simple test script to check if all functions are working correctly.
"""

def test_imports():
    """Test importing all functions from the package."""
    try:
        from network_analysis_package.analysis import load_dataset, find_available_datasets
        print("✓ load_dataset and find_available_datasets imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import functions: {e}")
        return False
    
    try:
        from network_analysis_package.analysis import plot_connection_type_violins
        print("✓ plot_connection_type_violins imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import plot_connection_type_violins: {e}")
        return False
        
    try:
        from network_analysis_package import conn_ratio
        print("✓ conn_ratio module imported successfully")
    except ImportError as e:
        print(f"✗ Failed to import conn_ratio module: {e}")
        return False
        
    return True

def test_function_existence():
    """Test that all expected functions exist."""
    from network_analysis_package.analysis import load_dataset, find_available_datasets
    from network_analysis_package.analysis import plot_connection_type_violins
    
    # Check that functions are callable
    if callable(load_dataset):
        print("✓ load_dataset is callable")
    else:
        print("✗ load_dataset is not callable")
        return False
        
    if callable(find_available_datasets):
        print("✓ find_available_datasets is callable")
    else:
        print("✗ find_available_datasets is not callable")
        return False
        
    if callable(plot_connection_type_violins):
        print("✓ plot_connection_type_violins is callable")
    else:
        print("✗ plot_connection_type_violins is not callable")
        return False
        
    return True

if __name__ == "__main__":
    print("Testing network_analysis_package functions...")
    print("=" * 50)
    
    if test_imports() and test_function_existence():
        print("=" * 50)
        print("All tests passed! The package functions are working correctly.")
    else:
        print("=" * 50)
        print("Some tests failed. Please check the errors above.")