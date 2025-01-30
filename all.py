import pandas as pd
import os
import statistics

def find_event_files(base_folder):
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
    mis_mask = (ai_file['ai_hb'] != -2)

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

def error_houers_count (headbend_file):
    #read the file, sep="\t" because the files are in tsv format
    headbend_file= pd.read_csv(headbend_file, sep="\t")
    
    headbend_file= headbend_file['ai_hb']==-2
    houers_count=(headbend_file.sum()*30)/3600
    return houers_count

hb_vs_mj_sec=[]
psgai_vs_mj_sec=[]
error_houers=0
headband_files, psg_files= find_event_files('files_for_python_project')
for headband_file, psg_file in zip(headband_files, psg_files): #make sure that the files are matching to the same sub
     hb_vs_mj_sec.append(headbend_vs_majority(headband_file,psg_file))
     psgai_vs_mj_sec.append(aispg_vs_majority(psg_file))
     error_houers= error_houers_count(headband_file)+error_houers

hb_vs_mj_sec = [x for x in hb_vs_mj_sec if x is not None] #filter out all the "none"s


print (f"we found {round(statistics.mean(hb_vs_mj_sec),2)}% match between the headbend AI and the majority")
print (f"we found {round(statistics.mean(psgai_vs_mj_sec),2)}% match between the PSG AI and the majority")
print (f"there were {round(error_houers,2)} houers of missimg data from the headbend in total")

