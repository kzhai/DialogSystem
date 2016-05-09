import codecs;
import collections;
import heapq;
import matplotlib;
import matplotlib.pyplot;
import nltk;
import numpy;
import operator;
import optparse;
import os;
import re;
import scipy;
import shutil;
import sys;
import time;
import unicodedata;

'''
function_dict = {
    'least_confidence' : least_confidence,
    'my other class' : MyOtherClass
}
'''

# crfpp_sequence_label_probability_pattern = re.compile(r'# (\d+) ([\d\.]+)')

crfpp_sequence_label_probability_pattern = re.compile(r"# (?P<index>\d+) (?P<probability>\d+\.\d+)")

def least_confidence(predicted_file, heap_size):
    predicted_stream = codecs.open(predicted_file, 'r');
    heap = [];
    unlabeled = set();

    label_probability = -1;
    query_feature_string = "";
    
    for line in predicted_stream:
        line = line.strip();
        
        if label_probability == -1:
            matcher = re.match(crfpp_sequence_label_probability_pattern, line)
            if matcher:
                index = int(matcher.group("index"));
                probability = float(matcher.group("probability"));
                if index == 0:
                    label_probability = probability
                    query_feature_string = "";
        else:
            if len(line) == 0:
                heapq.heappush(heap, (1 - label_probability, query_feature_string));
                
                if len(heap) > heap_size:
                    unlabeled.add(heapq.heappop(heap));
                
                label_probability = -1;
                query_feature_string = "";
            else:
                tokens = line.split("\t")[:-1]
                query_feature_string += "%s\n" % "\t".join(tokens);

    return heap, unlabeled;

def least_margin(predicted_file, heap_size):
    predicted_stream = codecs.open(predicted_file, 'r');
    heap = [];
    unlabeled = set();
    
    label_probability = [];
    query_feature_string = "";
    
    for line in predicted_stream:
        line = line.strip();
        
        if len(label_probability) < 2:
            matcher = re.match(crfpp_sequence_label_probability_pattern, line)
            if matcher:
                index = int(matcher.group("index"));
                probability = float(matcher.group("probability"));
                if index == 0:
                    label_probability.append(probability);
                    query_feature_string = "";
                elif index == 1:
                    label_probability.append(probability);
                    query_feature_string = "";
        else:
            if len(line) == 0:
                heapq.heappush(heap, (label_probability[1] - label_probability[0], query_feature_string));
                
                if len(heap) > heap_size:
                    unlabeled.add(heapq.heappop(heap));
                
                label_probability = [];
                query_feature_string = "";
            else:
                tokens = line.split("\t")[:-1]
                query_feature_string += "%s\n" % "\t".join(tokens);
    
    return heap, unlabeled;

def n_best_sequence_entropy(predicted_file, heap_size, **kwargs):
    def n_best_sequence_entropy_helper():
        sequence_entropy = numpy.asarray(sequence_probability)
        heapq.heappush(heap, (-numpy.sum(sequence_entropy * numpy.log(sequence_entropy)), query_feature_string));
        if len(heap) > heap_size:
            unlabeled.add(heapq.heappop(heap));
    
    predicted_stream = codecs.open(predicted_file, 'r');
    heap = [];
    unlabeled = set();
    
    n_best = kwargs.get('n_best', -1)
    
    sequence_probability = [];
    query_feature_string = "";
    
    for line in predicted_stream:
        line = line.strip();
        if not line:
            continue;

        matcher = re.match(crfpp_sequence_label_probability_pattern, line)
        if not matcher:
            if len(sequence_probability) == 1:
                tokens = line.split("\t")[:-1]
                query_feature_string += "%s\n" % "\t".join(tokens);
        else:
            index = int(matcher.group("index"));
            probability = float(matcher.group("probability"));
            
            if index == 0:
                if query_feature_string != "":
                    n_best_sequence_entropy_helper();
                    '''
                    sequence_entropy = numpy.asarray(sequence_probability)
                    heapq.heappush(heap, (-numpy.sum(sequence_entropy * numpy.log(sequence_entropy)), query_feature_string));
                    if len(heap) > heap_size:
                        heapq.heappop(heap);
                    '''
                
                sequence_probability = [];
                query_feature_string = "";
            
            if probability > 0 and (n_best < 0 or index < n_best):
                sequence_probability.append(probability)
                # query_feature_string = "";

    n_best_sequence_entropy_helper();
    '''
    sequence_entropy = numpy.asarray(sequence_probability)
    heapq.heappush(heap, (-numpy.sum(sequence_entropy * numpy.log(sequence_entropy)), query_feature_string));
    if len(heap) > heap_size:
        heapq.heappop(heap);
    '''

    return heap, unlabeled;

def uncertainty_sampling(predicted_file, confused_file, unlabel_file, uncertainty_function, heap_size=2):
    heap, unlabeled = uncertainty_function(predicted_file, heap_size);
    
    confused_stream = codecs.open(confused_file, 'w');
    for (confidence_score, query_feature_string) in heap:
        confused_stream.write("%s\n" % query_feature_string);
    print "successfully output %d data to %s" % (len(heap), confused_file);
        
    unlabel_stream = codecs.open(unlabel_file, 'w');
    for (confidence_score, query_feature_string) in unlabeled:
        unlabel_stream.write("%s\n" % query_feature_string);
    print "successfully output %d data to %s" % (len(unlabeled), unlabel_file);
        
if __name__ == '__main__':
    parser = optparse.OptionParser()
    # parser.set_defaults()
    parser.add_option("--predicted_file", type="string", dest="predicted_file", default=None, help="predicted file")
    parser.add_option("--confused_file", type="string", dest="confused_file", default=None, help="confused file")
    parser.add_option("--unlabel_file", type="string", dest="unlabel_file", default=None, help="unlabel file")
    parser.add_option("--uncertainty_function", type="string", dest="uncertainty_function", default=None, help="uncertainty function")
    parser.add_option("--top_n_candidates", type="int", dest="top_n_candidates", default=None, help="top n candidates")
    (options, args) = parser.parse_args();
    
    predicted_file = options.predicted_file;
    confused_file = options.confused_file;
    unlabel_file = options.unlabel_file;
    uncertainty_function = options.uncertainty_function;
    uncertainty_function = locals()[uncertainty_function]
    top_n_candidates = options.top_n_candidates
    
    uncertainty_sampling(predicted_file, confused_file, unlabel_file, uncertainty_function, heap_size=top_n_candidates);
