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

def add_KB_lookup_bie_feature_description(feature_description, kb_directory):
    kb_dictionaries = collections.OrderedDict()
    for file_name in os.listdir(kb_directory):
        kb_file = os.path.join(kb_directory, file_name);
        if os.path.isdir(kb_file):
            continue;
        
        kb_dictionaries[file_name] = load_kb_unigram_bie(kb_file)[0];
        
        feature_description.append("token %s dictionary BIE lookup B" % file_name);
        feature_description.append("token %s dictionary BIE lookup I" % file_name);
        feature_description.append("token %s dictionary BIE lookup E" % file_name);
        
    return feature_description, kb_dictionaries

    '''
    manufacturer_unigram_bie, temp = load_kb_unigram_bie(os.path.join(kb_directory, "manufacturer.txt"));
    model_unigram_bie, temp = load_kb_unigram_bie(os.path.join(kb_directory, "model.txt"));
    product_unigram_bie, temp = load_kb_unigram_bie(os.path.join(kb_directory, "product.txt"));
    product_family_unigram_bie, temp = load_kb_unigram_bie(os.path.join(kb_directory, "product_family.txt"));
    
    feature_description.append("token manufacturer dictionary BIE lookup B");
    feature_description.append("token manufacturer dictionary BIE lookup I");
    feature_description.append("token manufacturer dictionary BIE lookup E");
    feature_description.append("token model dictionary BIE lookup B");
    feature_description.append("token model dictionary BIE lookup I");
    feature_description.append("token model dictionary BIE lookup E");
    feature_description.append("token product dictionary BIE lookup B");
    feature_description.append("token product dictionary BIE lookup I");
    feature_description.append("token product dictionary BIE lookup E");
    feature_description.append("token product family dictionary BIE lookup B");
    feature_description.append("token product family dictionary BIE lookup I");
    feature_description.append("token product family dictionary BIE lookup E");
    
    return feature_description, (manufacturer_unigram_bie, model_unigram_bie, product_unigram_bie, product_family_unigram_bie)
    '''
    
def add_KB_lookup_bie_feature(query_tokens,
                              feature_vectors,
                              kb_unigram_bie
                              ):
    for token_index in xrange(len(query_tokens)):
        query_token = query_tokens[token_index];
        
        for key in kb_unigram_bie.keys():
            (value_b, value_i, value_e) = kb_unigram_bie[key]
            feature_vectors[token_index].append("%s" % (query_token in value_b));
            feature_vectors[token_index].append("%s" % (query_token in value_i));
            feature_vectors[token_index].append("%s" % (query_token in value_e));
    
    return feature_vectors
    
    '''
    (manufacturer_unigram_bie, model_unigram_bie, product_unigram_bie, product_family_unigram_bie) = kb_unigram_bie
    
    (manufacturer_unigram_b, manufacturer_unigram_i, manufacturer_unigram_e) = manufacturer_unigram_bie; 
    (model_unigram_b,  model_unigram_i, model_unigram_e) = model_unigram_bie; 
    (product_unigram_b, product_unigram_i, product_unigram_e) = product_unigram_bie;
    (product_family_unigram_b, product_family_unigram_i, product_family_unigram_e) = product_family_unigram_bie;
    
    for token_index in xrange(len(query_tokens)):
        query_token = query_tokens[token_index]
        
        feature_vectors[token_index].append("%s" % (query_token in manufacturer_unigram_b));
        feature_vectors[token_index].append("%s" % (query_token in manufacturer_unigram_i));
        feature_vectors[token_index].append("%s" % (query_token in manufacturer_unigram_e));
        feature_vectors[token_index].append("%s" % (query_token in model_unigram_b));
        feature_vectors[token_index].append("%s" % (query_token in model_unigram_i));
        feature_vectors[token_index].append("%s" % (query_token in model_unigram_e));
        feature_vectors[token_index].append("%s" % (query_token in product_unigram_b));
        feature_vectors[token_index].append("%s" % (query_token in product_unigram_i));
        feature_vectors[token_index].append("%s" % (query_token in product_unigram_e));
        feature_vectors[token_index].append("%s" % (query_token in product_family_unigram_b));
        feature_vectors[token_index].append("%s" % (query_token in product_family_unigram_i));
        feature_vectors[token_index].append("%s" % (query_token in product_family_unigram_e));
        
    return feature_vectors;
    '''

def load_kb_unigram_bie(kb_input_path):
    unigram_b = set();
    unigram_i = set();
    unigram_e = set();
    all_gram = set();
    for line in open(kb_input_path, 'r'):
        line = line.strip();
        all_gram.add(line);
        
        feature_vectors = line.split();
        unigram_b.add(feature_vectors[0]);
        if len(feature_vectors)>1:
            unigram_e.add(feature_vectors[-1]);
        for word in feature_vectors[1:-1]:
            unigram_i.add(word);
    
    print "successfully load file %s..." % (kb_input_path);
    
    return (unigram_b, unigram_i, unigram_e), all_gram;
    
if __name__ == '__main__':
    input_directory = sys.argv[1];
    kb_directory = sys.argv[2];
    output_directory = sys.argv[3];
    kb_lookup_bie_features(input_directory, kb_directory, output_directory);