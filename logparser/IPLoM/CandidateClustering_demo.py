#!/usr/bin/env python

import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import numpy as np
from logparser.IPLoM import CandiateClustering as IPLoM
from logparser.LogCluster import LogCluster_iterative

#from logparser.LogCluster import LogCluster_iterative

input_dir  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/logs/Sample_logs/'  # The input directory of log file
output_dir   = 'CandidateClusteringResult'  # The output directory of parsing results
log_file   = 'fin-transaction_log_anonimized.log'
log_format = '<Date> <Time> <Level> <Module> \[<StatusAndPayThread>\] - <Content>'
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

# Applying iterative logCluster on IPLoM results
# Hyperparameter tuning for cisco_router.log :
# numIterations = 27 # Hyperparameter that needs to be tuned.
# rsupports = [23.9, 23, 9, 9, 9, 8, 8, 8, 7, 26.7, 7, 7, 8, 7, 10.1, 7, 5, 9, 5,7,5, 8.6, 5, 8, 5, 5]
# initial_support = 20
# file_name = "cisco_router.log"

# Hyperparameter tuning for 'fin-transaction_log_anonimized.log'
numIterations = 5
rsupports = [1.5, 1.2, 1, 0.0001, 2.95, 2, 2, 2, 1.47, 3.18, 2.3]
file_name = 'output.log'
initial_support = 2
for iteration in range(1,numIterations+1):
    if iteration==1:
        input_dir  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))+'/CandidateClusteringResult'  # The input directory of log file
        output_dir = 'CandidateClusteringResult'  # The output directory of parsing results
        log_file   = file_name#'cisco_router.log'
        log_format = '<Content>' # cisco_router log format
#        log_format = '<Date> <Time> <Level> <Module> \[<StatusAndPayThread>\] - <Content>'
        rsupport   = initial_support # The minimum threshold of relative support, 10 denotes 10%
        regex      = []
    else :
        input_dir  = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # The input directory of log file
        output_dir = 'CandidateClusteringResult'  # The output directory of parsing results
        log_file   = 'logcluster_input.log'
        log_format = '<Content>'
        rsupport   = rsupports[iteration-2] # The minimum threshold of relative support, 10 denotes 10%
        regex      = []

    print("Iteration : ",iteration)
    parser = LogCluster_iterative.LogParser(input_dir, log_format, output_dir, rsupport=rsupport, iteration=iteration, file_name = file_name, initial_support= initial_support)
    parser.parse(log_file)
