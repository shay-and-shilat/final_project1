import pandas as pd
import logging
import os

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to compare headband AI scoring with the majority expert scoring
def headbend_vs_majority(headband_files, psg_files):
    """
    Compares headband AI scoring to the majority expert scoring.
    
    Parameters:
    ai_file (str): Path to the headband AI scoring file (headband_events.tsv).
    experts_file (str): Path to the expert majority scoring file (psg_events.tsv).
    
    Returns:
    float or None: Percentage of agreement between AI and majority, or None if the error rate is too high.
    """
    logging.info("Comparing headband AI scoring with psg expert scoring...")
    
    try:
        ai_file = pd.read_csv(headband_files, sep="\t") 
        experts_file = pd.read_csv(psg_files, sep="\t")
    except Exception as e:
        logging.error(f"Error reading files: {e}")
        return None

    dis_mask = (experts_file['majority'] != 8)
    experts_file = experts_file[dis_mask].reset_index(drop=True)
    ai_file = ai_file[dis_mask].reset_index(drop=True)

    file_id = os.path.basename(headband_files).split("_")[0]
    ai_error = ai_file['ai_hb'] == -2
    error_pr = (ai_error.sum() / len(ai_file)) * 100

    if error_pr >= 40:
        logging.warning("Error rate is too high, skipping comparison.")
        return None

    mis_mask = (ai_file['ai_hb'] != -2)
    experts_file = experts_file[mis_mask].reset_index(drop=True)
    ai_file = ai_file[mis_mask].reset_index(drop=True)

    hb_vs_maj = ai_file['ai_hb'] == experts_file['majority']
    precent_match = (hb_vs_maj.sum() / len(hb_vs_maj)) * 100

    logging.info(f"Comparison completed. Percentage match for patient {file_id}: {precent_match}%")
    return precent_match

# Function to compare PSG AI scoring with the majority expert scoring
def aispg_vs_majority(psg_files):
    """
    Compares PSG AI scoring to the PSG expert scoring.
    
    Parameters:
    psg_file (str): Path to the PSG event file (psg_events.tsv).
    
    Returns:
    float: Percentage of agreement between AI and majority.
    """
    logging.info("Comparing PSG AI scoring with PSG expert scoring...")
    
    try:
        psg_file = pd.read_csv(psg_files, sep="\t")
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        return None

    mask = (psg_file['majority'] != 8)
    psg_file = psg_file[mask].reset_index(drop=True)


    file_number = os.path.basename(psg_files).split("_")[0]
    aipsg_vs_maj = psg_file['ai_psg'] == psg_file['majority']
    precent_match = (aipsg_vs_maj.sum() / len(psg_file)) * 100
    
    logging.info(f"PSG AI comparison completed. Percentage match for patient {file_number}: {precent_match}%")
    return precent_match