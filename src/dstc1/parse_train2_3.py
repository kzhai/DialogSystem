"""
@author: Ke Zhai (zhaikedavy@gmail.com)
"""

import nltk
import scipy

import re
import os
import json
import sys
import time

from parse_util import parse_system_transcripts
from parse_util import parse_user_transcripts

#import num2word;
#n2w = num2word.Num2Word();

def parse(input_directory, output_file, mapping_semantics=False):
    output_stream = open(output_file, 'w');
    for split_by_index in os.listdir(input_directory):
        data_split_by_date_index = os.path.join(input_directory, split_by_index);
        if os.path.isfile(data_split_by_date_index):
            print "skip file %s" % data_split_by_date_index;
            continue;
        
        dialog_file_path = os.path.join(data_split_by_date_index, "dstc.log.json")
        
        json_data=open(dialog_file_path);
        data = json.load(json_data);
    
        session_id = data['session-id']
        for turn_index in xrange(len(data['turns'])):
            turn = data['turns'][turn_index];
            
            debug_info = (session_id, turn_index)
            
            system_transcript, system_acts = parse_system_transcripts(turn, mapping_semantics, debug_info);
            
    
            assert "input" in turn, (session_id, turn_index, turn)
            assert "live" in turn['input'], (session_id, turn_index, turn['input'])
            assert "asr-hyps" in turn['input']['live'], (session_id, turn_index, turn['input']['live'])
            assert "slu-hyps" in turn['input']['live'], (session_id, turn_index, turn['input']['live'])
    
            user_transcript, user_acts = parse_user_transcripts(turn, mapping_semantics, debug_info);
            
            #output_stream.write("%s\t%d\t%s\t%s\n" % (session_id, turn_index, system_transcript, user_transcript));
            output_stream.write("%s\t%d\t%s\t%s\t%s\t%s\n" % (session_id, turn_index, system_transcript, " ".join(system_acts), user_transcript, " ".join(user_acts)));
    
        json_data.close()

if __name__ == "__main__":
    input_directory = sys.argv[1];
    output_file = sys.argv[2];
    parse(input_directory, output_file);