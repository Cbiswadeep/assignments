#!/usr/bin/env python
import os, sys,re
import string
import math
import re



class emission:
    def __init__(self, file_path):
        self.wordtag_dictionary = {}
        self.one_gram = {}
        self.labels = []
        self.words_dict = {}
        f = open(file_path, "r")
        lines = f.readlines()
        f.close()
        for line in lines:
            words = line.split()
            if len(words) < 3:
                continue
            if words[1] == 'WORDTAG':
                if not self.wordtag_dictionary.has_key(words[2]):
                    self.wordtag_dictionary[words[2]] = {}
                if not self.wordtag_dictionary[words[2]].has_key(words[3]):
                    self.wordtag_dictionary[words[2]][words[3]] = 0
                
                self.wordtag_dictionary[words[2]][words[3]] += string.atoi(words[0])
                

            elif words[1] == '1-GRAM':
                if not self.one_gram.has_key(words[2]):
                    self.one_gram[words[2]] = string.atoi(words[0])
                else:
                    self.one_gram[words[2]] += string.atoi(words[0])

    def calculate(self, calculate_path, calculate_out_path):
        f = open(calculate_path, 'r')
        lines = f.readlines()
        f.close()
        lines2 = []
        for line in lines:
            line2 = line
            words = line.split()
            if len(words) > 0:
                flag = False
                x = words[0]
                for y in self.wordtag_dictionary:
                    if self.wordtag_dictionary[y].has_key(x):
                        if (flag and float(self.wordtag_dictionary[y][x]) / self.one_gram[y] > max_prob) or not flag:
                            max_prob = float(self.wordtag_dictionary[y][x]) / self.one_gram[y]
                            max_label = y
                            flag = True
                if not flag:
                    x = "_RARE_"
                    for y in self.wordtag_dictionary:
                        if self.wordtag_dictionary[y].has_key(x):
                            if (flag and float(self.wordtag_dictionary[y][x]) / self.one_gram[y] > max_prob) or not flag:
                                max_prob = float(self.wordtag_dictionary[y][x]) / self.one_gram[y]
                                max_label = y
                                flag = True
                assert flag == True
                line2 = words[0] + " " + max_label + "\n"
            lines2.append(line2)
        f = open(calculate_out_path, "w")
        f.writelines(lines2)
        f.close()



if __name__ == "__main__":
    counts_path = sys.argv[1]
    calculate_path = sys.argv[2]
    calculate_out_path = sys.argv[3]
    epara = emission(counts_path)
    epara.calculate(calculate_path, calculate_out_path)
