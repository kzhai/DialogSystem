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

def extract_feature_vectors_for_directory(input_directory, kb_directory, output_directory):
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    
    kb_allgrams_dict = kb_allgrams_exist_lookup_features.load_kb_directory(kb_directory);

    file_name = "all.dat";
    input_file_path = os.path.join(input_directory, file_name);
    output_file_path = os.path.join(output_directory, file_name);
    label_index_file = os.path.join(output_directory, "label2index");
    
    extract_feature_vectors_for_file(input_file_path, output_file_path, kb_allgrams_dict, label_index_file, feature_only=False);
    print "successfully extract features for %s..." % file_name;
    
    for file_name in ["train.dat", "test.dat"]:
        input_file_path = os.path.join(input_directory, file_name);
        if not os.path.exists(input_file_path):
            continue;
        output_file_path = os.path.join(output_directory, file_name);
        
        extract_feature_vectors_for_file(input_file_path, output_file_path, kb_allgrams_dict, label_index_file, feature_only=True);
        print "successfully extract features for %s..." % file_name;

def extract_feature_vectors_for_file(input_file_path, output_file_path, kb_allgrams_dict, label_index_file, feature_only=True):
    if feature_only:
        assert os.path.exists(label_index_file);
        label_to_index, index_to_label = import_label_index(label_index_file);
    else:
        label_to_index = {};
        index_to_label = {};
        index_count = {};
        
    input_file_stream = codecs.open(input_file_path, 'r');
    output_file_stream = codecs.open(output_file_path, 'w');
    
    line_count = 0;
    for input_line in input_file_stream:
        line_count += 1;
        
        input_line = input_line.strip();
        input_line = input_line.lower();
        input_line = "".join([ch for ch in input_line if ch not in string.punctuation])
        
        fields = input_line.split("\t");
        assert len(fields) == 2;
        query_tokens = fields[0].split();
        label = fields[1];
        
        if feature_only:
            assert (label in label_to_index), input_line;
        else:
            if label not in label_to_index:
                label_to_index[label] = len(label_to_index) + 1;
                index_to_label[len(index_to_label) + 1] = label;
                
                index_count[label_to_index[label]] = 0;
                
            index_count[label_to_index[label]] += 1;
        
        index = label_to_index[label];
        
        feature_vector = [];
        feature_vector.append("%d" % index);
        
        feature_vector = extract_feature_vector_for_string(query_tokens, feature_vector, kb_allgrams_dict);

        #feature_vector = contextual_positional_features.add_contextual_positional_feature(query_tokens, feature_vector);
        #feature_vector = kb_allgrams_exist_lookup_features.add_kb_exist_lookup_features(query_tokens, feature_vector, kb_allgrams_dict)

        output_file_stream.write("%s\n" % (" ".join(feature_vector)));
        
    output_file_stream.close();
    
    if not feature_only:
        export_label_index(label_to_index, label_index_file);
        
def extract_feature_vector_for_string(query_tokens, feature_vector, kb_allgrams_dict):
    feature_vector = contextual_positional_features.add_contextual_positional_feature(query_tokens, feature_vector);
    feature_vector = kb_allgrams_exist_lookup_features.add_kb_exist_lookup_features(query_tokens, feature_vector, kb_allgrams_dict)

    return feature_vector

def import_label_index(label_index_file):
    label_index_file_stream = codecs.open(label_index_file, 'r');
    label_to_index = {};
    index_to_label = {};
    for line in label_index_file_stream:
        line = line.strip();
        tokens = line.split("\t");
        index_to_label[int(tokens[1])] = tokens[0];
        label_to_index[tokens[0]] = int(tokens[1]);
    
    return label_to_index, index_to_label

def export_label_index(label_to_index, label_index_file):
    label_index_file_stream = codecs.open(label_index_file, 'w');
    for label in label_to_index:
        label_index_file_stream.write("%s\t%d\n" % (label, label_to_index[label]));
    label_index_file_stream.close()
    print "successfully export label index..."
    
if __name__ == '__main__':
    input_directory = sys.argv[1];
    kb_directory = sys.argv[2];
    output_directory = sys.argv[3];
    
    extract_feature_vectors_for_directory(input_directory, kb_directory, output_directory);
