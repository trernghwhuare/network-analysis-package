"""
Network Analysis Package
========================

A package for analyzing neural network structures and connection ratios.

Modules:
- conn_ratio: Connection ratio analysis functionality
- analysis: General network analysis and visualization functions
"""

__version__ = "0.1.0"
__author__ = "Hua Cheng"

from . import conn_ratio
from . import analysis

# Import main functions for easy access
from .analysis import (
    plot_connection_type_violins,
    plot_clustered_heatmap,
    plot_combined_heatmaps,
    plot_ei_scatter_with_stacked,
    load_dataset,
    find_available_datasets
)

__all__ = [
    "plot_connection_type_violins",
    "plot_clustered_heatmap", 
    "plot_combined_heatmaps",
    "plot_ei_scatter_with_stacked",
    "load_dataset",
    "find_available_datasets",
    "conn_ratio",
    "analysis"
]