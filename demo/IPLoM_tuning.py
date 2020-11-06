#!/usr/bin/env python

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import numpy as np
from logparser import IPLoM

folder_name = 'Tuning_CT' # Mention the parameter that you are Tuning
input_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/logs/Sample_logs/'  # The input directory of log file
output_dir   = 'IPLoM_result/financial_transaction_results/Tuning_results/' + folder_name  # The output directory of parsing results
log_file   = 'fin-transaction_log_anonimized.log'
#log_file   = 'HDFS_2k.log'  # The input log file name
#log_format    = '<Date> <Time> <Pid> <Level> <Component>: <Content>' # HDFS log format
#log_format = '<Date> <Time> <Level> <Router> <Pid>: <Month> <Day> <UTCTime>: <Component>: <Content>' # cisco_router log format
log_format = '<Date> <Time> <Level> <Module> \[<StatusAndPayThread>\] - <Content>'

for CT in np.arange(0.3,.45, .01):
    maxEventLen  = 200  # The maximal token number of log messages (default: 200)
#    CT           = 0.35  # The cluster goodness threshold (default: 0.35)
    lowerBound   = 0.25  # The lower bound distance (default: 0.25)
    upperBound   = 0.9  # The upper bound distance (default: 0.9)
    regex        = []  # Regular expression list for optional preprocessing (default: [])
    step2Support = 0

    parser = IPLoM.LogParser(log_format=log_format, indir=input_dir, outdir=output_dir,
                            maxEventLen=maxEventLen, step2Support=step2Support, CT=round(CT,2), 
                            lowerBound=lowerBound, upperBound=upperBound, rex=regex)
    parser.parse(log_file)
