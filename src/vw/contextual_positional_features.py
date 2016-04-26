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

def add_contextual_positional_feature(query_tokens, feature_vector):
    feature_family = [];
    
    feature_family.append("|CONTEXT");
    feature_family.extend(query_tokens);
    
    feature_vector.append("%s" % " ".join(feature_family));
    
    return feature_vector;

def containsAny(str, set):
    """Check whether 'str' contains ANY of the chars in 'set'"""
    return 1 in [c in str for c in set]

def containsAll(str, set):
    """Check whether 'str' contains ALL of the chars in 'set'"""
    return 0 not in [c in str for c in set]

def extract_pattern(query_token):
    char_seq = query_token
    char_seq = ["a" if query_token_char in string.letters else query_token_char for query_token_char in char_seq]
    char_seq = ["0" if query_token_char in string.digits else query_token_char for query_token_char in char_seq]
    char_seq = ["-" if query_token_char in string.punctuation else query_token_char for query_token_char in char_seq]
    
    token_pattern = "".join(char_seq);
    
    token_summarized_pattern = token_pattern;
    token_summarized_pattern = re.sub(r"a+", "a", token_summarized_pattern);
    token_summarized_pattern = re.sub(r"0+", "0", token_summarized_pattern);
    token_summarized_pattern = re.sub(r"-+", "-", token_summarized_pattern);

    return token_pattern, token_summarized_pattern

if __name__ == '__main__':
    input_directory = sys.argv[1];
    output_directory = sys.argv[2];
    add_contextual_positional_feature(input_directory, output_directory);