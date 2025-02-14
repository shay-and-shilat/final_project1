import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random
import pandas as pd
import os
import numpy as np
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def plot_sleep_stages(psg_files, headband_files, colormap='viridis', title=None):
    """
    Plots sleep stage data from PSG and headband files.
    
    This function selects a random PSG file from the provided list, extracts relevant sleep stage data,
    and attempts to find a corresponding headband file based on subject ID. It then plots the sleep stages
    over time using a scatter plot and compares expert-labeled sleep stages with AI-derived predictions.
    
    Parameters:
    - psg_files (list of str): List of file paths to PSG data files.
    - headband_files (list of str): List of file paths to headband data files.
    - colormap (str, optional): The colormap to use for the scatter plot. Default is 'viridis'.
    - title (str, optional): Title for the plot. Default is None.
    
    Returns:
    - None: Displays the plot but does not return any values.
    """
    # Select a random PSG file from the provided list
    random_psg_file = random.choice(psg_files)
    
    # Check if the file exists
    if not os.path.exists(random_psg_file):
        logging.warning(f"File not found: {random_psg_file}. Skipping plot.")
        return
    
    # Load PSG data
    psg_data = pd.read_csv(random_psg_file, sep="\t")
    
    # Ensure required columns are present
    if psg_data.empty or not {'onset', 'majority', 'ai_psg'}.issubset(psg_data.columns):
        logging.warning(f"No valid data found in {random_psg_file}. Skipping plot.")
        return
    
    # Extract relevant columns
    onset = psg_data['onset']  # Time in seconds
    majority = psg_data['majority']  # Expert-labeled sleep stages
    ai_psg = psg_data['ai_psg']  # AI predictions from PSG
    
    # Create a colormap for sleep stages
    cmap = plt.get_cmap(colormap)
    norm = mcolors.Normalize(vmin=majority.min(), vmax=majority.max())
    colors = [cmap(norm(stage)) for stage in majority] if len(majority) > 0 else []
    
    if not colors:
        logging.warning(f"No valid majority values in {random_psg_file}. Skipping plot.")
        return
    
    # Extract subject ID from the PSG filename (assumed to be the first part of the filename)
    subject_id = os.path.basename(random_psg_file).split("_")[0]
    
    # Find the corresponding headband file for the same subject
    headband_file = next((file for file in headband_files if subject_id in os.path.basename(file)), None)
    
    # Check if the corresponding headband file exists
    if headband_file is None or not os.path.exists(headband_file):
        logging.warning(f"No corresponding headband file found or file does not exist for PSG file {random_psg_file}")
        return
    
    # Load headband data
    headband_data = pd.read_csv(headband_file, sep="\t")
    
    # Ensure required column 'ai_hb' is present
    if 'ai_hb' not in headband_data.columns:
        logging.warning(f"No 'ai_hb' data found in {headband_file}. Skipping plot.")
        return
    
    ai_hb = headband_data['ai_hb']  # AI predictions from headband
    
    # Plot sleep stages
    plt.figure(figsize=(14, 7))
    
    # First subplot: Scatter plot of expert sleep stages over time
    plt.subplot(2, 1, 1)
    plt.scatter(onset, majority, c=colors, cmap=colormap, edgecolor='none', s=20, alpha=0.7)
    plt.xlabel('Time (seconds)', fontsize=14)
    plt.ylabel('Sleep Stage', fontsize=14)
    plt.title(title or f'Sleep Stages Over Time In PSG (Subject: {subject_id})', fontsize=16)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.colorbar(label='Sleep Stage')
    
    # Second subplot: Line plot comparing expert and AI sleep stages
    plt.subplot(2, 1, 2)
    plt.plot(onset, majority, label='Experts', color='deeppink', alpha=0.7)
    plt.plot(onset, ai_psg, label='AI (PSG)', color='darkviolet', alpha=0.7)
    plt.plot(onset, ai_hb, label='AI (Headband)', color='darkturquoise', alpha=0.7)
    
    plt.xlabel('Time (seconds)', fontsize=14)
    plt.ylabel('Sleep Stage', fontsize=14)
    plt.title(f'Sleep Stages Comparison (Experts vs AI) for {subject_id}', fontsize=16)
    plt.legend()
    plt.grid(True, linestyle='--', linewidth=0.5)
    
    # Set y-axis ticks to match the range of sleep stages
    plt.yticks(np.arange(min(min(majority), min(ai_psg), min(ai_hb)), 
                         max(max(majority), max(ai_psg), max(ai_hb)) + 1, 1))
    
    plt.tight_layout()
    plt.show()
