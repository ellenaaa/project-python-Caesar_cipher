#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 02:09:24 2020

@author: ellenai
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 
# Final Project
#
# Name: Haipeng Zhang
# Email: zhanghp@bu.edu

import math
class TextModel:
    """ a blueprint for objects that model a body of text.
    """
    
    #Part I
    #1
    def  __init__(self, model_name):
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        self.stems = {}
        self.sentence_lengths = {}
        self.punctuation = {}
        
        
    #2
    def __repr__(self):
        """ returns a string that includes the name of the model as well as 
            the sizes of the dictionaries for each feature of the text.
        """
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) + '\n'
        s += '  number of stems: ' + str(len(self.stems)) + '\n'
        s += '  number of sentence_lengths: ' + str(len(self.sentence_lengths)) + '\n'
        s += '  number of punctuation: ' + str(len(self.punctuation))
        return s
    
    #4
    def add_string(self, s):
        """ adds a string of text s to the model by augmenting 
            the feature dictionaries defined in the constructor.
        """
        sen = s.split()
        #sentence lengths
        num = 0
        for w in sen:
            num += 1
            if w[-1] in '.?!':
                if num not in self.sentence_lengths:
                    self.sentence_lengths[num] = 1
                else:
                    self.sentence_lengths[num] += 1
                num = 0
        #punctuation
        for w in sen:
            if w[-1] in '.,?!:;"':
                if w[-1] not in self.punctuation:
                    self.punctuation[w[-1]] = 1
                else:
                    self.punctuation[w[-1]] += 1
            
        # Add code to clean the text and split it into a list of words.
        # *Hint:* Call one of the functions you have already written!
        word_list = clean_text(s)

        # Template for updating the words dictionary.
        for w in word_list:
            # Update self.words to reflect w
            # either add a new key-value pair for w
            # or update the existing key-value pair.
                
        # Add code to update other feature dictionaries.
            if w not in self.words:
                self.words[w] = 1
            else:
                self.words[w] += 1
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            else:
                self.word_lengths[len(w)] += 1
            #stems
            if stem(w) not in self.stems:
                self.stems[stem(w)] = 1
            else:
                self.stems[stem(w)] += 1
        
    #5
    def add_file(self, filename):
        """ adds all of the text in the file identified by filename to the model.
        """
        f = open(filename, 'r', encoding='utf8', errors='ignore')
        text = f.read()
        f.close()
        self.add_string(text)
        
    #Part II
    #1
    def save_model(self):
        """ saves the TextModel object self by writing its various feature 
            dictionaries to files.
        """
        f1 = open(self.name + '_' + 'words', 'w')
        f1.write(str(self.words))
        f1.close()
        
        f2 = open(self.name + '_' + 'word_lengths', 'w')
        f2.write(str(self.word_lengths))
        f2.close()
        
        f3 = open(self.name + '_' + 'stems', 'w')
        f3.write(str(self.stems))
        f3.close()
        
        f4 = open(self.name + '_' + 'sentence_lengths', 'w')
        f4.write(str(self.sentence_lengths))
        f4.close()
        
        f5 = open(self.name + '_' + 'punctuation', 'w')
        f5.write(str(self.punctuation))
        f5.close()
        
        
    #2
    def read_model(self):
        """ reads the stored dictionaries for the called TextModel object from 
            their files and assigns them to the attributes of the called TextModel.
        """
        f6 = open(self.name + '_' + 'words', 'r')
        dword_str = f6.read()
        f6.close()
        self.words = dict(eval(dword_str))
        
        f7 = open(self.name + '_' + 'word_lengths', 'r')
        dlen_str = f7.read()
        f7.close()
        self.word_lengths = dict(eval(dlen_str))
        
        f8 = open(self.name + '_' + 'stems', 'r')
        dstem_str = f8.read()
        f8.close()
        self.stems = dict(eval(dstem_str))
        
        f9 = open(self.name + '_' + 'sentence_lengths', 'r')
        dsen_str = f9.read()
        f9.close()
        self.sentence_lengths = dict(eval(dsen_str))
        
        f10 = open(self.name + '_' + 'punctuation', 'r')
        dpun_str = f10.read()
        f10.close()
        self.punctuation = dict(eval(dpun_str))
    
    #Part IV
    #2
    def similarity_scores(self, other):
        """ returns a list of log similarity scores measuring the similarity 
            of self and other.
        """
        word_score = compare_dictionaries(other.words, self.words)
        word_lengths_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        stems_score = compare_dictionaries(other.stems, self.stems)
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        punctuation_score = compare_dictionaries(other.punctuation, self.punctuation)
        scorelist = [word_score, word_lengths_score, stems_score, sentence_lengths_score, punctuation_score]
        return scorelist
    
    #3
    def classify(self, source1, source2):
        """ compares the called TextModel object (self) to two other “source” 
            TextModel objects (source1 and source2) and determines which of 
            these other TextModels is the more likely source of the called TextModel.
        """
        
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)
        nscores1 = []
        nscores2 = []
        for x in scores1:
            nscores1 += ['%.3f' % x]
        for y in scores2:
            nscores2 += ['%.3f' % y]
        print('scores for', source1.name, ':', nscores1)
        print('scores for', source2.name, ':', nscores2)
        a = 0
        b = 0
        for i in range(len(nscores1)):
            if nscores1[i] > nscores2[i]:
                a += 1
            elif nscores1[i] < nscores2[i]:
                b += 1
        if a > b:
            print(self.name, 'is more likely to have come from ', source1.name)
        else:
            print(self.name, 'is more likely to have come from ', source2.name)

#3
def clean_text(txt):
    """ takes a string of text txt as a parameter
        returns a list containing the words in txt after it has been 'cleaned'. 
    """
    txt = txt.replace('.', '')
    txt = txt.replace(',', '')
    txt = txt.replace('?', '')
    txt = txt.replace('!', '')
    txt = txt.replace(';', '')
    txt = txt.replace(':', '')
    txt = txt.replace('"', '')
    txt = txt.lower()
    return txt.split(' ')

#Part III
#2
def stem(s):
    """ takes a string as a parameter.
        returns the stem of s.
    """
    if s[-2:] == 'ies':
        if len(s) >= 5:
            s = s[:-2]
    elif s[-3:] == 'ves':
        if len(s) >= 5:
            s = s[:-3] + 'fe'
    elif s[-2:] == 'es' and (s[-3:-1] == 'sh' or s[-3:-1] == 'ch' or s[-3:-1] != 's' or s[-3:-1] != 'x'):
        if len(s) >= 5:
            s = s[:-2]
    elif s[-1] == 's':
        return stem(s[:-1])
    if s[-1] == 'y' and s[-2] not in 'aeiou':
        s = s[:-1] + 'i'
    if s[-3:] == 'ing':
        if len(s) >= 6:
            s = s[:-3]
            if s[-1] == s[-2]:
                s = s[:-1]
    if s[-2:] == 'er':
        if len(s) >= 5:
            s = s[:-2]
            if s[-1] == s[-2]:
                s = s[:-1]
    if s[-2:] == 'ed':
        if len(s) >= 5:
            s = s[:-2]
            if s[-1] == s[-2]:
                s = s[:-1]
    if s[-4:] == 'able' or s[-4:] == 'ible':
        if len(s) >= 7:
            s = s[:-4]
            if s[-1] == s[-2]:
                s = s[:-1]
    if s[-1] == 'e':
        if len(s) >= 4:
            s = s[:-1]
    return s

#Part IV
#1
def compare_dictionaries(d1, d2):
    """ take two feature dictionaries d1 and d2 as inputs
        returns their log similarity score.
    """
    score = 0
    total = 0
    for x in d1:
        total += d1[x]
    for w in d2:
        if w in d1:
            score += math.log(d1[w]/total) * d2[w]
        else:
            score += math.log(0.5/total) * d2[w]
    return score


def test():
    """ your docstring goes here """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
        
def run_tests():
    """ your docstring goes here """
    source1 = TextModel('JKR')
    source1.add_file('jkr.txt')

    source2 = TextModel('shakespeare')
    source2.add_file('ws.txt')

        

        