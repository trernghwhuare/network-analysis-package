# Network Analysis Package

A Python package for analyzing neural network structures and connection ratios.

## Author

Hua Cheng <trernghwhuare@aliyun.com>

## Overview

This package provides tools for analyzing neural networks, with a focus on:

1. Connection type distributions
2. Correlation analysis between different metrics
3. Excitatory/Inhibitory (E/I) ratio analysis
4. Visualization of network properties

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd network-analysis-package

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Main Analysis Tools

The package includes several analysis modules:

1. **Connection Ratio Analysis** - Analyze E/I ratios in neural networks
2. **Standard Analysis** - General network analysis and visualization

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

### Standard Analysis Tools

Standard analysis includes:

- Connection type violin plots
- Correlation heatmaps
- E/I scatter plots with stacked bars
- Batch processing capabilities

## Output

The analysis tools generate several types of plots:

1. **Connection Ratio Plots**:
   - `{network}_regression.png` - Scatter plots with regression lines
   - `{network}_ratio_distributions.png` - Histograms of E/I ratios

2. **Standard Analysis Plots**:
   - `{basename}_summary_connection_violins.png` - Violin plots of connection types
   - `{basename}_clustermap.png` - Clustered correlation heatmap
   - `{basename}_combined_heatmaps.png` - Side-by-side correlation heatmaps
   - `{basename}_ei_with_stacked.png` - E/I ratio scatter plots

## Requirements

- Python 3.6+
- NumPy
- Pandas
- Matplotlib
- Seaborn
- SciPy

See `requirements.txt` for detailed version information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Documentation

See [ANALYSIS_WORKFLOW.md](ANALYSIS_WORKFLOW.md) for detailed documentation on the analysis workflow, function usage, and the new connection ratio analysis module.