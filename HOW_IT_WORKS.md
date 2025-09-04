# How the Network Analysis Package Works

## Overview

The network analysis package provides tools for analyzing neural networks, with a focus on:

1. Connection type distributions
2. Correlation analysis between different metrics
3. Excitatory/Inhibitory (E/I) ratio analysis
4. Visualization of network properties

## Package Structure

The package consists of two main modules:

1. **conn_ratio**: Connection ratio analysis functionality
2. **analysis**: General network analysis and visualization functions

## Connection Ratio Analysis (conn_ratio)

### Data Input

The analysis takes JSON files as input, which contain network statistics. Each JSON file should include:

- Network name
- Synaptic connection counts (EE, EI, IE, II)
- Electrical connection counts (EE, II)
- Correlation values

Example JSON structure:
```json
{
  "network_name": "CTC_max_plus_network",
  "syn_ee_contacts": 18000,
  "syn_ei_contacts": 15000,
  "syn_ie_contacts": 12000,
  "syn_ii_contacts": 10000,
  "ele_ee_conductances": 3000,
  "ele_ii_conductances": 2500,
  "correlation": 0.87
}
```

### Ratio Calculations

The analysis calculates several types of ratios:

1. **Overall E/I Ratio**: 
   - (syn_ee_contacts + syn_ie_contacts + ele_ee_conductances) / 
     (syn_ei_contacts + syn_ii_contacts + ele_ii_conductances)

2. **Synaptic E/I Ratio**: 
   - (syn_ee_contacts + syn_ie_contacts) / (syn_ei_contacts + syn_ii_contacts)

3. **Electrical E/I Ratio**: 
   - ele_ee_conductances / ele_ii_conductances

### Visualization

The analysis generates two types of plots:

1. **Regression Plots**:
   - Scatter plot showing the relationship between overall E/I ratio and network correlation
   - Includes a regression line to show the trend

2. **Distribution Plots**:
   - Histograms showing the distribution of different ratio types
   - Helps understand the spread and central tendency of the ratios

## Standard Analysis (analysis)

The standard analysis module provides several visualization functions:

1. **Connection Type Violin Plots**:
   - [plot_connection_type_violins()](file:///home/leo520/pynml/network-analysis-package-github-clean/network_analysis_package/analysis.py#L47-L94) - Violin plots for different connection types

2. **Correlation Heatmaps**:
   - [plot_clustered_heatmap()](file:///home/leo520/pynml/network-analysis-package-github-clean/network_analysis_package/analysis.py#L97-L136) - Clustered correlation heatmap
   - [plot_combined_heatmaps()](file:///home/leo520/pynml/network-analysis-package-github-clean/network_analysis_package/analysis.py#L139-L192) - Side-by-side correlation heatmaps

3. **E/I Ratio Visualization**:
   - [plot_ei_scatter_with_stacked()](file:///home/leo520/pynml/network-analysis-package-github-clean/network_analysis_package/analysis.py#L195-L255) - E/I ratio scatter plots with stacked bars

## Integration with Main Workflow

Both analysis modules are integrated into the main analysis workflow through the `demo_workflow.py` script, which:

1. Generates network data (simulated in our case)
2. Runs both connection ratio analysis and standard analysis
3. Produces visualizations for analysis
4. Outputs results to console and files

## Running the Analysis

You can run the analysis in several ways:

### As Modules
```bash
python -m network_analysis_package.conn_ratio
python -m network_analysis_package.analysis
```

### From Scripts
```python
from network_analysis_package import conn_ratio, analysis

# Connection ratio analysis
results = conn_ratio.analyze_connection_ratios(json_files, plots_dir='plots')

# Standard analysis
analysis.plot_connection_type_violins(dataframe, outpath='plots/violins.png')
```

### Using the Demo Workflow
```bash
python demo_workflow.py
```

## Author

Hua Cheng <trernghwhuare@aliyun.com>