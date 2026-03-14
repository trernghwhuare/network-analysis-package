#!/usr/bin/env python3
"""
Run standard analysis on population-level data.

This script demonstrates the proper workflow for running standard analysis
using the population-level CSV data generated in analysis_out/ directory.
"""

import os
import sys
from pathlib import Path


def run_standard_analysis_for_dataset(basename, indir="analysis_out", outdir="output_plots"):
    """
    Run standard analysis for a specific dataset.
    
    Parameters:
      - basename: base name of the dataset (e.g., "CTC_max_plus_network")
      - indir: input directory containing population data
      - outdir: output directory for plots
    """
    try:
        from network_analysis_package import analysis
        
        # Load dataset
        dataset = analysis.load_dataset(basename, indir=indir)
        pop_stats_df = dataset['pop_stats_df']
        
        # Create output directory
        Path(outdir).mkdir(exist_ok=True)
        
        print(f"Running standard analysis for {basename}...")
        
        # Run all analysis functions
        analysis.plot_connection_type_violins(
            pop_stats_df, 
            outpath=f"{outdir}/{basename}_summary_connection_violins.png",
            basename=basename
        )
        
        analysis.plot_clustered_heatmap(
            pop_stats_df,
            outpath=f"{outdir}/{basename}_clustermap.png",
            basename=basename
        )
        
        analysis.plot_combined_heatmaps(
            pop_stats_df,
            outpath=f"{outdir}/{basename}_combined_heatmaps.png",
            basename=basename
        )
        
        analysis.plot_ei_scatter_with_stacked(
            pop_stats_df,
            outpath=f"{outdir}/{basename}_ei_with_stacked.png",
            basename=basename
        )
        
        print(f"✓ Completed standard analysis for {basename}")
        return True
        
    except Exception as e:
        print(f"✗ Error running standard analysis for {basename}: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_standard_analyses(indir="analysis_out", outdir="output_plots"):
    """
    Run standard analysis for all available datasets.
    """
    try:
        from network_analysis_package import analysis
        
        # Find all available datasets
        basenames = analysis.find_available_datasets(indir=indir)
        
        if not basenames:
            print(f"No datasets found in {indir}/ directory.")
            print("Please run 'python generate_population_data.py' first to create population data.")
            return False
        
        print(f"Found {len(basenames)} datasets: {basenames}")
        print("Running standard analysis for all datasets...")
        
        success_count = 0
        for basename in basenames:
            if run_standard_analysis_for_dataset(basename, indir=indir, outdir=outdir):
                success_count += 1
        
        print(f"\nCompleted analysis for {success_count}/{len(basenames)} datasets.")
        return success_count > 0
        
    except Exception as e:
        print(f"Error running all standard analyses: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main function to run standard analysis."""
    print("Network Analysis - Standard Analysis Runner")
    print("=" * 50)
    
    # Check if analysis_out directory exists and has data
    if not Path("analysis_out").exists() or not list(Path("analysis_out").glob("*_populations.csv")):
        print("No population data found in analysis_out/ directory.")
        print("Generating population data from input_data/ JSON files...")
        
        # Import and run population data generation
        try:
            from generate_population_data import generate_analysis_out_data
            if not generate_analysis_out_data():
                print("Failed to generate population data. Exiting.")
                sys.exit(1)
        except ImportError:
            print("generate_population_data.py not found. Please create it first.")
            sys.exit(1)
    
    # Run standard analysis
    success = run_all_standard_analyses()
    
    if success:
        print("\n✓ All standard analyses completed successfully!")
        print("Check the 'output_plots' directory for network-specific plots:")
        print("  - {network}_summary_connection_violins.png")
        print("  - {network}_clustermap.png")  
        print("  - {network}_combined_heatmaps.png")
        print("  - {network}_ei_with_stacked.png")
    else:
        print("\n✗ Some analyses failed. Please check error messages above.")


if __name__ == "__main__":
    main()