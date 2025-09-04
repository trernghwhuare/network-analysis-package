# Network Analysis Package

A comprehensive Python package for analyzing neural network structures and connection ratios, with advanced visualization capabilities.

![Build Status](https://img.shields.io/github/actions/workflow/status/trernghwhuare/network-analysis-workflow/python-app.yml?branch=main)
![License](https://img.shields.io/github/license/trernghwhuare/network-analysis-workflow)
![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)

## Overview

This package provides a robust set of tools for analyzing neural networks, with a focus on:

1. Connection type distributions
2. Correlation analysis between different metrics
3. Excitatory/Inhibitory (E/I) ratio analysis
4. Visualization of network properties
5. Batch processing capabilities

## Author

Hua Cheng <trernghwhuare@aliyun.com>

## Installation

```bash
# Clone the repository
git clone https://github.com/trernghwhuare/network-analysis-workflow.git
cd network-analysis-workflow

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Main Analysis Tools

The package includes several powerful analysis modules:

1. **Connection Ratio Analysis** - Comprehensive analysis of E/I ratios in neural networks
2. **Standard Analysis** - General network analysis and visualization tools

### Running Connection Ratio Analysis

```python
from network_analysis_package import conn_ratio

# Analyze connection ratios from JSON files
results = conn_ratio.analyze_connection_ratios(
    json_files=['analysis_out/network_connection_stats.json'],
    plots_dir='plots'
)
```

Or run directly as a module:
```bash
python -m network_analysis_package.conn_ratio
```

### Running Standard Analysis

```python
from network_analysis_package import analysis

# Plot connection type violins
analysis.plot_connection_type_violins(dataframe, outpath='plots/violins.png')

# Plot clustered heatmap
analysis.plot_clustered_heatmap(dataframe, outpath='plots/clustermap.png')

# Plot combined heatmaps
analysis.plot_combined_heatmaps(dataframe, outpath='plots/combined.png')

# Plot E/I scatter with stacked bars
analysis.plot_ei_scatter_with_stacked(dataframe, outpath='plots/ei_stacked.png')
```

Or run the standard analysis script:
```bash
# Process all datasets in analysis_out directory
python analysis.py --all

# Process a specific dataset
python analysis.py --basename network_name
```

## Package Structure

```
network_analysis_package/
├── __init__.py
├── conn_ratio.py          # Connection ratio analysis functionality
├── analysis.py            # Standard analysis tools
└── ...                    # Other modules
```

## Features

### Connection Ratio Analysis

The connection ratio analysis module provides:

- Overall E/I ratio calculations
- Synaptic E/I ratio calculations
- Electrical E/I ratio calculations
- Scatter plots with regression analysis
- Distribution histograms for different ratio types
- Batch processing of multiple networks
- Detailed statistical analysis

### Standard Analysis Tools

Standard analysis includes:

- Connection type violin plots
- Correlation heatmaps (clustered and combined views)
- E/I scatter plots with stacked bars
- Customizable visualization options
- Batch processing capabilities

## Output

The analysis tools generate several types of publication-quality plots:

1. **Connection Ratio Plots**:
   - `{network}_regression.png` - Scatter plots with regression lines
   - `{network}_ratio_distributions.png` - Histograms of E/I ratios

2. **Standard Analysis Plots**:
   - `{basename}_summary_connection_violins.png` - Violin plots of connection types
   - `{basename}_clustermap.png` - Clustered correlation heatmap
   - `{basename}_combined_heatmaps.png` - Side-by-side correlation heatmaps
   - `{basename}_ei_with_stacked.png` - E/I ratio scatter plots

All plots are saved in the specified output directory with consistent naming conventions.

## Requirements

- Python 3.6+
- NumPy
- Pandas
- Matplotlib
- Seaborn
- SciPy
- scikit-learn (for clustering)
- statsmodels (for statistical analysis)

See `requirements.txt` for detailed version information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Documentation

See [ANALYSIS_WORKFLOW.md](ANALYSIS_WORKFLOW.md) for detailed documentation on the analysis workflow, function usage, and the new connection ratio analysis module.