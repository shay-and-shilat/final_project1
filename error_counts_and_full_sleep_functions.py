import pandas as pd
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to calculate the total hours of missing data (artifacts)
def error_houers_count(headbend_file):
    """
    Calculates the total number of hours with missing data (artifacts) from the headband file.
    
    Parameters:
    headbend_file (str): Path to the headband event file (headband_events.tsv).
    
    Returns:
    float: Total hours of missing data (artifacts).
    """
    try:
        headbend_file = pd.read_csv(headbend_file, sep="\t")
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return 0

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
    try:
        headbend_file = pd.read_csv(headbend_file, sep="\t")
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return 0

    #finds the total number of rows from the file, removes the title row of the file and multiplies by 30 to represent the total sleep in seconds. 
    sleeping_seconds = (len(headbend_file)-1) * 30
    sleeping_hours = sleeping_seconds / 3600
    return sleeping_hours
