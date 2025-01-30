import pandas as pd

def headbend_vs_majority (ai_file, experts_file):

    #read the files, sep="\t" because the files are in tsv format
    ai_file= pd.read_csv(ai_file, sep="\t") 
    experts_file= pd.read_csv(experts_file, sep="\t")

    #create a mask for rows where 'majority' is 8 (8=PSG disconnections (e.g., due to bathroom breaks; human-scored only))
    dis_mask = (experts_file['majority'] != 8)

    #apply the mask to both dataframes and reset the index
    experts_file = experts_file[dis_mask].reset_index(drop=True)
    ai_file = ai_file[dis_mask].reset_index(drop=True)

    # Identify rows where AI marked the data as artifacts (-2= Artifacts and missing data (AI-scored only))
    ai_error= ai_file['ai_hb']== -2
    # If more than 40% of the data consists of artifacts, return None
    error_pr= (ai_error.sum()/len(ai_file))*100
    if error_pr>=40:
        return None
    

    #create a mask for rows where 'hb_ai' is -2 (-2= Artifacts and missing data (AI-scored only))
    mis_mask = (ai_file['hb_ai'] != -2)

    #apply the mask to both dataframes and reset the index
    experts_file = experts_file[mis_mask].reset_index(drop=True)
    ai_file = ai_file[mis_mask].reset_index(drop=True)

    hb_vs_maj= []
    hb_vs_maj= ai_file['ai_hb']==experts_file['majority']
    precent_match= (hb_vs_maj.sum()/len(hb_vs_maj))*100
    return precent_match

def aispg_vs_majority (psg_file):

    #read the files, sep="\t" because the files are in tsv format
    psg_file= pd.read_csv(psg_file, sep="\t")

    #create a mask for rows where 'majority' is 8 (8=PSG disconnections (e.g., due to bathroom breaks; human-scored only))
    mask = (psg_file['majority'] != 8)

    #apply the mask to both dataframes and reset the index
    psg_file = psg_file[mask].reset_index(drop=True)
    
    aipsg_vs_maj= []
    aipsg_vs_maj= psg_file['ai_psg']==psg_file['majority']
    precent_match= (aipsg_vs_maj.sum()/len(psg_file))*100
    return precent_match