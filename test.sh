#!/bin/bash
echo "testing rand.py | armodel.py | ewma.py > armodel.data"
python rand.py | python armodel.py | python ewma.py > armodel.data

#test the moving average code for its arguments and chain ability
echo "testing moving average works to std out"
python moving_average.py 50 2 
echo "testing moving average works with unix file redirection"
python moving_average.py 500 2  > "mamodel.data"
echo "testing  average works with pipe to ewma"
python moving_average.py 500 10 | python ewma.py > mamodel_smoothed.data

#test the plotter
echo "about to plot all files ending in .data, prepare for gui!"
python -i plotter *.data
echo "we made the plots! or crashed"
