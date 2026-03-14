# Network Analysis Workflow: Comprehensive Guide

## Table of Contents
1. [Why Perform Neural Network Analysis?](#why-perform-neural-network-analysis)
2. [Prerequisites](#prerequisites)
3. [Scientific Objectives](#scientific-objectives)
4. [Scientific Contributions](#scientific-contributions)
5. [Procedure Steps](#procedure-steps)
6. [Expected Outputs and Outcome Plots](#expected-outputs-and-outcome-plots)
7. [Best Practices](#best-practices)

---

## Why Perform Neural Network Analysis?

### Biological Significance of E/I Balance

**Excitatory/Inhibitory (E/I) balance** is a fundamental principle in neuroscience that governs neural circuit function, stability, and information processing. The precise ratio between excitatory and inhibitory connections determines:

- **Network Stability**: Proper E/I balance prevents runaway excitation (seizures) or excessive inhibition (silencing)
- **Information Processing**: Optimal E/I ratios enable efficient signal transmission and noise filtering
- **Plasticity and Learning**: Dynamic adjustment of E/I balance underlies learning and memory formation
- **Disease States**: Disrupted E/I balance is implicated in numerous neurological disorders including epilepsy, autism spectrum disorders, schizophrenia, and Alzheimer's disease

### Scientific Rationale for Quantitative Analysis

#### 1. **Beyond Qualitative Descriptions**
Traditional neuroscience often relies on qualitative descriptions of "more excitatory" or "balanced networks." However, precise **quantitative measurement** of E/I ratios enables:
- Objective comparison between different brain regions or experimental conditions
- Statistical validation of hypotheses about network properties
- Reproducible research across laboratories and model systems

#### 2. **Multi-Modal Integration**
Neural circuits utilize both **chemical synapses** and **electrical gap junctions**, each contributing differently to E/I balance:
- **Chemical synapses** provide directional, modifiable communication with neurotransmitter-specific effects
- **Electrical synapses** enable rapid, bidirectional coupling that synchronizes neuronal activity
- **Integrated analysis** reveals how these modalities complement or compensate for each other

#### 3. **Structure-Function Relationships**
The **structural connectivity** (who connects to whom) directly influences **functional dynamics** (how the network behaves):
- Networks with similar overall E/I ratios may have vastly different functional properties based on connection distribution
- Correlation analysis reveals which structural features predict functional outcomes
- Understanding these relationships helps bridge the gap between anatomy and physiology

### Clinical and Research Applications

#### **Neurological Disease Modeling**
- **Epilepsy**: Characterize hyperexcitable networks with elevated E/I ratios
- **Autism Spectrum Disorders**: Investigate imbalanced E/I ratios in specific circuit motifs
- **Neurodegenerative Diseases**: Track progressive changes in network connectivity patterns
- **Psychiatric Disorders**: Identify circuit-level abnormalities underlying behavioral symptoms

#### **Computational Neuroscience**
- **Model Validation**: Compare simulated network architectures to biological data
- **Parameter Optimization**: Use E/I ratios as constraints for realistic network models
- **Emergent Properties**: Understand how microscopic connectivity rules generate macroscopic dynamics

#### **Developmental Neuroscience**
- **Circuit Maturation**: Track how E/I balance evolves during development
- **Critical Periods**: Identify windows when E/I balance is most plastic
- **Experience-Dependent Plasticity**: Quantify how sensory experience shapes network architecture

### Why This Specific Analysis Approach?

#### **Comprehensive Multi-Scale Analysis**
This workflow provides analysis at multiple scales:
- **Overall Network Level**: Global E/I balance across entire circuits
- **Synaptic Level**: Chemical synapse-specific E/I ratios
- **Electrical Level**: Gap junction-specific E/I ratios
- **Population Level**: E/I composition of individual neuronal populations

#### **Statistical Rigor and Visualization**
- **Robust Statistics**: Uses both parametric (Pearson) and non-parametric (Spearman) correlation methods
- **Advanced Visualization**: Employs violin plots, heatmaps, and regression analyses to reveal complex patterns
- **Batch Processing**: Enables systematic comparison across multiple networks or conditions

#### **Reproducible and Standardized**
- **Automated Pipeline**: Reduces human error and ensures consistency
- **Publication-Quality Output**: Generates figures ready for scientific publications
- **Open Source Framework**: Enables collaboration and methodological transparency

### Key Questions This Analysis Addresses

1. **"What is the overall E/I balance in my neural network?"**
   - Quantifies the fundamental excitatory/inhibitory ratio

2. **"How do chemical and electrical connections contribute differently to E/I balance?"**
   - Reveals modality-specific contributions to network stability

3. **"Are there correlations between E/I ratios and other network properties?"**
   - Identifies structure-function relationships

4. **"How variable are connection patterns across different neuronal populations?"**
   - Characterizes heterogeneity within networks

5. **"How does my network compare to established baselines or other experimental conditions?"**
   - Enables comparative analysis across datasets

This analysis framework transforms qualitative observations into **quantitative, statistically rigorous insights** about neural circuit organization, providing essential tools for understanding both normal brain function and pathological states.

---

## Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows
- **Python Version**: Python 3.6 or higher (Python 3.9+ recommended)
- **Disk Space**: Sufficient space for input data and output plots
- **Memory**: At least 4GB RAM (8GB+ recommended for large datasets)

### Software Dependencies
Install the following Python packages using pip:

```bash
pip install numpy>=1.18.0 pandas>=1.0.0 matplotlib>=3.1.0 seaborn>=0.10.0 scipy>=1.4.0
```

Or install from the requirements file:
```bash
pip install -r requirements.txt
```

### Data Requirements
- **Input Format**: JSON files containing network connection statistics
- **Required Fields** in JSON files:
  - `network_name`: String identifier for the network
  - `syn_ee_contacts`: Excitatory-to-excitatory synaptic contacts
  - `syn_ei_contacts`: Excitatory-to-inhibitory synaptic contacts  
  - `syn_ie_contacts`: Inhibitory-to-excitatory synaptic contacts
  - `syn_ii_contacts`: Inhibitory-to-inhibitory synaptic contacts
  - `ele_ee_conductances`: Excitatory electrical conductances
  - `ele_ii_conductances`: Inhibitory electrical conductances
  - `correlation`: Correlation coefficient (optional but recommended)

### Directory Structure Setup
Ensure your project directory contains:
```
network-analysis-workflow/
├── input_data/             # Place your JSON files here
├── analysis_out/           # Population-level CSV data (auto-generated)
├── output_plots/           # Output directory (will be created automatically)
└── network_analysis_package/  # Core analysis modules
```

---

## Scientific Objectives

### Primary Goals
1. **Quantify Excitatory/Inhibitory (E/I) Balance**: Calculate and analyze E/I ratios across different neural network configurations
2. **Characterize Connection Distributions**: Analyze the statistical properties of different connection types (chemical vs. electrical, excitatory vs. inhibitory)
3. **Identify Correlation Patterns**: Discover relationships between network metrics and functional properties
4. **Enable Comparative Analysis**: Facilitate comparison between multiple network architectures or experimental conditions

### Specific Analysis Capabilities
- **Overall E/I Ratio Analysis**: (EE + IE) / (EI + II) calculations
- **Synaptic E/I Ratio Analysis**: Synapse-specific E/I balance assessment
- **Electrical E/I Ratio Analysis**: Gap junction-based E/I balance assessment
- **Multi-dimensional Visualization**: Comprehensive plotting of network properties
- **Batch Processing**: Automated analysis of multiple networks simultaneously

---

## Scientific Contributions

### Methodological Innovations
1. **Integrated Multi-Modal Analysis**: Combines chemical synaptic and electrical gap junction analysis in a unified framework
2. **Comprehensive E/I Quantification**: Provides three distinct E/I ratio metrics (overall, synaptic, electrical) for nuanced analysis
3. **Advanced Visualization Suite**: Offers publication-ready visualizations including violin plots, clustered heatmaps, and regression analyses
4. **Automated Workflow Pipeline**: Streamlines the entire analysis process from raw data to final plots

### Scientific Impact Areas
- **Neural Circuit Characterization**: Enables detailed characterization of neural circuit architecture
- **E/I Balance Studies**: Supports research into excitatory/inhibitory balance in health and disease
- **Network Comparison**: Facilitates systematic comparison between different network models or experimental conditions
- **Reproducible Research**: Provides standardized analysis pipeline for consistent, reproducible results

### Unique Features
- **Dual Analysis Modules**: Separate but complementary connection ratio and standard analysis tools
- **Statistical Rigor**: Implements both Spearman and Pearson correlation analyses with proper handling of non-finite values
- **Scalable Architecture**: Designed for both single-network analysis and batch processing of multiple datasets
- **Publication-Quality Output**: Generates high-resolution, customizable plots suitable for scientific publications

---

## Procedure Steps

### Step 1: Environment Setup
```bash
# Clone the repository (if not already done)
git clone https://github.com/trernghwhuare/network-analysis-workflow.git
cd network-analysis-workflow

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Data Preparation
1. **Prepare JSON Files**: Create JSON files with network statistics following the required format
2. **Place in Input Directory**: Copy all JSON files to the `input_data/` directory
3. **Verify Data Integrity**: Ensure all required fields are present and values are valid numbers

**Example JSON structure**:
```json
{
  "network_name": "CTC_max_plus",
  "syn_ee_contacts": 15000,
  "syn_ei_contacts": 12000,
  "syn_ie_contacts": 10000,
  "syn_ii_contacts": 8000,
  "ele_ee_conductances": 2500,
  "ele_ii_conductances": 2000,
  "correlation": 0.85
}
```

### Step 3: Generate Population-Level Data (NEW STEP)
The standard analysis functions expect population-level CSV data in the `analysis_out/` directory. Run the population data generator:

```bash
python generate_population_data.py
```

This script will:
- Read JSON files from `input_data/`
- Generate synthetic population-level data that reflects the network statistics
- Create the required CSV files in `analysis_out/`:
  - `{network}_populations.csv`
  - `{network}_population_stats.csv` 
  - `{network}_summary.json`

### Step 4: Run Connection Ratio Analysis
Choose one of the following approaches:

**Option A: Interactive Getting Started Script**
```bash
python getting_started.py
```

**Option B: Direct Module Execution**
```bash
python -m network_analysis_package.conn_ratio
```

**Option C: Command Line with Specific Files**
```bash
# Process all files in input_data directory
python run_conn_ratio.py

# Or specify individual files
python demo_conn_ratio.py
```

### Step 5: Run Standard Analysis (NEW PROPER WORKFLOW)
Use the dedicated standard analysis runner to process population-level data:

```bash
# Process all datasets with proper population-level analysis
python run_standard_analysis.py

# Or run the complete demo workflow (includes both analyses)
python demo_workflow.py
```

### Step 5: Generate Sample Plots (For Documentation/Demonstration)
```bash
# Create placeholder images for documentation
python create_placeholder_images.py

# Generate sample plots with real data
python generate_sample_plots.py
```

### Step 6: Verify Results
1. **Check Output Directory**: Verify that plots are generated in `output_plots/`
2. **Validate Plot Quality**: Ensure plots are readable and contain expected data
3. **Review Console Output**: Check for any warnings or error messages

### Step 7: Advanced Usage (Custom Scripts)
For integration into your own workflows:

```python
from network_analysis_package import conn_ratio, analysis
import pandas as pd

# Connection ratio analysis
results = conn_ratio.analyze_connection_ratios(
    json_files=['input_data/your_network.json'],
    plots_dir='output_plots'
)

# Standard analysis with custom DataFrame
df = pd.read_json('input_data/your_network.json')
analysis.plot_connection_type_violins(df, outpath='output_plots/custom_violins.png')
```

---

## Expected Outputs and Outcome Plots

### Connection Ratio Analysis Plots

#### 1. Regression Scatter Plots (`{network_name}_regression.png`)
**What it shows**: Relationship between overall E/I ratio and correlation coefficient
- **X-axis**: Overall E/I ratio = (EE + IE) / (EI + II)
- **Y-axis**: Correlation coefficient from your input data
- **Features**: 
  - Individual data points for each network
  - Linear regression line with confidence intervals
  - Correlation coefficient (R²) and p-value displayed
  - Publication-ready styling with proper labels and legends

**Scientific value**: Reveals whether networks with higher E/I balance tend to have stronger correlations, indicating potential functional relationships between structural balance and network dynamics.

#### 2. Ratio Distribution Histograms (`{network_name}_ratio_distributions.png`)
**What it shows**: Distribution of three different E/I ratio types across your networks
- **Three subplots** showing:
  - **Overall E/I ratios**: Total excitatory vs. inhibitory connections
  - **Synaptic E/I ratios**: Chemical synapse-specific balance
  - **Electrical E/I ratios**: Gap junction-specific balance
- **Features**:
  - Histogram bars showing frequency distribution
  - Kernel density estimation curves overlaid
  - Mean and median markers
  - Statistical summary in plot annotations

**Scientific value**: Allows comparison of how different connection modalities (chemical vs. electrical) contribute to overall E/I balance, revealing modality-specific imbalances.

### Standard Analysis Plots (NOW NETWORK-SPECIFIC!)

#### 3. Connection Type Violin Plots (`{network_name}_summary_connection_violins.png`)
**What it shows**: Distribution characteristics of different connection types **within each network**
- **Connection types displayed**:
  - Chemical outgoing connections (cont_out)
  - Chemical incoming connections (cont_in)  
  - Electrical outgoing connections (elec_out)
  - Electrical incoming connections (elec_in)
  - Excitatory inputs (exc_inputs)
  - Inhibitory inputs (inh_inputs)
- **Features**:
  - Violin shapes showing full distribution (not just quartiles)
  - Logarithmic scaling for wide-ranging data
  - Individual data points overlaid on violins
  - **Network-specific analysis** (each plot shows one network's population distributions)

**Scientific value**: Provides detailed insight into the variability and central tendencies of different connection types **within individual networks**, revealing which connection modalities show the most heterogeneity at the population level.

#### 4. Clustered Correlation Heatmap (`{network_name}_clustermap.png`)
**What it shows**: Correlation matrix with hierarchical clustering **for each network's populations**
- **Matrix content**: Pairwise correlations between all network metrics **across populations within one network**
- **Clustering**: Rows and columns reordered based on similarity
- **Features**:
  - Color-coded correlation strength (-1 to +1)
  - Dendrograms showing clustering relationships
  - Automatic handling of non-finite values
  - Spearman correlation by default (robust to outliers)

**Scientific value**: Identifies groups of highly correlated metrics **within individual networks**, revealing redundant measurements and highlighting key independent variables for further analysis at the population level.

#### 5. Combined Correlation Heatmaps (`{network_name}_combined_heatmaps.png`)
**What it shows**: Side-by-side comparison of Spearman vs. Pearson correlations **for each network**
- **Left panel**: Spearman rank correlation (non-parametric)
- **Right panel**: Pearson correlation (parametric)
- **Features**:
  - Direct visual comparison of correlation methods
  - Highlights differences in correlation sensitivity
  - Same color scale for easy comparison
  - Identical metric ordering for direct comparison

**Scientific value**: Helps determine whether relationships are linear (similar Pearson/Spearman) or monotonic but non-linear (different Pearson/Spearman) **within individual networks**, guiding appropriate statistical interpretation.

#### 6. E/I Scatter Plots with Stacked Bars (`{network_name}_ei_with_stacked.png`)
**What it shows**: Multi-dimensional visualization combining scatter and bar plots **for each network's populations**
- **Main scatter plot**: Various E/I metrics vs. other network properties **across populations**
- **Stacked bars**: Population composition breakdown
- **Features**:
  - Individual populations as data points
  - Stacked bar charts showing excitatory/inhibitory composition per population
  - Regression analysis with correlation coefficients
  - Multiple subplot arrangements for comprehensive view

**Scientific value**: Integrates structural connectivity patterns with population-level E/I composition **within individual networks**, revealing how macro-scale balance relates to micro-scale connection patterns.

### Statistical Results Summary
In addition to visual outputs, the analysis provides:
- **Regression statistics**: Slope, intercept, R², p-values, confidence intervals
- **Descriptive statistics**: Mean, median, standard deviation, quartiles for all ratios
- **Correlation matrices**: Full numerical correlation matrices for programmatic access
- **Clustering results**: Hierarchical clustering dendrograms and cluster assignments

### File Naming Convention
All output files follow consistent naming patterns:
- **Connection Ratio**: `{network_identifier}_regression.png`, `{network_identifier}_ratio_distributions.png`
- **Standard Analysis**: `{network_identifier}_summary_connection_violins.png`, `{network_identifier}_clustermap.png`, etc.
- **Output Location**: All files saved in `output_plots/` directory with automatic creation if needed

### Plot Quality Specifications
- **Resolution**: High-DPI (300 DPI) suitable for publication
- **Format**: PNG files with lossless compression
- **Styling**: Professional scientific styling with proper fonts, colors, and layouts
- **Customization**: All plots use matplotlib/seaborn defaults but can be customized through function parameters

---

## Best Practices

### Data Management
1. **Consistent Naming**: Use descriptive, consistent names for network files
2. **Backup Original Data**: Always keep copies of original input data
3. **Version Control**: Track changes to analysis parameters and data

### Analysis Quality
1. **Validate Input Data**: Always verify JSON file integrity before analysis
2. **Cross-Validation**: Use both connection ratio and standard analysis modules for comprehensive results
3. **Visual Inspection**: Manually inspect generated plots for anomalies or unexpected patterns

### Reproducibility
1. **Document Parameters**: Record all analysis parameters and software versions
2. **Use Relative Paths**: Ensure scripts work regardless of absolute directory location
3. **Test Regularly**: Run test scripts (`test_package.py`, `test_conn_ratio.py`) to verify functionality

### Performance Optimization
1. **Memory Management**: Monitor memory usage for large datasets
2. **Batch Processing**: Use `--all` flag for efficient processing of multiple networks
3. **Incremental Analysis**: Start with small datasets to verify workflow before scaling up

### Troubleshooting Common Issues
- **Missing Files**: Verify all required JSON fields are present
- **Plot Generation Failures**: Check data ranges and ensure sufficient variation in values
- **Memory Errors**: Process datasets individually rather than in large batches
- **Import Errors**: Ensure all dependencies are properly installed with correct versions

This workflow provides a complete, end-to-end solution for neural network analysis with emphasis on E/I balance quantification and comprehensive visualization capabilities.