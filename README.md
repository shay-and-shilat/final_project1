-Sleep_Analysis-AI_vs_Experts-

Overview
This project evaluates the accuracy of AI models in classifying sleep stages using data from two sources: a wearable EEG headband and a PSG (Polysomnography) system.
The dataset includes recordings from one participant over 30 nights, with sleep stages labeled by both AI models and human experts. Each file contains 30-second segments of the night, indicating the sleep stage during that time.
The project compares the AI’s sleep stage classifications against the expert-labeled stages, using the expert labels as the “ground truth” for accuracy.
It analyzes the performance of the AI using:
Headband EEG Data – AI classifications from the headband data.
PSG Data – AI classifications from the PSG data.
By comparing the results from both sources, the project assesses how well AI can classify sleep stages, considering the type and quality of data available.
Data
Link to the data: https://openneuro.org/datasets/ds005555/versions/1.0.0
We used data of 30 nights.

The sleep stages label:
0: Wake,
1: NonREM sleep stage 1 (N1),
2: NonREM sleep stage 2 (N2),
3: NonREM sleep stage 3 (N3),
4: REM sleep,
8: PSG disconnections (e.g., due to bathroom breaks; human-scored only)
-2: Artifacts and missing data (AI-scored only)

The functions
find_event_files: Find and the relevant data files 
headbend_vs_majority: Compare AI using EEG headbend data classifications with expert labels of sleep stage
aispg_vs_majority: Compare AI using PSG data classifications with expert labels of sleep stage
error_hours_count: count how many hours of sleep were unusable data
total_sleeping_hours: count how many hours of sleep were in total
review_subjects: takes input from user and gives output based on the user's answer
plot_sleep_stages_over_time: Visualize the results

how to use the project
run the program in the "all.py" file. the program will then return the comparison "PSG AI scoring with PSG expert scoring" and "headband AI scoring with PSG expert" results for each experiment night, as well as the avarage comparison rates for all nights and the amount of missing data from headband experiment. the program will then ask the user to enter a subject number they would like to review (the meaning is what experiment night they want to review). after entering a number, the program will show the user two plots containing information about the spesific night number the user picked - the first plot shows the different sleep stages from that night based on the expert's analisys, ant the second plot shows the different sleep stages that the headband ai, psg ai and psg experts gave the patient in the same night.
the program will then ask the user if they would like to review another subject's data. if the user replies "y", the program will once again ask them to choose a subject number. is the user replies "n", the program will be exited. 