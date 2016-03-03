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

def add_kb_exist_lookup_features(query_tokens,
                                 feature_vector,
                                 kb_allgrams_dict):
    
    feature_family = [];
    feature_family.append("|EXIST");
    for kb_name in kb_allgrams_dict:
        found_match = exist_lookup_tokens_from_kb(query_tokens, kb_allgrams_dict[kb_name]);
        if found_match:
            feature_family.append("found.%s" % kb_name);
    feature_vector.append("%s" % " ".join(feature_family));
    
    return feature_vector;

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
    
def load_kb_directory(kb_directory):
    kb_allgrams_dict = {};
    for file_name in os.listdir(kb_directory):
        if file_name.startswith("."):
            continue;
        
        kb_file = os.path.join(kb_directory, file_name);
        if os.path.isdir(kb_file):
            continue;
        
        kb_allgrams_dict[file_name] = load_kb(kb_file);
    
    return kb_allgrams_dict;

def load_kb(kb_input_path):
    allgrams = set();
    for line in open(kb_input_path, 'r'):
        line = line.strip();
        allgrams.add(line);
    
    #print "successfully load file %s..." % (kb_input_path);

    return allgrams;

if __name__ == '__main__':
    input_directory = sys.argv[1];
    kb_directory = sys.argv[2];
    output_directory = sys.argv[3];
    add_kb_exist_lookup_features(input_directory, kb_directory, output_directory);