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

import feature_extractor;

def import_label_index(label_index_file, prediced_index_file, label_class_file=None):
    label_to_index, index_to_label, index_to_count = feature_extractor.import_label_index(label_index_file);
    
    label_to_class = {};
    if label_class_file!=None:
        for line in open(label_class_file, 'r'):
            line = line.strip();
            tokens = line.split("\t");
            label_to_class[tokens[0]] = tokens[1];
        
    for line in open(prediced_index_file, 'r'):
        line = line.strip();
        index = int(line.split(".")[0]);
        label = index_to_label[index]
        if label_class_file!=None:
            print label_to_class[label];
        else:
            print label;
    
if __name__ == '__main__':
    label_index_file = sys.argv[1];
    predicted_index_file = sys.argv[2];
    if len(sys.argv)==4:
        label_class_file = sys.argv[3];
    else:
        label_class_file = None;
    import_label_index(label_index_file, predicted_index_file, label_class_file);
