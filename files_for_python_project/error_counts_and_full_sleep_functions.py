import pandas as pd
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to calculate the total hours of missing data (artifacts)
def error_hours_count(headband_file):
    """
    Calculates the total number of hours with missing data (artifacts) from the headband file.
    
    Parameters:
    headband_file (str): Path to the headband event file (headband_events.tsv).
    
    Returns:
    float: Total hours of missing data (artifacts).
    """
    headband_file = pd.read_csv(headband_file, sep="\t")
    
    if 'ai_hb' not in headband_file.columns:
        logging.error("Missing 'ai_hb' column in the file")
        return 0

    # Calculate total hours of missing data (artifacts)
    headband_file = headband_file['ai_hb'] == -2
    hours_count = (headband_file.sum() * 30) / 3600
    return hours_count

# Function to calculate total sleeping hours (excluding artifacts)


# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Function to calculate total sleeping hours (excluding artifacts)
def total_sleeping_hours(headband_file):
    # Read the file
    headband_file = pd.read_csv(headband_file, sep="\t")

    # Check if 'majority' column exists
    if 'ai_hb' not in headband_file.columns:
        logging.error(f"The file {headband_file} is missing the 'ai_hb' column.")
        return 0
    
    # Proceed with your current logic if the column exists
    valid_data = headband_file.iloc[1:]
    total_sleep = ((len(valid_data)) * 30) / 3600

    # You can adjust the final calculation as needed
    return total_sleep
