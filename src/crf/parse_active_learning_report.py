#!/usr/bin/env python

import sys

dict = {}
f1 = open("random_select.eval")
count = 0
for line in f1:
    count = count + 1

    if count % 5 == 1 and "evaluating on" in line:
        round = (count/5 + 1)*2 + 20
    if count % 5 == 3 and "accuracy" in line:
        F1_score = line.split("FB1: ")[1].strip()
    if count % 5 == 0:
        #print count,"\t",F1_score
        print F1_score
