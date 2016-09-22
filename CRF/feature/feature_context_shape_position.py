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

def add_context_shape_position_feature_description(feature_description):
    feature_description.append("token value");
    
    feature_description.append("bias constant");
    
    feature_description.append("token is all digits");
    feature_description.append("token is all alpha chars");
    feature_description.append("token is all alphanumeric");
    
    feature_description.append("token contains any punctuation");
    feature_description.append("token contains any apostrophe");
    
    feature_description.append("token extract alpha chars only");
    feature_description.append("token extract non-alpha chars only");
    
    feature_description.append("token pattern");
    feature_description.append("token summarized pattern");
    
    feature_description.append("token position from start");
    feature_description.append("token position from end");
    
    return feature_description

def add_context_shape_position_feature(query_tokens, feature_vectors):
    for token_index in xrange(len(query_tokens)):
        query_token = query_tokens[token_index];
        
        feature_vectors[token_index].append("%s" % query_token);
        
        feature_vectors[token_index].append("%d" % 1);
        
        feature_vectors[token_index].append("%s" % query_token.isdigit());
        feature_vectors[token_index].append("%s" % query_token.isalpha());
        feature_vectors[token_index].append("%s" % query_token.isalnum());
        
        feature_vectors[token_index].append("%s" % containsAny(query_token, '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~'));
        feature_vectors[token_index].append("%s" % containsAny(query_token, "'"));
        
        feature_vectors[token_index].append("_" + "".join([query_token_char for query_token_char in query_token if query_token_char in string.letters]));
        feature_vectors[token_index].append("_" + "".join([query_token_char for query_token_char in query_token if query_token_char not in string.letters]));
        
        token_pattern, token_summarized_pattern = extract_pattern(query_token);
        
        feature_vectors[token_index].append("%s" % token_pattern);
        feature_vectors[token_index].append("%s" % token_summarized_pattern);
        
        feature_vectors[token_index].append("%d" % (token_index+1));
        feature_vectors[token_index].append("%d" % (len(query_tokens) - token_index));
        
    return feature_vectors;

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
    extract_feature_vectors(input_directory, output_directory);