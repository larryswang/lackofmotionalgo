'''
This file is used to calculate TP/FP used to draw the ROC curve
argument list:
argv[0]: name of the script
argv[1]: Lack of Motion file name -- .txt expected
    enter the name before "-", this script will search for all txt files and process them
argv[2]: BodiTrak mat file name -- .xlsx expected
argv[3]: threshold for Lack of Motion file, the threshold for each sensor should be 
    argv[3] * sigma_i, wherein the sigma_i is the standard deviation of sensor i
argv[4]: threshold for BodiTrak mat, the threshold should be in format of (mmHg)^2 of pressure square change

This part of the algorithm is confidential
Please contact shiyuw@umich.edu at Biomechanics Research Lab
'''
import sys
import numpy as np
import pdb
import glob
import xlrd

def main():

    if len(sys.argv) != 5:
        print("must specify 4 additional arugments, detials see script!")
        exit(1)
    
    th_lackofmotion = float(sys.argv[3])
    th_boditrak = float(sys.argv[4])

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

    print("The motion detected by Lack of Motion data system")
    print("top motion:")
    print(move_top)
    print("mid motion:")
    print(move_mid)
    print("bot motion:")
    print(move_bot)

    ### motion determined by BodiTrak system
    ### please make sure that the usb is at head side
    print("loading BodiTrak excel data, it may take a while")
    
    wb = xlrd.open_workbook(sys.argv[2]) 
    sheet = wb.sheet_by_index(0)

    print("finish loading xls file")
    ncols = sheet.ncols
    nrows = sheet.nrows

    move_top_boditrak = []
    move_mid_boditrak = []
    move_bot_boditrak = []

    last_pressure_map = None

    for j in range(1, ncols):
        curtime = sheet.cell_value(1, j)
        cur_pressure_map = np.zeros((1728))

        for i in range(13, 1740):
            cur_pressure_map[i-13] = sheet.cell_value(i, j)

        ## compare with pressure map in the last frame to determine any motion
        if last_pressure_map is None:
            last_pressure_map = cur_pressure_map
            continue
        
        top_diff = np.linalg.norm(cur_pressure_map[:540] - last_pressure_map[:540], 2)
        mid_diff = np.linalg.norm(cur_pressure_map[540:1216] - last_pressure_map[540:1216], 2)
        bot_diff = np.linalg.norm(cur_pressure_map[1216:] - last_pressure_map[1216:], 2)

        if top_diff > th_boditrak:
            move_top_boditrak.append(curtime)
        if mid_diff > th_boditrak:
            move_mid_boditrak.append(curtime)
        if bot_diff > th_boditrak:
            move_bot_boditrak.append(curtime)

        last_pressure_map = cur_pressure_map
    
    print("The motion detected by BodiTrak system")
    print("top motion:")
    print(move_top_boditrak)
    print("mid motion:")
    print(move_mid_boditrak)
    print("bot motion:")
    print(move_bot_boditrak)

if __name__ == "__main__":
    main()