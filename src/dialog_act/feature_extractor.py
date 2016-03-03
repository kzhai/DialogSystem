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
# import kb_allgrams_exist_lookup_features;
# import lm_features;

transcript_index = 4
act_index = 5
weight_index = -1

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

def extract_feature_vectors_for_directory(input_directory, output_directory, kb_directory=None, lm_directory=None, inverse_weighted=False):
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    
    '''
    kb_allgrams_dict = kb_allgrams_exist_lookup_features.load_kb_directory(kb_directory);
    if lm_directory!=None:
        lm_dict = lm_features.load_lm_directory(lm_directory);
    else:
        lm_dict = None,
    '''
    
    '''
    file_name = "all.dat";
    input_file_path = os.path.join(input_directory, file_name);
    output_file_path = os.path.join(output_directory, file_name);
    label_index_file = os.path.join(output_directory, "label2index");
    
    extract_feature_vectors_for_file(input_file_path, output_file_path, kb_allgrams_dict, label_index_file, feature_only=False);
    print "successfully extract features for %s..." % file_name;
    '''
    
    training_data_file = os.path.join(input_directory, "train.dat");
    label_index_count_file = os.path.join(output_directory, "label2index");
    label_index_count = extract_label_information(training_data_file, label_index_count_file);
    
    input_file_path = os.path.join(input_directory, "train.dat");
    output_file_path = os.path.join(output_directory, "train.dat");
    extract_feature_vectors_for_file(input_file_path, output_file_path, label_index_count, inverse_weighted=inverse_weighted);
    print "successfully extract features for %s..." % "train.dat";
    
    input_file_path = os.path.join(input_directory, "dev.dat");
    output_file_path = os.path.join(output_directory, "dev.dat");
    extract_feature_vectors_for_file(input_file_path, output_file_path, label_index_count, inverse_weighted=inverse_weighted);
    print "successfully extract features for %s..." % "dev.dat";
        
    input_file_path = os.path.join(input_directory, "test.dat");
    output_file_path = os.path.join(output_directory, "test.dat");
    extract_feature_vectors_for_file(input_file_path, output_file_path, label_index_count, inverse_weighted=False);  # kb_allgrams_dict, lm_dict, 
    print "successfully extract features for %s..." % "test.dat";

def extract_feature_vectors_for_file(input_file_path, output_file_path, label_index_count, inverse_weighted=True, multi_label_setting=True):  # kb_allgrams_dict, lm_dict, 
    label_to_index, index_to_label, index_to_counts = label_index_count;
    
    # index_to_counts = {};
    index_to_weight = numpy.asarray(index_to_counts.values(), dtype=float);
    log_index_to_weight = numpy.log(index_to_weight);
    log_index_to_weight = numpy.sum(log_index_to_weight) - log_index_to_weight;
    index_to_weight = log_index_to_weight - scipy.misc.logsumexp(log_index_to_weight);
    index_to_weight = numpy.exp(index_to_weight);
    
    input_file_stream = codecs.open(input_file_path, 'r');
    output_file_stream = codecs.open(output_file_path, 'w');
    
    line_count = 0;
    for input_line in input_file_stream:
        line_count += 1;
        
        # input_line = input_line.strip();
        input_line = input_line.lower();
        # input_line = "".join([ch for ch in input_line if ch not in string.punctuation])
        
        fields = input_line.split("\t");
        tokens = fields[transcript_index];
        tokens = "".join([ch for ch in tokens if ch not in string.punctuation]);
        tokens = tokens.split();
        if len(tokens) == 0:
            continue;
        labels = fields[act_index].split();
        if len(labels) == 0:
            continue;
        
        if not multi_label_setting:
            labels = labels[:1]
        # fields[0] = "".join([ch for ch in fields[0] if ch not in string.punctuation]);
        
        indices = [];
        weights = [];
        for label in labels:
            if label not in label_to_index:
                print "warning: labels not found for line \"%s\" in file \"%s\"..." % (input_line, input_file_path)
                continue;
            
            index = label_to_index[label]
            indices.append(index)
            weight = 1;
            if inverse_weighted:
                weight *= index_to_weight[index - 1];
            if weight_index >= 0 and weight_index < len(fields):
                weight *= float(fields[weight_index]);
            weights.append(weight)
        
        feature_vector = [];
        if (weight_index >= 0 and weight_index < len(fields)) or inverse_weighted:
            feature_vector.append("%s" % (" ".join(["%d:%g" % (index, weights) for index, weights in zip(indices, weights)])));
        else:
            feature_vector.append("%s" % (" ".join(["%d" % index for index in indices])));
        
        feature_vector = extract_feature_vector_for_string(tokens, feature_vector);

        # feature_vector = contextual_positional_features.add_contextual_positional_feature(tokens, feature_vector);
        # feature_vector = kb_allgrams_exist_lookup_features.add_kb_exist_lookup_features(tokens, feature_vector, kb_allgrams_dict)
        
        output_file_stream.write("%s\n" % (" ".join(feature_vector)));
        
    output_file_stream.close();

def extract_feature_vector_for_string(query_tokens, feature_vector):
    feature_vector = contextual_positional_features.add_contextual_positional_feature(query_tokens, feature_vector);
    # feature_vector = kb_allgrams_exist_lookup_features.add_kb_exist_lookup_features(query_tokens, feature_vector, kb_allgrams_dict)
    # feature_vector = lm_features.add_language_model_features(query_tokens, feature_vector, lm_dict);

    return feature_vector

def extract_label_information(training_data_file, label_index_count_file=None, multi_label_setting=True):
    input_file_stream = codecs.open(training_data_file, 'r');
    
    label_to_index = {};
    index_to_label = {};
    index_to_count = {};
    
    line_count = 0;
    for input_line in input_file_stream:
        line_count += 1;
        
        # input_line = input_line.strip();
        input_line = input_line.lower();
        # input_line = "".join([ch for ch in input_line if ch not in string.punctuation])
        
        fields = input_line.split("\t");
        # tokens = fields[transcript_index].split();
        labels = fields[act_index].split();
        
        if not multi_label_setting:
            labels = labels[:1];
        
        for label in labels:
            if label not in label_to_index:
                label_to_index[label] = len(label_to_index) + 1;
                index_to_label[len(index_to_label) + 1] = label;
                index_to_count[label_to_index[label]] = 0;

            weight = 1;
            if weight_index >= 0 and weight_index < len(fields):
                weight *= float(fields[weight_index]);
                
            index_to_count[label_to_index[label]] += weight;
    
    export_label_index(label_index_count_file, label_to_index, index_to_count);

    return label_to_index, index_to_label, index_to_count;

def import_label_index(label_index_count_file):
    label_index_file_stream = codecs.open(label_index_count_file, 'r');
    label_to_index = {};
    index_to_label = {};
    index_to_count = {};
    for line in label_index_file_stream:
        line = line.strip();
        tokens = line.split("\t");
        index_to_label[int(tokens[1])] = tokens[0];
        label_to_index[tokens[0]] = int(tokens[1]);
        if len(tokens) == 3:
            index_to_count[int(tokens[1])] = int(tokens[2]);
    
    return label_to_index, index_to_label, index_to_count;

def export_label_index(label_index_count_file, label_to_index, index_to_count=None):
    label_index_file_stream = codecs.open(label_index_count_file, 'w');
    for label in label_to_index:
        if index_to_count != None:
            label_index_file_stream.write("%s\t%d\t%d\n" % (label, label_to_index[label], index_to_count[label_to_index[label]]));
        else:
            label_index_file_stream.write("%s\t%d\n" % (label, label_to_index[label]));
    label_index_file_stream.close()
    print "successfully export label index..."

if __name__ == '__main__':
    input_directory = sys.argv[1];
    output_directory = sys.argv[2];
    
    '''
    kb_directory = sys.argv[3];
    
    if len(sys.argv)<=4:
        lm_directory = None;
    else:
        lm_directory = sys.argv[4];
    
    if len(sys.argv)<=5:
        weighted=False;
    else:
        if sys.argv[5].lower()=="false":
            weighted=False;
        elif sys.argv[5].lower()=="true":
            weighted=True;
        else:
            sys.stderr.write("unrecognized option...")
            sys.exit();
    '''
    
    # extract_feature_vectors_for_directory(input_directory, output_directory, kb_directory, lm_directory, weighted);
    
    extract_feature_vectors_for_directory(input_directory, output_directory);
    
