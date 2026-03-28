# Comprehensive Pipeline for Large-Scale Neuronal Network Construction and Analysis

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/trernghwhuare/network-analysis-package/main)

This repository contains the complete computational pipeline for constructing, simulating, and analyzing large-scale biologically detailed neuronal networks spanning multiple cortical and thalamic regions.

## Overview

Our methodology integrates morphologically realistic single-cell models with region-specific connectivity rules derived from anatomical data, enabling the generation of networks containing over 145,000 neurons and 581,743 synaptic and electrical connections. The pipeline employs a multi-layered approach combining chemical synapses (AMPA, NMDA, GABA_A, GABA_B) with electrical gap junctions, and incorporates cell-type-specific classification based on transcriptomic and morphological criteria.

## Key Features

- **Morphologically detailed single-cell models** based on experimental reconstructions
- **Cell-type-specific connectivity rules** derived from anatomical and physiological data  
- **Comprehensive thalamocortical integration** with appropriate driver/modulator distinctions
- **Standardized model representation** using NeuroML2 for interoperability
- **Scalable architecture** supporting networks with >145K neurons and >580K connections

## Repository Structure

```
├── cell_files/           # Morphologically detailed neuronal models
├── channel_files/        # Ion channel models
├── net_files/            # Generated network files
├── net_params/           # Network parameter configurations
├── analysis_out/         # Analysis output files (JSON format)
├── html/                 # Interactive HTML visualizations
├── plots/                # Static plots and figures
├── *.py                  # Core analysis and simulation scripts
├── *.nml                 # NeuroML2 model files
└── neuronal_network_construction_analysis_paper.md  # Main paper
```

## Installation and Setup

### Using Conda
```bash
# Clone the repository
git clone https://github.com/trernghwhuare/network-analysis-package.git
cd network-analysis-package

# Create environment from environment.yml
conda env create -f environment.yml
conda activate pynml-neurolibre

# Install NEURON separately (not available via conda)
# Follow instructions at: https://neuron.yale.edu/neuron/download
```

### Using Pixi (Recommended)
```bash
# Install pixi if not already installed
curl -fsSL https://pixi.sh/install.sh | bash

# Activate the environment
pixi shell
```

## Usage

The pipeline consists of several key steps:

1. **Single-cell simulation**: Run individual cell simulations using scripts like `00_sim_TCRc.py`
2. **Network construction**: Generate networks using scripts like `11_C2T_max+.py`  
3. **Analysis**: Perform network analysis using `analysis.py` and related scripts
4. **Visualization**: Generate interactive HTML visualizations using `create_interactive_layered_graph.py`

For detailed usage instructions, refer to the main paper document.

## Reproducibility

This repository is designed for full reproducibility and has been prepared for publication on [neuroLibre](https://neurolibre.ca/). All dependencies are specified in:
- `pixi.toml` (primary dependency management)
- `environment.yml` (conda environment)
- `requirements.txt` (pip requirements)

## Citation

If you use this work in your research, please cite:

> Cheng, H. (2026). Comprehensive Pipeline for Large-Scale Neuronal Network Construction and Analysis. *neuroLibre*.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Blue Brain Project for neuronal reconstructions and standardized cell templates
- NeuroMorpho.Org database for morphological data
- Allen Institute Cell Types Database for transcriptomic classifications
- pyNeuroML and NEURON communities for simulation infrastructure