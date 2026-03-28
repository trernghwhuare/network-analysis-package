#!/usr/bin/env python3
"""
Interactive Layered Graph Visualization for Neural Networks

This script creates interactive visualizations based on net_params JSON files,
showing neurons arranged in cortical and thalamic layers with connection lines,
similar to the EPFL microcircuit portal but optimized for large-scale data.

Instead of individual neurons (which would be too dense), it shows:
- Layer bands with neuron density representation
- Connection strength between layers as curved lines
- Interactive hover information and highlighting
"""

import json
import os
import sys
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import logging
import re
from typing import Dict, List, Tuple, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Layer order and configuration for consistent positioning
LAYER_CONFIG = {
    'L1': {'y_pos': 0.9, 'color': '#FFD700', 'height': 0.08},        # Gold
    'L23': {'y_pos': 0.75, 'color': '#FF8C00', 'height': 0.12},      # Orange  
    'L4': {'y_pos': 0.6, 'color': '#DC143C', 'height': 0.12},        # Crimson
    'L5': {'y_pos': 0.45, 'color': '#228B22', 'height': 0.12},       # Forest Green
    'L6': {'y_pos': 0.3, 'color': '#4169E1', 'height': 0.12},        # Royal Blue
    'TCs_core': {'y_pos': 0.15, 'color': '#8A2BE2', 'height': 0.1},  # Blue Violet
    'TCs_matrix': {'y_pos': 0.05, 'color': '#9370DB', 'height': 0.1}, # Medium Purple
    'TCs_intralaminar': {'y_pos': -0.05, 'color': '#BA55D3', 'height': 0.1}  # Medium Orchid
}

LAYER_ORDER = list(LAYER_CONFIG.keys())

# Neuron type classifications for potential future use
EXCITATORY_TYPES = {
    "PC", "SP", "SS", "TTPC1", "TTPC2", "UTPC", "STPC", "IPC", "BPC", "TPC_L4", "TPC_L1",
    # L1 axon types (CT neurons - Cortico-Thalamic, excitatory)
    "DAC", "DLAC", "HAC", "NGCDA", "NGCSA", "SLAC",
    # Thalamic excitatory types (TCR = Thalamo-Cortical Relay)
    "TCR", "TCRc", "TCRm", "nRTm", 
}
INHIBITORY_TYPES = {
    "MC", "BTC", "DBC", "BP", "NGC", "LBC", "NBC", "SBC", "ChC",
    # Thalamic inhibitory types (nRT = nucleus Reticularis Thalami)  
    "nRT", "nRTc", "nRTil", "TCRil",
}

# Thalamic neuron type to layer mapping
THALAMIC_TYPE_TO_LAYER = {
    # TCs_core
    'TCRc': 'TCs_core',
    'nRT': 'TCs_core',   
    'nRTc': 'TCs_core',
    # TCs_matrix  
    'TCR': 'TCs_matrix',
    'TCRm': 'TCs_matrix',
    'nRTm': 'TCs_matrix',
    # TCs_intralaminar
    'TCRil': 'TCs_intralaminar',
    'nRTil': 'TCs_intralaminar'
}

def parse_connection_key(connection_key: str) -> Optional[Dict]:
    """Parse connection key with proper thalamic layer mapping."""
    try:
        if not connection_key or ':' not in connection_key:
            return None
        source_part, target_part = connection_key.split(':', 1)
        # Parse source part
        if '_' in source_part:
            # Has layer_type format (cortical neurons)
            source_parts = source_part.split('_', 1)
            source_layer, source_type = source_parts[0], source_parts[1]
        else:
            # Just type (thalamic neurons) - map to layer
            source_type = source_part
            source_layer = THALAMIC_TYPE_TO_LAYER.get(source_type)
            if source_layer is None:
                # Unknown thalamic type, skip
                return None
        
        # Parse target part  
        if '_' in target_part:
            # Has layer_type format (cortical neurons)
            target_parts = target_part.split('_', 1)
            target_layer, target_type = target_parts[0], target_parts[1]
        else:
            # Just type (thalamic neurons) - map to layer
            target_type = target_part
            target_layer = THALAMIC_TYPE_TO_LAYER.get(target_type)
            if target_layer is None:
                # Unknown thalamic type, skip
                return None
        
        # Validate layers
        if source_layer not in LAYER_ORDER or target_layer not in LAYER_ORDER:
            return None
            
        return {
            'connection_key': connection_key,
            'source_layer': source_layer,
            'source_type': source_type,
            'target_layer': target_layer,
            'target_type': target_type
        }
    except Exception as e:
        logger.warning(f"Error parsing connection key '{connection_key}': {e}")
        return None

def load_network_data(network_name: str) -> Tuple[Dict, Dict, Dict, Dict]:
    """Load anatomy, circuit, physiology, and layer data for a network."""
    base_path = Path("net_params") / network_name
    
    anatomy_file = base_path / f"extracted_{network_name}_anatomy.json"
    circuit_file = base_path / f"extracted_{network_name}_circuit.json" 
    physiology_file = base_path / f"extracted_{network_name}_pathways_physiology.json"
    layer_file = base_path / f"extracted_{network_name}_layer.json"
    
    required_files = [anatomy_file, circuit_file, physiology_file, layer_file]
    if not all(f.exists() for f in required_files):
        raise FileNotFoundError(f"Required files not found for network: {network_name}")
    
    with open(anatomy_file, 'r') as f:
        anatomy_data = json.load(f)
    with open(circuit_file, 'r') as f:
        circuit_data = json.load(f)
    with open(physiology_file, 'r') as f:
        physiology_data = json.load(f)
    with open(layer_file, 'r') as f:
        layer_data = json.load(f)
        
    return anatomy_data, circuit_data, physiology_data, layer_data

def identify_network_regions(network_name: str) -> Tuple[str, List[str]]:
    """
    Identify regions from network name by reading the actual region JSON file.
    """
    net_params_dir = Path("net_params")
    network_dir = net_params_dir / network_name
    region_json_file = network_dir / f'extracted_{network_name}_region.json'
    
    if region_json_file.exists():
        try:
            with open(region_json_file, 'r') as f:
                region_data = json.load(f)
            
            # Handle different region data structures
            if isinstance(region_data, dict):
                regions = list(region_data.keys())
            elif isinstance(region_data, list):
                regions = region_data
            else:
                regions = [str(region_data)]
            
            if len(regions) == 1:
                return 'single', regions
            elif len(regions) > 1:
                return 'multi', regions
            else:
                # Fallback if empty
                pass
                
        except (json.JSONDecodeError, IOError, KeyError) as e:
            logger.warning(f"Could not read or parse region file {region_json_file}: {e}")
    
    # Enhanced fallback logic with better pattern recognition
    if network_name == 'iT_max_plus':
        return 'single', ['iT']
    elif network_name == 'iC_max':
        return 'single', ['iC']
    elif network_name.startswith('loop_'):
        base_name = network_name.replace('loop_', '')
        # Check if base_name corresponds to a single layer
        if base_name in LAYER_CONFIG or re.match(r'^[A-Z]\d+[a-zA-Z]*$', base_name):
            return 'single', [base_name]
        else:
            # Try to extract multiple regions from complex loop names
            regions = extract_regions_from_name(base_name)
            if regions:
                return 'multi' if len(regions) > 1 else 'single', regions
    
    # Extract regions from network name as last resort
    regions = extract_regions_from_name(network_name)
    if len(regions) == 1:
        return 'single', regions
    elif len(regions) > 1:
        return 'multi', regions
    else:
        return 'single', [network_name]

def extract_regions_from_name(network_name: str) -> List[str]:
    """Extract potential region names from network name using regex patterns."""
    regions = []
    
    # Remove common suffixes
    clean_name = network_name
    for suffix in ['_max_plus', '_max', '_plus', '_max+']:
        clean_name = clean_name.replace(suffix, '')
    
    # Handle concatenated region names
    if clean_name == 'M2M1S1':
        regions = ['M2', 'M1', 'S1']
    elif clean_name == 'M2aM1aS1a':
        regions = ['M2a', 'M1a', 'S1a']
    elif clean_name == 'S1bM1bM2b':
        regions = ['S1b', 'M1b', 'M2b']
    elif clean_name == 'TC2IT2PTCT':
        regions = ['TC2', 'IT2', 'PT', 'CT']
    elif clean_name == 'TC2IT4_IT2CT':
        regions = ['TC2', 'IT4', 'IT2', 'CT']
    elif clean_name == 'TC2PT':
        regions = ['TC2', 'PT']
    elif re.match(r'^[A-Z]\d+[a-zA-Z]*$', clean_name):
        regions = [clean_name]
    else:
        regions = [clean_name]
    
    return regions

def classify_cell_type(cell_type: str) -> str:
    """Classify a cell type as excitatory, inhibitory, or unknown."""
    # Check against known excitatory morphological types
    if any(cell_type.startswith(prefix) for prefix in EXCITATORY_TYPES):
        return 'excitatory'
    
    # Check against known inhibitory morphological types  
    if any(cell_type.startswith(prefix) for prefix in INHIBITORY_TYPES):
        return 'inhibitory'
    
    # Handle electrical type naming conventions
    # Common excitatory electrical type patterns
    excitatory_patterns = ['PC', 'SS', 'SP', 'BP', 'cAD', 'cNAD', 'cIR', 'bIR']
    inhibitory_patterns = ['MC', 'BTC', 'DBC', 'ChC', 'LBC', 'NBC', 'SBC', 'cSTUT', 'cACint', 'cNAC', 'bNAC']
    
    if any(pattern in cell_type for pattern in excitatory_patterns):
        return 'excitatory'
    elif any(pattern in cell_type for pattern in inhibitory_patterns):
        return 'inhibitory'
    
    # Default classification based on common naming
    if 'PC' in cell_type or 'SS' in cell_type or 'SP' in cell_type or 'BP' in cell_type:
        return 'excitatory'
    else:
        return 'inhibitory'

def create_layered_visualization(anatomy_data: Dict, layer_data: Dict, network_name: str, network_type: str, regions_list: List[str]) -> go.Figure:
    """Create an interactive layered visualization showing neurons and connections at cell type level."""
    
    # Parse all connections first to identify all layers that actually exist
    parsed_connections = []
    all_connection_layers = set()
    
    for connection_key in anatomy_data.keys():
        parsed_conn = parse_connection_key(connection_key)
        if parsed_conn:
            parsed_connections.append(parsed_conn)
            all_connection_layers.add(parsed_conn['source_layer'])
            all_connection_layers.add(parsed_conn['target_layer'])
    
    # Initialize layer data including layers from connections
    layer_neurons = {}
    layer_cell_types = {}
    
    # Start with layers from layer_data
    for layer in LAYER_ORDER:
        layer_neurons[layer] = 0
        layer_cell_types[layer] = set()
    
    # Add layers from connection data that might not be in layer_data
    for layer in all_connection_layers:
        if layer not in layer_neurons:
            layer_neurons[layer] = 0
            layer_cell_types[layer] = set()
    
    # Calculate total neurons per layer from layer_data
    for layer, layer_info in layer_data.items():
        if layer in layer_neurons:
            morph_types = layer_info.get('No. of neurons per morphological types', {})
            total_neurons = sum(morph_types.values()) if morph_types else 0
            layer_neurons[layer] = total_neurons
            layer_cell_types[layer] = set(morph_types.keys())
    
    # Always collect cell types from connection data for ALL layers
    # This ensures that electrical types used in connections are included even if they differ from morphological types
    for parsed_conn in parsed_connections:
        source_layer = parsed_conn['source_layer']
        target_layer = parsed_conn['target_layer']
        # Ensure layers exist in our data structures (should already be there, but just in case)
        if source_layer not in layer_cell_types:
            layer_cell_types[source_layer] = set()
        if target_layer not in layer_cell_types:
            layer_cell_types[target_layer] = set()
        # Add cell types from connections for ALL layers
        layer_cell_types[source_layer].add(parsed_conn['source_type'])
        layer_cell_types[target_layer].add(parsed_conn['target_type'])
    
    # Store cell type connections for detailed visualization (always use cell type level)
    cell_type_connections = {}
    
    for parsed_conn in parsed_connections:
        connection_key = parsed_conn['connection_key']
        conn_data = anatomy_data[connection_key]
        synapse_count = conn_data.get('total_synapse_count', 0)
        connection_prob = conn_data.get('connection_probability', 0)
        
        if synapse_count > 0:
            cell_type_pair = (f"{parsed_conn['source_layer']}_{parsed_conn['source_type']}", 
                            f"{parsed_conn['target_layer']}_{parsed_conn['target_type']}")
            cell_type_connections[cell_type_pair] = {
                'synapses': synapse_count,
                'probability': connection_prob,
                'source_layer': parsed_conn['source_layer'],
                'target_layer': parsed_conn['target_layer'],
                'source_type': parsed_conn['source_type'],
                'target_type': parsed_conn['target_type']
            }
    
    # Get relevant layers that have neurons or connections
    layers_with_neurons = {layer for layer in LAYER_ORDER if layer_neurons[layer] > 0}
    layers_with_connections = set()
    for conn_data in cell_type_connections.values():
        layers_with_connections.add(conn_data['source_layer'])
        layers_with_connections.add(conn_data['target_layer'])
    
    all_relevant_layers = layers_with_neurons.union(layers_with_connections)
    
    # Create figure
    fig = go.Figure()
    
    # Always show cell type level connections for all networks
    max_synapses = max([conn['synapses'] for conn in cell_type_connections.values()] or [1])
    
    # Add layer bands for all relevant layers
    layer_y_positions = {}
    for layer in LAYER_ORDER:
        if layer in all_relevant_layers and layer in LAYER_CONFIG:
            config = LAYER_CONFIG[layer]
            y_pos = config['y_pos']
            layer_y_positions[layer] = y_pos
            color = config['color']
            
            # Add layer band background with artistic softening
            fig.add_shape(
                type="rect",
                x0=-0.1, x1=1.1,
                y0=y_pos - config['height']/2, 
                y1=y_pos + config['height']/2,
                fillcolor=color,
                opacity=0.15,  # Reduced from 0.2 for softer appearance
                line=dict(width=0),
                layer='below'
            )
            
            # Add layer label and neuron count
            neuron_count = layer_neurons.get(layer, 0)
            fig.add_annotation(
                x=0.02,
                y=y_pos,
                text=f"{layer}",
                showarrow=False,
                font=dict(color=color, family='Arial Black', size=14),
                xanchor='left',
                yanchor='middle'
            )
            if neuron_count > 0:
                fig.add_annotation(
                    x=0.98,
                    y=y_pos,
                    text=f"{neuron_count:,} neurons",
                    showarrow=False,
                    font=dict(color=color, size=12),
                    xanchor='right',
                    yanchor='middle'
                )
    
    # Position cell types within each layer
    layer_cell_type_positions = {}
    
    for layer in all_relevant_layers:
        if layer in layer_cell_types and layer in layer_y_positions:
            cell_types = sorted(list(layer_cell_types[layer]))
            if len(cell_types) == 0:
                continue
                
            y_pos = layer_y_positions[layer]
            config = LAYER_CONFIG.get(layer, {'height': 0.12})
            layer_height = config['height']
            
            # Position cell types horizontally within the layer band
            n_cell_types = len(cell_types)
            if n_cell_types == 1:
                x_positions = [0.5]
            else:
                # Leave some margin on sides
                x_positions = np.linspace(0.15, 0.85, n_cell_types)
            
            layer_cell_type_positions[layer] = {}
            
            # Add cell type nodes
            for i, cell_type in enumerate(cell_types):
                x_pos = x_positions[i]
                # Add small vertical offset within layer band for better visibility
                y_offset = (np.random.random() - 0.5) * layer_height * 0.6 if n_cell_types > 1 else 0
                node_y = y_pos + y_offset
                
                # Get neuron count for this cell type
                neuron_count = 0
                if layer in layer_data:
                    morph_types = layer_data[layer].get('No. of neurons per morphological types', {})
                    neuron_count = morph_types.get(cell_type, 0)
                
                # Determine marker based on cell type
                cell_classification = classify_cell_type(cell_type)
                marker_symbol = 'circle' if cell_classification == 'excitatory' else 'diamond'
                color = LAYER_CONFIG[layer]['color']
                
                fig.add_trace(go.Scatter(
                    x=[x_pos],
                    y=[node_y],
                    mode='markers+text',
                    marker=dict(
                        color=color,
                        size=max(6, min(15, np.log10(neuron_count + 1) * 4)) if neuron_count > 0 else 8,
                        symbol=marker_symbol,
                        line=dict(width=1, color='white')
                    ),
                    text=[cell_type[:12] + '...' if len(cell_type) > 15 else cell_type],  # Truncate long names
                    textposition="top center",
                    textfont=dict(size=8, color=color),
                    hoverinfo='text',
                    hovertext=f"<b>{layer}_{cell_type}</b><br>"
                             f"<span style='color:{color}'>●</span> Neurons: {neuron_count:,}<br>"
                             f"<span style='color:{color}'>●</span> Type: {cell_classification.title()}",
                    customdata=[{'layer': layer, 'cell_type': cell_type}],
                    showlegend=False
                ))
                
                layer_cell_type_positions[layer][cell_type] = (x_pos, node_y)
    
    # Add connections between cell types across all layers
    for (source_full, target_full), conn_data in cell_type_connections.items():
        # Use pre-parsed layer and type information instead of splitting strings
        # This avoids issues with layer names containing underscores (like TCs_matrix)
        source_layer = conn_data['source_layer']
        source_type = conn_data['source_type']
        target_layer = conn_data['target_layer']
        target_type = conn_data['target_type']
        
        # Skip very weak connections for clarity - extremely permissive filtering
        # Use both relative and absolute thresholds to show virtually all connections
        relative_threshold = max_synapses * 0.0001  # Very low relative threshold
        absolute_threshold = 1  # Minimum of 1 synapse (should filter only pure noise)
        # Safety check in case max_synapses is unexpectedly 0
        final_threshold = max(relative_threshold, absolute_threshold) if max_synapses > 0 else 1
        if conn_data['synapses'] < final_threshold:
            continue
        
        # Get positions
        if (source_layer in layer_cell_type_positions and 
            source_type in layer_cell_type_positions[source_layer] and
            target_layer in layer_cell_type_positions and
            target_type in layer_cell_type_positions[target_layer]):
            
            source_x, source_y = layer_cell_type_positions[source_layer][source_type]
            target_x, target_y = layer_cell_type_positions[target_layer][target_type]
            color = LAYER_CONFIG[source_layer]['color']
            
            # Calculate line width based on connection strength
            line_width = max(0.3, min(4, (conn_data['synapses'] / max_synapses) * 3))
            
            # Create connection line
            if source_layer == target_layer and source_type == target_type:
                # Self-connection: create small loop
                mid_x = source_x
                mid_y = source_y + 0.03
                x_points = [source_x - 0.02, mid_x, source_x + 0.02]
                y_points = [source_y, mid_y, source_y]
            elif source_layer == target_layer:
                # Same layer, different cell types
                mid_x = (source_x + target_x) / 2
                mid_y = (source_y + target_y) / 2 + 0.02
                x_points = [source_x, mid_x, target_x]
                y_points = [source_y, mid_y, target_y]
            else:
                # Different layers
                mid_x = (source_x + target_x) / 2
                mid_y = (source_y + target_y) / 2
                # Add curvature based on layer positions
                control_y = mid_y + 0.05 * np.sign(target_y - source_y)
                t = np.linspace(0, 1, 20)
                x_points = (1 - t) * source_x + t * target_x
                y_points = (1 - t)**2 * source_y + 2 * (1 - t) * t * control_y + t**2 * target_y
            
            # Determine line shape and dash pattern based on connection strength
            if conn_data['synapses'] > max_synapses * 0.5:
                line_shape = 'linear'
                dash_pattern = 'solid'
                opacity = 1.0
            elif conn_data['synapses'] > max_synapses * 0.1:
                line_shape = 'spline'
                dash_pattern = 'dash'
                opacity = 0.8
            else:
                line_shape = 'spline'
                dash_pattern = 'dot'
                opacity = 0.6
            
            base_color = color
            
            # Enhanced traditional line with artistic softening effects
            fig.add_trace(go.Scatter(
                x=x_points,
                y=y_points,
                mode='lines',
                line=dict(
                    color=base_color,
                    width=line_width,
                    shape=line_shape,
                    dash=dash_pattern
                ),
                hoverinfo='text',
                hovertext=f"<b>{source_layer}_{source_type} → {target_layer}_{target_type}</b><br>"
                         f"<span style='color:{base_color}; font-weight:bold;'>━━━</span> "
                         f"<b>Synapses:</b> {conn_data['synapses']:,}<br>"
                         f"<span style='color:{base_color}; font-weight:bold;'>━━━</span> "
                         f"<b>Probability:</b> {conn_data['probability']:.4f}<br>"
                         f"<span style='color:{base_color}; font-weight:bold;'>━━━</span> "
                         f"<b>Strength:</b> {'Strong' if conn_data['synapses'] > max_synapses * 0.5 else 'Moderate' if conn_data['synapses'] > max_synapses * 0.1 else 'Weak'}",
                customdata=[{'source': source_full, 'target': target_full}],
                showlegend=False,
                # Add subtle artistic softening with gentle opacity
                opacity=opacity * 0.9 + 0.1 * np.random.random(),  # Slight organic variation
                # Add subtle glow effect for stronger connections
                marker=dict(size=0)
            ))
            
            # Add subtle glow effect for stronger connections (artistic enhancement)
            if conn_data['synapses'] > max_synapses * 0.3:
                glow_opacity = opacity * 0.3
                glow_width = line_width * 1.8
                
                fig.add_trace(go.Scatter(
                    x=x_points,
                    y=y_points,
                    mode='lines',
                    line=dict(
                        color=base_color,
                        width=glow_width,
                        shape=line_shape,
                        dash=dash_pattern
                    ),
                    hoverinfo='skip',  # Don't show hover for glow
                    showlegend=False,
                    opacity=glow_opacity,
                    marker=dict(size=0)
                ))
    
    # Update layout
    title_suffix = "Cell Type Level"
    
    # Adaptive layout for complex networks (3+ regions)
    is_complex_network = len(regions_list) >= 3
    base_width = 1400 if is_complex_network else 1200  # Increased width for better cell type spacing
    base_height = 900 if is_complex_network else 800
    font_size = 9 if is_complex_network else 10
    
    # Adjust y-axis range to accommodate all layers
    y_min = min(layer_y_positions.values()) - 0.2 if layer_y_positions else -0.2
    y_max = max(layer_y_positions.values()) + 0.2 if layer_y_positions else 1.0
    
    fig.update_layout(
        title={
            'text': f"Interactive Layered Network Visualization<br><sub>{network_name} • {network_type.title()} Region{'s' if network_type == 'multi' else ''} • {title_suffix}</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial Black'}
        },
        width=base_width,
        height=base_height,
        plot_bgcolor='rgba(245, 247, 249, 0.8)',  # Soft light gray with subtle transparency
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[-0.1, 1.1],
            constrain='domain'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=[y_min, y_max],
            constrain='domain'
        ),
        showlegend=False,
        margin=dict(l=50, r=50, t=100, b=50),
        font=dict(family='Arial', size=font_size)
    )
    
    return fig

def create_interactive_html(fig: go.Figure, network_name: str, network_type: str, regions_list: List[str], layer_data: Dict, anatomy_data: Dict) -> str:
    """Create complete HTML with sidebar and interactive features."""
    
    # Calculate total neurons
    total_neurons = 0
    for layer in LAYER_ORDER:
        if layer in layer_data:
            morph_types = layer_data[layer].get('No. of neurons per morphological types', {})
            total_neurons += sum(morph_types.values()) if morph_types else 0
    
    # Count active connections
    active_connections = 0
    total_synapses = 0
    for connection_key in anatomy_data.keys():
        parsed_conn = parse_connection_key(connection_key)
        if parsed_conn:
            conn_data = anatomy_data[connection_key]
            synapse_count = conn_data.get('total_synapse_count', 0)
            if synapse_count > 0:
                active_connections += 1
                total_synapses += synapse_count
    
    # Build sidebar content with enhanced region display for complex networks
    sidebar_content = f"""
            <h3>Network Data Summary</h3>
            <p><b>Network:</b> {network_name}</p>
            <p><b style="color: {'#27ae60' if network_type == 'single' else '#2980b9'}">Type:</b> <span style="background-color: {'#d5f5e3' if network_type == 'single' else '#d6eaf8'}; padding: 2px 6px; border-radius: 4px;">{network_type.title()} Region{'s' if network_type == 'multi' else ''}</span></p>
    """
    
    # Enhanced region display for complex networks
    if len(regions_list) >= 3:
        # Group regions by base name for cleaner display
        region_groups = {}
        for region in regions_list:
            base_name = re.sub(r'[ab]$', '', region)  # Remove trailing a/b
            if base_name not in region_groups:
                region_groups[base_name] = []
            region_groups[base_name].append(region)
        
        regions_display = []
        for base, variants in region_groups.items():
            if len(variants) == 1:
                regions_display.append(variants[0])
            else:
                regions_display.append(f"{base} ({', '.join([v[-1] for v in sorted(variants)])})")
        
        sidebar_content += f'            <p><b>Regions:</b> {", ".join(regions_display)}</p>\n'
    else:
        sidebar_content += f'            <p><b>Regions:</b> {", ".join(regions_list)}</p>\n'
    
    sidebar_content += f"""
            <p><b>Total Neurons:</b> {total_neurons:,}</p>
            <p><b>Active Connections:</b> {active_connections:,}</p>
            <p><b>Total Synapses:</b> {total_synapses:,}</p>
            
            <h4>Layers</h4>
    """
    
    for layer in LAYER_ORDER:
        if layer in layer_data:
            morph_types = layer_data[layer].get('No. of neurons per morphological types', {})
            total_layer_neurons = sum(morph_types.values()) if morph_types else 0
            if total_layer_neurons > 0:
                sidebar_content += f'            <p><b>{layer}:</b> {total_layer_neurons:,} neurons ({len(morph_types)} m-types)</p>\n'
    
    # Convert figure to HTML
    import plotly.io as pio
    
    plot_html = pio.to_html(fig, include_plotlyjs=True, full_html=False)
    
    # Create complete HTML
    network_type_display = f"({network_type.title()} Region{'s' if network_type == 'multi' else ''})"
    complete_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Layered Graph - {network_name} {network_type_display}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4edf9 100%);
            min-height: 100vh;
        }}
        .container {{
            display: flex;
            height: 100vh;
            width: 100vw;
        }}
        .plot-container {{
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }}
        .data-sidebar {{
            width: 320px;
            background: rgba(255, 255, 255, 0.95);
            border-left: 2px solid #ccc;
            padding: 20px;
            overflow-y: auto;
            box-shadow: -2px 0 8px rgba(0,0,0,0.1);
            z-index: 10;
        }}
        .data-sidebar h3 {{
            margin-top: 0;
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
            font-size: 18px;
        }}
        .data-sidebar h4 {{
            margin-top: 15px;
            color: #34495e;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 5px;
            font-size: 14px;
        }}
        .data-sidebar p {{
            margin: 8px 0;
            font-size: 13px;
            line-height: 1.4;
        }}
        .data-sidebar b {{
            color: #2c3e50;
        }}
        .network-type-single {{
            background-color: #d5f5e3;
            color: #27ae60;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
        }}
        .network-type-multi {{
            background-color: #d6eaf8;
            color: #2980b9;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="plot-container" id="plot-container">
            {plot_html}
        </div>
        <div class="data-sidebar">
            {sidebar_content}
        </div>
    </div>
</body>
</html>
"""
    
    return complete_html

def create_interactive_layered_graph(network_name: str):
    """Main function to create interactive layered graph visualization."""
    logger.info(f"Loading network data for: {network_name}")
    
    try:
        anatomy_data, circuit_data, physiology_data, layer_data = load_network_data(network_name)
    except FileNotFoundError as e:
        logger.error(str(e))
        return
    
    # Identify network type
    network_type, regions_list = identify_network_regions(network_name)
    
    # Create layered visualization
    logger.info("Creating layered visualization...")
    fig = create_layered_visualization(anatomy_data, layer_data, network_name, network_type, regions_list)
    
    # Create complete HTML
    html_content = create_interactive_html(fig, network_name, network_type, regions_list, layer_data, anatomy_data)
    
    # Save visualization
    output_dir = Path("html")
    output_dir.mkdir(exist_ok=True)
    html_file = output_dir / f"layered_graph_{network_name}.html"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"Layered graph visualization saved to: {html_file}")

def get_all_network_names() -> List[str]:
    """Get all available network names from the net_params directory."""
    net_params_dir = Path("net_params")
    if not net_params_dir.exists():
        logger.error(f"net_params directory not found at {net_params_dir.absolute()}")
        return []
    
    network_names = []
    for item in net_params_dir.iterdir():
        if item.is_dir():
            network_names.append(item.name)
    
    return sorted(network_names)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Create interactive layered graph visualization')
    parser.add_argument('--network', help='Network name (e.g., C2T_max_plus, loop_L1)')
    parser.add_argument('--all', action='store_true', help='Process all available network datasets')
    args = parser.parse_args()
    
    if args.all:
        if args.network:
            logger.warning("Both --network and --all specified. Using --all and ignoring --network.")
        network_names = get_all_network_names()
        if not network_names:
            logger.error("No network datasets found in net_params directory.")
            sys.exit(1)
        
        logger.info(f"Processing {len(network_names)} network datasets: {network_names}")
        for i, network_name in enumerate(network_names, 1):
            logger.info(f"Processing network {i}/{len(network_names)}: {network_name}")
            try:
                create_interactive_layered_graph(network_name)
            except Exception as e:
                logger.error(f"Failed to process network {network_name}: {e}")
                continue
        logger.info("All network datasets processed successfully!")
    else:
        if not args.network:
            parser.error("Either --network or --all must be specified.")
        # Use the main function that produces proper HTML with sidebar and styling
        create_interactive_layered_graph(args.network)

if __name__ == "__main__":
    main()