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

import re, string;
pattern = re.compile('[^a-zA-Z0-9\s]+')

prefix_string = "PREFIX"
postfix_string = "POSTFIX"

def generate_templates(query_file, seeds_file, template_file):
    #entity_seeds = set();
    entity_patterns = set();
    seeds_file_stream = codecs.open(seeds_file, 'r', encoding="utf-8");
    for line in seeds_file_stream:
        line = line.strip();
    
        entity_pattern = re.compile(r'(?P<prefix>.+) (?P<entity>(%s)) (?P<postfix>.+)' % (line));
        entity_patterns.add(entity_pattern);
        
        #print entity_pattern.pattern

    query_file_stream = codecs.open(query_file, 'r', encoding='utf-8');
    line_count = 0;
    #template_to_index = {}
    #template_to_count = {}
    template_counter = collections.Counter()
    for line in query_file_stream:
        line_count += 1;
        line = line.strip();

        fields = line.split("\t");
        assert len(fields) == 2;
        #if float(fields[1])<=100:
        #continue;
        
        #fields[0] = pattern.sub('', fields[0])
        amended_query = "%s %s %s" % (prefix_string, fields[0], postfix_string);
        
        for entity_pattern in entity_patterns:
            matcher = re.match(entity_pattern, amended_query);
            if matcher is None:
                continue;
        
            entity = matcher.group("entity");
            prefix = matcher.group("prefix")
            postfix = matcher.group("postfix")
            
            # this is to avoid entity only patterns
            if prefix==prefix_string and postfix==postfix_string:
                continue;
            
            '''
            if fields[0].startswith('cleveland'):
                print entity_pattern.pattern
                print entity, prefix, postfix
            '''
            
            template_counter[(prefix, postfix)] += 1;
            
        if line_count % 10000 == 0:
            print "successfully processed %d lines..." % line_count
    
    template_file_stream = codecs.open(template_file, 'w', encoding="utf-8");        
    for (template, count) in template_counter.most_common():
        template_file_stream.write("%s\t%s\t%g\n" % (template[0], template[1], template_counter[template]));
        
if __name__ == '__main__':
    query_file = sys.argv[1]
    seeds_file = sys.argv[2]
    template_file = sys.argv[3]
    generate_templates(query_file, seeds_file, template_file);
