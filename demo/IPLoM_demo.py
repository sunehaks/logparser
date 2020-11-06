#!/usr/bin/env python

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logparser import IPLoM

input_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/logs/Sample_logs/'  # The input directory of log file
output_dir   = 'IPLoM_result/'  # The output directory of parsing results
log_file   = 'cisco_router.log'
#log_file   = 'HDFS_2k.log'  # The input log file name
#log_format    = '<Date> <Time> <Pid> <Level> <Component>: <Content>' # HDFS log format
log_format = '<Date> <Time> <Level> <Router> <Pid>: <Month> <Day> <UTCTime>: <Component>: <Content>' # cisco_router log format
#log_format = '<Date> <Time>,<Pid> <Level> <Initiator> [<Comment>] - <Content>'
maxEventLen  = 200  # The maximal token number of log messages (default: 200)
step2Support = 6  # The minimal support for creating a new partition (default: 0)
CT           = 0.35  # The cluster goodness threshold (default: 0.35)
lowerBound   = 0.25  # The lower bound distance (default: 0.25)
upperBound   = 1.0  # The upper bound distance (default: 0.9)
regex        = []  # Regular expression list for optional preprocessing (default: [])

parser = IPLoM.LogParser(log_format=log_format, indir=input_dir, outdir=output_dir,
                         maxEventLen=maxEventLen, step2Support=step2Support, CT=CT, 
                         lowerBound=lowerBound, upperBound=upperBound, rex=regex)
parser.parse(log_file)
