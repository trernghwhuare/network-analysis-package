# Connection Ratio Analysis Demo

This directory contains a simple demonstration of how the connection ratio analysis works.

## How it works

The connection ratio analysis calculates various ratios related to excitatory (E) and inhibitory (I) connections in neural networks:

1. **Overall E/I Ratio**: Total excitatory connections / Total inhibitory connections
2. **Synaptic E/I Ratio**: Synaptic excitatory connections / Synaptic inhibitory connections
3. **Electrical E/I Ratio**: Electrical excitatory connections / Electrical inhibitory connections

These ratios are calculated from JSON files containing network statistics and visualized in scatter plots with regression lines and distribution histograms.

## Running the demo

To run the demo:

```bash
python run_demo.py
```

This will:
1. Create sample network data in the `analysis_out` directory
2. Run the connection ratio analysis on this data
3. Generate visualization plots in the `plots` directory

## Understanding the output

The analysis generates two types of plots:

1. **Regression plots** (`{network}_regression.png`):
   - Scatter plot showing correlation between overall E/I ratio and network correlation
   - Regression line showing the trend

2. **Distribution plots** (`{network}_ratio_distributions.png`):
   - Histograms showing the distribution of different ratio types
   - Helps understand the spread and central tendency of the ratios

## Integration with the full workflow

The connection ratio analysis is integrated into the main workflow through the `demo_workflow.py` script in the parent directory. This script:

1. Generates network data (simulated in our case)
2. Runs the connection ratio analysis
3. Produces visualizations for analysis