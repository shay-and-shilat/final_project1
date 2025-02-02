import pandas as pd
import os
import statistics
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

# Function to find event files within the provided base folder
def find_event_files(base_folder):
    """
    Finds and returns pairs of headband and PSG event files within the given directory structure.
    
    Parameters:
    base_folder (str): The path to the base folder containing the subject data folders.
    
    Returns:
    tuple: A tuple containing two lists - headband_files and psg_files.
    """
    headband_files = []
    psg_files = []

    # Check if base_folder exists and is a directory
    if not os.path.isdir(base_folder):
        print(f"Error: '{base_folder}' is not a valid directory.")
        return headband_files, psg_files

    # Iterate through each subfolder in the base folder
    for entry in os.scandir(base_folder):
        if entry.is_dir():
            eeg_folder_path = os.path.join(entry.path, "eeg")

            if os.path.isdir(eeg_folder_path):
                headband_file, psg_file = None, None

                # Loop through files in "eeg" folder
                for file_entry in os.scandir(eeg_folder_path):
                    if file_entry.is_file():
                        # Identify headband and PSG event files
                        if file_entry.name.endswith("headband_events.tsv"):
                            headband_file = file_entry.path
                        elif file_entry.name.endswith("psg_events.tsv"):
                            psg_file = file_entry.path

                    # If both files are found, exit loop early
                    if headband_file and psg_file:
                        break

                # Only add files if BOTH are found
                if headband_file and psg_file:
                    headband_files.append(headband_file)
                    psg_files.append(psg_file)

    return headband_files, psg_files

# Function to compare headband AI scoring with the majority expert scoring
def headbend_vs_majority(ai_file, experts_file):
    """
    Compares headband AI scoring to the majority expert scoring.
    
    Parameters:
    ai_file (str): Path to the headband AI scoring file (headband_events.tsv).
    experts_file (str): Path to the expert majority scoring file (psg_events.tsv).
    
    Returns:
    float or None: Percentage of agreement between AI and majority, or None if the error rate is too high.
    """
    ai_file = pd.read_csv(ai_file, sep="\t") 
    experts_file = pd.read_csv(experts_file, sep="\t")

    dis_mask = (experts_file['majority'] != 8)
    experts_file = experts_file[dis_mask].reset_index(drop=True)
    ai_file = ai_file[dis_mask].reset_index(drop=True)

    ai_error = ai_file['ai_hb'] == -2
    error_pr = (ai_error.sum() / len(ai_file)) * 100

    if error_pr >= 40:
        return None

    mis_mask = (ai_file['ai_hb'] != -2)
    experts_file = experts_file[mis_mask].reset_index(drop=True)
    ai_file = ai_file[mis_mask].reset_index(drop=True)

    hb_vs_maj = ai_file['ai_hb'] == experts_file['majority']
    precent_match = (hb_vs_maj.sum() / len(hb_vs_maj)) * 100
    return precent_match

# Function to compare PSG AI scoring with the majority expert scoring
def aispg_vs_majority(psg_file):
    """
    Compares PSG AI scoring to the majority expert scoring.
    
    Parameters:
    psg_file (str): Path to the PSG event file (psg_events.tsv).
    
    Returns:
    float: Percentage of agreement between AI and majority.
    """
    psg_file = pd.read_csv(psg_file, sep="\t")

    mask = (psg_file['majority'] != 8)
    psg_file = psg_file[mask].reset_index(drop=True)

    aipsg_vs_maj = psg_file['ai_psg'] == psg_file['majority']
    precent_match = (aipsg_vs_maj.sum() / len(psg_file)) * 100
    return precent_match

# Function to calculate the total hours of missing data (artifacts)
def error_houers_count(headbend_file):
    """
    Calculates the total number of hours with missing data (artifacts) from the headband file.
    
    Parameters:
    headbend_file (str): Path to the headband event file (headband_events.tsv).
    
    Returns:
    float: Total hours of missing data (artifacts).
    """
    headbend_file = pd.read_csv(headbend_file, sep="\t")

    headbend_file = headbend_file['ai_hb'] == -2
    houers_count = (headbend_file.sum() * 30) / 3600
    return houers_count

# Function to calculate total sleeping hours (excluding artifacts)
def total_sleeping_hours(headbend_file):
    """
    Calculates the total sleeping hours, excluding the artifacts (missing data).
    
    Parameters:
    headbend_file (str): Path to the headband event file (headband_events.tsv).
    
    Returns:
    float: Total sleeping hours.
    """
    headbend_file = pd.read_csv(headbend_file, sep="\t")

    sleeping_seconds = (len(headbend_file)-1) * 30
    sleeping_hours = sleeping_seconds / 3600
    return sleeping_hours

# Function to plot sleep stages over time with different colors for each sleep stage
def plot_sleep_stages_over_time(psg_files, headband_files, colormap='viridis', title=None):
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
        print(f"Warning: No data found in {random_psg_file}. Skipping plot.")
        return
    
    # Create a color map to represent the stages
    cmap = plt.get_cmap(colormap)  # User-defined colormap (default: 'viridis')
    norm = mcolors.Normalize(vmin=majority.min(), vmax=majority.max())
    
    # Only create colors if majority values are available
    if len(majority) > 0:
        colors = [cmap(norm(stage)) for stage in majority]  # Assign color for each stage
    else:
        print(f"Warning: No valid majority values in {random_psg_file}. Skipping plot.")
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
        print(f"Warning: No corresponding headband file found for {subject_id}. Skipping plot.")
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

# Main script execution
hb_vs_mj_sec = []
psgai_vs_mj_sec = []
error_houers = 0
sleeping_houers = 0

# Find event files
headband_files, psg_files = find_event_files('files_for_python_project')

# Iterate over the headband and PSG files to calculate statistics
for headband_file, psg_file in zip(headband_files, psg_files):
    hb_vs_mj_sec.append(headbend_vs_majority(headband_file, psg_file))
    psgai_vs_mj_sec.append(aispg_vs_majority(psg_file))
    error_houers += error_houers_count(headband_file)
    sleeping_houers += total_sleeping_hours(headband_file)

# Filter out None values from hb_vs_mj_sec list
hb_vs_mj_sec = [x for x in hb_vs_mj_sec if x is not None]

# Display results
print(f"We found {round(statistics.mean(hb_vs_mj_sec), 2)}% match between the headband AI and the majority")
print(f"We found {round(statistics.mean(psgai_vs_mj_sec), 2)}% match between the PSG AI and the majority")
print(f"There were {round(error_houers, 2)} hours of missing data out of a total of {round(sleeping_houers, 2)} sleeping hours in the headband experiment")

# Plot sleep stages over time and line comparison from a random PSG file
plot_sleep_stages_over_time(psg_files, headband_files)
