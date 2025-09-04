# Analysis Workflow Documentation

## Overview

This document provides instructions for using the analysis tools in the analysis.py script and the connection ratio analysis tools. The analysis workflow includes generating visualizations of network connection data and analyzing E/I ratios.

## Available Analysis Tools

### Main Analysis Script (analysis.py)

The main analysis script provides functions for generating visualizations of population statistics:

#### Connection Type Violin Plots
The `plot_connection_type_violins` function creates violin plots showing distributions of different connection types:
- Supports chemical connections (cont_out|cont_in)
- Supports electrical connections (elec_out|elec_in) 
- Supports input connections (exc_inputs|inh_inputs)
- Can group by regions when available
- Uses logarithmic scaling for better visualization of wide-ranging data

#### Correlation Heatmaps
The `plot_clustered_heatmap` function generates clustered correlation matrices:
- Spearman or Pearson correlation clustering
- Visual identification of metric redundancies
- Handles non-finite values gracefully

The `plot_combined_heatmaps` function generates side-by-side correlation heatmaps:
- Compares Spearman and Pearson correlations
- Visual comparison of different correlation methods

#### Scatter Plots with Stacked Bars
The `plot_ei_scatter_with_stacked` function creates scatter plots comparing various metrics:
- E/I ratios and other connection metrics
- Top N populations based on outgoing connections
- Stacked bar visualizations for population composition
- Regression analysis with correlation coefficients

### Connection Ratio Analysis (conn_ratio.py)

The connection ratio analysis module provides functions for analyzing E/I ratios in neural networks:

#### Connection Ratio Analysis
The `analyze_connection_ratios` function analyzes connection ratios from JSON files:
- Calculates overall, synaptic, and electrical E/I ratios
- Generates scatter plots with regression lines
- Creates distribution histograms for different ratio types
- Supports multiple network analysis in a single run

## Running Analysis

To run analysis on generated network data:

1. Make sure you have generated network data in the `analysis_out` directory
2. Run the analysis script:
   ```bash
   python analysis.py --basename network_name
   ```
   
   Or to process all datasets:
   ```bash
   python analysis.py --all
   ```
   
   Or without specifying basename (same as --all):
   ```bash
   python analysis.py
   ```

3. Run the connection ratio analysis:
   ```bash
   python -m network_analysis_package.conn_ratio
   ```
   
   Or using the demo workflow:
   ```bash
   python demo_workflow.py
   ```

4. Find the generated plots in the `plots` directory

## Output Files

### From analysis.py
- `{basename}_summary_connection_violins.png`: Violin plots showing connection type distributions
- `{basename}_clustermap.png`: Clustered correlation heatmap
- `{basename}_combined_heatmaps.png`: Combined Spearman/Pearson heatmaps
- `{basename}_ei_with_stacked.png`: E/I ratio scatter plots with stacked bars

### From conn_ratio.py
- `{network}_regression.png`: Scatter plots showing E/I relationships with regression lines
- `{network}_ratio_distributions.png`: Histograms showing distributions of E/I ratios

## Analysis Workflow

### Data Loading
The analysis script loads data from CSV files in the analysis_out directory:
- `{basename}_populations.csv`: Population statistics
- `{basename}_summary.json`: Summary statistics

The connection ratio analysis loads data from JSON files:
- `{network}_connection_stats.json`: Connection statistics

### Processing Steps
1. Load dataset using `load_dataset` function or from JSON files
2. Generate visualizations using the plotting functions
3. Save plots to the output directory
4. Return results including regression statistics

### Batch Processing
When using `--all` flag or not specifying a basename:
1. Find all available datasets using `find_available_datasets`
2. Process each dataset sequentially
3. Generate all plots for each dataset
4. Report success or failure for each dataset

## Best Practices

1. Always verify that network generation completed successfully before running analysis
2. Use descriptive, consistent names for networks
3. Compare new networks to established baselines
4. Use multiple visualization types to get a complete picture
5. Visually inspect plots for anomalies

## Troubleshooting

### Common Issues
1. Missing data files - check that all required files exist
2. Memory issues with large networks
3. Plot generation failures with insufficient data

### Diagnostic Steps
1. Check file paths and confirm all referenced files exist
2. Review console output for warnings or errors
3. Validate data in generated CSV files
4. Monitor memory usage for large networks

### Error Handling
The analysis script includes error handling for:
- Missing files with helpful error messages
- Non-finite values in correlation matrices
- Clustering failures due to data issues
- General exceptions with traceback printing