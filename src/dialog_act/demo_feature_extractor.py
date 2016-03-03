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

import contextual_positional_features
import kb_allgrams_exist_lookup_features;
import feature_extractor

def extract_feature_vectors_for_file(input_file_path, kb_directory, output_file_path):
    kb_allgrams_dict = kb_allgrams_exist_lookup_features.load_kb_directory(kb_directory);
    
    input_file_stream = codecs.open(input_file_path, 'r');
    output_file_stream = codecs.open(output_file_path, 'w');
    
    line_count = 0;
    for input_line in input_file_stream:
        line_count += 1;
        
        input_line = input_line.strip();
        input_line = input_line.lower();
        input_line = "".join([ch for ch in input_line if ch not in string.punctuation])
        
        query_tokens = input_line.split();
        
        feature_vector = [];
        feature_vector.append("%d" % 1);
        
        feature_vector = feature_extractor.extract_feature_vector_for_string(query_tokens, feature_vector, kb_allgrams_dict);
        
        #feature_vector = contextual_positional_features.add_contextual_positional_feature(query_tokens, feature_vector);
        #feature_vector = kb_allgrams_exist_lookup_features.add_kb_exist_lookup_features(query_tokens, feature_vector, kb_allgrams_dict)

        output_file_stream.write("%s\n" % (" ".join(feature_vector)));
        
    output_file_stream.close();
    
if __name__ == '__main__':
    input_file_path = sys.argv[1];
    kb_directory = sys.argv[2];
    output_file_path = sys.argv[3];
    extract_feature_vectors_for_file(input_file_path, kb_directory, output_file_path);