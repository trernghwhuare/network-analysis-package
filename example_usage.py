#!/usr/bin/env python3
"""
Example usage of the network analysis package
"""

import json
import os
from network_analysis_package import conn_ratio

# Create sample data directory
os.makedirs("analysis_out", exist_ok=True)

# Create sample network data
sample_network_data = {
    "network_name": "example_network",
    "syn_ee_contacts": 12000,
    "syn_ei_contacts": 10000,
    "syn_ie_contacts": 8000,
    "syn_ii_contacts": 6000,
    "ele_ee_conductances": 2000,
    "ele_ii_conductances": 1500,
    "correlation": 0.82
}

# Save sample data to JSON file
sample_file = "analysis_out/example_network_connection_stats.json"
with open(sample_file, "w") as f:
    json.dump(sample_network_data, f, indent=2)

print(f"Created sample data file: {sample_file}")

# Run connection ratio analysis
print("Running connection ratio analysis...")
results = conn_ratio.analyze_connection_ratios(
    json_files=[sample_file],
    plots_dir="plots"
)

# Display results
print("\nAnalysis Results:")
print("=" * 40)
for network, ratios in results.items():
    print(f"Network: {network}")
    for ratio_name, ratio_value in ratios.items():
        print(f"  {ratio_name}: {ratio_value:.6f}")

print("\nCheck the 'plots' directory for generated visualizations.")