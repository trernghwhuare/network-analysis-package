# How the Network Analysis Package Works

## Overview

The network analysis package provides a comprehensive set of tools for analyzing neural network structures and connection ratios. The package consists of two main modules:

1. **Connection Ratio Analysis** ([conn_ratio.py](file:///home/leo520/pynml/network-analysis-package-github-clean/network_analysis_package/conn_ratio.py)) - Specialized for E/I ratio calculations and visualization
2. **Standard Analysis** ([analysis.py](file:///home/leo520/pynml/network-analysis-package-github-clean/network_analysis_package/analysis.py)) - General network analysis and visualization tools

## Connection Ratio Analysis

### How It Works

The connection ratio analysis module processes JSON files containing network statistics and calculates various E/I ratios:

1. **Data Input**: JSON files in the `input_data` directory with network connection statistics
2. **Ratio Calculations**:
   - Overall E/I ratio: (EE + IE) / (EI + II)
   - Synaptic E/I ratio: (syn_ee + syn_ie) / (syn_ei + syn_ii)
   - Electrical E/I ratio: ele_ee / ele_ii
3. **Visualization**:
   - Scatter plots showing correlation between ratios and other metrics
   - Distribution histograms for different ratio types
4. **Output**: Plots saved in the `output_plots` directory

### Key Functions

- `analyze_connection_ratios()`: Main analysis function
- `calculate_ratios()`: Calculates various E/I ratios
- `plot_regression()`: Creates scatter plots with regression lines
- `plot_distributions()`: Generates distribution histograms

## Standard Analysis

### How It Works

The standard analysis module provides general network analysis and visualization capabilities:

1. **Data Input**: DataFrame with network statistics
2. **Analysis Types**:
   - Connection type distributions (violin plots)
   - Correlation analysis (heatmaps)
   - E/I ratio comparisons (scatter plots)
3. **Visualization**:
   - Violin plots for different connection types
   - Clustered correlation heatmaps
   - Combined heatmaps (Spearman vs Pearson)
   - E/I scatter plots with stacked bars
4. **Output**: Plots saved in the `output_plots` directory

### Key Functions

- `plot_connection_type_violins()`: Creates violin plots for connection types
- `plot_clustered_heatmap()`: Generates clustered correlation heatmap
- `plot_combined_heatmaps()`: Creates side-by-side correlation heatmaps
- `plot_ei_scatter_with_stacked()`: Generates E/I ratio scatter plots

## Directory Structure

To avoid confusion with directory names, the package uses a clear directory structure:

```
network-analysis-workflow/
├── input_data/             # Input data (JSON files with network statistics)
├── output_plots/           # Output visualizations and plots
├── network_analysis_package/
│   ├── __init__.py
│   ├── conn_ratio.py       # Connection ratio analysis functionality
│   └── analysis.py         # Standard analysis tools
├── example_usage.py        # Example script
├── demo_workflow.py        # Demo workflow
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

## Workflow Integration

Both analysis modules can be used independently or together in a complete workflow:

1. **Prepare Data**: Place JSON files in the `input_data` directory
2. **Run Analysis**: Execute either or both analysis modules
3. **View Results**: Check generated plots in the `output_plots` directory

### Example Workflow

```python
# Connection ratio analysis
from network_analysis_package import conn_ratio
results = conn_ratio.analyze_connection_ratios(
    json_files=['input_data/network_stats.json'],
    plots_dir='output_plots'
)

# Standard analysis
from network_analysis_package import analysis
analysis.plot_connection_type_violins(dataframe, outpath='output_plots/violins.png')
```

## Data Format

### JSON Input Format

The connection ratio analysis expects JSON files with the following structure:

```json
{
  "network_name": "Sample_Network",
  "syn_ee_contacts": 15000,
  "syn_ei_contacts": 12000,
  "syn_ie_contacts": 10000,
  "syn_ii_contacts": 8000,
  "ele_ee_conductances": 2500,
  "ele_ii_conductances": 2000,
  "correlation": 0.85
}
```

### DataFrame Format

The standard analysis functions expect a pandas DataFrame with columns for different connection types:

```
network                syn_ee_contacts  syn_ei_contacts  ...  correlation
Sample_Network_1       15000            12000            ...  0.85
Sample_Network_2       18000            15000            ...  0.90
```

## Visualization Types

### Connection Ratio Analysis Plots

1. **Regression Plots**: Scatter plots showing relationship between E/I ratios and correlation
2. **Distribution Plots**: Histograms showing spread of different ratio types

### Standard Analysis Plots

1. **Violin Plots**: Distribution of different connection types
2. **Clustered Heatmaps**: Correlation matrices with clustering
3. **Combined Heatmaps**: Side-by-side Spearman and Pearson correlations
4. **E/I Scatter Plots**: E/I ratios with stacked bar visualizations

## Output Files

Generated plots are saved in the `output_plots` directory with descriptive names:

- `{network}_regression.png`: Connection ratio regression plots
- `{network}_ratio_distributions.png`: Ratio distribution histograms
- `{basename}_summary_connection_violins.png`: Connection type violin plots
- `{basename}_clustermap.png`: Clustered correlation heatmaps
- `{basename}_combined_heatmaps.png`: Combined correlation heatmaps
- `{basename}_ei_with_stacked.png`: E/I ratio scatter plots

## Best Practices

1. **Data Organization**: Keep input data in the `input_data` directory
2. **Output Management**: Check the `output_plots` directory for results
3. **Modular Usage**: Use either analysis module independently or together
4. **Consistent Naming**: Use descriptive names for networks and files