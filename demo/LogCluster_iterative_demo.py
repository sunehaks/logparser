#!/usr/bin/env python
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from logparser.LogCluster import LogCluster_iterative

# Hyperparameter tuning for cisco_router.log :
numIterations = 27 # Hyperparameter that needs to be tuned.
rsupports = [23.9, 23, 9, 9, 9, 8, 8, 8, 7, 26.7, 7, 7, 8, 7, 10.1, 7, 5, 9, 5,7,5, 8.6, 5, 8, 5, 5]
initial_support = 20
file_name = "cisco_router.log"

# Hyperparameter tuning for 'fin-transaction_log_anonimized.log'
# numIterations = 9
# rsupports = [2.7, 2.95, 2, 2, 2, 1.47, 3.18, 2.3]
# file_name = 'fin-transaction_log_anonimized.log'
# initial_support = 2.29
for iteration in range(1,numIterations+1):
    if iteration==1:
        input_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/logs/Sample_logs/'  # The input directory of log file
        output_dir = 'LogCluster_result/financial_transaction_results/Iterative_results'#cisco_router_results/Iterative_results' # The output directory of parsing results
        log_file   = file_name#'cisco_router.log'
        log_format = '<Date> <Time> <Level> <Router> <Pid>: <Month> <Day> <UTCTime>: <Component>: <Content>' # cisco_router log format
#        log_format = '<Date> <Time> <Level> <Module> \[<StatusAndPayThread>\] - <Content>'
        rsupport   = initial_support # The minimum threshold of relative support, 10 denotes 10%
        regex      = []
    else :
        input_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # The input directory of log file
        output_dir = 'LogCluster_result/financial_transaction_results/Iterative_results'#cisco_router_results/Iterative_results' # The output directory of parsing results
        log_file   = 'logcluster_input.log'
        log_format = '<Content>'
        rsupport   = rsupports[iteration-2] # The minimum threshold of relative support, 10 denotes 10%
        regex      = []

    print("Iteration : ",iteration)
    parser = LogCluster_iterative.LogParser(input_dir, log_format, output_dir, rsupport=rsupport, iteration=iteration, file_name = file_name, initial_support= initial_support)
    parser.parse(log_file)