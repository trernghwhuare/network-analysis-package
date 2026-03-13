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

1. Make sure you have generated network data in the `input_data` directory
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

4. Find the generated plots in the `output_plots` directory

## Using the Package Locally

To use the network analysis package locally, follow these steps:

### 1. Clone or Download the Repository

First, you need to get the code on your local machine:

```bash
git clone https://github.com/trernghwhuare/network-analysis-workflow.git
cd network-analysis-workflow
```

If you don't have Git installed, you can download the repository as a ZIP file from GitHub and extract it.

### 2. Set Up Your Environment

Make sure you have Python 3.6 or higher installed on your system. You can check your Python version with:

```bash
python --version
```

or

```bash
python3 --version
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install all necessary dependencies including:
- numpy
- pandas
- matplotlib
- seaborn
- scipy

### 4. Prepare Your Data

The package expects network data in JSON format. You'll need to create JSON files with network statistics in the `input_data` directory. Each file should contain data like:

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

### 5. Run the Analysis

#### Option 1: Use the Example Script

Run the example usage script to see how the package works:

```bash
python example_usage.py
```

This will create sample data and run both connection ratio analysis and standard analysis.

#### Option 2: Direct Module Usage

You can also run the modules directly:

```bash
# Run connection ratio analysis
python -m network_analysis_package.conn_ratio

# Run standard analysis (if you have data prepared)
python -m network_analysis_package.analysis
```

#### Option 3: Import in Your Own Scripts

Create your own Python script and import the modules:

```python
from network_analysis_package import conn_ratio, analysis
import pandas as pd
import json

# For connection ratio analysis
results = conn_ratio.analyze_connection_ratios(
    json_files=['input_data/your_network_data.json'],
    plots_dir='output_plots'
)

# For standard analysis
# Load your data into a DataFrame
df = pd.read_json('input_data/your_network_data.json')
analysis.plot_connection_type_violins(df, outpath='output_plots/violins.png')
```

### 6. View the Results

After running the analysis, you'll find the generated plots in the `output_plots` directory. The package generates several types of visualizations:

1. Connection ratio regression plots
2. Ratio distribution histograms
3. Connection type violin plots
4. Correlation heatmaps
5. E/I ratio scatter plots

### 7. Run the Demo Workflow

To see a complete workflow demonstration:

```bash
python demo_workflow.py
```

This will create sample data, run both analysis modules, and generate all visualization types.

### 8. Generate Sample Plots for Documentation

If you want to generate sample plots for documentation purposes:

```bash
# Generate placeholder images for documentation
python create_placeholder_images.py

# Generate sample plots with actual data
python generate_sample_plots.py
```

### 9. Test the Package

To verify that the package is working correctly:

```bash
python test_package.py
```

This will test importing the modules and check that key functions are available.

### Directory Structure

After running the analyses, your directory structure will look like this:

```
network-analysis-workflow/
├── input_data/             # Input data (JSON files)
├── output_plots/           # Output visualizations
├── network_analysis_package/
│   ├── __init__.py
│   ├── conn_ratio.py       # Connection ratio analysis
│   └── analysis.py         # Standard analysis tools
├── example_usage.py        # Example script
├── demo_workflow.py        # Demo workflow
├── requirements.txt        # Dependencies
└── README.md              # Documentation
```

### Troubleshooting

If you encounter any issues:

1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Check that you're using Python 3.6 or higher
3. Ensure your JSON data files are properly formatted
4. Verify that you have write permissions in the directory for creating output files

The package is designed to be modular, so you can use either the connection ratio analysis, the standard analysis, or both depending on your needs.

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
The analysis script loads data from CSV files in the input_data directory:
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