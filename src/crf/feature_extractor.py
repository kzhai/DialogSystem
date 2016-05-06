import codecs;
import collections;
import matplotlib;
import matplotlib.pyplot;
import nltk;
import numpy;
import operator;
import optparse;
import os;
import re;
import scipy;
import string;
import sys;
import time;
import unicodedata;

import feature.feature_context_shape_position as feature_context_shape_position;
import feature.kb_unigram_lookup_exist_features as kb_unigram_lookup_exist_features;
import feature.kb_unigram_lookup_bi_features as kb_unigram_lookup_bi_features;
import feature.kb_unigram_lookup_bie_features as kb_unigram_lookup_bie_features;

def import_feature_descriptions(feature_description_file_path):
    feature_descriptions = [];
    feature_description_file_stream = open(feature_description_file_path, 'r');
    for line in feature_description_file_stream:
        feature_descriptions.append(line.strip());
    print "successfully import feature descriptions..."
    return feature_descriptions

def export_feature_descriptions(feature_descriptions, feature_description_file_path):
    feature_description_file_stream = codecs.open(feature_description_file_path, 'w');
    for feature_description in feature_descriptions:
        feature_description_file_stream.write("%s\n" % feature_description);
    feature_description_file_stream.close()
    print "successfully export feature descriptions..."

def extract_feature_vectors(input_directory, output_directory, kb_directory=None):
    feature_descriptions = [];
    feature_descriptions = feature_context_shape_position.add_context_shape_position_feature_description(feature_descriptions);
    
    if kb_directory != None:
        feature_descriptions, kb_unigram_exist = kb_unigram_lookup_exist_features.add_KB_lookup_exist_feature_description(feature_descriptions, kb_directory);
        feature_descriptions, kb_unigram_bi = kb_unigram_lookup_bi_features.add_KB_lookup_bi_feature_description(feature_descriptions, kb_directory);
        feature_descriptions, kb_unigram_bie = kb_unigram_lookup_bie_features.add_KB_lookup_bie_feature_description(feature_descriptions, kb_directory);
    
    '''
    if os.path.isfile(input_directory):
        if not os.path.exists(output_directory):
            open(output_directory, "a").close();
        assert os.path.isfile(output_directory);
        input_file_path = input_directory;
        output_file_path = output_directory;
        feature_description_file_path = os.path.join(os.path.dirname(output_directory), "feature.description");
    '''
    if os.path.isdir(output_directory):
        feature_description_file_path = os.path.join(output_directory, "feature.description");
        export_feature_descriptions(feature_descriptions, feature_description_file_path)
    
    if kb_directory == None:
        kb_cache = None;
    else:
        kb_cache = (kb_unigram_exist, kb_unigram_bi, kb_unigram_bie);
    
    if os.path.isfile(input_directory) and os.path.isfile(output_directory):
        input_file_path = input_directory
        output_file_path = output_directory
        extract_feature_vectors_for_file(input_file_path, output_file_path, kb_cache);
    elif os.path.isdir(input_directory) and os.path.isdir(output_directory):
        for file_name in os.listdir(input_directory):
            if file_name.startswith("."):
                continue;
            
            input_file_path = os.path.join(input_directory, file_name);
            if os.path.isdir(input_file_path):
                continue;
            output_file_path = os.path.join(output_directory, file_name);
            
            extract_feature_vectors_for_file(input_file_path, output_file_path, kb_cache);
    else:
        sys.stderr.write("Error: directory or file? be consistent...\n");
    
def extract_feature_vectors_for_file(input_file_path, output_file_path, kb_cache=None):
    input_file_stream = codecs.open(input_file_path, 'r');
    output_file_stream = codecs.open(output_file_path, 'w')
    
    if kb_cache != None:
        kb_unigram_exist, kb_unigram_bi, kb_unigram_bie = kb_cache;
    
    line_count = 0;
    for input_line in input_file_stream:
        line_count += 1;
        
        input_line = input_line.strip();
        fields = input_line.split("\t");
        query_tokens = fields[0].split();
        feature_vectors = [[] for x in xrange(len(query_tokens))];
        
        feature_vectors = feature_context_shape_position.add_context_shape_position_feature(query_tokens, feature_vectors);
        if kb_cache != None:
            feature_vectors = kb_unigram_lookup_exist_features.add_KB_lookup_exist_feature(query_tokens, feature_vectors, kb_unigram_exist);
            feature_vectors = kb_unigram_lookup_bi_features.add_KB_lookup_bi_feature(query_tokens, feature_vectors, kb_unigram_bi);
            feature_vectors = kb_unigram_lookup_bie_features.add_KB_lookup_bie_feature(query_tokens, feature_vectors, kb_unigram_bie);
        
        if line_count == 1:
            number_of_fields = len(fields);
        else:
            if len(fields) != number_of_fields:
                print "warning: unrecongnized pattern for line %d, %s..." % (line_count, input_line);
                break;
            
        if len(fields) == 2:
            token_labels = fields[1].split();
            assert len(query_tokens) == len(token_labels);
            add_token_label(query_tokens, feature_vectors, token_labels);

        for feature_vector in feature_vectors:
            output_file_stream.write("%s\n" % ("\t".join(feature_vector)));
        output_file_stream.write("\n");
        
    output_file_stream.close();
    print "successfully extracted features for %s..." % input_file_path;
    
def add_token_label(query_tokens, feature_vectors, token_labels):
    for token_index in xrange(len(query_tokens)):
        feature_vectors[token_index].append(token_labels[token_index]);
        
if __name__ == '__main__':
    parser = optparse.OptionParser()
    # parser.set_defaults()
    parser.add_option("--input_directory", type="string", dest="input_directory", default=None, help="input directory")
    parser.add_option("--output_directory", type="string", dest="output_directory", default=None, help="output directory")
    parser.add_option("--knowledgebase_directory", type="string", dest="knowledgebase_directory", default=None, help="knowledgebase directory")
    # parser.add_option("--top_ranked", type="int", dest="top_ranked", default=-1, help="top n ranked")
    (options, args) = parser.parse_args();
    
    input_directory = options.input_directory
    output_directory = options.output_directory
    knowledgebase_directory = options.knowledgebase_directory
    # top_ranked = options.top_ranked
    
    extract_feature_vectors(input_directory, output_directory, knowledgebase_directory);
