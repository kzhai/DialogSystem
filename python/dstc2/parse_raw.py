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

#import num2word;
#n2w = num2word.Num2Word();

time_pattern = re.compile(r'(\d+):(\d+)( [ap]m)?');
ampm_pattern = re.compile(r' [ap] m?');
post_route_pattern = re.compile(r'(\d+)(\D?)');
pre_route_pattern= re.compile(r'(\D?)(\d+)');
multiple_spaces = re.compile(r' +');

singleton_pattern = re.compile(r' [^ai] ');

month_dictionary = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];

def parse(input_directory, config_directory, output_directory, mapping_semantics=True):
    train_list_file = os.path.join(config_directory, "dstc2_train.flist")
    train_output_file = os.path.join(output_directory, "train.dat")
    parse_data_split(input_directory, train_list_file, train_output_file, mapping_semantics);
    
    dev_list_file = os.path.join(config_directory, "dstc2_dev.flist")
    dev_output_file = os.path.join(output_directory, "dev.dat")
    parse_data_split(input_directory, dev_list_file, dev_output_file, mapping_semantics);
    
def parse_data_split(input_directory, list_file_path, output_file_path, mapping_semantics):
    list_file_stream = open(list_file_path, 'r');
    output_stream = open(output_file_path, 'w');
    for line in list_file_stream:
        line = line.strip();
        dialog_file_path = os.path.join(input_directory, line, "log.json");

        json_data=open(dialog_file_path);
        data = json.load(json_data);
        
        session_id = data['session-id']
        for turn_index in xrange(len(data['turns'])):
            turn = data['turns'][turn_index];
            
            assert "output" in turn, (session_id, turn_index, turn)
            if "transcript" not in turn["output"]:
                sys.stderr.write("Missing transcript from system for session %s turn %d\n" % (session_id, turn_index));
                system_transcript = "";
            else:
                system_transcript = turn['output']['transcript'].lower().strip();
                
                if mapping_semantics:
                    system_transcript = re.sub(time_pattern, "<time>", system_transcript);
                    system_transcript = re.sub(post_route_pattern, " \\1 \\2 ", system_transcript);
                    system_transcript = re.sub(pre_route_pattern, " \\1 \\2 ", system_transcript);
                    system_transcript = re.sub(multiple_spaces, " ", system_transcript);
                    
                    value_slot_mapping = {};
                    assert "dialog-acts" in turn['output']
                    for act_index in xrange(len(turn['output']['dialog-acts'])):
                        assert len(turn['output']['dialog-acts'][act_index])==2, (session_id, turn_index, turn)
                        assert "slots" in turn['output']['dialog-acts'][act_index]
                        #assert len(turn['output']['dialog-acts'][act_index]["slots"])<=1, turn['output']['dialog-acts'][act_index]["slots"]
                        assert "act" in turn['output']['dialog-acts'][act_index]
                        for slot_index in xrange(len(turn['output']['dialog-acts'][act_index]["slots"])):
                            assert len(turn['output']['dialog-acts'][act_index]["slots"][slot_index])==2;
                            
                            if turn['output']['dialog-acts'][act_index]["slots"][slot_index][1]==None:
                                continue;
                            if turn['output']['dialog-acts'][act_index]["slots"][slot_index][0]=="act":
                                continue;
                            
                            mapping_value = ("%s" % (turn['output']['dialog-acts'][act_index]["slots"][slot_index][1])).lower();
                            mapping_slot = turn['output']['dialog-acts'][act_index]["slots"][slot_index][0];
                            
                            if mapping_value.isalpha() and mapping_slot=="route":
                                continue;
                            
                            if "time" in mapping_slot:
                                mapping_slot = "<time> ";
                            elif "date" in mapping_slot:
                                if "absmonth" in mapping_slot:
                                    mapping_value = month_dictionary[int(mapping_value)-1];
                                mapping_slot = "<date> ";
                            else:
                                mapping_slot = "<%s> " % mapping_slot.split(".")[-1];
                            
                            if (mapping_value in value_slot_mapping) and (value_slot_mapping[mapping_value]!=mapping_slot):
                                print "duplicated mappings:", session_id, turn_index, mapping_value, value_slot_mapping[mapping_value], mapping_slot
                            else:
                                value_slot_mapping[mapping_value] = mapping_slot;
                                
                                mapping_value = re.sub(post_route_pattern, " \\1 \\2 ", mapping_value).strip();
                                mapping_value = re.sub(pre_route_pattern, " \\1 \\2 ", mapping_value).strip();
                                mapping_value = re.sub(multiple_spaces, " ", mapping_value);
                                value_slot_mapping[mapping_value] = mapping_slot
                                
                                if session_id=="dt-201112311705-33103" and turn_index==19:
                                    print "checkpoint 0:", value_slot_mapping
                                    
                                text_mapping_value = " ";
                                for mapping_value_token in ("%s" % mapping_value).split():
                                    if mapping_value_token.isdigit():
                                        text_mapping_value += "%s " % n2w.to_cardinal(int(mapping_value_token));
                                    else:
                                        text_mapping_value += "%s " % mapping_value_token;
                                text_mapping_value = text_mapping_value.strip();
                                if len(text_mapping_value)>0:
                                    if text_mapping_value=="y one":
                                        text_mapping_value = " %s" % text_mapping_value;
                                        mapping_slot = " %s" % mapping_slot
                                    value_slot_mapping[text_mapping_value] = mapping_slot
                                    
                                if session_id=="dt-201008052256-07038" and turn_index==10:
                                    print "checkpoint 0:", value_slot_mapping
                    
                    for mapping_value in sorted(value_slot_mapping, key=lambda key: len("%s" % key), reverse=True):
                        system_transcript = system_transcript.replace(mapping_value, value_slot_mapping[mapping_value]);
                
                system_transcript = re.sub(singleton_pattern, " ", system_transcript);    
                system_transcript = re.sub(multiple_spaces, " ", system_transcript);

            assert "input" in turn, (session_id, turn_index, turn)
            assert "live" in turn['input'], (session_id, turn_index, turn['input'])
            assert "asr-hyps" in turn['input']['live'], (session_id, turn_index, turn['input']['live'])
            assert "slu-hyps" in turn['input']['live'], (session_id, turn_index, turn['input']['live'])

            if len(turn['input']['live']['asr-hyps'])<1:
                sys.stderr.write("Missing transcript from user for session %s turn %d\n" % (session_id, turn_index));
                user_transcript = ""
            else:
                user_transcript = turn['input']['live']['asr-hyps'][0]["asr-hyp"].lower().strip();
                
                if mapping_semantics:
                    user_transcript = re.sub(time_pattern, "<time>", user_transcript);
                    user_transcript = re.sub(post_route_pattern, " \\1 \\2 ", user_transcript);
                    user_transcript = re.sub(pre_route_pattern, " \\1 \\2 ", user_transcript);
                    user_transcript = re.sub(multiple_spaces, " ", user_transcript);

                    value_slot_mapping = {};
                    
                    assert len(turn['input']['live']['slu-hyps'][0]['slu-hyp'])==1, (session_id, turn_index);
                    assert len(turn['input']['live']['slu-hyps'][0]['slu-hyp'][0])==2, (session_id, turn_index);

                    for slot_index in xrange(len(turn['input']['live']['slu-hyps'][0]['slu-hyp'][0]['slots'])):
                        assert len(turn['input']['live']['slu-hyps'][0]['slu-hyp'][0]['slots'][slot_index])==2;
                            
                        if turn['input']['live']['slu-hyps'][0]['slu-hyp'][0]['slots'][slot_index][1]==None:
                            continue;
                        if turn['input']['live']['slu-hyps'][0]['slu-hyp'][0]['slots'][slot_index][1]=="act":
                            continue;
                            
                        mapping_value = ("%s" % turn['input']['live']['slu-hyps'][0]['slu-hyp'][0]['slots'][slot_index][1]).lower();
                        mapping_slot = turn['input']['live']['slu-hyps'][0]['slu-hyp'][0]['slots'][slot_index][0];
                        
                        if mapping_value.isalpha() and mapping_slot=="route":
                            continue;

                        if "time" in mapping_slot:
                            mapping_slot = "<time> ";
                        elif "date" in mapping_slot:
                            if "absmonth" in mapping_slot:
                                mapping_value = month_dictionary[int(mapping_value)-1];
                            mapping_slot = "<date> ";
                        else:
                            mapping_slot = "<%s> " % mapping_slot.split(".")[-1];

                        if (mapping_value in value_slot_mapping) and (value_slot_mapping[mapping_value]!=mapping_slot):
                            print session_id, turn_index, mapping_value, value_slot_mapping[mapping_value], mapping_slot
                        else:
                            value_slot_mapping[mapping_value] = mapping_slot;
                            
                            mapping_value = re.sub(post_route_pattern, " \\1 \\2 ", mapping_value).strip();
                            mapping_value = re.sub(pre_route_pattern, " \\1 \\2 ", mapping_value).strip();
                            mapping_value = re.sub(multiple_spaces, " ", mapping_value);
                            value_slot_mapping[mapping_value] = mapping_slot

                            text_mapping_value = "";
                            for mapping_value_token in mapping_value.split():
                                if mapping_value_token.isdigit():
                                    text_mapping_value += "%s " % n2w.to_cardinal(int(mapping_value_token));
                                else:
                                    text_mapping_value += "%s " % mapping_value_token;
                            text_mapping_value = text_mapping_value.strip();
                            if len(text_mapping_value)>0:
                                value_slot_mapping[text_mapping_value] = mapping_slot
                    
                    for mapping_value in sorted(value_slot_mapping, key=lambda key: len("%s" % key), reverse=True):
                        user_transcript = user_transcript.replace(mapping_value, value_slot_mapping[mapping_value]);
                    
                user_transcript = re.sub(singleton_pattern, " ", user_transcript);
                user_transcript = re.sub(multiple_spaces, " ", user_transcript);

            output_stream.write("%s\t%d\t%s\t%s\n" % (session_id, turn_index, system_transcript, user_transcript));
            
        json_data.close()
                
if __name__ == "__main__":
    input_directory = sys.argv[1];
    config_directory = sys.argv[2]
    output_directory = sys.argv[3]
    parse(input_directory, config_directory, output_directory);