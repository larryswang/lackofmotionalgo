# Lack of Motion Algorithm

## Files
README.md     introductory files

ROCcurve.py   the file used to generate ROC curve

rotation.py   the file used to align rotation

20190405-1.txt example data from lack of motion system

20190405.xlsx example data from BodiTrak system

data.txt example data from wearable IMU sensor

## ROCcurve.py
Example call: 
`python ROCcurve.py 20190405 20190405.xlsx 3 1`

Meaning of different arguments see script

This file is used to get movement timestamps of both lack of motion system and boditrak system and print in terminal. To dump the output into a file, simply use

`python ROCcurve.py 20190405 20190405.xlsx 3 1 > output.txt`

## rotation.py
Example call:
`python3.7 rotation.py data.txt 20190405 3 1`

Meaning of different arguments see script

This file is used to get movement timestamps of both lack of motion system and wearing IMU to print in terminal. To dump the output into a file, see above.