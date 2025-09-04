#!/usr/bin/env python3
"""
Create placeholder images for documentation purposes.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

def create_placeholder_images():
    """Create simple placeholder images for documentation."""
    # Create directory for images
    os.makedirs("docs/images", exist_ok=True)
    
    # 1. Sample regression plot
    plt.figure(figsize=(8, 6))
    x = np.linspace(0, 1, 20)
    y = 0.8 * x + np.random.normal(0, 0.1, 20)
    plt.scatter(x, y, alpha=0.7)
    plt.plot(x, 0.8 * x, 'r-', label='Regression line')
    plt.xlabel('Overall E/I Ratio')
    plt.ylabel('Correlation')
    plt.title('Sample Regression Plot')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('docs/images/sample_regression.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Sample distribution plot
    plt.figure(figsize=(10, 6))
    data1 = np.random.normal(1.2, 0.3, 1000)
    data2 = np.random.normal(0.8, 0.2, 1000)
    data3 = np.random.normal(1.0, 0.25, 1000)
    
    plt.hist(data1, bins=30, alpha=0.7, label='Overall E/I Ratio', density=True)
    plt.hist(data2, bins=30, alpha=0.7, label='Synaptic E/I Ratio', density=True)
    plt.hist(data3, bins=30, alpha=0.7, label='Electrical E/I Ratio', density=True)
    
    plt.xlabel('Ratio Value')
    plt.ylabel('Density')
    plt.title('Sample Distribution Plot')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('docs/images/sample_distributions.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Sample violin plot
    plt.figure(figsize=(10, 6))
    data = [np.random.normal(0, std, 100) for std in range(1, 7)]
    plt.violinplot(data, positions=range(1, 7))
    plt.xlabel('Connection Types')
    plt.ylabel('Connection Count (log scale)')
    plt.title('Sample Violin Plot')
    plt.xticks(range(1, 7), ['EE', 'EI', 'IE', 'II', 'Ele EE', 'Ele II'])
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('docs/images/sample_violins.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Sample heatmap
    plt.figure(figsize=(8, 6))
    data = np.random.rand(6, 6)
    im = plt.imshow(data, cmap='coolwarm', interpolation='nearest')
    plt.colorbar(im)
    plt.title('Sample Correlation Heatmap')
    plt.xlabel('Connection Types')
    plt.ylabel('Connection Types')
    plt.xticks(range(6), ['EE', 'EI', 'IE', 'II', 'EleEE', 'EleII'])
    plt.yticks(range(6), ['EE', 'EI', 'IE', 'II', 'EleEE', 'EleII'])
    plt.tight_layout()
    plt.savefig('docs/images/sample_clustermap.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Sample combined heatmaps
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # First heatmap
    data1 = np.random.rand(6, 6)
    im1 = ax1.imshow(data1, cmap='coolwarm', interpolation='nearest')
    ax1.set_title('Correlation Matrix')
    ax1.set_xticks(range(6))
    ax1.set_yticks(range(6))
    ax1.set_xticklabels(['EE', 'EI', 'IE', 'II', 'EleEE', 'EleII'])
    ax1.set_yticklabels(['EE', 'EI', 'IE', 'II', 'EleEE', 'EleII'])
    
    # Second heatmap
    data2 = np.abs(data1)
    im2 = ax2.imshow(data2, cmap='Reds', interpolation='nearest')
    ax2.set_title('Absolute Correlation Matrix')
    ax2.set_xticks(range(6))
    ax2.set_yticks(range(6))
    ax2.set_xticklabels(['EE', 'EI', 'IE', 'II', 'EleEE', 'EleII'])
    ax2.set_yticklabels(['EE', 'EI', 'IE', 'II', 'EleEE', 'EleII'])
    
    plt.tight_layout()
    plt.savefig('docs/images/sample_combined_heatmaps.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Sample E/I scatter plot
    plt.figure(figsize=(10, 6))
    networks = ['Net1', 'Net2', 'Net3', 'Net4', 'Net5']
    e_ratios = [1.2, 0.9, 1.1, 1.3, 0.8]
    i_ratios = [0.8, 1.1, 0.9, 0.7, 1.2]
    
    x = range(len(networks))
    plt.bar(x, e_ratios, label='E Ratio', alpha=0.7)
    plt.bar(x, i_ratios, bottom=e_ratios, label='I Ratio', alpha=0.7)
    
    plt.xlabel('Networks')
    plt.ylabel('Ratio Values')
    plt.title('Sample E/I Ratio Scatter Plot')
    plt.xticks(x, networks)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('docs/images/sample_ei_stacked.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Placeholder images created successfully!")
    print("Check the 'docs/images' directory for the generated images.")

if __name__ == "__main__":
    create_placeholder_images()