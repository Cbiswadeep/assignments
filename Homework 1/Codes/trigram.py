#!/usr/bin/env python
import os, sys,re
import string
import math
import re


class viterbi_algo:
    def __init__(self, file_path):
        self.xy_dict = {}
        self.one_gram = {}
        self.two_gram = {}
        self.three_gram = {}
        self.words_dict = {}
        self.labels = []
        f = open(file_path, "r")
        lines = f.readlines()
        f.close()
        for line in lines:
            words = line.split()
            if len(words) < 3:
                continue
            if words[1] == 'WORDTAG':
                if not self.xy_dict.has_key(words[2]):
                    self.xy_dict[words[2]] = {}
                if not self.xy_dict[words[2]].has_key(words[3]):
                    self.xy_dict[words[2]][words[3]] = 0
                self.xy_dict[words[2]][words[3]] += string.atoi(words[0])

                if words[2] not in self.labels:
                    self.labels.append(words[2])
                if words[3] not in self.words_dict:
                    self.words_dict[words[3]] = 0
            elif words[1] == '1-GRAM':
                if not self.one_gram.has_key(words[2]):
                    self.one_gram[words[2]] = string.atoi(words[0])
                else:
                    self.one_gram[words[2]] += string.atoi(words[0])
            elif words[1] == '2-GRAM':
                if not self.two_gram.has_key(words[2]):
                    self.two_gram[words[2]] = {}
                if not self.two_gram[words[2]].has_key(words[3]):
                    self.two_gram[words[2]][words[3]] = string.atoi(words[0])
                else:
                    self.two_gram[words[2]][words[3]] += string.atoi(words[0])
            elif words[1] == '3-GRAM':
                if not self.three_gram.has_key(words[2]):
                    self.three_gram[words[2]] = {}
                if not self.three_gram[words[2]].has_key(words[3]):
                    self.three_gram[words[2]][words[3]] = {}
                if not self.three_gram[words[2]][words[3]].has_key(words[4]):
                    self.three_gram[words[2]][words[3]][words[4]] = string.atoi(words[0])
                else:
                    self.three_gram[words[2]][words[3]][words[4]] += string.atoi(words[0])
        

    def classify(self, classify_path, classify_out_path):
        f = open(classify_path, 'r')
        lines = f.readlines()
        f.close()
        lines2 = []
        sentence = []
        
        for line in lines:
            line2 = line
            if len(line) <= 1:
                max_labels = self.classify_sentence(sentence)
                for i in range(0,len(sentence)):
                    words = sentence[i].split()
                    line2 = words[0] + " " + max_labels[i] + "\n"
                    lines2.append(line2)
                lines2.append("\n")
                sentence = []
            else:
                sentence.append(line)
        f = open(classify_out_path, 'w')
        f.writelines(lines2)
        f.close()
            
        
    def classify_sentence(self, sentence):
        v_numeric = re.compile(r"^.*[0-9]+.*$")
        v_all_cap = re.compile(r"^[A-Z]+$")
        v_last_cap = re.compile(r"^.*[A-Z]$")
        v_states = []
        v_labels = []
        v_states.append({})
        v_labels.append({})
        v_states[0]['*'] = {}
        v_labels[0]['*'] = {}
        for label in self.labels:
            v_labels[0]['*'][label] = '*'
            word = sentence[0].split()[0]
            if not self.words_dict.has_key(word):
                if v_numeric.match(word):
                    word = '_NUMERIC_'
                elif v_all_cap.match(word):
                    word = '_ALLCAP_'
                elif v_last_cap.match(word):
                    word = '_LASTCAP_'
                else:
                    word = '_RARE_'
            v_states[0]['*'][label] = math.log(self.three_gram['*']['*'][label]) - math.log(self.two_gram['*']['*']) + math.log((self.xy_dict[label].has_key(word) and self.xy_dict[label][word] or 1)) - math.log(self.one_gram[label])
            v_states[0]['*'][label] = self.xy_dict[label].has_key(word) and v_states[0]['*'][label] or float('-inf')
        v_states.append({})
        v_labels.append({})
        for label in self.labels:
            if not v_states[1].has_key(label):
                v_states[1][label] = {}
            if not v_labels[1].has_key(label):
                v_labels[1][label] = {}
            for label2 in self.labels:
                word = sentence[1].split()[0]
                if not self.words_dict.has_key(word):
                    if v_numeric.match(word):
                        word = '_NUMERIC_'
                    elif v_all_cap.match(word):
                        word = '_ALLCAP_'
                    elif v_last_cap.match(word):
                        word = '_LASTCAP_'
                    else:
                        word = '_RARE_'
                v_states[1][label][label2] = v_states[0]['*'][label] + math.log(self.three_gram['*'][label][label2]) - math.log(self.two_gram['*'][label]) + math.log(self.xy_dict[label2].has_key(word) and self.xy_dict[label2][word] or 1) - math.log(self.one_gram[label2])
                v_states[1][label][label2] = self.xy_dict[label2].has_key(word) and v_states[1][label][label2] or float('-inf')
                v_labels[1][label][label2] = '*'
                
                
        for i in range(2,len(sentence)):
            v_states.append({})
            v_labels.append({})
            for label in self.labels:
                if not v_states[i].has_key(label):
                    v_states[i][label] = {}
                if not v_labels[i].has_key(label):
                    v_labels[i][label] = {}
                for label2 in self.labels:
                    flag = False
                    word = sentence[i].split()[0]
                    if not self.words_dict.has_key(word):
                        if v_numeric.match(word):
                            word = '_NUMERIC_'
                        elif v_all_cap.match(word):
                            word = '_ALLCAP_'
                        elif v_last_cap.match(word):
                            word = '_LASTCAP_'
                        else:
                            word = '_RARE_'
                    for label0 in self.labels:
                        if flag:
                            v_storage = v_states[i-1][label0][label] + math.log(self.three_gram[label0][label][label2]) - math.log(self.two_gram[label0][label]) + math.log(self.xy_dict[label2].has_key(word) and self.xy_dict[label2][word] or 1) - math.log(self.one_gram[label2])
                            v_storage = self.xy_dict[label2].has_key(word) and v_storage or float('-inf')
                            if v_storage > max_v_storage:
                                max_v_storage = v_storage
                                max_label0 = label0
                        else:
                            flag = True
                            v_storage = v_states[i-1][label0][label] + math.log(self.three_gram[label0][label][label2]) - math.log(self.two_gram[label0][label]) + math.log(self.xy_dict[label2].has_key(word) and self.xy_dict[label2][word] or 1) - math.log(self.one_gram[label2])
                            v_storage = self.xy_dict[label2].has_key(word) and v_storage or float('-inf')
                            max_v_storage = v_storage
                            max_label0 = label0
                    v_states[i][label][label2] = max_v_storage
                    v_labels[i][label][label2] = max_label0
                    
                    

        i = len(sentence)
        v_states.append({})
        v_labels.append({})
        label2 = 'STOP'
        for label in self.labels:
            if not v_states[i].has_key(label):
                v_states[i][label] = {}
            if not v_labels[i].has_key(label):
                v_labels[i][label] = {}
            flag = False
            for label0 in self.labels:
                if flag:
                    v_storage = v_states[i-1][label0][label] + math.log(self.three_gram[label0][label][label2]) - math.log(self.two_gram[label0][label])
                    if v_storage > max_v_storage:
                        max_v_storage = v_storage
                        max_label0 = label0
                else:
                    flag = True
                    v_storage = v_states[i-1][label0][label] + math.log(self.three_gram[label0][label][label2]) - math.log(self.two_gram[label0][label])
                    max_v_storage = v_storage
                    max_label0 = label0
            v_states[i][label][label2] = max_v_storage
            v_labels[i][label][label2] = max_label0

        max_labels = [0]*len(sentence)
        flag = False
        for label in self.labels:
            if flag:
                if v_states[i][label][label2] > max_v_storage:
                    max_v_storage = v_states[i][label][label2]
                    max_label = label
            else:
                flag = True
                max_v_storage = v_states[i][label][label2]
                max_label = label
        label = max_label
        label0 = v_labels[i][label][label2]
        for i in range(len(sentence)-1, -1, -1):
            max_labels[i] = label
            label2 = label
            label = label0
            label0 = v_labels[i][label][label2]
        return max_labels


if __name__ == "__main__":
    counts_path = sys.argv[1]
    test_path = sys.argv[2]
    test_out_path = sys.argv[3]
    epara = viterbi_algo(counts_path)
    epara.classify(test_path, test_out_path)
