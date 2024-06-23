Steps to Success: 
0) Learning: learn how to get the GPS to talk to the pi to talk to the screen
1) Circuit work: get everything to connect electrically
2) Implement the talking
3) Design an enclosure


It's best to do this all in a venv

Dependencies: 
1) pip install reverse_geocoder


Notes: 
1) The file data/rg_cities1000.csv must be copied to $VENV/lib/$PYTHON_VER/site-packages/reverse_geocoder. The one in the repo is a much truncated version of the full file. Truncation is ok since we're only gonna be in CO with this (likely).  
