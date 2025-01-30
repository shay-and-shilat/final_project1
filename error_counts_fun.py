import pandas as pd

def error_houers_count (headbend_file):
    #read the file, sep="\t" because the files are in tsv format
    headbend_file= pd.read_csv(headbend_file, sep="\t")
    headbend_file= headbend_file['ai_hb']==-2
    houers_count=(headbend_file.sum()*30)/3600
    return houers_count
m=error_houers_count ('sub-1_task-Sleep_acq-headband_events.tsv')
print(m)