#!/usr/bin/env python3
"""
Simplified String Graph Visualization for Layer-to-Layer Connections

This script creates circular chord diagrams showing aggregated connections 
between cortical and thalamic layers, rather than individual neuron types.
Each arc represents a layer, and chords show total connection strength 
between layers with width proportional to synapse count.

Much clearer and easier to interpret than the full neuron-level version.
"""

import json
import os
import sys
from pathlib import Path
import numpy as np
import plotly.graph_objects as go
import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Layer order for consistent positioning
LAYER_ORDER = ['L1', 'L23', 'L4', 'L5', 'L6', 'TCs_core', 'TCs_matrix', 'TCs_intralaminar']

# Layer-specific colors matching the enhanced visualization
LAYER_COLORS = {
    'L1': '#FFD700',        # Gold
    'L23': '#FF8C00',       # Orange  
    'L4': '#DC143C',        # Crimson
    'L5': '#228B22',        # Forest Green
    'L6': '#4169E1',        # Royal Blue
    'TCs_core': '#8A2BE2',  # Blue Violet
    'TCs_matrix': '#9370DB', # Medium Purple
    'TCs_intralaminar': '#BA55D3'  # Medium Orchid
}

def get_layer_color(layer_name):
    """Unified function to get layer color, ensuring consistency across all elements."""
    return LAYER_COLORS.get(layer_name, '#888888')

def create_concise_region_label(regions_list):
    """Create a concise label for regions by grouping similar base regions.
    
    Args:
        regions_list: List of region names (e.g., ['M1a', 'M1b', 'S1a', 'S1b', 'M2a', 'M2b'])
        
    Returns:
        str: Concise region label (e.g., 'M1(a,b),S1(a,b),M2(a,b)')
    """
    if not regions_list:
        return ""
    
    # Group regions by base name (everything before the last character)
    region_groups = {}
    for region in regions_list:
        if len(region) >= 2 and region[-1] in 'ab':
            # Region has variant suffix (a or b)
            base_name = region[:-1]
            variant = region[-1]
            if base_name not in region_groups:
                region_groups[base_name] = []
            region_groups[base_name].append(variant)
        else:
            # Region doesn't have variant suffix
            if region not in region_groups:
                region_groups[region] = []
    
    # Create concise labels for each group
    concise_parts = []
    for base_name in sorted(region_groups.keys()):
        variants = sorted(region_groups[base_name])
        if variants:
            # Has variants like a, b
            concise_parts.append(f"{base_name}({','.join(variants)})")
        else:
            # No variants, just the base name
            concise_parts.append(base_name)
    
    return ','.join(concise_parts)

# Neuron type classifications for marker differentiation
EXCITATORY_TYPES = {
    "PC", "SP", "SS", "TTPC1", "TTPC2", "UTPC", "STPC", "IPC", "BPC", "TPC_L4", "TPC_L1",
    # L1 axon types (CT neurons - Cortico-Thalamic, excitatory)
    "DAC", "DLAC", "HAC", "NGCDA", "NGCSA", "SLAC",
    # Thalamic excitatory types (TCR = Thalamo-Cortical Relay)
    "TCR", "TCRc", "TCRm", "TCRil"
}
INHIBITORY_TYPES = {
    "MC", "BTC", "DBC", "BP", "NGC", "LBC", "NBC", "SBC", "ChC",
    # Thalamic inhibitory types (nRT = nucleus Reticularis Thalami)  
    "nRT", "nRTc", "nRTm", "nRTil"
}

def get_mtype_marker(mtype):
    """Get appropriate marker symbol based on m-type classification."""
    # Handle complex m-types like "TPC_L4" by extracting the base type
    base_type = mtype.split('_')[0] if '_' in mtype else mtype
    
    if base_type in EXCITATORY_TYPES:
        return 'circle'  # Excitatory: circles
    elif base_type in INHIBITORY_TYPES:
        return 'diamond'  # Inhibitory: diamonds
    else:
        return 'square'  # Unknown/Unclassified: squares

# Thalamic neuron type to layer mapping
THALAMIC_TYPE_TO_LAYER = {
    # TCs_core
    'TCRc': 'TCs_core',
    'nRT': 'TCs_core',   # nRT appears to be in core based on data
    'nRTc': 'TCs_core',
    
    # TCs_matrix  
    'TCR': 'TCs_matrix',
    'TCRm': 'TCs_matrix',
    'nRTm': 'TCs_matrix',
    
    # TCs_intralaminar
    'TCRil': 'TCs_intralaminar',
    'nRTil': 'TCs_intralaminar'
}

def parse_connection_key(connection_key):
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

def load_network_data(network_name):
    """Load anatomy, circuit, and physiology data for a network."""
    base_path = Path("net_params") / network_name
    
    anatomy_file = base_path / f"extracted_{network_name}_anatomy.json"
    circuit_file = base_path / f"extracted_{network_name}_circuit.json" 
    physiology_file = base_path / f"extracted_{network_name}_pathways_physiology.json"
    
    if not all(f.exists() for f in [anatomy_file, circuit_file, physiology_file]):
        raise FileNotFoundError(f"Required files not found for network: {network_name}")
    
    with open(anatomy_file, 'r') as f:
        anatomy_data = json.load(f)
    with open(circuit_file, 'r') as f:
        circuit_data = json.load(f)
    with open(physiology_file, 'r') as f:
        physiology_data = json.load(f)
        
    return anatomy_data, circuit_data, physiology_data

def create_layer_connection_matrix(parsed_connections, anatomy_data):
    """Create adjacency matrix of layer-to-layer connection strengths."""
    n = len(LAYER_ORDER)
    layer_to_index = {layer: i for i, layer in enumerate(LAYER_ORDER)}
    connection_matrix = np.zeros((n, n))
    connection_count_matrix = np.zeros((n, n))  # Track number of connections
    
    # Aggregate connections by layer pairs
    layer_connection_stats = {}
    
    for conn in parsed_connections:
        source_layer = conn['source_layer']
        target_layer = conn['target_layer']
        layer_pair = (source_layer, target_layer)
        
        if layer_pair not in layer_connection_stats:
            layer_connection_stats[layer_pair] = {
                'total_synapses': 0,
                'total_connections': 0,
                'avg_probability': 0,
                'connection_count': 0
            }
        
        conn_data = anatomy_data.get(conn['connection_key'], {})
        synapse_count = conn_data.get('total_synapse_count', 0)
        connection_prob = conn_data.get('connection_probability', 0)
        
        layer_connection_stats[layer_pair]['total_synapses'] += synapse_count
        layer_connection_stats[layer_pair]['total_connections'] += 1
        layer_connection_stats[layer_pair]['avg_probability'] += connection_prob
        layer_connection_stats[layer_pair]['connection_count'] += 1
        
        # Fill matrices
        i = layer_to_index[source_layer]
        j = layer_to_index[target_layer]
        connection_matrix[i][j] += synapse_count
        connection_count_matrix[i][j] += 1
    
    return connection_matrix, connection_count_matrix, layer_connection_stats

def create_layer_string_graph(connection_matrix, connection_count_matrix, layer_connection_stats, network_name, layer_mtypes=None, network_type=None, regions_list=None, region_data=None, parsed_connections=None):
    """Create a simplified string graph visualization showing layer-to-layer connections with artistic strings.
    
    Args:
        connection_matrix: Adjacency matrix of connection strengths
        connection_count_matrix: Matrix of connection counts
        layer_connection_stats: Statistics for each layer pair
        network_name: Name of the network
        layer_mtypes: Dictionary mapping layers to their m-types
        network_type: 'single' or 'multi' region network
        regions_list: List of regions in the network
        region_data: Dictionary containing region-specific data for m-type mapping
        parsed_connections: List of parsed connection dictionaries (needed for accurate TCs_core region labeling)
    """
    n = len(LAYER_ORDER)
    layer_to_index = {layer: i for i, layer in enumerate(LAYER_ORDER)}
    
    # Initialize region_data if not provided
    if region_data is None:
        region_data = {}
    
    # Calculate angles for circular layout
    angles = np.linspace(0, 2*np.pi, n, endpoint=False)
    
    # Calculate arc widths based on total connections per layer
    total_connections = np.sum(connection_count_matrix, axis=1) + np.sum(connection_count_matrix, axis=0)
    max_connections = np.max(total_connections) if np.max(total_connections) > 0 else 1
    arc_widths = (total_connections / max_connections) * (np.pi / 3) + 0.1  # Minimum width
    
    # Create figure
    fig = go.Figure()
    
    # Use provided m-types or create placeholder if not available
    if layer_mtypes is None:
        layer_mtypes = {layer: [f"{layer}_type_{i}" for i in range(3)] for layer in LAYER_ORDER}
    
    # Add dots for each layer representing actual m-types instead of arcs
    for i, (layer, angle, arc_width) in enumerate(zip(LAYER_ORDER, angles, arc_widths)):
        color = get_layer_color(layer)
        
        # Get m-types for this layer
        mtypes = list(layer_mtypes.get(layer, []))
        if not mtypes:
            mtypes = [f"{layer}_placeholder"]  # Fallback if no m-types found
        
        num_dots = len(mtypes)
        
        # Create angular spread around the main layer angle
        if num_dots == 1:
            dot_angles = [angle]
        else:
            dot_angles = np.linspace(angle - arc_width/3, angle + arc_width/3, num_dots)
        
        dot_radius = 0.88  # Same radius as original arcs
        
        dot_x = np.cos(dot_angles) * dot_radius
        dot_y = np.sin(dot_angles) * dot_radius
        
        # Get layer statistics for hover
        outgoing_conns = int(np.sum(connection_count_matrix[i, :]))
        incoming_conns = int(np.sum(connection_count_matrix[:, i]))
        outgoing_synapses = int(np.sum(connection_matrix[i, :]))
        incoming_synapses = int(np.sum(connection_matrix[:, i]))
        
        # Ensure all values are Python ints for string formatting
        outgoing_conns = int(outgoing_conns)
        incoming_conns = int(incoming_conns)
        outgoing_synapses = int(outgoing_synapses)
        incoming_synapses = int(incoming_synapses)
        
        # Create individual dots with m-type specific hover info and markers
        for j, (x, y, mtype) in enumerate(zip(dot_x, dot_y, mtypes)):
            marker_symbol = get_mtype_marker(mtype)
            
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers',
                marker=dict(
                    color=color,
                    size=14,
                    symbol=marker_symbol,
                    line=dict(width=2, color='white')
                ),
                hoverinfo='text',
                hovertext=f"<b>{mtype}</b><br>"
                         f"<span style='color:{color}'>●</span> Layer: {layer}<br>"
                         f"<span style='color:{color}'>●</span> Outgoing: {outgoing_conns} connections ({outgoing_synapses:,} synapses)<br>"
                         f"<span style='color:{color}'>●</span> Incoming: {incoming_conns} connections ({incoming_synapses:,} synapses)<br>",
                customdata=[layer],
                showlegend=False
            ))
        
        # Create appropriate label based on network type and region data
        if network_type == 'multi' and region_data:
            # For multi-region networks, determine which regions contain this layer
            regions_with_layer = []
            
            # Special handling for TCs_core layer: only include regions that actually have valid TCs_core connections
            if layer == 'TCs_core':
                # Get all m-types that actually appear in TCs_core connections after filtering
                tc_core_mtypes_in_connections = set()
                if parsed_connections:  # Add null check
                    for conn in parsed_connections:
                        if conn['source_layer'] == 'TCs_core':
                            tc_core_mtypes_in_connections.add(conn['source_type'])
                        if conn['target_layer'] == 'TCs_core':
                            tc_core_mtypes_in_connections.add(conn['target_type'])
                
                # Check each region to see if it contains any of these actually-used m-types
                for region_name, region_info in region_data.items():
                    if 'No. of neurons per morphological types' in region_info:
                        morph_types = region_info['No. of neurons per morphological types']
                        # Check if any actually-used TCs_core m-type exists in this region
                        for mtype in tc_core_mtypes_in_connections:
                            if mtype in morph_types and morph_types[mtype] > 0:
                                # According to model construction rules, M2 regions should NOT have TCs_core connections
                                # Even if the m-type exists in the region data, exclude M2 regions from TCs_core labels
                                if not region_name.startswith('M2'):
                                    regions_with_layer.append(region_name)
                                logger.debug(f"TCs_core: {region_name} contains {mtype}, {'included' if not region_name.startswith('M2') else 'excluded (M2 region)'}")
                                break
            else:
                # Get all m-types for this layer
                layer_mtypes_list = list(layer_mtypes.get(layer, []))
                
                if layer_mtypes_list:
                    # Check each region to see if it contains any of these m-types
                    for region_name, region_info in region_data.items():
                        if 'No. of neurons per morphological types' in region_info:
                            morph_types = region_info['No. of neurons per morphological types']
                            
                            # Check if any m-type for this layer exists in this region
                            for mtype in layer_mtypes_list:
                                # Extract morphological type from mtype (e.g., "L1_DAC" -> "DAC")
                                if '_' in mtype:
                                    morph_type = mtype.split('_', 1)[1]
                                    if morph_type in morph_types and morph_types[morph_type] > 0:
                                        regions_with_layer.append(region_name)
                                        break
                                else:
                                    # Thalamic type - check if it exists in region
                                    if mtype in morph_types and morph_types[mtype] > 0:
                                        regions_with_layer.append(region_name)
                                        break
            
            if regions_with_layer:
                # Create concise labels for regions to avoid overly verbose display
                # Group regions by base name (e.g., M1a, M1b -> M1(a,b))
                regions_str = create_concise_region_label(regions_with_layer)
                display_label = f"{layer} ({regions_str})"
                logger.debug(f"Layer {layer} found in regions: {regions_str}")
                
                # For very long labels, split into multiple lines for better readability
                if len(display_label) > 25:  # Threshold for splitting
                    # Try to split at logical points (after layer name, or between region groups)
                    if '(' in display_label and ')' in display_label:
                        # Split as "L6" and "(M1(a,b),M2(a,b),S1(a,b))"
                        layer_part = display_label.split('(', 1)[0]
                        regions_part = '(' + display_label.split('(', 1)[1]
                        display_label = f"{layer_part}<br>{regions_part}"
                    else:
                        # Fallback: split at character limit
                        mid_point = len(display_label) // 2
                        display_label = f"{display_label[:mid_point]}<br>{display_label[mid_point:]}"
            else:
                # Fallback to just layer name
                display_label = layer
                logger.debug(f"Layer {layer} not found in any regions, using fallback")
        else:
            # For single-region networks, use just the layer name
            display_label = layer
        
        # Add layer label
        # Determine if this is a complex multi-region network
        is_complex_network = network_type == 'multi' and region_data and len(region_data) >= 3
        
        # Adjust label positioning and styling based on network complexity
        if is_complex_network:
            # For complex networks, position labels further out and use smaller font
            label_radius = 1.25
            label_font_size = 12
        else:
            # Default positioning for simple networks
            label_radius = 1.15
            label_font_size = 14
            
        label_x = np.cos(angle) * label_radius
        label_y = np.sin(angle) * label_radius
        
        # Enhanced multi-line splitting for complex networks
        final_display_label = display_label
        if is_complex_network and len(display_label) > 18:  # Lower threshold for complex networks
            # More aggressive splitting for complex networks
            if '(' in display_label and ')' in display_label:
                layer_part = display_label.split('(', 1)[0]
                regions_part = '(' + display_label.split('(', 1)[1]
                # For region parts, split them into individual lines if needed
                if len(regions_part) > 25:
                    # Split each region group onto its own line
                    regions_content = regions_part[1:-1]  # Remove parentheses
                    region_groups = regions_content.split(',')
                    regions_multiline = '<br>'.join(region_groups)
                    final_display_label = f"{layer_part}<br>({regions_multiline})"
                else:
                    final_display_label = f"{layer_part}<br>{regions_part}"
            else:
                # Fallback splitting
                mid_point = len(display_label) // 2
                final_display_label = f"{display_label[:mid_point]}<br>{display_label[mid_point:]}"
        elif len(display_label) > 25:
            # Original splitting logic for non-complex networks
            if '(' in display_label and ')' in display_label:
                layer_part = display_label.split('(', 1)[0]
                regions_part = '(' + display_label.split('(', 1)[1]
                final_display_label = f"{layer_part}<br>{regions_part}"
            else:
                mid_point = len(display_label) // 2
                final_display_label = f"{display_label[:mid_point]}<br>{display_label[mid_point:]}"
        else:
            final_display_label = display_label
        
        fig.add_trace(go.Scatter(
            x=[label_x], y=[label_y],
            mode='text',
            text=[final_display_label],
            textfont=dict(size=label_font_size, color=color, family='Arial Black'),
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add chords for layer-to-layer connections with multiple artistic strings per connection
    chord_traces = []
    max_connection_strength = np.max(connection_matrix) if np.max(connection_matrix) > 0 else 1
    
    # Create multiple strings per layer connection for artistic effect
    num_strings_per_connection = 3  # Number of parallel strings per layer connection
    
    # Group chord traces by source layer for interactive highlighting
    chord_traces_by_source = {layer: [] for layer in LAYER_ORDER}
    
    for i, source_layer in enumerate(LAYER_ORDER):
        for j, target_layer in enumerate(LAYER_ORDER):
            connection_strength = connection_matrix[i, j]
            if connection_strength <= 0:
                continue
                
            source_angle = angles[i]
            target_angle = angles[j]
            source_color = get_layer_color(source_layer)
            
            # Handle self-connections (i == j) specially for loop networks
            if i == j:
                # For self-connections, create inner circular loops instead of straight chords
                # This makes loop networks much more visible and aesthetically pleasing
                
                # Create multiple concentric circular loops for self-connections
                num_self_loops = min(4, max(1, int(connection_strength / max_connection_strength * 4)))
                
                for loop_idx in range(num_self_loops):
                    # Create circles at different radii inside the main circle
                    loop_radius = 0.65 - (loop_idx * 0.08)
                    
                    # Create a full circle for self-connection
                    t_circle = np.linspace(0, 2*np.pi, 60)
                    circle_x = np.cos(t_circle + source_angle) * loop_radius
                    circle_y = np.sin(t_circle + source_angle) * loop_radius
                    
                    # Calculate width based on connection strength
                    base_width = max(1.0, min(4, (connection_strength / max_connection_strength) * 3))
                    loop_width = base_width * (0.8 + loop_idx * 0.1)
                    
                    # Get detailed statistics
                    stats = layer_connection_stats.get((source_layer, target_layer), {})
                    avg_prob = stats.get('avg_probability', 0)
                    conn_count = stats.get('connection_count', 0)
                    
                    # Create self-loop trace
                    self_loop_trace = go.Scatter(
                        x=circle_x,
                        y=circle_y,
                        mode='lines',
                        line=dict(
                            color=source_color,
                            width=loop_width,
                            shape='spline'
                        ),
                        hoverinfo='text',
                        hovertext=f"<b>{source_layer}</b> → <b>{target_layer}</b> (Self-loop)<br>"
                                 f"<span style='color:{source_color}'>●</span> Synapses: {int(connection_strength):,}<br>"
                                 f"<span style='color:{source_color}'>●</span> Connections: {conn_count}<br>"
                                 f"<span style='color:{source_color}'>●</span> Avg Probability: {avg_prob:.3f}",
                        customdata=[{'source': source_layer, 'target': target_layer}],
                        showlegend=False,
                        opacity=0.85
                    )
                    chord_traces.append(self_loop_trace)
                    chord_traces_by_source[source_layer].append(self_loop_trace)
            else:
                # Skip very weak inter-layer connections for cleaner look
                if connection_strength < max_connection_strength * 0.05:
                    continue
                
                # Create multiple parallel strings with slight angular offsets
                for string_idx in range(num_strings_per_connection):
                    # Add small angular offset for each string
                    angle_offset = (string_idx - (num_strings_per_connection - 1) / 2) * 0.02
                    
                    adjusted_source_angle = source_angle + angle_offset
                    adjusted_target_angle = target_angle + angle_offset
                    
                    # Calculate string width based on connection strength
                    base_width = max(0.8, min(3, (connection_strength / max_connection_strength) * 2.5))
                    string_width = base_width * (0.7 + string_idx * 0.15)  # Vary width slightly
                    
                    # Create bezier curve control points for artistic appearance
                    radius_inner = 0.72
                    radius_outer = 0.88
                    
                    # Source and target points on inner circle
                    x0, y0 = np.cos(adjusted_source_angle) * radius_inner, np.sin(adjusted_source_angle) * radius_inner
                    x1, y1 = np.cos(adjusted_target_angle) * radius_inner, np.sin(adjusted_target_angle) * radius_inner
                    
                    # Control points for bezier curve (create curved, organic look)
                    cx0, cy0 = np.cos(adjusted_source_angle) * radius_outer, np.sin(adjusted_source_angle) * radius_outer
                    cx1, cy1 = np.cos(adjusted_target_angle) * radius_outer, np.sin(adjusted_target_angle) * radius_outer
                    
                    # Create smooth bezier curve
                    t = np.linspace(0, 1, 40)
                    bezier_x = (1-t)**3 * x0 + 3*(1-t)**2*t * cx0 + 3*(1-t)*t**2 * cx1 + t**3 * x1
                    bezier_y = (1-t)**3 * y0 + 3*(1-t)**2*t * cy0 + 3*(1-t)*t**2 * cy1 + t**3 * y1
                    
                    # Get detailed statistics
                    stats = layer_connection_stats.get((source_layer, target_layer), {})
                    avg_prob = stats.get('avg_probability', 0)
                    conn_count = stats.get('connection_count', 0)
                    
                    # Create chord trace
                    chord_trace = go.Scatter(
                        x=bezier_x,
                        y=bezier_y,
                        mode='lines',
                        line=dict(
                            color=source_color,
                            width=string_width,
                            shape='spline'
                        ),
                        hoverinfo='text',
                        hovertext=f"<b style='font-size:16px;'>{source_layer} → {target_layer}</b><br>"
                                 f"<span style='color:{source_color}'>━━━</span> Total Synapses: <b>{int(connection_strength):,}</b><br>"
                                 f"<span style='color:{source_color}'>━━━</span> Connection Count: {conn_count}<br>"
                                 f"<span style='color:{source_color}'>━━━</span> Avg Probability: {avg_prob:.4f}",
                        customdata=[{'source': source_layer, 'target': target_layer}],
                        showlegend=False,
                        opacity=0.85
                    )
                    chord_traces.append(chord_trace)
                    chord_traces_by_source[source_layer].append(chord_trace)
    
    # Add all chord traces to figure
    for trace in chord_traces:
        fig.add_trace(trace)
    
    # Create highlight traces for each layer (for hover interaction)
    # These will be shown when hovering over any dot in a layer
    for i, source_layer in enumerate(LAYER_ORDER):
        highlight_color = get_layer_color(source_layer)
        
        # Collect all highlight elements (both inter-layer chords and self-loops)
        layer_highlight_x = []
        layer_highlight_y = []
        
        for j, target_layer in enumerate(LAYER_ORDER):
            connection_strength = connection_matrix[i, j]
            if connection_strength <= 0:
                continue
                
            # Handle self-connections for highlighting
            if i == j:
                # Create prominent self-loop for highlighting
                if connection_strength > 0:
                    source_angle = angles[i]
                    # Create 2-3 thick concentric circles for self-loop highlighting
                    num_highlight_loops = min(3, max(1, int(connection_strength / max_connection_strength * 3)))
                    
                    for loop_idx in range(num_highlight_loops):
                        loop_radius = 0.68 - (loop_idx * 0.1)
                        t_circle = np.linspace(0, 2*np.pi, 60)
                        circle_x = np.cos(t_circle + source_angle) * loop_radius
                        circle_y = np.sin(t_circle + source_angle) * loop_radius
                            
                        layer_highlight_x.extend(circle_x.tolist())
                        layer_highlight_y.extend(circle_y.tolist())
                        layer_highlight_x.append(None)
                        layer_highlight_y.append(None)
            else:
                # Skip very weak inter-layer connections for highlighting
                if connection_strength < max_connection_strength * 0.05:
                    continue
                    
                source_angle = angles[i]
                target_angle = angles[j]
                    
                # Create multiple highlight strings (thicker and more prominent)
                num_highlight_strings = 2
                for string_idx in range(num_highlight_strings):
                    angle_offset = (string_idx - (num_highlight_strings - 1) / 2) * 0.03
                        
                    adjusted_source_angle = source_angle + angle_offset
                    adjusted_target_angle = target_angle + angle_offset
                        
                    radius_inner = 0.72
                    radius_outer = 0.88
                        
                    x0, y0 = np.cos(adjusted_source_angle) * radius_inner, np.sin(adjusted_source_angle) * radius_inner
                    x1, y1 = np.cos(adjusted_target_angle) * radius_inner, np.sin(adjusted_target_angle) * radius_inner
                    cx0, cy0 = np.cos(adjusted_source_angle) * radius_outer, np.sin(adjusted_source_angle) * radius_outer
                    cx1, cy1 = np.cos(adjusted_target_angle) * radius_outer, np.sin(adjusted_target_angle) * radius_outer
                        
                    t = np.linspace(0, 1, 40)
                    bezier_x = (1-t)**3 * x0 + 3*(1-t)**2*t * cx0 + 3*(1-t)*t**2 * cx1 + t**3 * x1
                    bezier_y = (1-t)**3 * y0 + 3*(1-t)**2*t * cy0 + 3*(1-t)*t**2 * cy1 + t**3 * y1
                        
                    layer_highlight_x.extend(bezier_x.tolist())
                    layer_highlight_y.extend(bezier_y.tolist())
                    # Add None to separate different chords
                    layer_highlight_x.append(None)
                    layer_highlight_y.append(None)
            
            if layer_highlight_x:
                # Remove the last None separator
                layer_highlight_x = layer_highlight_x[:-1]
                layer_highlight_y = layer_highlight_y[:-1]
                
                highlight_trace = go.Scatter(
                    x=layer_highlight_x,
                    y=layer_highlight_y,
                    mode='lines',
                    line=dict(
                        color=highlight_color,
                        width=6,  # Thicker for highlighting
                        shape='spline'
                    ),
                    name=f'From {source_layer}',
                    visible=False,  # Hidden by default, shown on hover
                    showlegend=False,
                    hoverinfo='skip'
                )
                fig.add_trace(highlight_trace)
    
    # Update layout with professional styling
    # Determine if this is a complex multi-region network
    is_complex_network = network_type == 'multi' and region_data and len(region_data) >= 3
    
    if is_complex_network:
        # Larger figure size and expanded axis range for complex networks
        fig_width = 1200
        fig_height = 1200
        axis_range = [-1.6, 1.6]
        margin_config = dict(l=80, r=80, t=120, b=80)
    else:
        # Default sizing for simple networks
        fig_width = 1000
        fig_height = 1000
        axis_range = [-1.4, 1.4]
        margin_config = dict(l=50, r=50, t=100, b=50)
    
    fig.update_layout(
        title={
            'text': f"Layer-to-Layer Connectivity Network<br><sub>{network_name} • Interactive String Graph</sub>",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'family': 'Arial Black'}
        },
        width=fig_width,
        height=fig_height,
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=axis_range,
            constrain='domain'
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            range=axis_range,
            constrain='domain'
        ),
        showlegend=False,
        margin=margin_config,
        font=dict(family='Arial', size=12)
    )
    
    return fig

def is_connection_valid_for_network(connection_data, network_name, network_type, regions_list):
    """
    Validate if a connection is appropriate for the given network type based on model construction rules.
    
    For pure M2 networks (M2, M2a, M2b as single regions), only allow connections to TCs_matrix and TCs_intralaminar,
    NOT to TCs_core (which contains TCRc, nRTc, nRT).
    
    For compound networks containing M2 plus other regions (like M2M1S1, M2aM1aS1a, S1bM1bM2b), 
    allow all connections since other regions (S1, M1) can have TCRc/nRTc connections.
    
    For iT networks, only allow thalamic connections (no cortical layers).
    """
    # Define thalamic layer groups
    TCs_core_types = {'TCRc', 'nRTc', 'nRT'}
    TCs_matrix_types = {'TCR', 'TCRm', 'nRTm'}
    TCs_intralaminar_types = {'TCRil', 'nRTil'}
    
    # Check if this is a pure M2 network (single region starting with M2)
    is_pure_m2_network = (
        len(regions_list) == 1 and 
        regions_list[0].startswith('M2')
    )
    
    if is_pure_m2_network:
        source_layer = connection_data.get('source_layer')
        target_layer = connection_data.get('target_layer')
        source_type = connection_data.get('source_type')
        target_type = connection_data.get('target_type')
        
        # For pure M2 networks, reject any connections involving TCs_core
        if source_type in TCs_core_types or target_type in TCs_core_types:
            return False
        
        # Also check layer-based rejection (though types should be sufficient)
        if source_layer == 'TCs_core' or target_layer == 'TCs_core':
            return False
    
    # For iT networks, only allow thalamic connections (no cortical layers)
    is_it_network = any('iT' in region for region in regions_list) or 'iT' in network_name
    if is_it_network:
        # iT networks should only have thalamic-to-thalamic connections
        cortical_layers = {'L1', 'L23', 'L4', 'L5', 'L6'}
        source_layer = connection_data.get('source_layer')
        target_layer = connection_data.get('target_layer')
        
        if (source_layer in cortical_layers) or (target_layer in cortical_layers):
            return False
    
    return True


def identify_network_regions(network_name):
    """
    Identify regions from network name by reading the actual region JSON file in net_params directory.
    This provides accurate single vs multi-region detection based on real data.
    
    Returns:
        tuple: (network_type, regions_list) where network_type is 'single' or 'multi'
    """
    # Construct the path to the region JSON file
    net_params_dir = os.path.join(os.path.dirname(__file__), 'net_params')
    network_dir = os.path.join(net_params_dir, network_name)
    region_json_file = os.path.join(network_dir, f'extracted_{network_name}_region.json')
    
    # Check if the region JSON file exists
    if os.path.exists(region_json_file):
        try:
            with open(region_json_file, 'r') as f:
                region_data = json.load(f)
            
            # Get the top-level region keys
            regions = list(region_data.keys())
            
            if len(regions) == 1:
                return 'single', regions
            elif len(regions) > 1:
                return 'multi', regions
            else:
                # Empty region file - fallback to network name
                return 'single', [network_name]
                
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Could not read region file {region_json_file}: {e}")
            # Fallback to network name-based detection
            pass
    
    # Fallback logic for cases where region JSON doesn't exist or can't be read
    # Handle special cases first
    if network_name == 'iT_max_plus':
        return 'single', ['iT']
    elif network_name == 'loop_iT_max_plus':
        return 'multi', ['M2a', 'M2b', 'M1a', 'M1b', 'S1a', 'S1b']
    elif network_name == 'iC_max':
        return 'single', ['iC']
    elif network_name.startswith('loop_'):
        # Loop networks are typically multi-region
        base_name = network_name.replace('loop_', '')
        if base_name in ['L1', 'L23', 'L4', 'L5', 'L6']:
            return 'single', [base_name]
        else:
            # Try to extract regions from the name
            regions = extract_regions_from_name(base_name)
            if len(regions) > 1:
                return 'multi', regions
            else:
                return 'single', regions
    
    # Extract regions from network name using pattern recognition
    regions = extract_regions_from_name(network_name)
    
    if len(regions) == 1:
        return 'single', regions
    elif len(regions) > 1:
        return 'multi', regions
    else:
        # Fallback: try to infer from common patterns
        if '_max_plus' in network_name:
            base_part = network_name.replace('_max_plus', '')
            # Check if base_part is a known multi-region prefix
            if base_part in ['M1', 'M2', 'S1']:
                return 'multi', [f"{base_part}a", f"{base_part}b"]
            elif base_part == 'M2M1S1':
                return 'multi', ['M2', 'M1', 'S1']
            elif base_part == 'M2aM1aS1a':
                return 'multi', ['M2a', 'M1a', 'S1a']
            elif base_part == 'S1bM1bM2b':
                return 'multi', ['S1b', 'M1b', 'M2b']
            elif base_part == 'TC2IT2PTCT':
                return 'multi', ['TC', 'IT', 'PT', 'CT']
            elif base_part == 'TC2IT4_IT2CT':
                return 'multi', ['TC', 'IT4', 'IT', 'CT']
            elif base_part == 'TC2PT':
                return 'multi', ['TC', 'PT']
        
        # Default to single region with the network name
        return 'single', [network_name]

def extract_regions_from_name(network_name):
    """
    Extract potential region names from network name using regex patterns.
    """
    regions = []
    
    # Remove common suffixes
    clean_name = network_name
    for suffix in ['_max_plus', '_max', '_plus', '_max+']:
        clean_name = clean_name.replace(suffix, '')
    
    # Handle concatenated region names (like M2M1S1, M2aM1aS1a, etc.)
    if re.match(r'^[A-Z]\d+[a-zA-Z]*$', clean_name):
        # Single region (e.g., M1, S1a, TC2)
        regions = [clean_name]
    elif re.match(r'^([A-Z]\d+[a-zA-Z]*)([A-Z]\d+[a-zA-Z]*)+$', clean_name):
        # Multiple concatenated regions - split them
        # This is tricky, so use known patterns
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
        else:
            # Try to split by capital letters followed by numbers
            parts = re.findall(r'[A-Z][a-z]*\d+[a-zA-Z]*', clean_name)
            if parts:
                regions = parts
            else:
                regions = [clean_name]
    else:
        regions = [clean_name]
    
    return regions

def create_interactive_layer_string_graph(network_name, use_cell_type_mode=False):
    """Main function to create simplified layer string graph visualization."""
    logger.info(f"Loading network data for: {network_name}")
    
    try:
        anatomy_data, circuit_data, physiology_data = load_network_data(network_name)
    except FileNotFoundError as e:
        logger.error(str(e))
        return
    
    # Identify network type (single vs multi-region) FIRST, before filtering connections
    network_type, regions_list = identify_network_regions(network_name)
    
    # Parse all connection keys and collect m-types per layer (for dots only)
    # Apply network-type-specific filtering based on model construction rules
    parsed_connections = []
    layer_mtypes = {layer: set() for layer in LAYER_ORDER}
    
    for connection_key in anatomy_data.keys():
        parsed_conn = parse_connection_key(connection_key)
        if parsed_conn:
            # Validate connection against network type rules
            if is_connection_valid_for_network(parsed_conn, network_name, network_type, regions_list):
                parsed_connections.append(parsed_conn)
                # Collect m-types for each layer (for creating dots)
                layer_mtypes[parsed_conn['source_layer']].add(parsed_conn['source_type'])
                layer_mtypes[parsed_conn['target_layer']].add(parsed_conn['target_type'])
            else:
                logger.debug(f"Filtered out invalid connection for {network_name}: {connection_key}")
    
    logger.info(f"Parsed {len(parsed_connections)} valid connections (filtered inappropriate ones)")
    
    # Create layer connection matrix
    connection_matrix, connection_count_matrix, layer_connection_stats = create_layer_connection_matrix(
        parsed_connections, anatomy_data
    )
    
    # Load region data for m-type to region mapping in multi-region networks
    region_data = {}
    if network_type == 'multi':
        net_params_dir = os.path.join(os.path.dirname(__file__), 'net_params')
        network_dir = os.path.join(net_params_dir, network_name)
        region_json_file = os.path.join(network_dir, f'extracted_{network_name}_region.json')
        
        if os.path.exists(region_json_file):
            try:
                with open(region_json_file, 'r') as f:
                    region_data = json.load(f)
            except (ValueError, IOError) as e:  # Use ValueError instead of json.JSONDecodeError
                logger.warning(f"Could not read region file {region_json_file}: {e}")
    
    # Create simplified string graph with m-type dots but layer-to-layer chords
    logger.info("Creating layer-to-layer string graph visualization...")
    fig = create_layer_string_graph(connection_matrix, connection_count_matrix, layer_connection_stats, network_name, layer_mtypes, network_type, regions_list, region_data, parsed_connections)
    
    # Calculate statistics for sidebar directly to avoid numpy formatting issues
    total_connections = int(np.sum(connection_count_matrix))
    total_synapses = int(np.sum(connection_matrix))
    layers_with_data = []
    for i, layer in enumerate(LAYER_ORDER):
        outgoing = int(np.sum(connection_matrix[i, :]))
        incoming = int(np.sum(connection_matrix[:, i]))
        if outgoing > 0 or incoming > 0:
            layers_with_data.append(layer)
    active_layers = len(layers_with_data)
    
    # Convert figure to HTML string
    import plotly.io as pio
    plot_html = pio.to_html(fig, include_plotlyjs=True, full_html=False)
    
    # Create JSON-serializable layer colors and order for JavaScript
    layer_colors_json = json.dumps(LAYER_COLORS)
    layer_order_json = json.dumps(LAYER_ORDER)
    
    # Identify network type (single vs multi-region)
    network_type, regions_list = identify_network_regions(network_name)
    
    # Build sidebar content with network type information
    sidebar_content = f"""
            <h3>Network Data Summary</h3>
            <p><b>Network:</b> {network_name}</p>
            <p><b style="color: {'#27ae60' if network_type == 'single' else '#2980b9'}">Type:</b> <span style="background-color: {'#d5f5e3' if network_type == 'single' else '#d6eaf8'}; padding: 2px 6px; border-radius: 4px;">{network_type.title()} Region{'s' if network_type == 'multi' else ''}</span></p>
            <p><b>Regions:</b> {', '.join(regions_list)}</p>
            <p><b>Total Connections:</b> {total_connections:,}</p>
            <p><b>Total Synapses:</b> {total_synapses:,}</p>
            <p><b>Active Layers:</b> {active_layers}/7 ({', '.join(layers_with_data) if layers_with_data else 'None'})</p>
            
            <h4>Layer Connections</h4>
    """
    
    for i, source_layer in enumerate(LAYER_ORDER):
        outgoing_conns = int(np.sum(connection_count_matrix[i, :]))
        outgoing_synapses = int(np.sum(connection_matrix[i, :]))
        if outgoing_conns > 0:
            sidebar_content += f'            <p><b>{source_layer}:</b> {outgoing_conns:,} connections, {outgoing_synapses:,} synapses</p>\n'
    
    sidebar_content += """
            <h4>Cell Types (M-types)</h4>
    """
    
    if layer_mtypes:
        total_mtypes = 0
        for layer, mtypes in layer_mtypes.items():
            if mtypes:
                total_mtypes += len(mtypes)
                mtype_list = sorted(list(mtypes))
                display_mtypes = mtype_list[:3]
                if len(mtype_list) > 3:
                    display_mtypes.append(f"... (+{len(mtype_list)-3} more)")
                sidebar_content += f'            <p><b>{layer}:</b> {len(mtypes)} types ({", ".join(display_mtypes)})</p>\n'
        sidebar_content += f'            <p><b>Total M-types:</b> {total_mtypes}</p>\n'

    # Create complete HTML with sidebar - update title to include network type
    network_type_display = f"({network_type.title()} Region{'s' if network_type == 'multi' else ''})"
    complete_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Layer String Graph - {network_name} {network_type_display}</title>
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
    <script>
        // Layer configuration from Python
        const LAYER_COLORS = {layer_colors_json};
        const LAYER_ORDER = {layer_order_json};
        
        console.log('Layer Colors:', LAYER_COLORS);
        console.log('Layer Order:', LAYER_ORDER);
    </script>
</body>
</html>
"""
    
    # Save visualization
    output_dir = Path("html")
    output_dir.mkdir(exist_ok=True)
    html_file = output_dir / f"layer_string_graph_{network_name}.html"
    
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(complete_html)
    
    # Add custom JavaScript for dynamic arc and chord highlighting on hover
    add_dynamic_layer_highlighting(html_file, LAYER_ORDER)
    
    logger.info(f"Layer string graph visualization saved to: {html_file}")

def add_dynamic_layer_highlighting(html_file, layer_order):
    """Add custom JavaScript to enable dynamic highlighting of arcs and chords on hover."""
    import json
    
    # Read the existing HTML file
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Custom JavaScript for dynamic highlighting - Use customdata for robust mapping with variable dot traces
    layer_order_json = json.dumps(LAYER_ORDER)
    
    js_code = '<script>\n'
    js_code += '// Dynamic layer highlighting on hover - Use customdata for robust mapping with variable dot traces\n'
    js_code += '(function() {\n'
    js_code += f'    const LAYER_ORDER = {layer_order_json};\n'
    js_code += '    const plotContainer = document.getElementById("plot-container");\n'
    js_code += '    let currentHighlightedLayer = null;\n'
    js_code += '    let plotDiv = null;\n'
    js_code += '    \n'
    js_code += '    // Wait for Plotly to be ready\n'
    js_code += '    function waitForPlotly() {\n'
    js_code += '        if (!plotContainer) return;\n'
    js_code += '        plotDiv = plotContainer.querySelector(".plotly-graph-div");\n'
    js_code += '        if (typeof Plotly !== \'undefined\' && plotDiv && plotDiv.data && plotDiv.data.length > 0) {\n'
    js_code += '            initializeHighlighting(plotDiv);\n'
    js_code += '        } else {\n'
    js_code += '            setTimeout(waitForPlotly, 100);\n'
    js_code += '        }\n'
    js_code += '    }\n'
    js_code += '    \n'
    js_code += '    function initializeHighlighting(plotDiv) {\n'
    js_code += f'        const LAYER_ORDER = {layer_order_json};\n'
    js_code += '        const totalTraces = plotDiv.data.length;\n'
    js_code += '        \n'
    js_code += '        // Scan all traces to build mappings based on customdata and trace properties\n'
    js_code += '        const layerDotTraces = {};\n'
    js_code += '        const highlightTraceMap = {};\n'
    js_code += '        const baseChordTraces = [];\n'
    js_code += '        \n'
    js_code += '        // Initialize layer mappings\n'
    js_code += '        LAYER_ORDER.forEach(layerName => {\n'
    js_code += '            layerDotTraces[layerName] = [];\n'
    js_code += '        });\n'
    js_code += '        \n'
    js_code += '        // Scan all traces to categorize them\n'
    js_code += '        for (let i = 0; i < totalTraces; i++) {\n'
    js_code += '            const trace = plotDiv.data[i];\n'
    js_code += '            \n'
    js_code += '            // Check if this is a highlight trace (has name starting with "From " and visible=False initially)\n'
    js_code += '            if (trace.name && trace.name.startsWith(\'From \')) {\n'
    js_code += '                const layerName = trace.name.substring(5);\n'
    js_code += '                if (LAYER_ORDER.includes(layerName)) {\n'
    js_code += '                    highlightTraceMap[layerName] = i;\n'
    js_code += '                    continue;\n'
    js_code += '                }\n'
    js_code += '            }\n'
    js_code += '            \n'
    js_code += '            // Check if this is a base chord trace (has customdata with source/target)\n'
    js_code += '            if (trace.customdata && Array.isArray(trace.customdata) && \n'
    js_code += '                trace.customdata.length > 0 && \n'
    js_code += '                typeof trace.customdata[0] === \'object\' && \n'
    js_code += '                trace.customdata[0].hasOwnProperty(\'source\')) {\n'
    js_code += '                baseChordTraces.push(i);\n'
    js_code += '                continue;\n'
    js_code += '            }\n'
    js_code += '            \n'
    js_code += '            // Check if this is a dot trace (has customdata with layer name)\n'
    js_code += '            if (trace.customdata && Array.isArray(trace.customdata) && \n'
    js_code += '                trace.customdata.length > 0 && \n'
    js_code += '                typeof trace.customdata[0] === \'string\' && \n'
    js_code += '                LAYER_ORDER.includes(trace.customdata[0])) {\n'
    js_code += '                const layerName = trace.customdata[0];\n'
    js_code += '                layerDotTraces[layerName].push(i);\n'
    js_code += '                continue;\n'
    js_code += '            }\n'
    js_code += '        }\n'
    js_code += '        \n'
    js_code += '        console.log(\'Highlight trace map:\', highlightTraceMap);\n'
    js_code += '        console.log(\'Base chord traces count:\', baseChordTraces.length);\n'
    js_code += '        \n'
    js_code += '        // Add hover event listener\n'
    js_code += '        plotDiv.on(\'plotly_hover\', function(data) {\n'
    js_code += '            const customData = data.points[0].data.customdata;\n'
    js_code += '            let layerName = null;\n'
    js_code += '            \n'
    js_code += '            // Extract layer name from customdata\n'
    js_code += '            if (Array.isArray(customData) && customData.length > 0) {\n'
    js_code += '                layerName = customData[0];\n'
    js_code += '            }\n'
    js_code += '            \n'
    js_code += '            if (layerName && highlightTraceMap.hasOwnProperty(layerName)) {\n'
    js_code += '                // Hide all base chords during highlighting\n'
    js_code += '                if (baseChordTraces.length > 0) {\n'
    js_code += '                    Plotly.restyle(plotDiv, {\'visible\': false}, baseChordTraces);\n'
    js_code += '                }\n'
    js_code += '                \n'
    js_code += '                // Show highlight chords for this layer\n'
    js_code += '                const highlightTraceIdx = highlightTraceMap[layerName];\n'
    js_code += '                Plotly.restyle(plotDiv, {\'visible\': true}, [highlightTraceIdx]);\n'
    js_code += '                \n'
    js_code += '                currentHighlightedLayer = layerName;\n'
    js_code += '            }\n'
    js_code += '        });\n'
    js_code += '        \n'
    js_code += '        // Add unhover event listener\n'
    js_code += '        plotDiv.on(\'plotly_unhover\', function(data) {\n'
    js_code += '            if (currentHighlightedLayer) {\n'
    js_code += '                // Show all base chords again\n'
    js_code += '                if (baseChordTraces.length > 0) {\n'
    js_code += '                    Plotly.restyle(plotDiv, {\'visible\': true}, baseChordTraces);\n'
    js_code += '                }\n'
    js_code += '                \n'
    js_code += '                // Hide highlight chords\n'
    js_code += '                const highlightTraceIdx = highlightTraceMap[currentHighlightedLayer];\n'
    js_code += '                Plotly.restyle(plotDiv, {\'visible\': false}, [highlightTraceIdx]);\n'
    js_code += '                \n'
    js_code += '                currentHighlightedLayer = null;\n'
    js_code += '            }\n'
    js_code += '        });\n'
    js_code += '    }\n'
    js_code += '    \n'
    js_code += '    // Start initialization\n'
    js_code += '    waitForPlotly();\n'
    js_code += '})();\n'
    js_code += '</script>\n'
    
    # Insert the JavaScript before the closing </body> tag
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', js_code + '\n</body>')
    else:
        # If no body tag, append to end
        html_content += js_code
    
    # Write back to file
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"Added dynamic layer highlighting to: {html_file}")

def main():
    """Command line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create simplified layer-to-layer string graph visualizations")
    parser.add_argument("--network", type=str, default="max_CTC_plus",
                        help="Network name to visualize (default: max_CTC_plus)")
    parser.add_argument("--all", action="store_true",
                        help="Process all networks in net_params directory")
    parser.add_argument("--cell-type-mode", action="store_true",
                        help="Enable cell type level visualization (layer_celltype to layer_celltype)")
    
    args = parser.parse_args()
    
    if args.all:
        # Process all networks
        net_params_dir = Path("net_params")
        if net_params_dir.exists():
            networks = [d.name for d in net_params_dir.iterdir() if d.is_dir()]
            logger.info(f"Processing {len(networks)} networks...")
            for network in networks:
                try:
                    create_interactive_layer_string_graph(network, use_cell_type_mode=args.cell_type_mode)
                except Exception as e:
                    logger.error(f"Error processing {network}: {e}")
        else:
            logger.error("net_params directory not found!")
    else:
        # Process single network
        create_interactive_layer_string_graph(args.network, use_cell_type_mode=args.cell_type_mode)

if __name__ == "__main__":
    main()