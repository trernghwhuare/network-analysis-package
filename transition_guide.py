#!/usr/bin/env python3
"""
Transition guide and helper script for the new directory structure.

This script helps users transition from the old directory structure 
(analysis_out, plots) to the new clearer structure (input_data, output_plots).
"""

import os
import shutil
from pathlib import Path

def print_transition_info():
    """Print information about the directory structure transition."""
    print("=" * 60)
    print("Network Analysis Package - Directory Structure Transition")
    print("=" * 60)
    
    print("\nDIRECTORY STRUCTURE CHANGES:")
    print("To reduce confusion, we've updated the directory names:")
    print("  OLD NAME     → NEW NAME")
    print("  analysis_out → input_data")
    print("  plots        → output_plots")
    
    print("\nWHY THIS CHANGE:")
    print("• Clearer purpose identification (input vs output)")
    print("• Reduced confusion with multiple directories of the same name")
    print("• More intuitive naming for new users")
    
    print("\nBENEFITS:")
    print("• Easier to understand data flow")
    print("• Clearer separation of input and output")
    print("• More maintainable project structure")

def check_existing_directories():
    """Check for existing directories and their contents."""
    print("\n" + "=" * 40)
    print("Checking Existing Directories")
    print("=" * 40)
    
    dirs_to_check = ["analysis_out", "plots", "input_data", "output_plots"]
    
    for dir_name in dirs_to_check:
        if os.path.exists(dir_name):
            files = list(Path(dir_name).glob("*"))
            print(f"\n{dir_name}/ ({len(files)} items):")
            if files:
                for file in files[:5]:  # Show first 5 items
                    print(f"  - {file.name}")
                if len(files) > 5:
                    print(f"  ... and {len(files) - 5} more items")
            else:
                print("  (empty directory)")
        else:
            print(f"\n{dir_name}/ (does not exist)")

def migrate_directories():
    """Help migrate from old to new directory structure."""
    print("\n" + "=" * 40)
    print("Migration Options")
    print("=" * 40)
    
    # Check if we have old directories with content
    old_input_exists = os.path.exists("analysis_out") and any(Path("analysis_out").iterdir())
    old_output_exists = os.path.exists("plots") and any(Path("plots").iterdir())
    
    new_input_exists = os.path.exists("input_data") and any(Path("input_data").iterdir())
    new_output_exists = os.path.exists("output_plots") and any(Path("output_plots").iterdir())
    
    if old_input_exists or old_output_exists:
        print("\nMigration needed: Old directories detected with content")
        
        if old_input_exists and not new_input_exists:
            print("\n1. Migrating analysis_out → input_data")
            try:
                if not os.path.exists("input_data"):
                    os.makedirs("input_data")
                for item in Path("analysis_out").iterdir():
                    shutil.move(str(item), "input_data/")
                print("   ✓ Migration completed")
            except Exception as e:
                print(f"   ✗ Migration failed: {e}")
        
        if old_output_exists and not new_output_exists:
            print("\n2. Migrating plots → output_plots")
            try:
                if not os.path.exists("output_plots"):
                    os.makedirs("output_plots")
                for item in Path("plots").iterdir():
                    shutil.move(str(item), "output_plots/")
                print("   ✓ Migration completed")
            except Exception as e:
                print(f"   ✗ Migration failed: {e}")
    else:
        print("\nNo migration needed: No content in old directories")

def create_directory_structure():
    """Create the recommended directory structure."""
    print("\n" + "=" * 40)
    print("Setting Up Recommended Structure")
    print("=" * 40)
    
    recommended_dirs = ["input_data", "output_plots"]
    
    for dir_name in recommended_dirs:
        try:
            os.makedirs(dir_name, exist_ok=True)
            print(f"✓ Created/verified {dir_name}/ directory")
        except Exception as e:
            print(f"✗ Failed to create {dir_name}/ directory: {e}")

def update_script_references():
    """Provide guidance on updating script references."""
    print("\n" + "=" * 40)
    print("Updating Script References")
    print("=" * 40)
    
    print("\nTo update your own scripts, look for and replace:")
    print("  'analysis_out/'     → 'input_data/'")
    print("  'plots/'           → 'output_plots/'")
    
    print("\nIn Python code:")
    print("  # Old")
    print("  with open('analysis_out/data.json', 'r') as f:")
    print("  plt.savefig('plots/figure.png')")
    print("\n  # New")
    print("  with open('input_data/data.json', 'r') as f:")
    print("  plt.savefig('output_plots/figure.png')")

def main():
    """Main function."""
    print_transition_info()
    check_existing_directories()
    migrate_directories()
    create_directory_structure()
    update_script_references()
    
    print("\n" + "=" * 60)
    print("Transition Guide Complete")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run your analysis scripts using the new directory structure")
    print("2. Check the 'input_data' directory for input files")
    print("3. Check the 'output_plots' directory for generated plots")
    print("4. Refer to README.md for updated usage instructions")

if __name__ == "__main__":
    main()