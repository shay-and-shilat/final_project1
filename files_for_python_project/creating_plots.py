import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import pandas as pd
import os
import numpy as np
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to plot sleep stages over time with different colors for each sleep stage
def plot_sleep_stages(psg_files, headband_files, colormap='viridis', title=None):
    """
    Plots the sleep stages over time with a customizable colormap, and adds a third line for the 'ai_hb' from the headband file.
    
    Parameters:
    psg_files (list): A list of PSG event file paths.
    headband_files (list): A list of headband event file paths.
    colormap (str): The colormap to use for the plot. Default is 'viridis'.
    title (str): Optional title for the plot. If None, it will use the subject's ID.
    """
    # Select a random PSG file from the list
    random_psg_file = random.choice(psg_files)
    psg_data = pd.read_csv(random_psg_file, sep="\t")
    
    # Extract time and sleep stages from the PSG data
    onset = psg_data['onset']  # Time in 30-second epochs
    majority = psg_data['majority']  # Sleep stage
    ai_psg = psg_data['ai_psg']  # AI PSG stage
    
    # Ensure there is data for both 'onset' and 'majority'
    if len(onset) == 0 or len(majority) == 0 or len(ai_psg) == 0:
        logging.warning(f"No data found in {psg_files}. Skipping plot.")
        return
    
    # Create a color map to represent the stages
    cmap = plt.get_cmap(colormap)  # User-defined colormap (default: 'viridis')
    norm = mcolors.Normalize(vmin=majority.min(), vmax=majority.max())
    
    # Only create colors if majority values are available
    if len(majority) > 0:
        colors = [cmap(norm(stage)) for stage in majority]  # Assign color for each stage
    else:
        logging.warning(f"No valid majority values in {psg_files}. Skipping plot.")
        return
    
    # Extract subject ID from the filename (assuming the subject ID is the first part of the filename)
    subject_id = os.path.basename(random_psg_file).split("_")[0]
    
    # Find the corresponding headband file for the subject
    headband_file = None
    for file in headband_files:
        if subject_id in os.path.basename(file):
            headband_file = file
            break
    
    if headband_file is None:
        logging.warning(f"No corresponding headband file found for {subject_id}. Skipping plot.")
        return

    # Read the headband file to get the 'ai_hb' sleep stages
    headband_data = pd.read_csv(headband_file, sep="\t")
    ai_hb = headband_data['ai_hb']  # AI Headband sleep stages
    
    # Plot the sleep stages over time using a scatter plot (colored points)
    plt.figure(figsize=(14, 7))
    plt.subplot(2, 1, 1)  # Scatter plot in the first subplot
    plt.scatter(onset, majority, c=colors, cmap=colormap, edgecolor='none', s=20, alpha=0.7)
    plt.xlabel('Time (seconds)', fontsize=14)
    plt.ylabel('Sleep Stage', fontsize=14)
    if title is None:
        title = f'Sleep Stages Over Time In PSG (Subject: {subject_id})'
    plt.title(title, fontsize=16)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.colorbar(label='Sleep Stage')
    
    # Line plot comparing 'majority', 'ai_psg', and 'ai_hb'
    plt.subplot(2, 1, 2)  # Line plot in the second subplot
    plt.plot(onset, majority, label='experts', color='deeppink', alpha=0.7)
    plt.plot(onset, ai_psg, label='AI (PSG)', color='darkviolet', alpha=0.7)
    plt.plot(onset, ai_hb, label='AI (Headband)', color='darkturquoise', alpha=0.7)
    
    plt.xlabel('Time (seconds)', fontsize=14)
    plt.ylabel('Sleep Stage', fontsize=14)
    plt.title(f'Sleep Stages Comparison (experts vs AI) for {subject_id}', fontsize=16)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    # Ensure the Y-axis shows only whole numbers
    plt.yticks(np.arange(min(min(majority), min(ai_psg), min(ai_hb)), max(max(majority), max(ai_psg), max(ai_hb)) + 1, 1))

    plt.tight_layout()
    plt.show()

    
    
    
print(pd.__version__)
print(np.__version__)
