#!/usr/bin/python
import re

def basic_tokenise(string):
    # separate punctuation
    for char in r',.;?!:)(-—–—―‒"':
        string = re.sub('(?<! )' + re.escape(char), ' ' + char, string)
    for char in '\'"’':
        string = re.sub(char + '(?! )' , char + ' ', string)
    return string.strip()

def detokenise(string):
    string = re.sub(' ([,\.;?!:\)(\-\—\–\—\―\‒"]+)', r'\1', string)
    string = re.sub('([\'"’]) ', r'\1', string)
    return string

# assumes that string is a sentence
def tokenise(string):
    return basic_tokenise(string)
