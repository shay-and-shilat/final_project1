import pandas as pd
import logging

# Set up logging configuration to capture error and info messages with timestamps
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to calculate the total hours of missing data (artifacts)
def error_hours_count(headband_file):
    """
    Calculates the total number of hours with missing data (artifacts) from the headband file.
    
    Parameters:
    headband_file (str): Path to the headband event file (headband_events.tsv), which should contain the data to be analyzed.
    
    Returns:
    float: Total hours of missing data (artifacts). 
           If the 'ai_hb' column is missing, an error message is logged, and the function returns 0.
    """
    # Read the headband event file into a pandas DataFrame
    headband_file = pd.read_csv(headband_file, sep="\t")
    
    # Check if the 'ai_hb' column exists in the file
    if 'ai_hb' not in headband_file.columns:
        logging.error("Missing 'ai_hb' column in the file")
        return 0

    # Identify rows with missing data (artifacts) represented by -2 in the 'ai_hb' column
    headband_file = headband_file['ai_hb'] == -2
    
    # Sum the number of artifacts, multiply by 30 (assuming 30 seconds per data point),
    # and convert from seconds to hours (3600 seconds in an hour)
    hours_count = (headband_file.sum() * 30) / 3600
    
    return hours_count

# Function to calculate total sleeping hours (excluding artifacts)
def total_sleeping_hours(headband_file):
    """
    Calculates the total number of sleeping hours (excluding artifacts) from the headband data.
    
    Parameters:
    headband_file (str): Path to the headband event file (headband_events.tsv), which should contain the data to be analyzed.
    
    Returns:
    float: Total sleeping hours. If the 'ai_hb' column is missing, an error message is logged, and the function returns 0.
    """
    # Read the headband event file into a pandas DataFrame
    headband_file = pd.read_csv(headband_file, sep="\t")

    # Check if the 'ai_hb' column exists in the file
    if 'ai_hb' not in headband_file.columns:
        logging.error(f"The file {headband_file} is missing the 'ai_hb' column.")
        return 0
    
    # Collect all data values, excluding the first row (which is assumed to be the header)
    valid_data = headband_file.iloc[1:]
    
    # Calculate total number of hours by counting data points, assuming each point represents 30 seconds of data
    total_sleep = ((len(valid_data)) * 30) / 3600  # Convert from seconds to hours (30 seconds per data point)
    
    return total_sleep
