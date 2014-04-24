#! /bin/bash

# 
# Download the various geographic datasets. This helps us look up county
# codes, zip coes, etc. 
# 
python /home/ferry/pydata/census/geography.py /home/ferry/pydata/data

#
# Create the economic datasets.
#
python /home/ferry/pydata/census/population.py economic Tennessee /home/ferry/pydata/data/ /home/ferry/pydata/data/tn_econ.psv
python /home/ferry/pydata/census/population.py economic Texas /home/ferry/pydata/data/ /home/ferry/pydata/data/tx_econ.psv
python /home/ferry/pydata/census/population.py economic Kentucky /home/ferry/pydata/data/ /home/ferry/pydata/data/ky_econ.psv

#
# Create the median income plots and output to an HTML file. 
#
python /home/ferry/pydata/bokeh/init.py
python /home/ferry/pydata/bokeh/plot.py Tennessee tn /home/ferry/pydata/data/tn_econ.psv /home/ferry/pydata/bokeh/templates/
python /home/ferry/pydata/bokeh/plot.py Texas tx /home/ferry/pydata/data/tx_econ.psv /home/ferry/pydata/bokeh/templates/
python /home/ferry/pydata/bokeh/plot.py Kentucky ky /home/ferry/pydata/data/ky_econ.psv /home/ferry/pydata/bokeh/templates/