import pandas as pd

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