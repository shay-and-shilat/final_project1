import pandas as pd
import logging
import os

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Function to compare headband AI scoring with the majority expert scoring
def headband_vs_majority(headband_file, psg_file):
    """
    Compares headband AI scoring to the majority expert scoring.

    Parameters:
    headband_file (str): Path to the headband AI scoring file (headband_events.tsv).
    psg_file (str): Path to the expert majority scoring file (psg_events.tsv).

    Returns:
    float or None: Percentage of agreement between AI and majority, or None if the error rate is too high.
    """
    logging.info("Comparing headband AI scoring with PSG expert scoring...")

    try:
        ai_df = pd.read_csv(headband_file, sep="\t")
        experts_df = pd.read_csv(psg_file, sep="\t")
    except Exception as e:
        logging.error(f"Error reading files: {e}")
        return None

    # Constants
    NO_DATA_COLLECTED = -2
    AWAKE_STAGE = 8

    # Filter out awake stage before processing
    mask = experts_df["majority"] != AWAKE_STAGE
    ai_df = ai_df.loc[mask].reset_index(drop=True)
    experts_df = experts_df.loc[mask].reset_index(drop=True)

    if ai_df.empty or experts_df.empty:
        logging.warning("Filtered data is empty. Skipping comparison.")
        return None

    file_id = os.path.basename(headband_file).split("_")[0]

    # Calculate error rate
    error_mask = ai_df["ai_hb"] == NO_DATA_COLLECTED
    error_percentage = (error_mask.sum() / len(ai_df)) * 100

    if error_percentage >= 40:
        logging.warning(f"Error rate is too high ({error_percentage:.2f}%), skipping comparison.")
        return None

    # Filter out erroneous AI readings
    valid_ai_mask = ~error_mask
    ai_df = ai_df.loc[valid_ai_mask].reset_index(drop=True)
    experts_df = experts_df.loc[valid_ai_mask].reset_index(drop=True)

    # Ensure indices align
    if len(ai_df) != len(experts_df):
        logging.warning("Mismatch in filtered DataFrame lengths. Skipping comparison.")
        return None

    # Compute percentage match
    match_percentage = (ai_df["ai_hb"] == experts_df["majority"]).mean() * 100

    logging.info(f"Comparison completed. Percentage match for patient {file_id}: {match_percentage:.2f}%")
    return match_percentage


# Function to compare PSG AI scoring with the majority expert scoring
def aispg_vs_majority(psg_file):
    """
    Compares PSG AI scoring to the PSG expert scoring.

    Parameters:
    psg_file (str): Path to the PSG event file (psg_events.tsv).

    Returns:
    float: Percentage of agreement between AI and majority.
    """
    logging.info("Comparing PSG AI scoring with PSG expert scoring...")

    try:
        psg_df = pd.read_csv(psg_file, sep="\t")
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return None

    AWAKE_STAGE = 8

    # Filter out awake stage
    mask = psg_df["majority"] != AWAKE_STAGE
    psg_df = psg_df.loc[mask].reset_index(drop=True)

    if psg_df.empty:
        logging.warning("Filtered data is empty. Skipping comparison.")
        return None

    file_id = os.path.basename(psg_file).split("_")[0]

    # Compute percentage match
    match_percentage = (psg_df["ai_psg"] == psg_df["majority"]).mean() * 100

    logging.info(f"PSG AI comparison completed. Percentage match for patient {file_id}: {match_percentage:.2f}%")
    return match_percentage
