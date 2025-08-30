"""
Network Analysis Package
========================

A package for analyzing neural network structures and connections.

This package provides tools for:
- Generating visualizations of network connection data
- Computing centrality metrics
- Performing statistical analysis and visualization
- Comparing different network configurations

Main functions:
- plot_connection_type_violins: Creates violin plots for different connection types
- plot_clustered_heatmap: Generates clustered correlation matrices
- plot_combined_heatmaps: Creates side-by-side correlation heatmaps
- plot_ei_scatter_with_stacked: Produces scatter plots with stacked bars for E/I ratios

For command-line usage, run:
    analyze-networks --help
"""

__version__ = "0.1.0"
__author__ = "Hua Cheng"

# Import main functions for easy access
from .analysis import (
    plot_connection_type_violins,
    plot_clustered_heatmap,
    plot_combined_heatmaps,
    plot_ei_scatter_with_stacked,
    load_dataset,
    process_multiple_datasets
)

__all__ = [
    "plot_connection_type_violins",
    "plot_clustered_heatmap",
    "plot_combined_heatmaps",
    "plot_ei_scatter_with_stacked",
    "load_dataset",
    "process_multiple_datasets"
]