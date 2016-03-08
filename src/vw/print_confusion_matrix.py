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
from matplotlib.pyplot import matshow

def print_confusion_matrix(groundtruth_label_file, prediction_label_file, label_to_index_file):
    label_to_index = {};
    label_to_index_stream = open(label_to_index_file, 'r');
    for line in label_to_index_stream:
        line = line.strip();
        tokens = line.split();
        label_to_index[int(tokens[1])] = tokens[0];
    
    number_of_classes = len(label_to_index);
    #groundtruth_label_matrix = numpy.zeros((0, number_of_classes));
    #prediction_label_matrix = numpy.zeros((0, number_of_classes));
    confusion_matrix = numpy.zeros((number_of_classes, number_of_classes), dtype=int);
    
    groundtruth_label_stream = open(groundtruth_label_file, 'r');
    prediction_label_stream = open(prediction_label_file, 'r');
    while True:
        groundtruth_line = groundtruth_label_stream.readline().strip();
        if len(groundtruth_line) == 0:
            groundtruth_line = None;
        
        prediction_line = prediction_label_stream.readline().strip();
        if len(prediction_line) == 0:
            prediction_line = None;
        
        if (groundtruth_line == None) and (prediction_line == None):
            break;
        elif (groundtruth_line == None) and (prediction_line != None):
            sys.stderr.write("eof %s before eof %s...\n" % (groundtruth_label_file, prediction_label_file));
            sys.exit()
        elif (groundtruth_line != None) and (prediction_line == None):
            sys.stderr.write("eof %s after eof %s...\n" % (groundtruth_label_file, prediction_label_file));
            sys.exit()
        else:
            pass
            
        groundtruth_label = int(groundtruth_line.split()[0]);
        prediction_label = int(float(prediction_line.split()[0]));
        
        '''
        if groundtruth_label > prediction_label:
            max_class_index = groundtruth_label;
        else:
            max_class_index = prediction_label;
            
        if max_class_index > number_of_classes:
            confusion_matrix = numpy.hstack((confusion_matrix, numpy.zeros((number_of_classes, max_class_index - number_of_classes), dtype=int)));
            confusion_matrix = numpy.vstack((confusion_matrix, numpy.zeros((max_class_index - number_of_classes, max_class_index), dtype=int)));
            number_of_classes = max_class_index;
        '''
        
        confusion_matrix[groundtruth_label - 1, prediction_label - 1] += 1;
        
    diagonal_element = numpy.diag(confusion_matrix);
    
    '''
    print "\t".join([label_to_index[x+1] for x in xrange(len(label_to_index))])
    for x in xrange(len(label_to_index)):
        print "%s\t%s" % (label_to_index[x+1], "\t".join("%s" % value for value in confusion_matrix[x, :]))
    '''
        
    precision_sum = numpy.sum(confusion_matrix, axis=0);
    recall_sum = numpy.sum(confusion_matrix, axis=1);
    
    precision = 1.0 * numpy.sum(diagonal_element) / numpy.sum(precision_sum)
    recall = 1.0 * numpy.sum(diagonal_element) / numpy.sum(recall_sum)
    f_score = 2 * precision * recall / (precision + recall);
    print "%s\t%f (%d/%d)\t%f (%d/%d)\t%f" % ("all",
                                              precision,
                                              numpy.sum(diagonal_element),
                                              numpy.sum(precision_sum),
                                              recall,
                                              numpy.sum(diagonal_element),
                                              numpy.sum(recall_sum),
                                              f_score
                                              )
    
    for x in xrange(len(label_to_index)):
        if precision_sum[x] == 0:
            precision = 0;
        else:
            precision = 1.0 * diagonal_element[x] / precision_sum[x];
        if recall_sum[x] == 0:
            recall = 0;
        else:
            recall = 1.0 * diagonal_element[x] / recall_sum[x];
        if precision + recall == 0:
            f_score = 0;
        else:
            f_score = 2 * precision * recall / (precision + recall);
        print "%s\t%f (%d/%d)\t%f (%d/%d)\t%f" % (label_to_index[x + 1],
                                                  precision,
                                                  diagonal_element[x],
                                                  precision_sum[x],
                                                  recall,
                                                  diagonal_element[x],
                                                  recall_sum[x],
                                                  f_score
                                                  )
    # print "accuracy:\n", 1.0 * numpy.sum(numpy.diag(confusion_matrix)) / numpy.sum(confusion_matrix);
    
if __name__ == '__main__':
    groundtruth_label_file = sys.argv[1];
    prediction_label_file = sys.argv[2];
    label_to_index_file = sys.argv[3];
    print_confusion_matrix(groundtruth_label_file, prediction_label_file, label_to_index_file);
