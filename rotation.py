'''
This file is used to determine the maximum angular speed needed to trigger the lack of motion system
argument list:
argv[0]: name of the script
argv[1]: rotation file, *.txt form
argv[2]: Lack of Motion file name -- .txt expected
    enter the name before "-", this script will search for all txt files and process them
argv[3]: threshold for Lack of Motion file, the threshold for each sensor should be 
    argv[3] * sigma_i, wherein the sigma_i is the standard deviation of sensor i
argv[4]: axis selected for rotation file, 1 for x axis, 2 for y axis and 3 for z axis

This part of the algorithm is confidential
Please contact shiyuw@umich.edu at Biomechanics Research Lab
'''

import sys
import numpy as np
import glob

def main():
    if len(sys.argv) != 5:
        print("must specify 4 additional arugments, detials see script!")
        exit(1)
    
    th_lackofmotion = float(sys.argv[3])

    ### motion determined by lack of motion
    print("processing lack of motion sensor data files")
    ## read data from file
    print("calibrating lack of motion system")

    calibration_data = []
    with open(sys.argv[2] + "-1.txt") as f:
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

    for filename in glob.glob(sys.argv[2] + "*.txt"):
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
    print("The motion detected by Lack of Motion data system")
    print("top motion:")
    print(move_top)
    print("mid motion:")
    print(move_mid)
    print("bot motion:")
    print(move_bot)

    ### process rotation file
    print("processing rotation file")

    rot_10 = []
    rot_20 = []
    rot_30 = []

    axis = int(sys.argv[4])

    with open(sys.argv[1]) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()

            line[1] = float(line[1])
            line[2] = float(line[2])
            line[3] = float(line[3])

            if abs(line[axis] - 10) <= 1:
                rot_10.append(line[0])
            
            elif abs(line[axis] - 20) <= 1:
                rot_20.append(line[0])

            elif abs(line[axis] - 30) <= 1:
                rot_30.append(line[0])

    print("finish processing rotation file")
    print("rot at 10 degree:")
    print(rot_10)
    print("rot at 20 degree:")
    print(rot_20)
    print("rot at 30 degree:")
    print(rot_30)
    

if __name__ == "__main__":
    main()