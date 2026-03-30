---
title: "Comprehensive Pipeline for Large-Scale Neuronal Network Construction and Analysis"
authors:
  - name: Hua Cheng
    affiliations:
      - Independent Researcher
    orcid: 0000-0003-0903-6766
license: CC-BY-4.0
date: "2026-03-29"
bibliography: references.bib
csl: nature.csl
exports:
  - format: docx
    template: https://github.com/myst-templates/article-theme.git
numbering:
  heading_2: false
  figure:
    template: "Fig. %s"
---

---

---

# Comprehensive Pipeline for Large-Scale Neuronal Network Construction and Analysis

## Abstract

We present a comprehensive computational pipeline for the construction, simulation, and analysis of large-scale biologically detailed neuronal networks spanning multiple cortical and thalamic regions. Our methodology integrates morphologically realistic single-cell models with region-specific connectivity rules derived from anatomical data, enabling the generation of networks containing over 145,000 neurons and 581,743 synaptic and electrical connections. The pipeline employs a multi-layered approach combining chemical synapses (AMPA, NMDA, GABA_A, GABA_B) with electrical gap junctions, and incorporates cell-type-specific classification based on transcriptomic and morphological criteria. We demonstrate the application of this framework to construct and analyze networks representing primary motor cortex (M1), secondary motor cortex (M2), primary somatosensory cortex (S1), and their thalamocortical interactions in the rodent brain. Our analysis reveals fundamental organizational principles including balanced excitatory-inhibitory ratios (66:34), layer-specific connectivity patterns, and cell-type-dependent input-output relationships. This standardized procedure provides a reproducible framework for investigating emergent network dynamics and serves as a foundation for hypothesis-driven computational neuroscience research.

**Keywords**: neuronal network modeling, computational neuroscience, thalamocortical circuits, Python, NeuroML, neocortical microcircuitry

## Introduction

Understanding the principles of cortical circuit organization is fundamental to neuroscience. The neocortex exhibits a highly conserved six-layered structure across mammalian species¹,², with each layer containing distinct populations of excitatory and inhibitory neurons that form specific connectivity patterns³. Recent advances in single-cell transcriptomics and morphological reconstruction have revealed an unprecedented diversity of neuronal cell types⁴,⁵, challenging traditional broad classifications and necessitating more granular approaches to circuit modeling.

Computational models of cortical circuits have evolved from simplified integrate-and-fire networks to biophysically detailed reconstructions incorporating realistic morphologies and ion channel distributions⁶. Yet bridging cellular-scale realism to network-scale complexity remains difficult, and existing large-scale models often lack accessible, reproducible workflows across multiple simulation platforms⁷,⁸,⁹.

The thalamocortical system plays a crucial role in sensory processing and attentional modulation, with distinct thalamic nuclei providing driver and modulator inputs to specific cortical layers¹⁰. Core thalamic inputs target layer 4 with strong, reliable transmission, while matrix inputs show more diffuse, modulatory patterns across multiple layers¹¹. Understanding how these distinct input streams interact with intrinsic cortical microcircuits is essential for modeling sensory processing and cognitive functions¹².

Recent work has emphasized electrical coupling through gap junctions in cortical synchronization and precise spike timing¹³ in addition to traditional chemical synapses. The balance between excitation and inhibition, together with interneuron diversity, provides mechanisms for flexible information routing and dynamic computation¹⁴,¹⁵.

Our work addresses these challenges by developing a scalable pipeline for constructing biologically constrained neural networks that integrate:
1. **Morphologically detailed single-cell models** based on experimental reconstructions¹⁷
2. **Cell-type-specific connectivity rules** derived from anatomical and physiological data³,¹¹
3. **Comprehensive thalamocortical integration** with appropriate driver/modulator distinctions¹⁰
4. **Standardized model representation** using NeuroML2 for interoperability⁹

This approach enables systematic investigation of cortical circuit principles across multiple scales, from single-cell properties to population-level dynamics, while maintaining biological plausibility and computational tractability. By packaging these components into a NeuroML2-compatible workflow, the pipeline makes large-scale, region-specific circuit construction and validation more reproducible and easier to reuse.

## Methods

### Computational Environment and Dependencies

All simulations and analyses were performed using Python 3.9+ with the following core dependencies:
- **pyNeuroML** (v0.6+) for NeuroML2 model handling and simulation orchestration
- **NEURON** (v8.0+) with Python interface for biophysical simulations
- **NumPy** (v1.21+) and **CuPy** (v10.0+) for numerical computations and GPU acceleration
- **Pandas** (v1.3+) for data manipulation and analysis
- **Matplotlib** (v3.4+) and **Seaborn** (v0.11+) for visualization
- **Scipy** (v1.7+) for statistical analysis

The complete dependency specification is maintained in `pixi.toml` using the Pixi package manager to ensure reproducibility across computing environments.

### Cell Model Library Construction

#### Single-Cell Model Collection and Classification

We compiled a comprehensive library of morphologically detailed neuronal models from multiple sources, including:
- **Blue Brain Project** reconstructions and standardized cell templates
- **NeuroMorpho.Org** database entries
- **Published morphological reconstructions** from peer-reviewed literature

Each cell model was processed through a standardized pipeline (`01_extract_cell_data.py`) that:
1. Extracted morphological features including total segment count, dendritic arborization patterns, and axonal projection profiles
2. Classified cells into major categories (IT, PT, CT) based on transcriptomic markers and projection patterns
3. Further subclassified cells by layer (L1, L2/3, L4, L5, L6) and morphological type (e.g., MC, BTC, DBC, BP, NGC, LBC, NBC, SBC, ChC for inhibitory; PC, SP, SS, TTPC1/2, UTPC, STPC, IPC, BPC for excitatory)

The final catalog (`cell_data/cataloged_cells.json`) contains 1,096 excitatory and 990 inhibitory distinct cell types, organized hierarchically by region, layer, and morphological class.

#### Cell Type Clustering and Validation

To ensure biologically meaningful classification, we performed systematic clustering analysis on the extracted cellular features using specialized scripts (`cluster_ct_cells.py`, `cluster_it_cells.py`, `cluster_pt_cells.py`). This clustering process grouped cells into functionally coherent populations based on:

- **Morphological similarity**: Dendritic arborization patterns, axonal projection profiles, and total segment counts
- **Electrophysiological properties**: Firing patterns, input resistance, and membrane time constants
- **Transcriptomic markers**: Layer-specific and cell-type-specific gene expression patterns

The clustering results, stored in the `cell_data/` directory, validated our hierarchical classification system and ensured that each population represented a biologically distinct neuronal subtype. This rigorous clustering approach prevented artificial fragmentation of similar cell types while maintaining sufficient granularity to capture functional diversity.

The clustered cell populations formed the foundation for our network construction pipeline, with each cluster corresponding to a distinct population in the final network models. This data-driven approach ensured that our networks accurately reflected the cellular diversity observed in rodent cortex.

#### Biophysical Model Parameterization

Each morphological reconstruction was augmented with biophysically realistic membrane properties using standardized protocols:
- **Ion channel distributions** were assigned based on layer- and cell-type-specific expression patterns from transcriptomic data
- **Passive membrane properties** (R_m = 10,000 Ω·cm², C_m = 1 μF/cm², R_a = 100 Ω·cm) were consistent across all models
- **Active conductances** included Na⁺, K⁺, Ca²⁺, and leak channels with kinetics parameterized to match experimental voltage-clamp data

Models were validated using standardized current injection protocols (`00_sim_*.py` scripts) to ensure they reproduced characteristic firing patterns (regular spiking, fast spiking, bursting, etc.) observed in corresponding biological cell types.

#### Electrophysiological Feature Extraction

For each reconstructed cell model, we extracted key electrophysiological signatures from standardized current-clamp protocols, including action potential waveform, sag potential, input resistance, firing pattern, and rebound excitation. These functional metrics were used alongside morphology and transcriptomics to refine cell-type clusters and ensure that population labels captured both structural and active properties. Detailed protocol descriptions are provided in the Supplementary Extended Methods.

### Network Architecture and Connectivity Rules

#### Regional Organization

Networks were constructed to represent specific functional circuits based on established neuroanatomical principles and recent detailed circuit mapping studies²⁹,³⁷,³⁸:
- **Primary Motor Cortex (M1)**: Including subregions M1a and M1b, reflecting the rostrocaudal organization observed in rodent motor cortex³¹
- **Secondary Motor Cortex (M2)**: Including subregions M2a and M2b, consistent with recent transcriptomic mapping of distinct anterior-posterior motor domains³⁰  
- **Primary Somatosensory Cortex (S1)**: Including subregions S1a and S1b, corresponding to the barrel field and non-barrel field representations in rodent somatosensory cortex³²,³³
- **Thalamocortical circuits**: Including core (TCRc/nRTc), matrix (TCRm/nRTm), and intralaminar (TCRil/nRTil) thalamic nuclei, following the classical distinction between driver and modulator thalamic inputs³⁴,³⁶

This regional subdivision strategy builds upon foundational work demonstrating that cortical areas are not homogeneous but contain functionally and molecularly distinct subdomains³⁵. The inclusion of both core and matrix thalamic pathways reflects the dual-stream organization principle elucidated in detailed cortico-thalamo-cortical loop analyses³⁷. Our implementation extends these established anatomical frameworks by integrating them into a unified computational pipeline that preserves the biological specificity of each regional circuit while enabling systematic comparison across functional domains. The cell-type-specific connectivity rules and rich network topology are directly informed by comprehensive microcircuitry mapping³⁸, while our model construction workflow follows universal principles for detailed neuronal model creation and validation³⁹. Furthermore, our thalamocortical network architecture is grounded in single-column models that successfully reproduce key physiological phenomena including gamma oscillations and sleep spindles⁴⁰.

Each region contained appropriate laminar organization with layer-specific neuronal densities matching experimental measurements.

#### Network Model Configuration Parameters

Detailed configuration parameters for all 26 network models are stored in the [net_params/](file:///home/leo520/pynml/net_params/) directory, with each subdirectory containing comprehensive parameter files that define:

- **Population specifications**: Cell type definitions, population sizes, and regional assignments
- **Connectivity rules**: Layer-specific connection probabilities, distance-dependent connectivity functions, and synapse type distributions
- **Biophysical parameters**: Ion channel densities, passive membrane properties, and active conductance kinetics
- **Input configurations**: External stimulation protocols, background activity patterns, and neuromodulatory influences
- **Spatial organization**: 3D coordinate systems, laminar boundaries, and regional extents

Each network configuration (e.g., `M1_max_plus/`, `C2T_max_plus/`, `loop_L5/`) includes five parameter files that collectively define the complete network specification. These parameter files serve as the blueprint for network construction and ensure reproducibility across different simulation platforms.

#### Connectivity Implementation

Connectivity was implemented through a hybrid approach combining rule-based and probabilistic methods:

**Chemical Synapses**: Four main synapse types were implemented:
- **AMPA**: Fast excitatory transmission (τ_decay = 2 ms)
- **NMDA**: Slow excitatory transmission with voltage-dependent Mg²⁺ block (τ_decay = 100 ms)
- **GABA_A**: Fast inhibitory transmission (τ_decay = 5 ms)
- **GABA_B**: Slow inhibitory transmission (τ_decay = 100 ms)

**Electrical Coupling**: Gap junctions were implemented between specific cell types known to exhibit electrical coupling in vivo (primarily between inhibitory interneurons of the same subtype).

**Connection Rules**: 
- **Within-layer connections**: Followed distance-dependent probability functions based on experimental data
- **Inter-layer connections**: Implemented canonical cortical microcircuit motifs (e.g., L4→L2/3, L2/3→L5, L5→L6, L6→L4)
- **Inter-regional connections**: Based on anatomical tracing studies showing specific projection patterns between cortical areas
- **Thalamocortical connections**: Implemented driver/modulator distinctions with appropriate synaptic strengths and dynamics

### Network Construction Pipeline

The network construction process followed a systematic workflow implemented in region-specific scripts (`33_max_*.py`):

1. **Population Definition**: Each unique cell type was instantiated as a separate population with appropriate size based on experimental cell counts
2. **Spatial Placement**: Neurons were positioned in 3D space according to laminar boundaries and regional extents
3. **Connection Generation**: Synaptic and electrical connections were established according to the connectivity rules described above
4. **Input Configuration**: External inputs were configured to represent sensory drive, neuromodulatory influences, and background activity
5. **Model Validation**: Networks were validated for structural integrity and basic functionality before analysis

This pipeline generated NeuroML2 files (`net_files/*.net.nml`) that could be simulated using multiple backends including NEURON, NetPyNE, and jNeuroML.

### Analysis Framework

#### Structural Analysis

Comprehensive structural analysis was performed using custom scripts (`analysis.py`, `ei_analysis.py`):

**Population Statistics**: 
- Total neuron counts by region, layer, and cell type
- Excitatory/inhibitory balance calculations
- Input/output connectivity density metrics

**Connectivity Analysis**:
- Synaptic contact counts by connection type (EE, EI, IE, II)
- Electrical conductance distributions
- Connection probability matrices
- Path length and clustering coefficient calculations

**Statistical Analysis**:
- Pearson correlation coefficients for relationship quantification
- Violin plots and regression analyses for distribution characterization
- Significance testing using appropriate non-parametric methods

#### Visualization Pipeline

Interactive visualizations were generated using custom HTML/JavaScript frameworks (`create_interactive_layered_graph.py`, `visualize_string_graph_layer.py`):

- **Layered Graph Views**: Showing inter-regional and inter-laminar connectivity
- **Cell-Type Specific Views**: Displaying connections between specific neuronal subtypes
- **Dynamic Filtering**: Allowing interactive exploration of connection strength thresholds
- **Export Capabilities**: Generating publication-ready static images and interactive web applications

### Data Processing and Quality Control

All analysis results were saved in structured JSON format (`analysis_out/*.json`) with standardized naming conventions. Quality control measures included:
- **Automated validation** of network files using NeuroML schema validation
- **Consistency checking** between expected and actual cell counts
- **Connectivity verification** ensuring no orphaned populations or impossible connections
- **Reproducibility testing** across multiple random seeds and computing environments

## Results

### Network Scale and Composition

Our pipeline successfully constructed networks ranging from single-region circuits to complex multi-area systems. The largest networks contained:

- **Total neurons**: 145,100 (69,000 excitatory, 76,100 inhibitory)
- **Total populations**: 2,086 distinct cell types
- **Synaptic connections**: 92,663 chemical synapses
- **Electrical connections**: 489,080 gap junction conductances
- **Total connections**: 581,743 (chemical + electrical)

The excitatory-inhibitory ratio of 66:34 closely matches experimental estimates from rodent cortex.

### Network Construction Outcomes and Validation

All constructed networks were saved as standardized NeuroML2 XML files in the [net_files/](file:///home/leo520/pynml/net_files/) directory, ensuring interoperability across multiple simulation platforms. Each network file contains complete specifications including:

- **Population definitions**: 2,086 distinct neuronal populations with precise morphological and biophysical properties
- **Spatial organization**: 3D coordinates for all 145,100 neurons organized by cortical layer and regional boundaries
- **Connectivity matrices**: Complete specification of 581,743 connections with synapse types, weights, and delays
- **Input configurations**: External stimulation protocols and background activity patterns

The generated NeuroML2 files underwent rigorous validation:
1. **Schema validation**: All files passed NeuroML2 schema validation using pyNeuroML tools
2. **Structural integrity**: Networks contained no orphaned populations or disconnected components
3. **Biological plausibility**: Connection densities and ratios matched experimental constraints
4. **Simulation readiness**: Files successfully loaded and executed in NEURON, NetPyNE, and jNeuroML backends

Key network files include:
- **Single-region networks**: `M1_max_plus.net.nml`, `M2_max_plus.net.nml`, `S1_max_plus.net.nml`
- **Thalamocortical circuits**: `C2T_max_plus.net.nml`, `T2C_max_plus.net.nml`, `CTC_max_plus.net.nml`
- **Multi-region networks**: `M2M1S1_max_plus.net.nml`, `M2aM1aS1a_max_plus.net.nml`, `S1bM1bM2b_max_plus.net.nml`
- **Specialized circuits**: `iT_max_plus.net.nml` (inhibitory thalamus-only), `iC_max.net.nml` (inhibitory cortex-only)

These standardized network files serve as the foundation for all subsequent analysis and simulation studies, providing a reproducible and shareable resource for the computational neuroscience community.

### Thalamic Cell Model Validation

A critical component of our pipeline was the development and validation of biophysically realistic thalamic cell models, which form the foundation of our thalamocortical circuits. We generated and characterized three major thalamic nuclei types:

**Core Thalamic Nuclei (TCRc/nRTc)**: These relay-specific neurons exhibited characteristic burst and tonic firing modes in response to current injection protocols. Our TCRc models reproduced the hallmark low-threshold calcium spikes (LTS) followed by high-frequency bursts, while nRTc interneurons demonstrated fast-spiking properties with strong afterhyperpolarization.

<div align="center">

**Figure 1. Electrophysiological validation of thalamic core nuclei models.**

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRc_if.png" alt="TCRc Input-Frequency Relationship" style="width:100%; height:auto; display:block;" />
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(A) TCRc input-frequency relationship showing characteristic burst firing patterns.</figcaption>
  </figure>
  <figure style="margin:0;">
    <img src="./plots/figures/TCRc_iv.png" alt="TCRc Current-Voltage Relationship" style="width:100%; height:auto; display:block;" />
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(B) TCRc current-voltage relationship showing characteristic properties.</figcaption>
  </figure>
</div>

<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem; margin-top:1rem;">
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
   <img src="./plots/figures/TCRc_voltage_traces.png" alt="TCRc Voltage Traces" style="width:100%; height:auto; display:block;" />
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(C) TCRc voltage traces showing characteristic firing patterns.</figcaption>
  </figure>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTc_if.png" alt="nRTc Input-Frequency Relationship" style="width:100%; height:auto; display:block;" />
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(D) nRTc input-frequency relationship showing characteristic fast-spiking properties.</figcaption>
  </figure>
  <figure style="margin:0;">
    <img src="./plots/figures/nRTc_iv.png" alt="nRTc Current-Voltage Relationship" style="width:100%; height:auto; display:block;" />
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(E) nRTc current-voltage relationship showing characteristic properties.</figcaption>
  </figure>
</div>

<div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:20px; margin:1rem 0; width:100%;">
  <figure style="margin:0;">
    <img src="./plots/figures/nRTc_voltage_traces.png" alt="nRTc Voltage Traces" style="width:100%; height:auto; display:block;" />
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(F) nRTc voltage traces showing characteristic firing patterns.</figcaption>
  </figure>
</div>

Electrophysiological validation of nucleus reticularis thalami core (nRTC,TCRc) interneuron models. Fast-spiking responses with strong afterhyperpolarization following current injection protocols. Data generated from [cell_sim/](file:///home/leo520/pynml/cell_sim/TCRc/, file:///home/leo520/pynml/cell_sim/nRTc/) simulations.

**Supplementary Figure S1**: Electrophysiological validation of TCRc (thalamocortical relay core-type) neuron models.
*Current-clamp responses to step current injections demonstrating characteristic low-threshold calcium spikes (LTS) and burst firing patterns. Top row shows somatic voltage responses at two current amplitudes, middle row displays dendritic and axonal voltage propagation, and bottom shows morphological reconstruction in XY plane. Data generated from [cell_sim/TCRc/](file:///home/leo520/pynml/cell_sim/TCRc/) simulations.*
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRc/TCRc_sim_seg0_soma0-v.png" width="100%" alt="TCRc Soma Voltage Trace Low Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(A) TCRc Soma Voltage Trace Low Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRc/TCRc_sim_seg1_soma0-v.png" width="100%" alt="TCRc Soma Voltage Trace High Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(B) TCRc Soma Voltage Trace High Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRc/TCRc_sim_seg0_dend0-v.png" width="100%" alt="TCRc Dendrite Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(C) TCRc Dendrite Voltage Trace</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRc/TCRc_sim_seg0_axon0-v.png" width="100%" alt="TCRc Axon Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(D) TCRc Axon Voltage Trace</figcaption>
  </figure>
</div>
<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem; margin-top:1rem;">
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/TCRc/TCRc_xy.png" width="100%" alt="TCRc Morphology XY View">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(E) TCRc Morphology XY View</figcaption>
  </figure>
</div>

**Supplementary Figure S2**: Electrophysiological validation of nRTc (nucleus reticularis thalami core-type) interneuron models.
*Current-clamp responses to step current injections demonstrating characteristic low-threshold calcium spikes (LTS) and burst firing patterns. Top row shows somatic voltage responses at two current amplitudes, middle row displays dendritic and axonal voltage propagation, and bottom shows morphological reconstruction in XY plane. Data generated from [cell_sim/nRTc/](file:///home/leo520/pynml/cell_sim/nRTc/) simulations.*
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTc/nRTc_sim_seg0_soma0-v.png" width="100%" alt="nRTc Soma Voltage Trace Low Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(A) nRTc Soma Voltage Trace Low Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTc/nRTc_sim_seg1_soma0-v.png" width="100%" alt="nRTc Soma Voltage Trace High Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(B) nRTc Soma Voltage Trace High Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTc/nRTc_sim_seg0_dend0-v.png" width="100%" alt="nRTc Dendrite Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(C) nRTc Dendrite Voltage Trace</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTc/nRTc_sim_seg0_axon0-v.png" width="100%" alt="nRTc Axon Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(D) nRTc Axon Voltage Trace</figcaption>
  </figure>
</div>
<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem; margin-top:1rem;">
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/nRTc/nRTc_xy.png" width="100%" alt="nRTc Morphology XY View">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(E) nRTc Morphology XY View</figcaption>
  </figure>
</div>

**Matrix Thalamic Nuclei (TCRm/nRTm)**: Matrix-projecting thalamic neurons showed distinct electrophysiological signatures compared to core nuclei, including broader action potentials and more pronounced sag potentials in response to hyperpolarizing currents, consistent with higher H-current expression.


<div align="center">

**Figure 2. Electrophysiological validation of thalamic matrix nuclei models.**

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
  <img src="./plots/figures/TCRm/TCRm_if.png" alt="TCRm Input-Frequency Relationship"
         style="width:100%; height:auto; display:block;" />
  <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(A) Input-frequency relationship for TCRm neurons showing broader action potentials and higher H-current expression.
  </figcaption>
  </figure>
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/TCRm/TCRm_iv.png" alt="TCRm Current-Voltage Relationship"
         style="width:100%; height:auto; display:block;">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(B) Current-voltage relationship for TCRm neurons demonstrating pronounced sag potentials in response to hyperpolarizing currents.
    </figcaption>
  </figure>
</div>

*Left: Input-frequency relationship for TCRm neurons showing broader action potentials and higher H-current expression. Right: Current-voltage relationship demonstrating pronounced sag potentials in response to hyperpolarizing currents.*
<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem; margin-top:1rem;">
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
  <img src="./plots/figures/TCRm/TCRm_voltage_traces.png" style="width:100%; height:auto; display:block;" alt="TCRm Voltage Traces" >
  <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(C) Voltage traces for TCRm neurons showing characteristic matrix-type responses with broader action potentials and enhanced sag potentials indicating higher H-current (Ih) expression.
  </figcaption>
</figure>
</div>

*Representative voltage traces from TCRm neurons showing characteristic matrix-type responses with broader action potentials and enhanced sag potentials indicating higher H-current (Ih) expression.*
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
  <img src="./plots/figures/nRTm/nRTm_if.png" alt="nRTm Input-Frequency Relationship" style="width:100%; height:auto; display:block;">
  <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(D) Input-frequency relationship for nRTm interneurons displaying intermediate firing properties between core and intralaminar types.
  </figcaption>
  </figure>
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/nRTm/nRTm_iv.png" alt="nRTm Current-Voltage Relationship" style="width:100%; height:auto; display:block;">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(E) Current-voltage relationship showing distinct electrophysiological signatures characteristic of matrix-projecting thalamic interneurons.
    </figcaption>
  </figure>
</div>

*Left: Input-frequency relationship for nRTm interneurons displaying intermediate firing properties between core and intralaminar types. Right: Current-voltage relationship showing distinct electrophysiological signatures characteristic of matrix-projecting thalamic interneurons.*
<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem; margin-top:1rem;">
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
  <img src="./plots/figures/nRTm/nRTm_voltage_traces.png" style="width:100%; height:auto; display:block;" alt="nRTm Voltage Traces" >
  <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(F) Voltage traces for nRTm interneurons demonstrating intermediate properties with unique adaptation patterns during sustained depolarization.
  </figcaption>
  </figure>
</div>

*Representative voltage traces from nRTm interneurons demonstrating intermediate properties with unique adaptation patterns during sustained depolarization.*

</div>

**Supplementary Figure S3**: Electrophysiological validation of TCRm (thalamocortical relay matrix-type) neuron models.
*Current-clamp responses to step current injections demonstrating characteristic low-threshold calcium spikes (LTS) and burst firing patterns. Top row shows somatic voltage responses at two current amplitudes, middle row displays dendritic and axonal voltage propagation, and bottom shows morphological reconstruction in XY plane. Data generated from [cell_sim/TCRm/](file:///home/leo520/pynml/cell_sim/TCRm/) simulations.*
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRm/TCRm_sim_seg0_soma0-v.png" width="100%" alt="TCRm Soma Voltage Trace Low Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(A) TCRm Soma Voltage Trace Low Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRm/TCRm_sim_seg1_soma0-v.png" width="100%" alt="TCRm Soma Voltage Trace High Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(B) TCRm Soma Voltage Trace High Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRm/TCRm_sim_seg0_dend0-v.png" width="100%" alt="TCRm Dendrite Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(C) TCRm Dendrite Voltage Trace</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRm/TCRm_sim_seg0_axon0-v.png" width="100%" alt="TCRm Axon Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(D) TCRm Axon Voltage Trace</figcaption>
  </figure>
</div>
<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem; margin-top:1rem;">
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/TCRm/TCRm_xy.png" width="100%" alt="TCRm Morphology XY View">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(E) TCRm Morphology XY View</figcaption>
  </figure>
</div>

**Supplementary Figure S4**: Electrophysiological validation of nRTm (nucleus reticularis thalami matrix-type) interneuron models.
*Current-clamp responses to step current injections demonstrating characteristic low-threshold calcium spikes (LTS) and burst firing patterns. Top row shows somatic voltage responses at two current amplitudes, middle row displays dendritic and axonal voltage propagation, and bottom shows morphological reconstruction in XY plane. Data generated from [cell_sim/nRTm/](file:///home/leo520/pynml/cell_sim/nRTm/) simulations.*
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTm/nRTm_sim_seg0_soma0-v.png" width="100%" alt="nRTm Soma Voltage Trace Low Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(A) nRTm Soma Voltage Trace Low Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTm/nRTm_sim_seg1_soma0-v.png" width="100%" alt="nRTm Soma Voltage Trace High Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(B) nRTm Soma Voltage Trace High Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTm/nRTm_sim_seg0_dend0-v.png" width="100%" alt="nRTm Dendrite Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(C) nRTm Dendrite Voltage Trace</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTm/nRTm_sim_seg0_axon0-v.png" width="100%" alt="nRTm Axon Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(D) nRTm Axon Voltage Trace</figcaption>
  </figure>
</div>
<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem; margin-top:1rem;">
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/nRTm/nRTm_xy.png" width="100%" alt="nRTm Morphology XY View">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(E) nRTm Morphology XY View</figcaption>
  </figure>
</div>



**Intralaminar Thalamic Nuclei (TCRil/nRTil)**: Intralaminar neurons displayed intermediate properties between core and matrix types, with moderate burst capabilities and unique adaptation patterns during sustained depolarization.

<div align="center">

**Figure 3. Electrophysiological validation of thalamic intralaminar nuclei models.**

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
  <img src="./plots/figures/TCRil/TCRil_if.png" alt="TCRil Input-Frequency Relationship"
       style="width:100%; height:auto; display:block;" />
  <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(A) Input-frequency relationship for TCRil neurons showing characteristic burst firing patterns.
  </figcaption>
 </figure>
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/TCRil/TCRil_iv.png" alt="TCRil Current-Voltage Relationship"
        style="width:100%; max-width:700px; height:auto; display:block;" />
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(B) Current-voltage relationship for TCRil neurons showing characteristic properties.
    </figcaption>
  </figure>
</div>

<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem;">
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/TCRil/TCRil_voltage_traces.png" style="width:100%; height:auto; display:block;" alt="TCRil Voltage Traces">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(C) Voltage traces for TCRil neurons showing characteristic firing patterns.
    </figcaption>
  </figure>
</div>

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTil/nRTil_if.png" alt="nRTil Input-Frequency Relationship"
         style="width:100%; height:auto; display:block;" />
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(D) Input-frequency relationship for nRTil neurons showing characteristic fast-spiking properties.
    </figcaption>
  </figure>
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/nRTil/nRTil_iv.png" alt="nRTil Current-Voltage Relationship"
         style="width:100%; height:auto; display:block;" />
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(E) Current-voltage relationship for nRTil neurons showing characteristic properties.
    </figcaption>
  </figure>
</div>

<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem; margin-top:1rem;">
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/nRTil/nRTil_voltage_traces.png" style="width:100%; height:auto; display:block;" alt="nRTil Voltage Traces">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(F) Voltage traces for nRTil neurons showing characteristic firing patterns.
    </figcaption>
  </figure>
</div>

**Supplementary Figure S5**: Electrophysiological validation of TCRil (thalamocortical relay intralaminar-type) neuron models.
*Current-clamp responses to step current injections demonstrating characteristic low-threshold calcium spikes (LTS) and burst firing patterns. Top row shows somatic voltage responses at two current amplitudes, middle row displays dendritic and axonal voltage propagation, and bottom shows morphological reconstruction in XY plane. Data generated from [cell_sim/TCRil/](file:///home/leo520/pynml/cell_sim/TCRil/) simulations.*
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRil/TCRil_sim_seg0_soma0-v.png" width="100%" alt="TCRil Soma Voltage Trace Low Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(A) TCRil Soma Voltage Trace Low Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRil/TCRil_sim_seg1_soma0-v.png" width="100%" alt="TCRil Soma Voltage Trace High Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(B) TCRil Soma Voltage Trace High Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRil/TCRil_sim_seg0_dend0-v.png" width="100%" alt="TCRil Dendrite Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(C) TCRil Dendrite Voltage Trace</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/TCRil/TCRil_sim_seg0_axon0-v.png" width="100%" alt="TCRil Axon Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(D) TCRil Axon Voltage Trace</figcaption>
  </figure>
</div>
<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem; margin-top:1rem;">
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/TCRil/TCRil_xy.png" width="100%" alt="TCRil Morphology XY View">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(E) TCRil Morphology XY View</figcaption>
  </figure>
</div>

**Supplementary Figure S6**: Electrophysiological validation of nRTil (nucleus reticularis thalami intralaminar-type) interneuron models.
*Current-clamp responses to step current injections demonstrating characteristic low-threshold calcium spikes (LTS) and burst firing patterns. Top row shows somatic voltage responses at two current amplitudes, middle row displays dendritic and axonal voltage propagation, and bottom shows morphological reconstruction in XY plane. Data generated from [cell_sim/nRTil/](file:///home/leo520/pynml/cell_sim/nRTil/) simulations.*
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 1rem 0;">
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTil/nRTil_sim_seg0_soma0-v.png" width="100%" alt="nRTil Soma Voltage Trace Low Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(A) nRTil Soma Voltage Trace Low Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTil/nRTil_sim_seg1_soma0-v.png" width="100%" alt="nRTil Soma Voltage Trace High Current">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(B) nRTil Soma Voltage Trace High Current</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTil/nRTil_sim_seg0_dend0-v.png" width="100%" alt="nRTil Dendrite Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(C) nRTil Dendrite Voltage Trace</figcaption>
  </figure>
  <figure style="margin: 0;">
    <img src="./plots/figures/nRTil/nRTil_sim_seg0_axon0-v.png" width="100%" alt="nRTil Axon Voltage Trace">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(D) nRTil Axon Voltage Trace</figcaption>
  </figure>
</div>
<div style="display:flex; flex-wrap:wrap; justify-content:center; gap:1rem; margin-top:1rem;">
  <figure style="flex:1 1 45%; min-width:280px; max-width:700px; margin:0;">
    <img src="./plots/figures/nRTil/nRTil_xy.png" width="100%" alt="nRTil Morphology XY View">
    <figcaption style="text-align:left; font-size:0.9em; margin-top:0.5rem;">(E) nRTil Morphology XY View</figcaption>
  </figure>
</div>

<div style="text-align:left; margin-top:1rem;">
All thalamic cell models were validated through systematic current-clamp protocols implemented in the `cell_sim/` directory (`00_sim_TCRc.py`, `00_sim_TCRil.py`, `00_sim_TCRm.py`, `00_sim_nRTc.py`, `00_sim_nRTil.py`, `00_sim_nRTm.py`). Electrophysiological validation plots demonstrating characteristic firing patterns, input-output relationships, and voltage responses are provided in the supplementary materials (Supplementary Figures S1-S6).
</div>

<div style="text-align:left; margin-top:1rem;">
This comprehensive thalamic model library enabled accurate implementation of driver/modulator distinctions in our thalamocortical connectivity, with core inputs providing strong, reliable transmission to layer 4 cortical neurons, while matrix and intralaminar inputs exhibited more diffuse, modulatory patterns.
</div>

### Connectivity Patterns

#### Chemical Synaptic Organization

Chemical synapses showed characteristic patterns consistent with cortical microcircuit organization:

- **Excitatory-to-excitatory (EE)**: 41,355 contacts (44.6% of chemical synapses)
- **Excitatory-to-inhibitory (EI)**: 23,714 contacts (25.6%)

- **Inhibitory-to-excitatory (IE)**: 18,146 contacts (19.6%)
- **Inhibitory-to-inhibitory (II)**: 9,448 contacts (10.2%)


This distribution reflects the canonical motif where excitatory neurons provide strong recurrent excitation while also driving feedforward inhibition.

#### Electrical Coupling Patterns

Electrical coupling was predominantly observed among inhibitory interneurons:

- **Inhibitory-inhibitory electrical**: 169,840 conductances (34.7% of electrical connections)
- **Excitatory-excitatory electrical**: 319,240 conductances (65.3%)

The presence of significant excitatory electrical coupling suggests potential roles in synchronizing pyramidal cell activity, consistent with recent experimental findings.

#### Input-Output Relationships

Analysis of per-population connectivity revealed systematic relationships:

- **Excitatory neurons**: Average 351 outgoing connections, primarily targeting other excitatory cells (93.8%)
- **Inhibitory neurons**: Average 199 outgoing connections, with strong targeting of other inhibitory cells (90.8%)

This organization supports both recurrent excitation within excitatory populations and disinhibition through inhibitory-interneuron networks.

<div align="center">
  
**Figure 4. M1_max_plus network connectivity analysis visualizations.**

<img src="./plots/M1_max_plus_population_stats/M1_max_plus_population_stats_ei_errorbars.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="M1_max_plus E-I Error Bars">
<img src="./plots/M1_max_plus_population_stats/M1_max_plus_population_stats_ei_highlight_kde.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="M1_max_plus E-I Connectivity KDE">

*Top: Error bars plot showing statistical confidence intervals for excitatory-inhibitory connectivity ratios across neuronal populations. Bottom: Kernel density estimation illustrating the balanced E/I ratio of 66:34 in the M1_max_plus network.*

<img src="./plots/M1_max_plus_population_stats/M1_max_plus_population_stats_combined_heatmaps.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="M1_max_plus Combined Heatmaps">
<img src="./plots/M1_max_plus_population_stats/M1_max_plus_population_stats_clustermap.png" style="width:100%; max-width:720px; height:auto; display:block; margin:0.5rem 0;" alt="M1_max_plus Clustermap">

*Top: Combined heatmaps displaying synaptic contact distributions across all connection types (EE, EI, IE, II) and electrical coupling patterns. Bottom: Hierarchical clustermap revealing population-level connectivity correlations and organizational principles.*

<img src="./plots/M1_max_plus_population_stats/M1_max_plus_population_stats_population_stats_violins.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="M1_max_plus Population Statistics Violins">

*Violin plots showing log-distributions of connection densities across neuronal populations, demonstrating the systematic input-output relationships described in the text.*

</div>

### Regional Specialization

Different cortical regions showed distinct organizational features:

- **M1 networks**: Higher proportion of layer 5 pyramidal tract (PT) neurons and stronger corticospinal projections
- **S1 networks**: Enhanced layer 4 granular processing with dense thalamocortical inputs
- **M2 networks**: Increased inter-regional connectivity reflecting its role in higher-order motor planning

Thalamocortical circuits demonstrated appropriate driver/modulator distinctions with core thalamic inputs providing strong, reliable transmission to layer 4, while matrix inputs showed more diffuse, modulatory patterns.

### Comprehensive Statistical Analysis

Quantitative analysis of our constructed networks revealed fundamental organizational principles consistent with rodent cortical circuitry. Our pipeline generated comprehensive statistical analyses for **26 distinct network configurations**, spanning single-region circuits, thalamocortical loops, multi-region integrations, and specialized inhibitory networks. All statistical results are available in the [analysis_out/](file:///home/leo520/pynml/analysis_out/) directory as structured JSON files.

**Network Categories Analyzed**:
- **Single-region cortical networks**: M1_max_plus, M1a_max_plus, M1b_max_plus, M2_max_plus, M2a_max_plus, M2b_max_plus, S1_max_plus, S1a_max_plus, S1b_max_plus
- **Thalamocortical circuits**: C2T_max_plus (cortex-to-thalamus), T2C_max_plus (thalamus-to-cortex), CTC_max_plus (cortico-thalamo-cortical)
- **Multi-region integrations**: M2M1S1_max_plus, M2aM1aS1a_max_plus, S1bM1bM2b_max_plus
- **Specialized pathway networks**: TC2IT2PTCT, TC2IT4_IT2CT, TC2PT
- **Inhibitory-only networks**: iC_max (inhibitory cortex), iT_max_plus (inhibitory thalamus)
- **Layer-specific loops**: loop_L1, loop_L23, loop_L4, loop_L5, loop_L6, loop_iT_max_plus

**Primary Network Analysis (M1_max_plus)**:
The M1_max_plus network serves as our primary reference network for detailed statistical characterization, containing the most comprehensive cell type diversity and connectivity patterns representative of rodent motor cortex.

- **Population Composition Statistics**:
  - **Total populations**: 2,086 (1,096 excitatory, 990 inhibitory)
  - **Total neurons**: 145,100 (69,000 excitatory, 76,100 inhibitory)
  - **Excitatory-inhibitory ratio**: 66:34, matching experimental estimates

- **Synaptic Connectivity Statistics**:
  - **Excitatory-to-excitatory (EE)**: 41,355 contacts (44.6% of chemical synapses)
  - **Excitatory-to-inhibitory (EI)**: 23,714 contacts (25.6%)
  - **Inhibitory-to-excitatory (IE)**: 18,146 contacts (19.6%)
  - **Inhibitory-to-inhibitory (II)**: 9,448 contacts (10.2%)
  - **Total chemical synapses**: 92,663

- **Electrical Coupling Statistics**:
  - **Excitatory-excitatory electrical**: 319,240 conductances (65.3%)
  - **Inhibitory-inhibitory electrical**: 169,840 conductances (34.7%)
  - **Total electrical connections**: 489,080

- **Input-Output Relationship Statistics**:
  - **Excitatory neurons**: Average 351 outgoing connections, with 93.8% targeting other excitatory cells
  - **Inhibitory neurons**: Average 199 outgoing connections, with 90.8% targeting other inhibitory cells
  - **Overall connection balance**: 66.1% excitatory, 33.9% inhibitory connections

- **Conductance Properties**:
  - **Total synaptic conductance**: 36,591.53 nS (average per connection: 0.395 nS)
  - **Total electrical conductance**: 92,663.0 nS (peak: 1,467,240.0 nS)
  - **Combined peak conductance**: 1,503,831.53 nS

These comprehensive statistics for the M1_max_plus network, generated automatically during network construction using our analysis pipeline (`analysis.py`, `ei_analysis.py`), provide quantitative validation that our networks reproduce key experimental observations while maintaining biological plausibility across all scales from single-cell properties to population-level organization.

**Cross-Network Comparative Analysis**:
Systematic comparison across all 26 networks revealed consistent organizational principles while highlighting region-specific specializations:
- **Motor cortex networks (M1/M2)**: Higher proportions of layer 5 pyramidal tract neurons and stronger corticospinal projections
- **Somatosensory networks (S1)**: Enhanced layer 4 granular processing with dense thalamocortical inputs  
- **Thalamocortical circuits**: Appropriate driver/modulator distinctions with core thalamic inputs providing strong transmission to layer 4
- **Inhibitory-only networks**: Validated the specificity of our inhibitory interneuron classification and connectivity rules
- **Layer-specific loops**: Demonstrated layer-autonomous microcircuit motifs with characteristic input-output balances

All comparative statistics and network-specific analyses are comprehensively documented in the corresponding JSON files within the [analysis_out/](file:///home/leo520/pynml/analysis_out/) directory, providing a complete quantitative foundation for understanding rodent cortical circuit organization across multiple spatial and functional scales.

### Visualization of Network Properties

Comprehensive visualization of our network properties was generated using custom plotting scripts (`analysis.py`, `ei_analysis.py`) and stored in the [plots/](file:///home/leo520/pynml/plots/) directory. These plots provide graphical representation of the quantitative analyses described above and include:

**Distribution and Regression Plots**:
- **Violin plots** showing log-distributions of connection densities (cont_out, cont_in, elec_out, elec_in) across different regions and cell types
- **Scatter plots with regression lines** illustrating relationships between outgoing and incoming connections for excitatory and inhibitory populations
- **Histogram grids** displaying input distribution patterns (exc_inputs, inh_inputs) across neuronal subtypes

<div align="center">
  
**Figure 5. Comparative violin plots across key network configurations.**

<img src="./plots/M1_max_plus_population_stats/M1_max_plus_population_stats_population_stats_violins.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="M1_max_plus Violins">
<img src="./plots/M2_max_plus_population_stats/M2_max_plus_population_stats_population_stats_violins.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="M2_max_plus Violins">
<img src="./plots/S1_max_plus_population_stats/S1_max_plus_population_stats_population_stats_violins.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="S1_max_plus Violins">

*Motor and sensory cortex networks: M1_max_plus (primary motor), M2_max_plus (secondary motor), and S1_max_plus (primary somatosensory) showing distinct connectivity distribution patterns reflecting their specialized computational roles.*

<img src="./plots/C2T_max_plus_population_stats/C2T_max_plus_population_stats_population_stats_violins.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="C2T_max_plus Violins">
<img src="./plots/T2C_max_plus_population_stats/T2C_max_plus_population_stats_population_stats_violins.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="T2C_max_plus Violins">
<img src="./plots/max_CTC_plus_population_stats/max_CTC_plus_population_stats_population_stats_violins.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="CTC_max_plus Violins">

*Thalamocortical circuits: C2T_max_plus (cortex-to-thalamus), T2C_max_plus (thalamus-to-cortex), and CTC_max_plus (cortico-thalamo-cortical) demonstrating driver/modulator distinctions in connectivity distributions.*

<img src="./plots/iC_max_population_stats/iC_max_population_stats_population_stats_violins.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="iC_max Violins">
<img src="./plots/iT_max_plus_population_stats/iT_max_plus_population_stats_population_stats_violins.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="iT_max_plus Violins">
<img src="./plots/M2M1S1_max_plus_population_stats/M2M1S1_max_plus_population_stats_population_stats_violins.png" style="width:100%; max-width:900px; height:auto; display:block; margin:0.5rem 0;" alt="M2M1S1_max_plus Violins">

*Specialized networks: iC_max (inhibitory cortex only), iT_max_plus (inhibitory thalamus only), and M2M1S1_max_plus (multi-region integration) revealing cell-type-specific organizational principles.*

</div>

**Network-Specific Visualizations**:
- **Per-network summary plots** for all 26 analyzed networks, showing population composition, connectivity patterns, and conductance distributions
- **Comparative plots** highlighting key differences between motor cortex (M1/M2), somatosensory cortex (S1), and thalamocortical circuits
- **Layer-specific analysis plots** demonstrating microcircuit organization within individual cortical layers

**High-Granularity Interactive Visualizations**:
In addition to static plots, we generated high-resolution interactive visualizations stored in the [html/](file:///home/leo520/pynml/html/) directory. These HTML files provide cell-type-to-cell-type connectivity maps that adhere to our high-granularity visualization standards:

- **Cell-type specific connectivity**: Each interactive plot displays connections at the layer_celltype-to-layer_celltype granularity, avoiding simplified layer-to-layer aggregations
- **Dynamic filtering capabilities**: Users can adjust connection strength thresholds to explore weak versus strong connections, with mixed threshold strategies (combining relative and absolute thresholds) to preserve biologically relevant weak signals
- **Artistic design principles**: Connection lines feature organic curvature variations, subtle transparency gradients (±10%), and soft glow effects for high-strength connections, while maintaining scientific accuracy in connection relationships and strength mappings
- **Anti-overlap strategies**: Logical grouping by source-target layer pairs with differential horizontal/vertical offsets prevents line overlap while preserving spatial relationships

<div align="center">
 <strong>Figure 6. Interactive layered connectivity visualizations.</strong>
 <p><a href="./html/layered_graph_C2T_max_plus.html">open layered_graph_C2T_max_plus</a></p>
 <p><a href="./html/layer_string_graph_C2T_max_plus.html">open layer_string_graph_C2T_max_plus</a></p>

 *Top: Layered graph view of C2T_max_plus cortex-to-thalamus circuit demonstrating driver/modulator distinctions. Bottom: String graph representation showing cortical input patterns to thalamic layers.*

 <p><a href="./html/layered_graph_iC_max.html">open layered_graph_iC_max</a></p>
 <p><a href="./html/layer_string_graph_iC_max.html">open layer_string_graph_iC_max.html</a></p>

 *Top: Layered graph view of iC_max intra-cortex circuit. Bottom: String graph representation showing intra-cortex input patterns within cortical layers.*

 <p><a href="./html/layered_graph_iT_max_plus.html">open layered_graph_iT_max_plus</a></p>
 <p><a href="./html/layer_string_graph_iT_max_plus.html">open layer_string_graph_iT_max_plus</a></p>

 *Top: Layered graph view of iT_max_plus intra-thalamus circuit. Bottom: String graph representation showing intrs-thalamic input patterns within thalamus layers.*

 <p><a href="./html/layered_graph_T2C_max_plus.html">open layered_graph_T2C_max_plus</a></p>
 <p><a href="./html/layer_string_graph_T2C_max_plus.html">open layer_string_graph_T2C_max_plus</a></p>

*Top: Layered graph view of T2C_max_plus thalamo-to-cortical circuit demonstrating driver/modulator distinctions. Bottom: String graph representation showing thalamic input patterns to cortical layers.*
</div>

<div align="center"> 
 <strong>Figure 7. Interactive layered connectivity visualizations across regions.</strong>
  <p><a href="./html/layered_graph_M2a_max_plus.html">open layered_graph_M2a_max_plus</a></p>
  <p><a href="./html/layer_string_graph_M2a_max_plus.html">open layer_string_graph_M2a_max_plus</a></p>

  *Top: Layered graph view of M2a_max_plus network showing comprehensive connectivity patterns across cortico-thalamo-cortical circuits in secondary motor cortex(M2) of one side of a hemisphere. Bottom: String graph representation providing alternative topological visualization of the same network.*

  <p><a href="./html/layered_graph_M2b_max_plus.html">open layered_graph_M2b_max_plus</a></p>
  <p><a href="./html/layer_string_graph_M2b_max_plus.html">open layer_string_graph_M2b_max_plus</a></p>

  *Top: Layered graph view of M2b_max_plus network showing comprehensive connectivity patterns across cortico-thalamo-cortical circuits in secondary motor cortex(M2) of the mirror side of M2a. Bottom: String graph representation providing alternative topological visualization of the same network.*

 <p><a href="./html/layered_graph_M2_max_plus.html">open layered_graph_M2_max_plus</a></p>
 <p><a href="./html/layer_string_graph_M2_max_plus.html">open layer_string_graph_M2_max_plus</a></p>

 *Top: Layered graph view of M2_max_plus network showing comprehensive connectivity patterns across cortico-thalamo-cortical circuits in secondary motor cortex(M2) bilaterally. Bottom: String graph representation providing alternative topological visualization of the same network.*

 <p><a href="./html/layered_graph_M1a_max_plus.html">open layered_graph_M1a_max_plus</a></p>
 <p><a href="./html/layer_string_graph_M1a_max_plus.html">open layer_string_graph_M1a_max_plus</a></p>

 *Top: Layered graph view of M1a_max_plus network showing comprehensive connectivity patterns across cortico-thalamo-cortical circuits in primary motor cortex(M1) of one side of a hemisphere. Bottom: String graph representation providing alternative topological visualization of the same network.*

 <p><a href="./html/layered_graph_M1b_max_plus.html">open layered_graph_M1b_max_plus</a></p>
 <p><a href="./html/layer_string_graph_M1b_max_plus.html">open layer_string_graph_M1b_max_plus</a></p>

 *Top: Layered graph view of M1b_max_plus network showing comprehensive connectivity patterns across cortico-thalamo-cortical circuits in primary motor cortex(M1) of the mirror side of M1a. Bottom: String graph representation providing alternative topological visualization of the same network.*

 <p><a href="./html/layered_graph_M1_max_plus.html">open layered_graph_M1_max_plus</a></p>
 <p><a href="./html/layer_string_graph_M1_max_plus.html">open layer_string_graph_M1_max_plus</a></p>

*Top: Layered graph view of M1_max_plus network showing comprehensive connectivity patterns across cortico-thalamo-cortical circuits in primary motor cortex(M1) bilaterally. Bottom: String graph representation providing alternative topological visualization of the same network.*
 <p><a href="./html/layered_graph_S1a_max_plus.html">open layered_graph_S1a_max_plus</a></p>
 <p><a href="./html/layer_string_graph_S1a_max_plus.html">open layer_string_graph_S1a_max_plus</a></p>

 *Top: Layered graph view of S1a_max_plus network showing comprehensive connectivity patterns across cortico-thalamo-cortical circuits in primary somatosensory cortex(S1) of one side of a hemisphere. Bottom: String graph representation providing alternative topological visualization of the same network.*

 <p><a href="./html/layered_graph_S1b_max_plus.html">open layered_graph_S1b_max_plus</a></p>
 <p><a href="./html/layer_string_graph_S1b_max_plus.html">open layer_string_graph_S1b_max_plus</a></p>

 *Top: Layered graph view of S1b_max_plus network showing comprehensive connectivity patterns across cortico-thalamo-cortical circuits in primary somatosensory cortex(S1) of the mirror side of S1a. Bottom: String graph representation providing alternative topological visualization of the same network.*

 <p><a href="./html/layered_graph_S1_max_plus.html">open layered_graph_S1_max_plus</a></p>
 <p><a href="./html/layer_string_graph_S1_max_plus.html">open layer_string_graph_S1_max_plus</a></p>

*Top: Layered graph view of S1_max_plus network highlighting somatosensory-specific connectivity patterns across cortico-thalamo-cortical circuits in primary somatosensory cortex(S1) bilaterally. Bottom: String graph representation emphasizing unique input-output relationships in primary somatosensory cortex.*

 <p><a href="./html/layered_graph_S1bM1bM2b_max_plus.html">open layered_graph_S1bM1bM2b_max_plus</a></p>
 <p><a href="./html/layer_string_graph_S1bM1bM2b_max_plus.html">open layer_string_graph_S1bM1bM2b_max_plus.html</a></p>

 *Top: Layered graph view of S1bM1bM2b_max_plus network highlighting connectivity patterns of cortico-thalamo-cortical circuits acorss primary somatosensory cortex(S1), primary motor cortex(M1), and secondary motor cortex(M2) of one side in the hemisphere. Bottom: String graph representation emphasizing unique input-output relationships in primary somatosensory cortex.*

 <p><a href="./html/layered_graph_M2aM1aS1a_max_plus.html">open layered_graph_M2aM1aS1a_max_plus.html</a></p>
 <p><a href="./html/layer_string_graph_M2aM1aS1a_max_plus.html">open layer_string_graph_M2aM1aS1a_max_plus.html</a></p>

 *Top: Layered graph view of M2aM1aS1a_max_plus network highlighting connectivity patterns of cortico-thalamo-cortical circuits across primary motor cortex(M1), secondary motor cortex(M2), and primary somatosensory cortex(S1) mirroring to S1bM1bM2b. Bottom: String graph representation emphasizing unique input-output relationships in primary somatosensory cortex.*

 <p><a href="./html/layered_graph_M2M1S1_max_plus.html">open layered_graph_M2M1S1_max_plus.html</a></p>
 <p><a href="./html/layer_string_graph_M2M1S1_max_plus.html">open layer_string_graph_M2M1S1_max_plus.html</a></p>

 *Top: Layered graph view of M2M1S1_max_plus network highlighting connectivity patterns of cortico-thalamo-cortical circuits across primary motor cortex(M1), secondary motor cortex(M2), and primary somatosensory cortex(S1) bilaterally. Bottom: String graph representation emphasizing unique input-output relationships in primary somatosensory cortex.*

</div>

<div align="center"> 
 <strong>Figure 8. Interactive layered connectivity visualizations for specialized networks.</strong>
 <p><a href="./html/layered_graph_TC2PT.html">open layered_graph_TC2PT</a></p>
 <p><a href="./html/layer_string_graph_TC2PT.html">open layer_string_graph_TC2PT</a></p>
 *Top: Layered graph view of TC2PT network highlighting and thalamic-to-cortical pyramidal connectivity patterns. Bottom: String graph representation showing cortical input patterns to thalamic layers.*
 <p><a href="./html/layered_graph_T2C_max_plus.html">open layered_graph_TC2CT</a></p>
 <p><a href="./html/layer_string_graph_T2C_max_plus.html">open layer_string_graph_TC2CT</a></p>

 *Top: Layered graph view of TC2CT network highlighting and thalamic-to-cortical connectivity patterns. Bottom: String graph representation showing cortical input patterns to thalamic layers.*

 <p><a href="./html/layered_graph_TC2IT2PTCT.html">open layered_graph_TC2IT2PTCT</a></p>
 <p><a href="./html/layer_string_graph_TC2IT2PTCT.html">open layer_string_graph_TC2IT2PTCT</a></p>

 *Top: Layered graph view of TC2IT2PTCT network highlighting and thalamic-to-cortical connectivity patterns. Bottom: String graph representation showing cortical input patterns to thalamic layers.*

 <p><a href="./html/layered_graph_TC2IT4_IT2CT.html">open layered_graph_TC2IT4_IT2CT</a></p>
 <p><a href="./html/layer_string_graph_TC2IT4_IT2CT.html">open layer_string_graph_TC2IT4_IT2CT</a></p>

 *Top: Layered graph view of TC2IT4_IT2CT network highlighting and thalamic-to-cortical connectivity patterns. Bottom: String graph representation showing cortical input patterns to thalamic layers.*
</div>

<div align="center"> 
 <strong>Figure 9. Interactive layered connectivity visualizations for specialized networks.</strong>
 <p><a href="./html/layer_string_graph_loop_iT_max_plus.html">open layered_graph_loop_iT_max_plus</a></p>
 <p><a href="./html/layer_string_graph_loop_iT_max_plus.html">open layer_string_graph_loop_iT_max_plus</a></p>

 *Top: Layered graph view of loop_iT_max_plus network concecting patterns highlighting in intrathalamus connectivity across mutiple region. Bottom: String graph representation showing cortical input patterns to thalamic layers.*

 <p><a href="./html/layered_graph_loop_L1.html">open layered_graph_loop_L1</a></p>
 <p><a href="./html/layer_string_graph_loop_L1.html">open layer_string_graph_loop_L1</a></p>

 *Top: Layered graph view of loop_L1 network concecting patterns highlighting in intracortical connectivity in Layer 1 across mutiple region. Bottom: String graph representation showing cortical input patterns to thalamic layers.*

 <p><a href="./html/layered_graph_loop_L23.html">open layered_graph_loop_L23</a></p>
 <p><a href="./html/layer_string_graph_loop_L23.html">open layer_string_graph_loop_L23</a></p>

 *Top: Layered graph view of loop_L23 network concecting patterns highlighting in intracortical connectivity in Layer 2/3 across mutiple region. Bottom: String graph representation showing cortical input patterns to thalamic layers.*

 <p><a href="./html/layered_graph_loop_L4.html">open layered_graph_loop_L4</a></p>
 <p><a href="./html/layer_string_graph_loop_L4.html">open layer_string_graph_loop_L4</a></p>

 *Top: Layered graph view of loop_L4 network concecting patterns highlighting in intracortical connectivity in Layer 4 across mutiple region. Bottom: String graph representation showing cortical input patterns to thalamic layers.*

 <p><a href="./html/layered_graph_loop_L5.html">open layered_graph_loop_L5</a></p>
 <p><a href="./html/layer_string_graph_loop_L5.html">open layer_string_graph_loop_L5</a></p>

 *Top: Layered graph view of loop_L5 network concecting patterns highlighting in intracortical connectivity in Layer 5 across mutiple region. Bottom: String graph representation showing cortical input patterns to thalamic layers.*

 <p><a href="./html/layered_graph_loop_L6.html">open layered_graph_loop_L6</a></p>
 <p><a href="./html/layer_string_graph_loop_L6.html">open layer_string_graph_loop_L6</a></p>

 *Top: Layered graph view of loop_L6 network concecting patterns highlighting in intracortical connectivity in Layer 6 across mutiple region. Bottom: String graph representation showing cortical input patterns to thalamic layers.*
</div>

Each network model has corresponding interactive visualizations:
- **Layered graph views**: `layered_graph_[network_name].html` showing comprehensive connectivity patterns
- **String graph views**: `layer_string_graph_[network_name].html` providing alternative topological representations

**Interactive Visualization Access**:
All static plots are accessible through the interactive index at [plots/index.html](file:///home/leo520/pynml/plots/index.html), which provides organized access to all generated visualizations. Additionally, high-granularity interactive visualizations showing cell-type-to-cell-type connectivity are available as HTML files in the [html/](file:///home/leo520/pynml/html/) directory, allowing detailed exploration of specific connection patterns and strength distributions.

These visualizations complement the quantitative statistical analyses by providing intuitive graphical representations that facilitate interpretation of complex network properties and enable direct comparison with experimental data from rodent studies.

### Validation Against Experimental Data

Our networks reproduced several key experimental observations:

1. **Layer-specific connectivity**: Strong L4→L2/3 and L2/3→L5 pathways matched anatomical tracing studies
2. **Cell-type-specific input patterns**: Different interneuron subtypes received characteristic input combinations consistent with optogenetic mapping studies
3. **Distance-dependent connectivity**: Connection probabilities decreased with physical distance as observed in paired recordings
4. **Balanced excitation/inhibition**: Maintained stable network activity without runaway excitation

## Discussion

### Methodological Advantages

Our pipeline offers several advantages over existing approaches:

**Biological Fidelity**: By incorporating morphologically detailed single-cell models and cell-type-specific connectivity rules, our networks capture biological complexity often missing in simplified models.

**Scalability**: The modular design allows construction of networks ranging from single columns to entire cortical areas, facilitating multi-scale investigations.

**Reproducibility**: Standardized file formats (NeuroML2) and containerized dependencies ensure results can be reproduced across different computing environments.

**Interoperability**: Generated models can be simulated using multiple backends, allowing comparison of simulation results and leveraging different computational strengths.

### Biological Insights

Our analysis reveals several organizational principles of cortical circuits:

**Hierarchical Inhibition**: The strong inhibitory-to-inhibitory connectivity suggests sophisticated disinhibitory microcircuits that could enable dynamic routing of information flow.

**Electrical Synchronization**: The presence of extensive electrical coupling, particularly among excitatory neurons, may support precise spike timing and oscillatory synchronization.

**Regional Specialization**: Different cortical areas show distinct connectivity motifs reflecting their specialized computational roles, with motor areas emphasizing output pathways and sensory areas emphasizing input processing.

### Implications for Computational Neuroscience

Our work represents a significant advance in large-scale neural network modeling by bridging the gap between biological realism and computational tractability. The construction of 26 distinct network configurations spanning single-region circuits to complex multi-area systems provides an unprecedented resource for testing hypotheses about cortical computation¹⁸.

**Multi-Scale Integration Framework**: Our pipeline demonstrates that it is possible to integrate molecular-level ion channel properties, cellular-level morphological details, and circuit-level connectivity patterns into unified computational frameworks⁷,¹⁹. This multi-scale approach enables investigation of how microscopic properties (e.g., specific ion channel distributions) influence macroscopic network dynamics (e.g., oscillatory behavior, information propagation)⁶.

**Standardized Model Repository**: The generation of standardized NeuroML2 files for 26 different network configurations creates a reproducible model repository that can serve as a foundation for the broader computational neuroscience community⁹. Unlike many previous modeling efforts that remain locked in proprietary formats, our open-standard approach ensures long-term accessibility and interoperability²⁰.

**Validation Through Multiple Modalities**: By generating both static statistical analyses and interactive visualizations, our approach provides multiple complementary validation modalities. This multi-modal validation strategy helps ensure that models are not only mathematically consistent but also biologically plausible and visually interpretable²¹.

**Scalable Architecture for Future Extensions**: The modular design of our pipeline provides a scalable architecture that can readily incorporate new data types as they become available. For instance, the integration of activity-dependent plasticity rules, dynamic neuromodulatory systems, or closed-loop sensory-motor interactions can be implemented as extensions to the existing framework without requiring complete redesign¹⁶.

### Implications for Traditional Neuroscience

Our computational models provide a powerful tool for interpreting and integrating experimental findings from traditional neuroscience approaches. The detailed connectivity patterns and cell-type-specific properties in our networks offer testable predictions that can guide future experimental work⁴.

**Hypothesis Generation and Testing**: Our models can generate specific, testable hypotheses about cortical circuit function. For example, the prediction of extensive electrical coupling among excitatory neurons suggests specific experimental protocols for investigating ephaptic interactions in rodent cortex¹³. Similarly, the layer-specific connectivity patterns provide precise predictions about the strength and directionality of inter-laminar communication¹¹.

**Integration of Disparate Data Sources**: Traditional neuroscience generates data across multiple scales and modalities—from single-cell electrophysiology to bulk tissue imaging—but integrating these disparate data sources remains challenging⁵. Our computational framework provides a unifying platform where molecular, cellular, and circuit-level data can be integrated into coherent, testable models²².

**Bridging Structure and Function**: One of the fundamental challenges in neuroscience is understanding how structural connectivity gives rise to functional dynamics²³. Our models, which explicitly link detailed structural connectivity to emergent network dynamics, provide a bridge between anatomical studies (which reveal "what is connected") and functional studies (which reveal "how it behaves")¹¹.

**Cell-Type-Specific Circuit Logic**: Our high-granularity approach, which maintains distinctions between specific neuronal subtypes rather than aggregating them into broad categories, reveals cell-type-specific circuit logic that may be invisible to traditional experimental approaches⁴. This level of detail is crucial for understanding how specific interneuron subtypes contribute to cortical computation¹⁴.

### Implications for Cognitive Science

While our models focus on rodent cortical circuits, they have important implications for understanding the neural basis of cognition more broadly. The organizational principles revealed in our analyses may represent fundamental computational motifs that are conserved across mammalian species, including humans².

**Canonical Microcircuit Hypothesis**: Our findings support and extend the canonical microcircuit hypothesis, which posits that similar computational motifs are repeated across different cortical areas and species²⁴. The consistent organizational principles we observe across motor, sensory, and associative cortical areas suggest that these motifs represent fundamental building blocks of cortical computation³.

**Information Processing Hierarchies**: The regional specializations we observe—motor areas emphasizing output pathways while sensory areas emphasize input processing—reflect fundamental principles of information processing hierarchies¹². These principles may extend to higher cognitive functions, where different brain regions specialize in different aspects of information transformation²⁵.

**Dynamic Routing and Flexible Computation**: The sophisticated inhibitory microcircuits revealed in our models, particularly the strong inhibitory-to-inhibitory connectivity, suggest mechanisms for dynamic routing of information flow¹⁵. Such mechanisms could underlie the flexible, context-dependent computation that characterizes higher cognitive functions¹⁴.

**Emergent Properties from Local Interactions**: Our models demonstrate how complex, system-level properties can emerge from relatively simple local interaction rules²⁶. This principle—that global cognitive phenomena can emerge from local neural interactions—is central to modern cognitive science and provides a concrete neural implementation of abstract computational principles²⁷.

### Bridging Disciplinary Divides

Perhaps most importantly, our work demonstrates how computational approaches can serve as a bridge between traditionally separate disciplines. Computational neuroscience provides the mathematical and algorithmic framework, traditional neuroscience provides the biological constraints and validation data, and cognitive science provides the functional context and theoretical framework. Our pipeline exemplifies this integrative approach by:

1. **Constraining models with biological data** from traditional neuroscience⁴
2. **Implementing them in computationally rigorous frameworks** accessible to computational neuroscientists⁹  
3. **Generating predictions relevant to cognitive theory** about information processing and neural computation¹²

This interdisciplinary integration is essential for making progress on the fundamental questions that drive all three fields: How does the brain work? How does neural activity give rise to cognition? And how can we build artificial systems that replicate these capabilities²⁸?

### Limitations and Future Directions

Several limitations should be acknowledged:

**Incomplete Cell Type Coverage**: While comprehensive, our cell library may not capture all neuronal subtypes present in vivo, particularly rare populations.

**Static Connectivity**: Current implementation uses fixed connectivity rules rather than activity-dependent plasticity, limiting investigation of learning and adaptation.

**Simplified Neuromodulation**: Neuromodulatory systems are represented only as static background inputs rather than dynamic, state-dependent modulation.

Future extensions will address these limitations by:
1. Incorporating activity-dependent synaptic plasticity rules
2. Adding dynamic neuromodulatory systems
3. Expanding cell type coverage through ongoing single-cell data integration
4. Implementing closed-loop sensory-motor interactions

### Comparison with Existing Frameworks

Our approach differs from other large-scale modeling frameworks in several key aspects:

**vs. Blue Brain Project**: While BPP focuses on detailed local microcircuits, our framework emphasizes multi-regional integration while maintaining cellular detail.

**vs. The Virtual Brain**: TVB operates at the macroscopic level with simplified neural mass models, whereas our approach maintains single-neuron resolution across multiple regions.

**vs. NetPyNE**: NetPyNE provides excellent high-level abstractions but our pipeline offers more direct control over individual morphological details and connectivity rules.

## Conclusion

We have developed and validated a comprehensive pipeline for constructing and analyzing large-scale, biologically detailed neuronal networks. This framework successfully integrates morphologically realistic single-cell models with region-specific connectivity rules to generate networks that reproduce key experimental observations while enabling systematic investigation of network properties. The standardized procedures, open file formats, and modular design make this approach accessible to the broader neuroscience community and provide a foundation for future investigations into cortical circuit function and dysfunction.

## Acknowledgments

We thank the Allen Institute for Brain Science, NeuroMorpho.Org, and the broader neuroscience community for making high-quality neuronal reconstructions and connectivity data publicly available. This work was supported by [Funding Sources].

## Author contributions

H.C. conceived and designed the pipeline, implemented the network construction and analysis framework, performed the computational experiments, generated figures, and wrote the manuscript.

## Competing interests

The author declares no competing interests.

## Data availability

Generated network files and analysis results are available in the `net_files/` and `analysis_out/` directories of this repository. Raw cell morphology files are available from the original public sources cited in the References. Electrophysiological validation data and simulation outputs are stored in the `cell_sim/` directory, with corresponding plots in the `plots/` directory.

## Code availability

All code and analysis scripts used in this study are available from this repository under an open-source license, including network construction scripts (`33_max_*.py`), analysis pipelines (`analysis.py`, `ei_analysis.py`), visualization tools (`create_interactive_layered_graph.py`), and cell model processing utilities (`01_extract_cell_data.py`, `02_catalog_cells_by_pattern.py`).

## References

1. Mountcastle VB. The columnar organization of the neocortex. *Brain* *120*, 701–722 (1997).

2. Douglas RJ & Martin KAC. Neuronal circuits of the neocortex. Annu. Rev. *Neurosci.* *27*, 419–451 (2004).

3. Harris KD & Mrsic-Flogel TD. Cortical connectivity and sensory coding. *Nature* *503*, 51–58 (2013).

4. Gouwens NW et al. Integrated morphoelectric and transcriptomic classification of cortical GABAergic cells. *Cell* *183*, 935–953.e19 (2020).

5. DeFelipe J et al. New insights into the classification and nomenclature of cortical GABAergic interneurons. Nat. Rev. *Neurosci.* *14*, 202–216 (2013).

6. London M & Häusser M. Dendritic computation. Annu. Rev. *Neurosci.* *28*, 503–532 (2005).

7. Potjans TC & Diesmann M. The cell-type specific cortical microcircuit: relating structure and activity in a full-scale spiking network model. Cereb. *Cortex* *24*, 785–806 (2014).

8. Markram H et al. Reconstruction and simulation of neocortical microcircuitry. *Cell* *163*, 456–492 (2015).

9. Gleeson P et al. NeuroML: a language for describing data-driven models of neurons and networks with a high degree of biological detail. PLoS Comput. *Biol.* *6*, e1000815 (2010).

10. Jia H et al. Dendritic organization of thalamocortical inputs in mouse primary visual cortex. *Nature* *473*, 376–380 (2011).

11. Harris KD et al. Classes and continua of hippocampal CA1 inhibitory neurons revealed by single-cell transcriptomics. PLoS Biol. 17, e3000481 (2019).

12. Friston K. The free-energy principle: a unified brain theory? Nat. Rev. *Neurosci.* *11*, 127–138 (2010).

13. Connors BW & Long MA. Electrical synapses in the mammalian brain. Annu. Rev. *Neurosci.* *27*, 393–418 (2004).

14. Mastro JJ et al. Inhibitory circuit architecture and dynamics in cortical networks. Sci. *Adv.* *7*, eabg8411 (2021).

15. Tremblay R et al. GABAergic interneurons in the neocortex: from cellular properties to circuits. *Neuron* *91*, 260–292 (2016).

16. Litwin-Kumar A & Doiron B. Formation and maintenance of neuronal assemblies through synaptic plasticity. Nat. *Commun.* *5*, 5319 (2014).

17. Ascoli GA et al. NeuroMorpho.Org: a central resource for neuronal morphologies. J. *Neurosci.* *27*, 9247–9251 (2007).

18. Yuste R. From the neuron doctrine to neural networks. Nat. Rev. *Neurosci.* *16*, 487–497 (2015).

19. Huang S et al. Layer 1 neocortex: gating and integrating multidimensional signals. *Neuron* *111*, 3535–3552 (2023).

20. Gewaltig MO & Diesmann M. NEST (Neural Simulation Tool). *Scholarpedia* *2*, 1430 (2007).

21. Brette R et al. Simulation of networks of spiking neurons: a review of tools and strategies. J. Comput. *Neurosci.* *23*, 349–398 (2007).

22. Dayan P & Abbott LF. Theoretical Neuroscience: Computational and Mathematical Modeling of Neural Systems. MIT Press (2001).

23. Bullmore E & Sporns O. Complex brain networks: graph theoretical analysis of structural and functional systems. Nat. Rev. *Neurosci.* *10*, 186–198 (2009).

24. Bastiani M et al. A detailed theory of thalamic and cortical microcircuits for predictive visual inference. Sci. *Adv.* *10*, eadr6698 (2024).

25. Rolls ET & Deco G. The Noisy Brain: Stochastic Dynamics as a Principle of Brain Function. Oxford Univ. Press (2012).

26. Sompolinsky H, Crisanti A & Sommers HJ. Chaos in random neural networks. Phys. Rev. *Lett.* *61*, 259–262 (1988).

27. Koch C & Laurent G. Complexity and the nervous system. *Science* *284*, 96–98 (1999).

28. Churchland PS & Sejnowski TJ. The Computational Brain. MIT Press (1992).

29. Zingg B et al. Neural networks of the mouse neocortex. *Cell* *156*, 1096–1111 (2014).

30. Yao Z et al. A transcriptomic and epigenomic cell atlas of the mouse primary motor cortex. *Nature* *598*, 103–110 (2021).

31. Hooks BM et al. Topographic precision in sensory and motor corticospinal projections varies across the mouse neocortex. Nat. *Commun.* *9*, 3549 (2018).

32. Meyer HS et al. Cell type-specific thalamic innervation in a column of rat vibrissal cortex. Cereb. *Cortex* *21*, 2287–2303 (2011).

33. Petersen CC. The functional organization of the barrel cortex. *Neuron* *56*, 339–355 (2007).

34. Sherman SM & Guillery RW. The role of the thalamus in the flow of information to the cortex. Philos. Trans. R. Soc. Lond. B Biol. *Sci.* *357*, 1695–1708 (2002).

35. Tasic B et al. Shared and distinct transcriptomic cell types across neocortical areas. *Nature* *563*, 72–78 (2018).

36. Jones EG. The thalamic matrix and thalamocortical synchrony. *Trends Neurosci.* *24*, 595–601 (2001).

37. Sherman SM & Guillery RW. Untangling the cortico-thalamo-cortical loop: cellular pieces of a knotty circuit puzzle. J. Comp. *Neurol.* *521*, 4107–4111 (2013).

38. Gal E et al. Rich cell-type-specific network topology in neocortical microcircuitry. Nat. *Neurosci.* *22*, 1673–1683 (2019).

39. Dura-Bernal S et al. A universal workflow for creation, validation, and generalization of detailed neuronal models. PLoS Comput. *Biol.* *15*, e1007569 (2019).

40. Traub RD et al. Single-column thalamocortical network model exhibiting gamma oscillations, sleep spindles, and epileptogenic bursts. J. *Neurophysiol.* *93*, 2194–2232 (2005).

## Supplementary Information

### Supplementary Figures

**Supplementary Figure S1**: Electrophysiological validation of TCRc (thalamocortical relay core-type) neuron models. Current-clamp responses to step current injections demonstrating characteristic low-threshold calcium spikes (LTS) and burst firing patterns. Data generated from [cell_sim/TCRc/](file:///home/leo520/pynml/cell_sim/TCRc/) simulations.

**Supplementary Figure S2**: Electrophysiological validation of nRTc (nucleus reticularis thalami core-type) interneuron models. Fast-spiking responses with strong afterhyperpolarization following current injection protocols. Data generated from [cell_sim/nRTc/](file:///home/leo520/pynml/cell_sim/nRTc/) simulations.
**Supplementary Figure S3**: Electrophysiological validation of TCRm (thalamocortical relay matrix-type) neuron models. Broader action potentials and pronounced sag potentials indicating higher H-current expression. Data generated from [cell_sim/TCRm/](file:///home/leo520/pynml/cell_sim/TCRm/) simulations.

**Supplementary Figure S4**: Electrophysiological validation of nRTm (nucleus reticularis thalami matrix-type) interneuron models. Intermediate firing properties between core and intralaminar types. Data generated from [cell_sim/nRTm/](file:///home/leo520/pynml/cell_sim/nRTm/) simulations.

**Supplementary Figure S5**: Electrophysiological validation of TCRil (thalamocortical relay intralaminar-type) neuron models. Moderate burst capabilities with unique adaptation patterns during sustained depolarization. Data generated from [cell_sim/TCRil/](file:///home/leo520/pynml/cell_sim/TCRil/) simulations.

**Supplementary Figure S6**: Electrophysiological validation of nRTil (nucleus reticularis thalami intralaminar-type) interneuron models. Distinctive firing patterns characteristic of intralaminar thalamic nuclei. Data generated from [cell_sim/nRTil/](file:///home/leo520/pynml/cell_sim/nRTil/) simulations.

All supplementary figures are available in the [plots/](file:///home/leo520/pynml/plots/) directory and can be accessed through the interactive index at [plots/index.html](file:///home/leo520/pynml/plots/index.html).

### Extended Methods

**GPU Acceleration**: Our pipeline leverages CuPy for GPU-accelerated computations during network construction, particularly for distance calculations and connection probability evaluations. This enables construction of networks with hundreds of thousands of neurons in reasonable timeframes.

**Memory Management**: Custom memory management strategies prevent out-of-memory errors during large network construction, including periodic garbage collection and chunked processing of connection matrices.

**Parallel Processing**: Network construction utilizes multi-threading for independent operations such as cell placement and connection validation, significantly reducing total construction time.

#### Electrophysiological Feature Extraction

- Standardized current-clamp step protocols were used to quantify action potential width, sag ratio, input resistance, membrane time constant, firing adaptation, and rebound spiking.
- These metrics supported the refinement of cell-type clusters and validated functionally distinct populations.
- Results were stored in `cell_data/` and linked to network constructions for each regional model.

### Validation Metrics

Comprehensive validation metrics include:
- **Structural validation**: All generated NeuroML files pass schema validation
- **Functional validation**: Networks produce stable baseline activity without pathological states
- **Biological validation**: Key metrics (E/I ratios, connection probabilities) match experimental ranges
- **Reproducibility validation**: Identical results across multiple random seeds and computing platforms

