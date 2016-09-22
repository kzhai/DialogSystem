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
import sys;
import time;
import unicodedata;

def add_KB_lookup_exist_feature_description(feature_description, kb_directory):
    kb_dictionaries = collections.OrderedDict()
    for file_name in os.listdir(kb_directory):
        if file_name.startswith("."):
            continue;
        
        kb_file = os.path.join(kb_directory, file_name);
        if os.path.isdir(kb_file):
            continue;
        
        kb_dictionaries[file_name] = load_kb_unigram_exist(kb_file)[0];
        
        feature_description.append("token %s dictionary lookup exist" % file_name);
    
    return feature_description, kb_dictionaries

    '''
    manufacturer_unigram_exist, temp = load_kb_unigram_exist(os.path.join(kb_directory, "manufacturer.txt"));
    model_unigram_exist, temp = load_kb_unigram_exist(os.path.join(kb_directory, "model.txt"));
    product_unigram_exist, temp = load_kb_unigram_exist(os.path.join(kb_directory, "product.txt"));
    product_family_unigram_exist, temp = load_kb_unigram_exist(os.path.join(kb_directory, "product_family.txt"));
    
    feature_description.append("token manufacturer dictionary lookup exist");
    feature_description.append("token model dictionary lookup exist");
    feature_description.append("token product dictionary lookup exist");
    feature_description.append("token product family dictionary lookup exist");
    
    return feature_description, (manufacturer_unigram_exist, model_unigram_exist, product_unigram_exist, product_family_unigram_exist)
    '''
    
def add_KB_lookup_exist_feature(query_tokens,
                                feature_vectors,
                                kb_unigram_exist
                                ):
    # (manufacturer_unigram_exist, model_unigram_exist, product_unigram_exist, product_family_unigram_exist) = kb_unigram_exist
    
    for token_index in xrange(len(query_tokens)):
        query_token = query_tokens[token_index];
        
        for key in kb_unigram_exist.keys():
            feature_vectors[token_index].append("%s" % (query_token in kb_unigram_exist[key]));
        
        '''
        feature_vectors[token_index].append("%s" % (query_token in manufacturer_unigram_exist));
        feature_vectors[token_index].append("%s" % (query_token in model_unigram_exist));
        feature_vectors[token_index].append("%s" % (query_token in product_unigram_exist));
        feature_vectors[token_index].append("%s" % (query_token in product_family_unigram_exist));
        '''
        
    return feature_vectors;
    
def load_kb_unigram_exist(kb_input_path):
    unigram_exist = set();
    all_gram = set();
    for line in open(kb_input_path, 'r'):
        line = line.strip();
        all_gram.add(line);
        for word in line.split():
            unigram_exist.add(word);
    
    print "successfully load file %s..." % (kb_input_path);
    
    return unigram_exist, all_gram;
        
if __name__ == '__main__':
    input_directory = sys.argv[1];
    kb_directory = sys.argv[2];
    output_directory = sys.argv[3];
    kb_lookup_exist_features(input_directory, kb_directory, output_directory);
