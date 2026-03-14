#!/usr/bin/env python3
"""
Analysis and plotting tool for network datasets.

This module provides functions for analyzing and visualizing neural network data,
including violin plots, heatmaps, and scatter plots.
"""

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # use non-interactive backend for headless servers
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from pathlib import Path
import json


def _maybe_log(df, cols, use_log=True):
    """Apply log transformation to data if requested."""
    if not use_log:
        return df[cols].copy()
    return np.log1p(df[cols].replace([np.inf, -np.inf], np.nan)).fillna(0)


def _make_outpath(outpath, basename):
    """Create output path with basename if provided."""
    from pathlib import Path
    p = Path(outpath)
    if basename:
        # Check if the path already contains the basename to avoid duplication
        path_str = str(p)
        if basename not in path_str:
            p = p.with_name(f"{basename}_{p.name}")
    p.parent.mkdir(parents=True, exist_ok=True)
    return str(p)


def load_dataset(basename, indir="analysis_out"):
    """
    Load dataset from previously saved files in the analysis_out directory.
    
    Parameters:
      - basename: base name used when saving the files (required)
      - indir: directory where files are stored
      
    Returns:
      dict with keys: pops_df, pop_stats_df, summary
    """
    indir = Path(indir)
    
    # Load CSV files
    pops_df = pd.read_csv(indir / f"{basename}_populations.csv", index_col="pop_id")
    pop_stats_df = pd.read_csv(indir / f"{basename}_population_stats.csv", index_col="pop_id")
    
    # Load JSON summary
    with open(indir / f"{basename}_summary.json", "r") as fh:
        summary = json.load(fh)
        
    dataset = {
        "pops_df": pops_df,
        "pop_stats_df": pop_stats_df,
        "summary": summary
    }
    return dataset


def find_available_datasets(indir="analysis_out"):
    """
    Find all available datasets in the directory by looking for population CSV files.
    
    Parameters:
      - indir: directory to search for datasets
      
    Returns:
      list of available dataset basenames
    """
    indir = Path(indir)
    csv_files = indir.glob("*_populations.csv")
    basenames = [f.name.replace("_populations.csv", "") for f in csv_files]
    return basenames


def plot_connection_type_violins(pop_stats_df,
                                 outpath="plots/summary_connection_violins.png",
                                 use_log=True,
                                 basename=None):
    """
    Plot violin plots for different connection types.
    
    Parameters:
      - pop_stats_df: DataFrame with population statistics
      - outpath: output path for the plot
      - use_log: whether to use log scale
      - basename: base name for the plot
    """
    # Apply log transformation if requested
    df = pop_stats_df.copy()
    
    # Define connection types to plot
    cols = [
        'syn_ee_contacts', 'syn_ei_contacts', 'syn_ie_contacts', 'syn_ii_contacts',
        'ele_ee_conductances', 'ele_ii_conductances'
    ]
    
    # Filter columns that exist in the dataframe
    existing_cols = [col for col in cols if col in df.columns]
    if not existing_cols:
        # Try alternative column names for network-level data
        alt_cols = ['cont_out', 'cont_in', 'elec_out', 'elec_in', 'exc_inputs', 'inh_inputs']
        existing_cols = [col for col in alt_cols if col in df.columns]
        if not existing_cols:
            print(f"Warning: No valid connection columns found in DataFrame. Available columns: {list(df.columns)}")
            return
    
    # Apply log transformation if requested
    plot_data = _maybe_log(df, existing_cols, use_log)
    
    # Create figure with subplots
    n_cols = len(existing_cols)
    n_rows = (n_cols + 2) // 3  # 3 columns per row
    fig, axes = plt.subplots(n_rows, 3, figsize=(15, 5 * n_rows))
    if n_rows == 1:
        axes = [axes] if n_cols <= 3 else axes.flatten()
    else:
        axes = axes.flatten()
    
    # Plot each connection type
    for i, col in enumerate(existing_cols):
        ax = axes[i]
        sns.violinplot(y=plot_data[col], ax=ax)
        ax.set_title(col.replace('_', ' ').title())
        ax.set_ylabel('Log(Connections)' if use_log else 'Connections')
    
    # Remove any unused subplots
    for i in range(len(existing_cols), len(axes)):
        fig.delaxes(axes[i])
    
    plt.tight_layout()
    
    # Save plot
    final_path = _make_outpath(outpath, basename)
    plt.savefig(final_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved connection type violin plots to {final_path}")


def plot_clustered_heatmap(pop_stats_df, cols=None, outpath="plots/clustermap.png", 
                           use_log=True, basename=None):
    """
    Plot clustered heatmap of correlation matrix.
    
    Parameters:
      - pop_stats_df: DataFrame with population statistics
      - cols: columns to include in heatmap (if None, use defaults)
      - outpath: output path for the plot
      - use_log: whether to use log scale
      - basename: base name for the plot
    """
    df = pop_stats_df.copy()
    
    # Default columns if none provided
    if cols is None:
        default_cols = [
            'syn_ee_contacts', 'syn_ei_contacts', 'syn_ie_contacts', 'syn_ii_contacts',
            'ele_ee_conductances', 'ele_ii_conductances'
        ]
        # Filter to only existing columns
        cols = [col for col in default_cols if col in df.columns]
        if not cols:
            # Try alternative columns for network-level data
            alt_cols = ['cont_out', 'cont_in', 'elec_out', 'elec_in', 'exc_inputs', 'inh_inputs']
            cols = [col for col in alt_cols if col in df.columns]
    
    if not cols:
        print(f"Warning: No valid columns found for heatmap. Available columns: {list(df.columns)}")
        return
    
    # Apply log transformation if requested
    plot_data = _maybe_log(df, cols, use_log)
    
    # Calculate correlation matrix
    corr_matrix = plot_data.corr()
    
    # Create clustered heatmap
    plt.figure(figsize=(max(8, len(cols) * 1.5), max(8, len(cols) * 1.5)))
    sns.clustermap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, fmt='.2f')
    plt.title('Clustered Correlation Heatmap')
    
    # Save plot
    final_path = _make_outpath(outpath, basename)
    plt.savefig(final_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved clustered heatmap to {final_path}")


def plot_combined_heatmaps(pop_stats_df, cols=None, outpath="plots/combined_heatmaps.png", 
                           use_log=True, basename=None):
    """
    Plot combined heatmaps showing correlation matrices.
    
    Parameters:
      - pop_stats_df: DataFrame with population statistics
      - cols: columns to include in heatmap (if None, use defaults)
      - outpath: output path for the plot
      - use_log: whether to use log scale
      - basename: base name for the plot
    """
    df = pop_stats_df.copy()
    
    # Default columns if none provided
    if cols is None:
        default_cols = [
            'syn_ee_contacts', 'syn_ei_contacts', 'syn_ie_contacts', 'syn_ii_contacts',
            'ele_ee_conductances', 'ele_ii_conductances'
        ]
        # Filter to only existing columns
        cols = [col for col in default_cols if col in df.columns]
        if not cols:
            # Try alternative columns for network-level data
            alt_cols = ['cont_out', 'cont_in', 'elec_out', 'elec_in', 'exc_inputs', 'inh_inputs']
            cols = [col for col in alt_cols if col in df.columns]
    
    if not cols:
        print(f"Warning: No valid columns found for heatmaps. Available columns: {list(df.columns)}")
        return
    
    # Apply log transformation if requested
    plot_data = _maybe_log(df, cols, use_log)
    
    # Calculate correlation matrix
    corr_matrix = plot_data.corr()
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Plot correlation heatmap
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                square=True, fmt='.2f', ax=ax1)
    ax1.set_title('Correlation Matrix')
    
    # Plot absolute correlation heatmap
    abs_corr_matrix = corr_matrix.abs()
    sns.heatmap(abs_corr_matrix, annot=True, cmap='Reds', square=True, 
                fmt='.2f', ax=ax2)
    ax2.set_title('Absolute Correlation Matrix')
    
    plt.tight_layout()
    
    # Save plot
    final_path = _make_outpath(outpath, basename)
    plt.savefig(final_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved combined heatmaps to {final_path}")


def plot_ei_scatter_with_stacked(pop_stats_df,
                                 outpath="plots/ei_with_stacked.png",
                                 use_log=True,
                                 basename=None):
    """
    Plot E/I ratio scatter plot with stacked bars.
    
    Parameters:
      - pop_stats_df: DataFrame with population statistics
      - outpath: output path for the plot
      - use_log: whether to use log scale
      - basename: base name for the plot
    """
    df = pop_stats_df.copy()
    
    # Check which columns are available for E/I calculation
    if all(col in df.columns for col in ['syn_ee_contacts', 'syn_ei_contacts', 'syn_ie_contacts', 'syn_ii_contacts']):
        # Population-level data format
        df['E_ratio'] = (df['syn_ee_contacts'] + df['syn_ie_contacts']) / (df['syn_ei_contacts'] + df['syn_ii_contacts'])
        df['I_ratio'] = (df['syn_ei_contacts'] + df['syn_ii_contacts']) / (df['syn_ee_contacts'] + df['syn_ie_contacts'])
    elif all(col in df.columns for col in ['exc_inputs', 'inh_inputs']):
        # Network-level data format
        df['E_ratio'] = df['exc_inputs'] / df['inh_inputs']
        df['I_ratio'] = df['inh_inputs'] / df['exc_inputs']
    else:
        print(f"Warning: Cannot calculate E/I ratios. Available columns: {list(df.columns)}")
        return
    
    # Handle infinite values
    df['E_ratio'] = df['E_ratio'].replace([np.inf, -np.inf], np.nan).fillna(0)
    df['I_ratio'] = df['I_ratio'].replace([np.inf, -np.inf], np.nan).fillna(0)
    
    # Apply log transformation if requested
    plot_cols = ['E_ratio', 'I_ratio']
    plot_data = _maybe_log(df, plot_cols, use_log)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create stacked bar chart
    x = range(len(df))
    ax.bar(x, plot_data['E_ratio'], label='E Ratio', alpha=0.7)
    ax.bar(x, plot_data['I_ratio'], bottom=plot_data['E_ratio'], label='I Ratio', alpha=0.7)
    
    ax.set_xlabel('Population/Network')
    ax.set_ylabel('Log(Ratio)' if use_log else 'Ratio')
    ax.set_title('E/I Ratios Across Populations/Networks')
    ax.legend()
    
    # Set x-axis labels
    ax.set_xticks(x)
    ax.set_xticklabels(df.index, rotation=45, ha='right')
    
    plt.tight_layout()
    
    # Save plot
    final_path = _make_outpath(outpath, basename)
    plt.savefig(final_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Saved E/I scatter plot with stacked bars to {final_path}")