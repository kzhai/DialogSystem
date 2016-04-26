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

import util.num2word
n2w = util.num2word.Num2Word()

non_decimal_pattern = re.compile(r'[^\d.]+')
time_pattern = re.compile(r'(\d+):(\d+)( [ap]m)?');
ampm_pattern = re.compile(r' [ap] m?');
# post_route_pattern = re.compile(r'(\d+)(\D?)');
# pre_route_pattern= re.compile(r'(\D?)(\d+)');
multiple_spaces = re.compile(r' +');

singleton_pattern = re.compile(r' [^ai] ');

month_dictionary = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december'];

bus_route_pattern = re.compile(r'(<d>\a*):(\d+)( [ap]m)?');
for val in ["61a"]:
    val = non_decimal_pattern.sub('', val)
    print val, "is", n2w.to_cardinal(int(val));
    #sys.exit()
    
def parse_system_transcripts_from_log(turn, mapping_semantics, debug_info):
    session_id, turn_index = debug_info
    
    system_acts = set();
    if "transcript" not in turn["output"]:
        sys.stderr.write("Missing transcript from system for session %s turn %d\n" % (session_id, turn_index));
        system_transcript = "";
    else:
        system_transcript = turn['output']['transcript'].lower().strip();
        system_transcript = re.sub(multiple_spaces, " ", system_transcript);
        
        value_slot_mapping = {};
        assert "dialog-acts" in turn['output']
        # assert len(turn['output']['dialog-acts']) == 1, turn['output']['dialog-acts'];
        for act_index in xrange(len(turn['output']['dialog-acts'])):
            assert len(turn['output']['dialog-acts'][act_index]) == 2, (session_id, turn_index, turn)
            
            assert "act" in turn['output']['dialog-acts'][act_index]
            system_act = turn['output']['dialog-acts'][act_index]["act"].strip();
            assert len(system_act.split()) == 1
            system_acts.add(system_act);
            
            assert "slots" in turn['output']['dialog-acts'][act_index]
            
            if mapping_semantics:
                for slot_index in xrange(len(turn['output']['dialog-acts'][act_index]["slots"])):
                    assert len(turn['output']['dialog-acts'][act_index]["slots"][slot_index]) == 2;
    
                    mapping_slot = turn['output']['dialog-acts'][act_index]["slots"][slot_index][0].lower().strip();
                    assert len(mapping_slot.split()) == 1;
                    
                    if mapping_slot.startswith("result"):
                        mapping_slot = mapping_slot.replace("result.", "")
                    if mapping_slot.startswith("from"):
                        mapping_slot = mapping_slot.replace("from.", "")
                    if mapping_slot.startswith("to"):
                        mapping_slot = mapping_slot.replace("to.", "")
                        
                    if mapping_slot=="":
                        continue;
                    
                    mapping_slot = "<%s>" % mapping_slot;

                    mapping_value = ("%s" % turn['output']['dialog-acts'][act_index]["slots"][slot_index][1]).lower().strip();
                    mapping_value = re.sub(multiple_spaces, " ", mapping_value);
                    
                    if (mapping_value in value_slot_mapping) and (value_slot_mapping[mapping_value] != mapping_slot):
                        #"duplicated mappings from value to slot:",
                        print "system:", session_id, turn_index, mapping_value, value_slot_mapping[mapping_value], mapping_slot
                        pass
                    else:
                        value_slot_mapping[mapping_value] = mapping_slot
                            
        for mapping_value in sorted(value_slot_mapping, key=lambda key: len("%s" % key), reverse=True):
            system_transcript = system_transcript.replace(mapping_value, value_slot_mapping[mapping_value]);
        
        # system_transcript = re.sub(singleton_pattern, " ", system_transcript);    
        system_transcript = re.sub(multiple_spaces, " ", system_transcript);
    
    return system_transcript, system_acts

def parse_user_transcripts(log_turn, label_turn, mapping_semantics, debug_info):
    session_id, turn_index = debug_info
    
    if "transcription" not in label_turn:
        # sys.stderr.write("Missing transcript from user for session %s turn %d\n" % (session_id, turn_index));
        user_transcript_from_label = ""
    else:
        user_transcript_from_label = label_turn["transcription"].lower().strip();
        user_transcript_from_label = re.sub(multiple_spaces, " ", user_transcript_from_label);
        
    user_acts = set();
    
    if len(log_turn['input']['live']['asr-hyps']) < 1:
        #sys.stderr.write("Missing transcript from user for session %s log_turn %d\n" % (session_id, turn_index));
        user_transcript_from_log = ""
    else:
        user_transcript_from_log = log_turn['input']['live']['asr-hyps'][0]["asr-hyp"].lower().strip();
        user_transcript_from_log = re.sub(multiple_spaces, " ", user_transcript_from_log);
        
        for slu_hyp_index in xrange(len(log_turn['input']['live']['slu-hyps'][0]['slu-hyp'])):
            assert len(log_turn['input']['live']['slu-hyps'][0]['slu-hyp'][slu_hyp_index]) == 2, (session_id, turn_index);
            
            assert "act" in log_turn['input']['live']['slu-hyps'][0]['slu-hyp'][slu_hyp_index]
            user_act = log_turn['input']['live']['slu-hyps'][0]['slu-hyp'][slu_hyp_index]['act'].strip()
            assert len(user_act.split()) == 1;
            user_acts.add(user_act);
        
    if mapping_semantics:
        value_slot_mapping = {};
        for slu_label_index in xrange(len(label_turn["slu-labels"])):
            # act_label = label_turn["system-specific"]["act-labels"][slu_label_index]
            slu_label = label_turn["slu-labels"][slu_label_index]["label"]
            if not slu_label:
                continue;
            
            slu_slots = label_turn["slu-labels"][slu_label_index]["slots"]
            for mapping_slot, mapping_value in slu_slots.iteritems():
                #mapping_slot = mapping_slot.split(".")[0];
                mapping_slot = "<%s>" % mapping_slot;
                
                mapping_value = "%s" % mapping_value;
                mapping_value = re.sub(multiple_spaces, " ", mapping_value);
                
                

                
                if (mapping_value in value_slot_mapping) and (value_slot_mapping[mapping_value] != mapping_slot):
                    print "user:", session_id, turn_index, value_slot_mapping[mapping_value], mapping_slot, mapping_value
                    pass
                else:
                    value_slot_mapping[mapping_value] = mapping_slot;
                    
        for mapping_value in sorted(value_slot_mapping, key=lambda key: len("%s" % key), reverse=True):
            user_transcript_from_log = user_transcript_from_log.replace(mapping_value, value_slot_mapping[mapping_value]);
            
            # user_transcript_from_log = re.sub(singleton_pattern, " ", user_transcript_from_log);
            user_transcript_from_log = re.sub(multiple_spaces, " ", user_transcript_from_log);
    
    #assert user_transcript_from_log == user_transcript_from_log, (user_transcript_from_log, user_transcript_from_log);
    return user_transcript_from_log, user_acts

def parse_user_transcripts_from_label(label_turn, mapping_semantics, debug_info):
    session_id, turn_index = debug_info
    
    user_acts = set();
    if "transcription" not in label_turn:
        # sys.stderr.write("Missing transcript from user for session %s turn %d\n" % (session_id, turn_index));
        user_transcript = ""
    else:
        user_transcript = label_turn["transcription"].lower().strip();
        user_transcript = re.sub(multiple_spaces, " ", user_transcript);
        
        value_slot_mapping = {};    
        for slu_label_index in xrange(len(label_turn["slu-labels"])):
            # act_label = label_turn["system-specific"]["act-labels"][slu_label_index]
            slu_label = label_turn["slu-labels"][slu_label_index]["label"]
            if not slu_label:
                continue;
            
            if mapping_semantics:
                slu_slots = label_turn["slu-labels"][slu_label_index]["slots"]
                for slot_index in xrange(len(slu_slots)):
                    assert len(slu_slots[slot_index]) == 2;
    
                    mapping_slot = slu_slots[slot_index][0].lower().strip();
                    assert len(mapping_slot.split()) == 1;
                    if mapping_slot == "this":
                        continue;
                    mapping_slot = "<%s>" % mapping_slot;
                    
                    mapping_value = ("%s" % slu_slots[slot_index][1]).lower().strip();
                    mapping_value = re.sub(multiple_spaces, " ", mapping_value);
                    
                    if (mapping_value in value_slot_mapping) and (value_slot_mapping[mapping_value] != mapping_slot):
                        print session_id, turn_index, value_slot_mapping[mapping_value], mapping_slot, mapping_value
                    else:
                        value_slot_mapping[mapping_value] = mapping_slot;
                        
        for mapping_value in sorted(value_slot_mapping, key=lambda key: len("%s" % key), reverse=True):
            user_transcript = user_transcript.replace(mapping_value, value_slot_mapping[mapping_value]);
                
            # user_transcript = re.sub(singleton_pattern, " ", user_transcript);
            user_transcript = re.sub(multiple_spaces, " ", user_transcript);
    
    return user_transcript, user_acts

def parse_user_transcripts_from_log(turn, mapping_semantics, debug_info):
    session_id, turn_index = debug_info
    
    user_acts = set();
    if len(turn['input']['live']['asr-hyps']) < 1:
        sys.stderr.write("Missing transcript from user for session %s turn %d\n" % (session_id, turn_index));
        user_transcript = ""
    else:
        user_transcript = turn['input']['live']['asr-hyps'][0]["asr-hyp"].lower().strip();
        user_transcript = re.sub(multiple_spaces, " ", user_transcript);
        
        value_slot_mapping = {};
        
        for slu_hyp_index in xrange(len(turn['input']['live']['slu-hyps'][0]['slu-hyp'])):
            assert len(turn['input']['live']['slu-hyps'][0]['slu-hyp'][slu_hyp_index]) == 2, (session_id, turn_index);
            
            assert "act" in turn['input']['live']['slu-hyps'][0]['slu-hyp'][slu_hyp_index]
            user_act = turn['input']['live']['slu-hyps'][0]['slu-hyp'][slu_hyp_index]['act'].strip()
            assert len(user_act.split()) == 1;
            user_acts.add(user_act);
            
            assert "slots" in turn['input']['live']['slu-hyps'][0]['slu-hyp'][slu_hyp_index]
            
            if mapping_semantics:
                for slot_index in xrange(len(turn['input']['live']['slu-hyps'][0]['slu-hyp'][slu_hyp_index]['slots'])):
                    assert len(turn['input']['live']['slu-hyps'][0]['slu-hyp'][slu_hyp_index]['slots'][slot_index]) == 2;
    
                    mapping_slot = turn['input']['live']['slu-hyps'][0]['slu-hyp'][slu_hyp_index]['slots'][slot_index][0].lower().strip();
                    assert len(mapping_slot.split()) == 1;
                    if mapping_slot == "this":
                        continue;
                    mapping_slot = "<%s>" % mapping_slot;
                    
                    mapping_value = ("%s" % turn['input']['live']['slu-hyps'][0]['slu-hyp'][slu_hyp_index]['slots'][slot_index][1]).lower().strip();
                    mapping_value = re.sub(multiple_spaces, " ", mapping_value);
                    
                    if (mapping_value in value_slot_mapping) and (value_slot_mapping[mapping_value] != mapping_slot):
                        print session_id, turn_index, value_slot_mapping[mapping_value], mapping_slot, mapping_value
                    else:
                        value_slot_mapping[mapping_value] = mapping_slot;
                        
        for mapping_value in sorted(value_slot_mapping, key=lambda key: len("%s" % key), reverse=True):
            user_transcript = user_transcript.replace(mapping_value, value_slot_mapping[mapping_value]);
            
        # user_transcript = re.sub(singleton_pattern, " ", user_transcript);
        user_transcript = re.sub(multiple_spaces, " ", user_transcript);
    
    return user_transcript, user_acts

if __name__ == "__main__":
    input_directory = sys.argv[1];
    output_file = sys.argv[2];
    parse(input_directory, output_file);
