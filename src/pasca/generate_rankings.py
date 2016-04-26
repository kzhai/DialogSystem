# -*- coding: utf-8 -*-

import nltk
import numpy
import scipy
import collections
import math
import string
import time
import sys
import operator
import os
import random
import codecs
import unicodedata
import re

from generate_templates import prefix_string, postfix_string, pattern

def JSD(P, Q):
    _P = P / numpy.linalg.norm(P, ord=1)
    _Q = Q / numpy.linalg.norm(Q, ord=1)
    _M = 0.5 * (_P + _Q)
    return 0.5 * (scipy.stats.entropy(_P, _M) + scipy.stats.entropy(_Q, _M))
    
def generate_query_templates(query_file, class_template_file, candidate_file, template_file, ranking_file):
    candidate_to_index = {};
    index_to_candidate = {};
    candidate_file_stream = codecs.open(candidate_file, 'r', encoding="utf-8");
    entity_patterns = set();
    for line in candidate_file_stream:
        line = line.strip();
        assert line not in candidate_to_index, (line)
        
        candidate_to_index[line] = len(candidate_to_index);
        index_to_candidate[len(index_to_candidate)] = line;
        entity_pattern = re.compile(r'(?P<prefix>.+) (?P<entity>(%s)) (?P<postfix>.+)' % (line));
        entity_patterns.add(entity_pattern)
        
    print "successfully load candidates..."
    
    #entity_patterns = re.compile(r'(?P<prefix>.+) (?P<entity>(%s)) (?P<postfix>.+)' % ("|".join(candidate_to_index.keys())));
    
    template_file_stream = codecs.open(template_file, "r", encoding="utf-8");
    template_to_index = {}
    index_to_template = {}
    index_to_template_pattern = {}
    for line in template_file_stream:
        line = line.strip("\n");
        fields = line.split("\t")
        
        prefix = fields[0];
        postfix = fields[1];
        
        template_to_index[(prefix, postfix)] = len(template_to_index);
        index_to_template[len(index_to_template)] = (prefix, postfix);
        index_to_template_pattern[len(index_to_template_pattern)] = re.compile(r'(?P<prefix>%s) (?P<entity>.+) (?P<postfix>%s)' % (prefix, postfix));
    
    print "successfully load templates..."
    
    class_vector = numpy.zeros(len(template_to_index));
    class_template_file_stream = codecs.open(class_template_file, 'r', encoding='utf-8');
    for line in class_template_file_stream:
        line = line.strip("\n");
        fields = line.split("\t")
        
        assert (fields[0], fields[1]) in template_to_index, (fields[0], fields[1], line);
        
        class_vector[template_to_index[(fields[0], fields[1])]] = float(fields[2]);
    class_vector /= numpy.sum(class_vector)
    
    print class_vector
    
    candidate_vectors = numpy.zeros((len(candidate_to_index), len(template_to_index)))
    query_file_stream = codecs.open(query_file, 'r', encoding='utf-8');
    line_count = 0
    for line in query_file_stream:
        line_count += 1;
        line = line.strip();

        fields = line.split("\t");
        assert len(fields) == 2;
        fields[0] = pattern.sub('', fields[0])
        fields[0] = "%s %s %s" % (prefix_string, fields[0], postfix_string);

        for template_index in index_to_template:
            #print template_index, index_to_template_pattern[template_index].pattern, fields[0]
            matcher = re.match(index_to_template_pattern[template_index], fields[0]);
            if matcher is not None:
                entity = matcher.group("entity");
                if entity not in candidate_to_index:
                    continue;
                candidate_index = candidate_to_index[entity];
                candidate_vectors[candidate_index, template_index] += float(fields[1]);
        
        if line_count % 10000 == 0:
            print "successfully processed %d lines..." % line_count
        
    candidate_vectors /= numpy.sum(candidate_vectors, axis=1)[:, numpy.newaxis];
    
    candidate_ranking = {};
    for candidate_index in xrange(len(candidate_to_index)):
        candidate_ranking[index_to_candidate[candidate_index]] = JSD(class_vector, candidate_vectors[candidate_index]);
        
    sorted_candidate_ranking = sorted(candidate_ranking.items(), key=operator.itemgetter(1))
    ranking_file_stream = codecs.open(ranking_file, 'w', encoding="utf-8");
    for (candidate, ranking) in sorted_candidate_ranking:
        ranking_file_stream.write("%s\t%g\n" % (candidate, ranking))
    
if __name__ == '__main__':
    query_file = sys.argv[1]
    seed_template_file = sys.argv[2]
    candidate_file = sys.argv[3]
    template_file = sys.argv[4]
    ranking_file = sys.argv[5]
    generate_query_templates(query_file, seed_template_file, candidate_file, template_file, ranking_file);
