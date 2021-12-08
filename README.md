# Data Extraction

## frames_to_pos.csv
Converts mp4s to a list of jpgs (was honestly just easier for me to comb through - I know this isn't necessary) 

## mp4_to_sequence_csv.py
Converts the jpgs from the previous file to pos csv

## data.csv
The data csv is labeled:

Lift, Frame, Label, joint_0_x, joint_1_x ... joint_33_x, joint_0_y ... joint_0_z ... joint_0_c

where x, y, z show the coordinates (normalized to the height and width of the image) and c shows confidence
