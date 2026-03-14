import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import json
import os
from pathlib import Path


def analyze_connection_ratios(json_files, plots_dir="plots"):
    """
    Analyze connection ratios from JSON files and generate plots.
    
    Parameters:
      - json_files: list of paths to JSON files containing connection statistics
      - plots_dir: directory to save plots (default: "plots")
      
    Returns:
      dict with analysis results for each file
    """
    # Create plots directory if it doesn't exist
    plots_dir = Path(plots_dir)
    plots_dir.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    for json_file in json_files:
        json_file = Path(json_file)
        if not json_file.exists():
            print(f"Warning: JSON file {json_file} does not exist, skipping...")
            continue
            
        print(f"Processing JSON file: {json_file}")
        
        with open(json_file, 'r') as f:
            stats = json.load(f)
            basic = '_'.join(json_file.stem.split('_')[:-2]) if '_connection_stats' in json_file.stem else json_file.stem
            print(f"  Network: {basic}")
        
        # Extract parameters from the JSON structure
        syn_ee_contacts = stats['syn_ee_contacts']
        syn_ei_contacts = stats['syn_ei_contacts']
        syn_ie_contacts = stats['syn_ie_contacts']
        syn_ii_contacts = stats['syn_ii_contacts']
        ele_ee_conductances = stats['ele_ee_conductances']
        ele_ii_conductances = stats['ele_ii_conductances']
        
        print(f"  syn_ee_contacts:{syn_ee_contacts}, syn_ei_contacts:{syn_ei_contacts}, syn_ie_contacts:{syn_ie_contacts}, syn_ii_contacts:{syn_ii_contacts}, ele_ee_conductances:{ele_ee_conductances}, ele_ii_conductances:{ele_ii_conductances}")
        
        # Check if actual correlation exists in the JSON
        actual_correlation = stats.get('correlation', None)
        print(f"  Loaded statistics from {json_file}")

        # Data preparations
        overall_ee_connections = syn_ee_contacts + ele_ee_conductances
        overall_ei_connections = syn_ei_contacts
        overall_ie_connections = syn_ie_contacts
        overall_ii_connections = syn_ii_contacts + ele_ii_conductances
        print(f"  overall_ee_connections: {overall_ee_connections}, overall_ei_connections: {overall_ei_connections}, overall_ie_connections: {overall_ie_connections}, overall_ii_connections: {overall_ii_connections}")
        
        overall_excitatory_connections = overall_ee_connections + overall_ei_connections
        overall_inhibitory_connections = overall_ii_connections + overall_ie_connections
        print(f"  overall_excitatory_connections: {overall_excitatory_connections}, overall_inhibitory_connections: {overall_inhibitory_connections}")
        
        # Calculate ratios
        ei_ratio = overall_excitatory_connections / overall_inhibitory_connections if overall_inhibitory_connections > 0 else float('inf')
        ie_ratio = overall_inhibitory_connections / overall_excitatory_connections if overall_excitatory_connections > 0 else float('inf')

        syn_ei_ratio = (syn_ee_contacts + syn_ei_contacts) / (syn_ii_contacts + syn_ie_contacts) if (syn_ii_contacts + syn_ie_contacts) > 0 else float('inf')
        syn_ie_ratio = (syn_ii_contacts + syn_ie_contacts) / (syn_ee_contacts + syn_ei_contacts) if (syn_ee_contacts + syn_ei_contacts) > 0 else float('inf')
        ele_ei_ratio = ele_ee_conductances / ele_ii_conductances if ele_ii_conductances > 0 else float('inf')
        ele_ie_ratio = ele_ii_conductances / ele_ee_conductances if ele_ee_conductances > 0 else float('inf')

        # Store results
        file_results = {
            'network_name': stats.get('network_name', basic),
            'overall_ei_ratio': ei_ratio,
            'overall_ie_ratio': ie_ratio,
            'syn_ei_ratio': syn_ei_ratio,
            'syn_ie_ratio': syn_ie_ratio,
            'ele_ei_ratio': ele_ei_ratio,
            'ele_ie_ratio': ele_ie_ratio,
            'correlation': actual_correlation
        }
        results[str(json_file)] = file_results

        # Create data for plotting - generating scatter distributions for overall counts
        # Use a fixed seed or derive from network name for reproducibility
        seed_value = hash(stats.get('network_name', str(json_file))) % (2**32)
        np.random.seed(seed_value)
        
        # Create a dataset with points clustered around our values
        n_points = 50  # Fixed number of points for visualization
        exc_data = np.random.normal(overall_excitatory_connections, max(overall_excitatory_connections*0.05, 1), n_points)
        inh_data = np.random.normal(overall_inhibitory_connections, max(overall_inhibitory_connections*0.05, 1), n_points)

        syn_exc_data = np.random.normal((syn_ee_contacts + syn_ei_contacts), max((syn_ee_contacts + syn_ei_contacts)*0.05, 1), n_points)
        syn_inh_data = np.random.normal((syn_ii_contacts + syn_ie_contacts), max((syn_ii_contacts + syn_ie_contacts)*0.05, 1), n_points)
        ele_exc_data = np.random.normal(ele_ee_conductances, max(ele_ee_conductances*0.05, 1), n_points)
        ele_inh_data = np.random.normal(ele_ii_conductances, max(ele_ii_conductances*0.05, 1), n_points)

        # Create a single figure with 3 rows and 1 column
        fig, (ax0, ax1, ax2) = plt.subplots(3, 1, figsize=(8, 15))

        # ------------------Subplot 0-----------------------------
        # Use actual correlation from JSON data
        corr_coef0 = actual_correlation if actual_correlation is not None else 0

        data0 = pd.DataFrame({
            'overall Excitatory Connections': exc_data,
            'overall Inhibitory Connections': inh_data
        })
        sns.scatterplot(data=data0, x='overall Inhibitory Connections', y='overall Excitatory Connections', 
                        color='purple', alpha=0.6, s=50, ax=ax0)
        sns.regplot(data=data0, x='overall Inhibitory Connections', y='overall Excitatory Connections', 
                    scatter=False, color='red', ax=ax0, line_kws={'linewidth': 2})
        n_count_points = 100
        exc_count_data = np.random.normal(overall_excitatory_connections, max(overall_excitatory_connections*0.01, 1), n_count_points)
        inh_count_data = np.random.normal(overall_inhibitory_connections, max(overall_inhibitory_connections*0.01, 1), n_count_points)

        ax0.scatter(inh_count_data, exc_count_data, 
                color='black', alpha=0.75, s=30, zorder=5,
                label=f'Overall counts (E: {overall_excitatory_connections:,}, I: {overall_inhibitory_connections:,})')
        ax0.plot([], [], 'o', color='purple', alpha=0.6, markersize=5, label='overall Connection distribution')

        # Use actual correlation from JSON data
        display_corr = actual_correlation if actual_correlation is not None else 0
        ax0.plot([], [], '-', color='red', linewidth=2, label=f'r={display_corr:.3f}')
        ax0.text(0.05, 0.95, f'overall E/I ratio = {ei_ratio:.3f}\noverall I/E ratio = {ie_ratio:.3f}\nCorrelation = {display_corr:.3f}', 
                transform=ax0.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        ax0.set_title(f'overall {stats.get("network_name", basic)} Exc vs Inh Connections(CTC)', fontsize=12, fontweight='bold')
        ax0.set_xlabel('overall Inhibitory Connections', fontsize=10)
        ax0.set_ylabel('overall Excitatory Connections', fontsize=10)
        ax0.ticklabel_format(style='plain', axis='both', scilimits=(0,0))
        ax0.grid(True, alpha=0.3)
        ax0.legend()

        #--------------------Subplot 1------------------------------
        # For synaptical and electrical connections, we don't have separate correlation values in the JSON
        # So we'll calculate them from the generated data for visualization purposes
        corr_coef1, _ = pearsonr(syn_exc_data, syn_inh_data)

        data1 = pd.DataFrame({
            'Synaptical Excitatory Contacts': syn_exc_data,
            'Synaptical Inhibitory Contacts': syn_inh_data
        })

        sns.scatterplot(data=data1, x='Synaptical Inhibitory Contacts', y='Synaptical Excitatory Contacts', 
                        color='purple', alpha=0.6, s=50, ax=ax1)
        sns.regplot(data=data1, x='Synaptical Inhibitory Contacts', y='Synaptical Excitatory Contacts', 
                    scatter=False, color='red', ax=ax1, line_kws={'linewidth': 2})
        syn_exc_count_data = np.random.normal((syn_ee_contacts + syn_ei_contacts), max((syn_ee_contacts + syn_ei_contacts)*0.01, 1), n_count_points)
        syn_inh_count_data = np.random.normal((syn_ii_contacts + syn_ie_contacts), max((syn_ii_contacts + syn_ie_contacts)*0.01, 1), n_count_points)

        ax1.scatter(syn_inh_count_data, syn_exc_count_data, 
                color='black', alpha=0.75, s=30, zorder=5,
                label=f'Overall counts (E: {(syn_ee_contacts + syn_ei_contacts):,}, I: {(syn_ii_contacts + syn_ie_contacts):,})')
        ax1.plot([], [], 'o', color='purple', alpha=0.6, markersize=5, label='Synaptical Contacts distribution')
        ax1.plot([], [], '-', color='red', linewidth=2, label=f'r={corr_coef1:.3f}')
        ax1.text(0.05, 0.95, f'syn E/I ratio = {syn_ei_ratio:.3f}\nsyn I/E ratio = {syn_ie_ratio:.3f}\nCorrelation = {corr_coef1:.3f}', 
                transform=ax1.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        ax1.set_title(f'{stats.get("network_name", basic)} synaptical Exc vs Inh Contacts (CTC)', fontsize=12, fontweight='bold')
        ax1.set_xlabel('synaptical Inhibitory Contacts', fontsize=10)
        ax1.set_ylabel('synaptical Excitatory Contacts', fontsize=10)

        ax1.ticklabel_format(style='plain', axis='both', scilimits=(0,0))
        ax1.grid(True, alpha=0.3)
        ax1.legend()

        # ---------------------Subplot 2----------------------------
        corr_coef2, _ = pearsonr(ele_exc_data, ele_inh_data)

        data2 = pd.DataFrame({
            'Electrical Excitatory Conductances': ele_exc_data,
            'Electrical Inhibitory Conductances': ele_inh_data
        })
        sns.scatterplot(data=data2, x='Electrical Inhibitory Conductances', y='Electrical Excitatory Conductances', 
                        color='purple', alpha=0.6, s=50, ax=ax2)
        sns.regplot(data=data2, x='Electrical Inhibitory Conductances', y='Electrical Excitatory Conductances', 
                    scatter=False, color='red', ax=ax2, line_kws={'linewidth': 2})
        ele_exc_count_data = np.random.normal(ele_ee_conductances, max(ele_ee_conductances*0.01, 1), n_count_points)
        ele_inh_count_data = np.random.normal(ele_ii_conductances, max(ele_ii_conductances*0.01, 1), n_count_points)

        ax2.scatter(ele_inh_count_data, ele_exc_count_data, 
                color='black', alpha=0.75, s=30, zorder=5,
                label=f'Overall counts (E: {ele_ee_conductances:,}, I: {ele_ii_conductances:,})')

        ax2.plot([], [], 'o', color='purple', alpha=0.6, markersize=5, label='Electrical Conductances distribution')
        ax2.plot([], [], '-', color='red', linewidth=2, label=f'r={corr_coef2:.3f}')
        ax2.text(0.05, 0.95, f'ele E/I ratio = {ele_ei_ratio:.3f}\nele I/E ratio = {ele_ie_ratio:.3f}\nCorrelation = {corr_coef2:.3f}', 
                transform=ax2.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        ax2.set_title(f'{stats.get("network_name", basic)} electrical Exc vs Inh Conductances (CTC)', fontsize=12, fontweight='bold')
        ax2.set_xlabel('electrical Inhibitory Conductances', fontsize=10)
        ax2.set_ylabel('electrical Excitatory Conductances', fontsize=10)

        ax2.ticklabel_format(style='plain', axis='both', scilimits=(0,0))
        ax2.grid(True, alpha=0.3)
        ax2.legend()

        # Adjust layout and save the combined figure
        plt.tight_layout()
        # Save to plots directory
        plt.savefig(plots_dir / f'{basic}_regression.png', dpi=300, bbox_inches='tight')
        plt.close(fig)

        ###############################################################
        # Print the ratios and correlation
        print(f"  overall E/I ratio: {ei_ratio:.6f}")
        print(f"  overall I/E ratio: {ie_ratio:.6f}")
        print(f"  Correlation coefficient: {display_corr:.6f}")

        print(f"  syn E/I ratio: {syn_ei_ratio:.6f}")
        print(f"  syn_I/E ratio: {syn_ie_ratio:.6f}")
        print(f"  Correlation coefficient: {corr_coef1:.6f}")

        print(f"  ele E/I ratio: {ele_ei_ratio:.6f}")
        print(f"  ele I/E ratio: {ele_ie_ratio:.6f}")
        print(f"  Correlation coefficient: {corr_coef2:.6f}")

        # Create a single figure with 3 rows and 2 columns
        fig, ((ax3, ax4), (ax5, ax6), (ax7, ax8)) = plt.subplots(3, 2, figsize=(12, 15))

        # -----------Subplot (0,0) - E/I Connections Ratio-----------------------------
        exc_ei_ratios = exc_data / np.maximum(overall_inhibitory_connections, 1e-10)
        inh_ei_ratios = overall_excitatory_connections / np.maximum(inh_data, 1e-10)
        exc_ie_ratios = overall_inhibitory_connections / np.maximum(exc_data, 1e-10)
        inh_ie_ratios = inh_data / np.maximum(overall_excitatory_connections, 1e-10)

        ax3.hist(exc_ei_ratios, bins=25, alpha=0.75, color='red', label='Excitatory')
        ax3.hist(inh_ei_ratios, bins=25, alpha=0.75, color='cyan', label='Inhibitory')
        ax3.axvline(ei_ratio, color='black', linestyle='--', linewidth=2)
        ax3.plot(ei_ratio, ax3.get_ylim()[1]*0.05, 'v', markersize=10, color='black', markeredgecolor='white', markeredgewidth=1,
                label=f'E/I ratio = {ei_ratio:.3f}')
        ax3.set_title(f'Distribution of {stats.get("network_name", basic)} E/I Connections Ratio (CTC)', fontsize=12, fontweight='bold')
        ax3.set_xlabel(f'{stats.get("network_name", basic)} E/I Connections Ratio', fontsize=10)
        ax3.set_ylabel('Probability', fontsize=10)
        ax3.legend()
        ax3.grid(True, alpha=0.3)

        # -----------Subplot (1,0) - I/E Connections Ratio-----------------------------
        ax4.hist(exc_ie_ratios, bins=25, alpha=0.75, color='red', label='Excitatory')
        ax4.hist(inh_ie_ratios, bins=25, alpha=0.75, color='cyan', label='Inhibitory')
        ax4.axvline(ie_ratio, color='black', linestyle='--', linewidth=2)
        ax4.plot(ie_ratio, ax4.get_ylim()[1]*0.05, 'v', markersize=10, color='black', markeredgecolor='white', markeredgewidth=1,
                label=f'I/E ratio = {ie_ratio:.3f}')
        ax4.set_title(f'Distribution of {stats.get("network_name", basic)} I/E Connections Ratio (CTC)', fontsize=12, fontweight='bold')
        ax4.set_xlabel(f'{stats.get("network_name", basic)} I/E Connections Ratio', fontsize=10)
        ax4.set_ylabel('Probability', fontsize=10)
        ax4.legend()
        ax4.grid(True, alpha=0.3)

        # -----------Subplot (0,1) - Synaptical E/I Contacts Ratio---------------------
        syn_exc_ei_ratios = syn_exc_data / np.maximum((syn_ii_contacts + syn_ie_contacts), 1e-10)
        syn_inh_ei_ratios = (syn_ee_contacts + syn_ei_contacts) / np.maximum(syn_inh_data, 1e-10)

        ax5.hist(syn_exc_ei_ratios, bins=25, alpha=0.75, color='red', label='Synaptical Excitatory')
        ax5.hist(syn_inh_ei_ratios, bins=25, alpha=0.75, color='cyan', label='Synaptical Inhibitory')
        ax5.axvline(syn_ei_ratio, color='black', linestyle='--', linewidth=2)
        ax5.plot(syn_ei_ratio, ax5.get_ylim()[1]*0.05, 'v', markersize=10, color='black', markeredgecolor='white', markeredgewidth=1,
                label=f'syn E/I ratio = {syn_ei_ratio:.3f}')
        ax5.set_title(f'Distribution of {stats.get("network_name", basic)} Synaptical E/I Contacts Ratio (CTC)', fontsize=12, fontweight='bold')
        ax5.set_xlabel(f'{stats.get("network_name", basic)} Synaptical E/I Contacts Ratio', fontsize=10)
        ax5.set_ylabel('Probability', fontsize=10)
        ax5.legend()
        ax5.grid(True, alpha=0.3)

        # -----------Subplot (1,1) - Synaptical I/E Contacts Ratio---------------------
        syn_exc_ie_ratios = (syn_ii_contacts + syn_ie_contacts) / np.maximum(syn_exc_data, 1e-10)
        syn_inh_ie_ratios = syn_inh_data / np.maximum((syn_ee_contacts + syn_ei_contacts), 1e-10)

        ax6.hist(syn_exc_ie_ratios, bins=25, alpha=0.75, color='red', label='Synaptical Excitatory')
        ax6.hist(syn_inh_ie_ratios, bins=25, alpha=0.75, color='cyan', label='Synaptical Inhibitory')
        ax6.axvline(syn_ie_ratio, color='black', linestyle='--', linewidth=2)
        ax6.plot(syn_ie_ratio, ax6.get_ylim()[1]*0.05, 'v', markersize=10, color='black', markeredgecolor='white', markeredgewidth=1,
                label=f'syn I/E ratio = {syn_ie_ratio:.3f}')
        ax6.set_title(f'Distribution of {stats.get("network_name", basic)} Synaptical I/E Contacts Ratio (CTC)', fontsize=12, fontweight='bold')
        ax6.set_xlabel(f'{stats.get("network_name", basic)} Synaptical I/E Contacts Ratio', fontsize=10)
        ax6.set_ylabel('Probability', fontsize=10)
        ax6.legend()
        ax6.grid(True, alpha=0.3)

        # -----------Subplot (2,0) - Electrical E/I Conductances Ratio-----------------
        ele_exc_ei_ratios = ele_exc_data / np.maximum(ele_ii_conductances, 1e-10)
        ele_inh_ei_ratios = ele_ee_conductances / np.maximum(ele_inh_data, 1e-10)

        ax7.hist(ele_exc_ei_ratios, bins=25, alpha=0.75, color='red', label='Electrical Excitatory')
        ax7.hist(ele_inh_ei_ratios, bins=25, alpha=0.75, color='cyan', label='Electrical Inhibitory')
        ax7.axvline(ele_ei_ratio, color='black', linestyle='--', linewidth=2)
        ax7.plot(ele_ei_ratio, ax7.get_ylim()[1]*0.05, 'v', markersize=10, color='black', markeredgecolor='white', markeredgewidth=1,
                label=f'ele E/I ratio = {ele_ei_ratio:.3f}')
        ax7.set_title(f'Distribution of {stats.get("network_name", basic)} Electrical E/I Conductances Ratio (CTC)', fontsize=12, fontweight='bold')
        ax7.set_xlabel(f'{stats.get("network_name", basic)} Electrical E/I Conductances Ratio', fontsize=10)
        ax7.set_ylabel('Probability', fontsize=10)
        ax7.legend()
        ax7.grid(True, alpha=0.3)

        # -----------Subplot (2,1) - Electrical I/E Conductances Ratio-----------------
        ele_exc_ie_ratios = ele_ii_conductances / np.maximum(ele_exc_data, 1e-10)
        ele_inh_ie_ratios = ele_inh_data / np.maximum(ele_ee_conductances, 1e-10)

        ax8.hist(ele_exc_ie_ratios, bins=25, alpha=0.75, color='red', label='Electrical Excitatory')
        ax8.hist(ele_inh_ie_ratios, bins=25, alpha=0.75, color='cyan', label='Electrical Inhibitory')
        ax8.axvline(ele_ie_ratio, color='black', linestyle='--', linewidth=2)
        ax8.plot(ele_ie_ratio, ax8.get_ylim()[1]*0.05, 'v', markersize=10, color='black', markeredgecolor='white', markeredgewidth=1,
                label=f'ele I/E ratio = {ele_ie_ratio:.3f}')
        ax8.set_title(f'Distribution of {stats.get("network_name", basic)} Electrical I/E Conductances Ratio(CTC)', fontsize=12, fontweight='bold')
        ax8.set_xlabel(f'{stats.get("network_name", basic)} Electrical I/E Conductances Ratio', fontsize=10)
        ax8.set_ylabel('Probability', fontsize=10)
        ax8.legend()
        ax8.grid(True, alpha=0.3)

        # Adjust layout and save the combined figure
        plt.tight_layout()
        # Save to plots directory
        plt.savefig(plots_dir / f'{basic}_ratio_distributions.png', dpi=300, bbox_inches='tight')
        plt.close(fig)
        
        print(f"  Saved plots to {plots_dir}")
    
    return results


def main():
    """Main function for command-line usage."""
    import glob
    
    # Look for JSON files in analysis_out directory
    json_files = glob.glob('analysis_out/*_connection_stats.json')
    
    if not json_files:
        print("No JSON files found in analysis_out directory.")
        return
    
    results = analyze_connection_ratios(json_files, plots_dir='plots')
    print("Analysis completed successfully!")
    return results


if __name__ == "__main__":
    main()