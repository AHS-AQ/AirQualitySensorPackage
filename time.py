import os
import sys
import time
import datetime

st = []
try:
    ts = time.time()
    sttime = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d,%H:%M:%S')
    ssttime = sttime.strip("'")
    st=''.join(sttime)
    print(st)
#   print(datetime.datetime.now())
#some more things but nothing else of interest for here

except:
#   error = "ERROR! No file 'bla' found!"
#   log = 'log.txt'
#   logfile = file.open(log, "w")
#   logfile.write(sttime + error + '\n')
#   logfile.close()
    sys.exit(0)
