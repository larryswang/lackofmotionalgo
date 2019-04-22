'''
This file is used to determine the maximum angular speed needed to trigger the lack of motion system
argument list:
argv[0]: name of the script
argv[1]: rotation file, *.txt form
argv[2]: Lack of Motion file name -- .txt expected
    enter the name before "-", this script will search for all txt files and process them
argv[3]: threshold for Lack of Motion file, the threshold for each sensor should be 
    argv[3] * sigma_i, wherein the sigma_i is the standard deviation of sensor i

This part of the algorithm is confidential
Please contact shiyuw@umich.edu at Biomechanics Research Lab
'''

import sys
import numpy as np
import glob

def main():
    if len(sys.argv) != 4:
        print("must specify 3 additional arugments, detials see script!")
        exit(1)
    
    th_lackofmotion = float(sys.argv[3])

    ### motion determined by lack of motion
    print("processing lack of motion sensor data files")
    ## read data from file
    print("calibrating lack of motion system")

    calibration_data = []
    with open(sys.argv[1] + "-1.txt") as f:
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

    ## auto-calibration for all sensors
    calibration_data = np.array(calibration_data)
    deviation = np.std(calibration_data, axis=0)
    
    move_top = []
    move_mid = []
    move_bot = []

    for filename in glob.glob(sys.argv[1] + "*.txt"):
        print("calibration done, processing file %s" % filename)

        data_lackofmotion = []
        with open(filename) as f:
            lines = f.readlines()
            for line in lines:
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

            ## detect motion happend during this time
            ## presented in string format time

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
                

    print("finish processing Lack of Motion data")

if __name__ == "__main__":
    main()