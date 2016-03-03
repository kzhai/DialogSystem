import codecs;
import collections;
import matplotlib;
import matplotlib.pyplot;
import nltk;
import numpy;
import operator;
import os;
import re;
import scipy;
import string;
import sys;
import time;
import unicodedata;

def add_language_model_features(query_tokens,
                                 feature_vector,
                                 lm_dict):
    
    feature_family = [];
    feature_family.append("|LM");

    if " ".join(query_tokens) not in lm_dict:
        #print "query tokens: %s" % query_tokens
        query_language_model = [];
    else:
        query_language_model = lm_dict[" ".join(query_tokens)];
    feature_family += ["%d:%s" % ((x + 1), query_language_model[x]) for x in xrange(len(query_language_model))];
    
    feature_vector.append("%s" % " ".join(feature_family));
    
    return feature_vector;

'''
def exist_lookup_tokens_from_kb(query_tokens, kb_allgrams):
    for length in xrange(len(query_tokens), 0, -1):
        found_match = exist_lookup_tokens_of_length_from_kb(query_tokens, length, kb_allgrams);
        if found_match:
            return True;
    return False
    
def exist_lookup_tokens_of_length_from_kb(query_tokens, length, kb_allgrams):
    assert length>0 and length<=len(query_tokens);
    #matched_strings = set();
    for start_index in xrange(len(query_tokens)-length+1):
        query_string = " ".join(query_tokens[start_index:start_index+length]);
        if query_string in kb_allgrams:
            return True;
            #matched_strings.append(query_string);
    #return matched_strings
    return False;

'''
def load_lm_directory(lm_directory):
    
    language_model = {};
    for file_name in os.listdir(lm_directory):
        if file_name.startswith("."):
            continue;
        
        lm_input_file = os.path.join(lm_directory, file_name);
        if os.path.isdir(lm_input_file):
            continue;
        
        for line in open(lm_input_file, 'r'):
            line = line.strip();
            tokens = line.split()
            
            language_model[" ".join(tokens[:-5])] = tokens[-5:]
        
    return language_model;

if __name__ == '__main__':
    input_directory = sys.argv[1];
    lm_file = sys.argv[2];
    output_directory = sys.argv[3];
    # add_language_model_features(input_directory, lm_file, output_directory);
