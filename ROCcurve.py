'''
This file is used to calculate TP/FP used to draw the ROC curve
argument list:
arg[0]: name of the script
arg[1]: Lack of Motion file name -- .txt expected
arg[2]: BodiTrak mat file name -- .xlsx expected
arg[3]: threshold for Lack of Motion file, the threshold for each sensor should be 
    arg[3] * sigma_i, wherein the sigma_i is the standard deviation of sensor i
arg[4]: threshold for BodiTrak mat, the threshold should be in format of mmHg of pressure change

This part of the algorithm is confidential
Please contact shiyuw@umich.edu at Biomechanics Research Lab
'''
import sys
import numpy as np
import pdb

def main():

    if len(sys.argv) != 5:
        print("must specify 4 additional arugments, detials see script!")
        exit(1)
    
    th_lackofmotion = float(sys.argv[3])
    th_boditrak = float(sys.argv[4])

    ### motion determined by lack of motion

    ## read data from file
    data_lackofmotion = []
    calibration_data = []
    
    with open(sys.argv[1]) as f:
        lines = f.readlines()
        for line in lines:
            if len(calibration_data) < 1000 and line[:3] != "AVE":
                line = line.strip().split()[1:]
                line[0] = float(line[0])
                line[1] = float(line[1])
                line[2] = float(line[2])
                line[3] = float(line[3])
                line[4] = float(line[4])
                line[5] = float(line[5])
                calibration_data.append(line)
            if line[:3] == "AVE":
                line = line[3:].strip().split()
                ## [timestring, sensor1, sensor2, sensor3, sensor4, sensor5, sensor6]
                line[1] = float(line[1])
                line[2] = float(line[2])
                line[3] = float(line[3])
                line[4] = float(line[4])
                line[5] = float(line[5])
                line[6] = float(line[6])
                data_lackofmotion.append(line)

    ## auto-calibration for all sensors
    calibration_data = np.array(calibration_data)
    deviation = np.std(calibration_data, axis=0)

    ## detect motion happend during this time
    ## presented in string format time
    
    move_top = []
    move_mid = []
    move_bot = []

    for i in range(len(data_lackofmotion)):
        if i >= 3:
            if abs(data_lackofmotion[i][1] - data_lackofmotion[i-3][1]) >= th_lackofmotion * deviation[0] or\
                abs(data_lackofmotion[i][4] - data_lackofmotion[i-3][4]) >= th_lackofmotion * deviation[3] :
                move_top.append(data_lackofmotion[i][0])

            if abs(data_lackofmotion[i][2] - data_lackofmotion[i-3][2]) >= th_lackofmotion * deviation[1] or\
                abs(data_lackofmotion[i][5] - data_lackofmotion[i-3][5]) >= th_lackofmotion * deviation[4] :
                move_mid.append(data_lackofmotion[i][0])

            if abs(data_lackofmotion[i][3] - data_lackofmotion[i-3][3]) >= th_lackofmotion * deviation[2] or\
                abs(data_lackofmotion[i][6] - data_lackofmotion[i-3][6]) >= th_lackofmotion * deviation[5] :
                move_bot.append(data_lackofmotion[i][0])
                
    

if __name__ == "__main__":
    main()