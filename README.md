# Network Analysis Package

This package provides tools for analyzing neural network structures and connections. It includes visualization functions for population statistics, correlation analysis, and other network metrics.

## Features

- Generate violin plots for different connection types
- Create clustered correlation heatmaps
- Produce scatter plots with stacked bars for E/I ratios
- Analyze network centrality metrics
- Batch process multiple network datasets

## Installation

To install this package, clone the repository and install with pip:

```bash
git clone <repository-url>
cd network_analysis_package
pip install -e .
```

Or install directly from the source:

```bash
pip install .
```

## Usage

### Command Line Interface

Process all datasets in the analysis_out directory:
```bash
analyze-networks --all
```

Process a specific dataset:
```bash
analyze-networks --basename network_name
```

### As a Module

```python
from network_analysis_package.analysis import (
    plot_connection_type_violins,
    plot_clustered_heatmap,
    plot_combined_heatmaps,
    plot_ei_scatter_with_stacked
)

# Use the functions directly in your code
```

## Functions

### plot_connection_type_violins
Creates violin plots showing distributions of different connection types:
- Chemical connections (cont_out|cont_in)
- Electrical connections (elec_out|elec_in) 
- Input connections (exc_inputs|inh_inputs)
- Can group by regions when available
- Uses logarithmic scaling for better visualization of wide-ranging data

### plot_clustered_heatmap
Generates clustered correlation matrices:
- Spearman or Pearson correlation clustering
- Visual identification of metric redundancies
- Handles non-finite values gracefully

### plot_combined_heatmaps
Generates side-by-side correlation heatmaps:
- Compares Spearman and Pearson correlations
- Visual comparison of different correlation methods

### plot_ei_scatter_with_stacked
Creates scatter plots comparing various metrics:
- E/I ratios and other connection metrics
- Top N populations based on outgoing connections
- Stacked bar visualizations for population composition
- Regression analysis with correlation coefficients

## Requirements

- Python 3.7+
- numpy
- pandas
- matplotlib
- seaborn
- scipy

## Documentation

See [ANALYSIS_WORKFLOW.md](ANALYSIS_WORKFLOW.md) for detailed documentation on the analysis workflow and function usage.