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

def load_dictionary(dictionary_path):
    word_set = set();
    for char in string.ascii_lowercase:
        word_set.add(char)

    dictionary_stream = open(dictionary_path, 'r');
    for line in dictionary_stream:
        line = line.strip().lower();
        if not line.isalpha():
            print "skip word %s..." % line;
            continue;
        word_set.add(line);

    return word_set

def word_break_for_file(input_path, dictionary_path, output_directory=None):
    word_set = load_dictionary(dictionary_path);
    input_stream = open(input_path, 'r');
    for line in input_stream:
        input_line = line.strip().lower();
        word_breaks = [word_break.upper().split("\t") for word_break in (word_break_for_line(input_line, word_set))];
        word_breaks.sort(key = lambda word_break:len(word_break));
        print "%s\t%s" % (input_line.upper(), word_breaks)

def word_break_for_line(input_line, word_set):
    word_breaks = {};
    for start in xrange(len(input_line)):
        word_breaks[(start, start + 1)] = set(input_line[start:start+1]);
        #word_breaks[(start, start + 1)] = set();
    for length in xrange(2, len(input_line) + 1):
        for start in xrange(len(input_line) + 1 - length):
            end = start + length;
            word_breaks[(start, end)] = set();
            if input_line[start:end] in word_set:
                word_breaks[(start, end)].add(input_line[start:end]);
            for middle in xrange(start + 1, end):
                for word_break_1 in word_breaks[(start, middle)]:
                    for word_break_2 in word_breaks[(middle, end)]:
                        word_breaks[(start, end)].add("%s\t%s" % (word_break_1, word_break_2));
    return word_breaks[(0, len(input_line))];

if __name__ == '__main__':
    input_path = sys.argv[1]
    dictionary_path = sys.argv[2]
    #output_directory = sys.argv[3]

    word_break_for_file(input_path, dictionary_path);