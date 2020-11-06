"""
Description : This file implements a wrapper around the original LogCluster code in perl
Author      : LogPAI team
License     : MIT
"""

import os
import pandas as pd
import re
import hashlib
from datetime import datetime
import subprocess


class LogParser():
    def __init__(self, indir, log_format, outdir, rex =[], support=None, rsupport=None, separator=None, lfilter=None, template=None,
                 lcfunc=None, syslog=None, wsize=None, csize=None, wweight=None, weightf=None, wfreq=None, wfilter=None,
                 wsearch=None, wrplace=None, wcfunc=None, outliers=None, readdump=None,
                 writedump=None, readwords=None, writewords=None,iteration=1, file_name = 'logcluster_input.log', initial_support = '10'):
        """
        Arguments
        ---------
            rsupport = < relative_support >
            separator = < word_separator_regexp >
            lfilter = < line_filter_regexp >
            template = < line_conversion_template >
            lcfunc = < perl_code >
            syslog = < syslog_facility >
            wsize = < word_sketch_size >
            csize = < candidate_sketch_size >
            wweight = < word_weight_threshold >
            weightf = < word_weight_function >
            wfreq = < word_frequency_threshold >
            wfilter = < word_filter_regexp >
            wsearch = < word_search_regexp >
            wreplace = < word_replace_string >
            wcfunc = < perl_code >
            outliers = < outlier_file >
            readdump = < dump_file >
            writedump = < dump_file >
            readwords = < word_file >
            writewords = < word_file >
            iteration =  < iteration_of_LogCluster >
        """
        self.path = indir
        self.log_format = log_format
        self.savepath = outdir
        self.paras = [support, rsupport, separator, lfilter, template,
                      lcfunc, syslog, wsize, csize, wweight, weightf, wfreq,
                      wfilter, wsearch, wrplace, wcfunc, outliers, readdump, writedump,
                      readwords, writewords, iteration, file_name, initial_support]
        self.paranames = ["support", "rsupport", "separator", "lfilter", "template", "lcfunc", "syslog",
                          "wsize", "csize", "wweight", "weightf", "wfreq", "wfilter", "wsearch", "wrplace",
                          "wcfunc", "outliers", "readdump", "writedump", "readwords", "writewords", "iteration", 
                          "file_name", "initial_support"]
        self.perl_command = "perl {} --input {}".format(os.path.join(os.path.dirname(__file__), 'logcluster.pl'), "logcluster_input.log")
        for idx, para in enumerate(self.paras):
            if para:
                self.perl_command += " -{} {}".format(self.paranames[idx], para)
        self.perl_command += " > logcluster_output.txt"
        self.rex = rex

    def parse(self, filename):
        start_time = datetime.now()
        filepath = os.path.join(self.path, filename)
        print('Parsing file: ' + filepath)
        self.filename = filename
        headers, regex = self.generate_logformat_regex(self.log_format)
#        print(headers, regex)
        self.df_log = self.log_to_dataframe(filepath, regex, headers, self.log_format)
        with open('logcluster_input.log', 'w') as fw:
            for line in self.df_log['Content']:
#                line = line.decode(errors='replace')
                if self.rex:
                    for currentRex in self.rex:
                        line = re.sub(currentRex, '', line)
                fw.write(line + '\n')
        try:
            print ("Run LogCluster command...\n>> {}".format(self.perl_command))
            subprocess.check_call(self.perl_command, shell=True)
        except:
            print("LogCluster run failed! Please check perl installed.\n")
            raise
        #os.remove("logcluster_input.log")
        #os.remove("logcluster_output.txt")

        # Write to logcluster_input.log file here
        lineNums = []
        with open("logcluster_output.txt", 'r') as fr: # this file has o/p of the algorithm. Where is that??
            for line in fr:
                line = line.split('\t')
                lineNum = line[1].split(',')
                lineNums.extend(lineNum)
        lineNums = [int(ele)-1 for ele in lineNums]
        new_df = self.df_log.drop(lineNums)
#        print(new_df.head())
        with open('logcluster_input.log', 'w') as fw:
            for line in new_df['Content']:
#                line = line.decode(errors='replace')
                if self.rex:
                    for currentRex in self.rex:
                        line = re.sub(currentRex, '', line)
                fw.write(line + '\n')
 #       self.df_log = self.df_log.merge(new_df, indicator = True, how = 'left').loc[lambda row : row['_merge']!='both']
        print('Parsing done. [Time taken: {!s}]'.format(datetime.now() - start_time))
        self.wirteResultToFile()


    def wirteResultToFile(self):
        if not os.path.isdir(self.savepath):
            os.makedirs(self.savepath)

        EventIdx_hash = [] # What's this ? The left-most code kind of thing in o/p_template.csv file
        LineID_EventIdx = {} # What's this ? A dictionary of indices with keys : lineNumbers, values : EventIdx
        Events = []
        Occurrences = [] # No. of occurances of a cluster
        EventIdx = 0 # What's this ?
        with open("logcluster_output.txt", 'r') as fr: # this file has o/p of the algorithm. Where is that??
            for line in fr:
#                print(line)
                line = line.split('\t')
                lineNums = line[1].split(',')
                Events.append(line[0].strip())
                EventIdx_hash.append(hashlib.md5(line[0].encode('utf-8')).hexdigest()[0:8])
                Occurrences.append(line[2].strip())
                for num in lineNums:
                    LineID_EventIdx[int(num)] = EventIdx
                EventIdx += 1

        EventTemplate = []
        EventId = []
        for i in range(self.df_log.shape[0]):
            i += 1
            e_idx = LineID_EventIdx.get(i, -1)
            if e_idx != -1 :
                EventTemplate.append(Events[e_idx])
                EventId.append(EventIdx_hash[e_idx])
            else:
                content = self.df_log.iloc[i-1]["Content"]
                EventTemplate.append(content)
                EventId.append(hashlib.md5(content.encode('utf-8')).hexdigest()[0:8])

        self.df_log["EventId"] = EventId
        self.df_log["EventTemplate"] = EventTemplate
        self.df_log["IterationNumber"] = self.paras[-3]
        

        eventDF = pd.DataFrame()
        eventDF['EventId'] = EventIdx_hash
        eventDF['EventTemplate'] = Events
        eventDF['Occurrences'] = Occurrences
        eventDF["IterationNumber"] = self.paras[-3]
#        print(self.paras[1],self.paras)
#        eventDF.to_csv(os.path.join(self.savepath, self.filename + '_templates_'+str(self.paras[1])+'_'+str(self.paras[-1])+'_'+'.csv'), index=False)
        if self.paras[-3] == 1:
            eventDF.to_csv(os.path.join(self.savepath, self.filename + '_templates_'+str(self.paras[1])+'.csv'), index=False,header=True, mode = 'w')
        else :
            eventDF.to_csv(os.path.join(self.savepath, str(self.paras[-2]) + '_templates_' + str(self.paras[-1]) +'.csv'), index=False,header=False, mode = 'a')

        occ_dict = dict(self.df_log['EventTemplate'].value_counts())
        df_event = pd.DataFrame()
        df_event['EventTemplate'] = self.df_log['EventTemplate'].unique()
        df_event['Occurrences'] = df_event['EventTemplate'].map(occ_dict)
        df_event['EventId'] = df_event['EventTemplate'].map(lambda x: hashlib.md5(x.encode('utf-8')).hexdigest()[0:8])
        if self.paras[-3] == 1: # self.paras[-3] --> iteration
            self.df_log.to_csv(os.path.join(self.savepath, self.filename + '_structured_'+str(self.paras[1])+'.csv'), index=False)
        else :
            self.df_log.to_csv(os.path.join(self.savepath, str(self.paras[-2]) + '_structured_' + str(self.paras[-1]) +'.csv'), index=False, header = None, mode = 'a')

#        self.df_log.to_csv(os.path.join(self.savepath, self.filename + '_structured_'+str(self.paras[1])+'_'+str(self.paras[-1])+'_'+'.csv'), index=False)

    def log_to_dataframe(self, log_file, regex, headers, logformat):
        """ Function to transform log file to dataframe 
        """
        log_messages = []
        linecount = 0
        print(log_file)
        with open(log_file, 'rb') as fin:
            for line in fin.readlines():
                line = line.decode(errors='replace')
                try:
                    match = regex.search(line.strip())
                    message = [match.group(header) for header in headers]
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    pass
        logdf = pd.DataFrame(log_messages, columns=headers)
        logdf.insert(0, 'LineId', None)
        logdf['LineId'] = [i + 1 for i in range(linecount)]
        return logdf

    def generate_logformat_regex(self, logformat):
        """ Function to generate regular expression to split log messages
        """
        headers = []
        splitters = re.split(r'(<[^<>]+>)', logformat)
        regex = ''
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(' +', r'\\s+', splitters[k])
                regex += splitter
            else:
                header = splitters[k].strip('<').strip('>')
                regex += '(?P<%s>.*?)' % header
                headers.append(header)
        regex = re.compile('^' + regex + '$')
        return headers, regex