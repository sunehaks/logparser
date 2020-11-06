#!/usr/bin/env python

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logparser.SLCT import SLCT

input_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/logs/Sample_logs/'  # The input directory of log file
output_dir = 'SLCT_result/'  # The output directory of parsing results
log_file   = 'fin-transaction_log_anonimized.log'
#log_file   = 'HDFS_2k.log'  # The input log file name
#log_format    = '<Date> <Time> <Pid> <Level> <Component>: <Content>' # HDFS log format
#log_format = '<Date> <Time> <Level> <Router> <Pid>: <Month> <Day> <UTCTime>: <Component>: <Content>' # cisco_router log format
log_format = '<Date> <Time>,<Pid> <Level> <Initiator> [<Comment>] - <Content>'
support    = 750  # The minimum support threshold
regex      = []  # Regular expression list for optional preprocessing (default: [])

parser = SLCT.LogParser(log_format=log_format, indir=input_dir, outdir=output_dir, 
                        support=support, rex=regex)
parser.parse(log_file)
