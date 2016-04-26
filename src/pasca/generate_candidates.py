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

def generate_entity_candidates(query_file, template_file, candidate_file):
    # template_dictionary = {};
    template_patterns = set();
    template_file_stream = codecs.open(template_file, "r", encoding="utf-8");
    for line in template_file_stream:
        line = line.strip("\n");
        fields = line.split("\t")
        # assert len(fields)==3;
        
        template_pattern = re.compile(r'(?P<prefix>%s) (?P<entity>.+) (?P<postfix>%s)' % (fields[0], fields[1]))
        template_patterns.add(template_pattern);
        
    query_file_stream = codecs.open(query_file, 'r', encoding='utf-8');
    candidate_set = set();
    line_count = 0;
    for line in query_file_stream:
        line_count += 1;
        line = line.strip();

        fields = line.split("\t");
        assert len(fields) == 2;
        fields[0] = pattern.sub('', fields[0])
        fields[0] = "%s %s %s" % (prefix_string, fields[0], postfix_string);
        
        for template_pattern in template_patterns:
            matcher = re.match(template_pattern, fields[0]);
            #if fields[0]=="samsung rugby case" or line=="samsung rugby case\t154":
                #print template_pattern.pattern, fields[0], matcher.group("entity");
            
            if matcher is not None:
                entity = matcher.group("entity");
                entity = entity.strip();
                candidate_set.add(entity);
            
        if line_count % 10000 == 0:
            print "successfully processed %d lines..." % line_count
    
    candidate_file_stream = codecs.open(candidate_file, "w", encoding="utf-8");
    for entity in candidate_set:
        candidate_file_stream.write("%s\n" % entity);
        
if __name__ == '__main__':
    query_file = sys.argv[1]
    template_file = sys.argv[2]
    candidate_file = sys.argv[3]
    #print query_file, template_file, candidate_file
    generate_entity_candidates(query_file, template_file, candidate_file);
