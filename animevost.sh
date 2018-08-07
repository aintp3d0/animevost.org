#!/bin/bash

# read html and get <script> var data = {"SERIES ID": VIDEOS ID} </script>
# store data in file: series.txt
curl "$1" | grep -i "var data = {" > series.txt

# running script python3 to parse file series.txt and download series
python3 down_series.py
