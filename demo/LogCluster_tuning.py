#!/usr/bin/env python
import sys,os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logparser.LogCluster import LogCluster

for rsupport in np.arange(2.29, 2.3,0.1):
    input_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/logs/Sample_logs/'  # The input directory of log file
    output_dir = 'LogCluster_result/financial_transaction_results' # The output directory of parsing results
    log_file   = 'fin-transaction_log_anonimized.log'
    #log_file   = 'HDFS_2k.log'  # The input log file name
    #log_format    = '<Date> <Time> <Pid> <Level> <Component>: <Content>' # HDFS log format
#    log_format = '<Date> <Time> <Level> <Router> <Pid>: <Month> <Day> <UTCTime>: <Component>: <Content>' # cisco_router log format
    log_format = '<Date> <Time> <Level> <Module> \[<StatusAndPayThread>\] - <Content>'
    #rsupport   = 10 # The minimum threshold of relative support, 10 denotes 10%
    regex      = [] # Regular expression list for optional preprocessing (default: [])
    print('rsupport :', round(rsupport,2))
    parser = LogCluster.LogParser(input_dir, log_format, output_dir, rsupport=round(rsupport,2))
    parser.parse(log_file)
