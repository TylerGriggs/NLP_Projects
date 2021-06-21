# -*- coding: utf-8 -*-
"""
@author: Tyler Griggs
@classwork: VCU CMSC416 Introduction to Natural Language Processing in Spring 2020.

@model_type: frequency of Tag-given-Word, or frequency[word][tag]

This program takes text file of words with their part of speech tag as input, and attempts to tag a separate file
    containing only words with their correct part-of-speech, based on what it learned from the first training file.

This algorithm processes the input text file to remove brackets dictating phrases and the extra tags on some words.
    Once the text has been read in, each word/tag-set is split into the component word and tag. The frequency of a tag
    given a word , and the frequency of that tag given the previous tag is tallied in two dictionaries of dictionaries.
    The second file is processed in a similar way as the first, splitting the words up separately. The trained model
    attempts to predict a tag by calculating the probability of seeing that tag given the current word. The greedy model
    only remembers the tag with the highest probability, and appends the calculated tag to the word.

Examples:
    ************************************************** POS Training ***************************************************
    [ The/DT securities/NNS ]       ---------------->   The/DT securities/NNS
    to/TO be/VB sold/VBN            ---------------->   to/TO be/VB sold/VBN
    [ next/JJ week/NN ]             ---------------->   next/JJ week/NN
    will/MD|NN raise/VB about/RB    ---------------->   will/MD raise/VB about/RB
    [ $/$ 10/CD billion/CD ]        ---------------->   $/$ 10/CD billion/CD
    in/IN                           ---------------->   in/IN
    [ cash/NN|VB ]                  ---------------->   cash/NN

    ************************************************** POS Testing ***************************************************
    [ There ]                       ---------------->   There/EX
    were                            ---------------->   were/VBD
    [ no major Eurobond ]           ---------------->   no/DT major/JJ Eurobond/NN
    or                              ---------------->   or/CC
    [ foreign bond offerings ]      ---------------->   foreign/JJ bond/NN offerings/NN
    in                              ---------------->   in/IN
    [ Europe Friday ]               ---------------->   Europe/NNP Friday/NNP
    .                               ---------------->  ./.
    
Sources:
    Some Syntax - VCU CMSC 416 Assignment 3 ngram.py @author: Tyler Griggs
    Regex Testing - regex101.com
"""

import re
from sys import argv


def freq_count(aDictEntry):
    """ Returns the total number of tags for a given word, given the dictionary of tag frequencies for that word
    Parameter:
        aDictEntry      # an entry of a dictionary, containing a dictionary of tags with frequencies of occurrence
    """
    total = 0           # Sum of all frequencies
    for x in aDictEntry:
        total += aDictEntry[x]  # Add to the total
    return total        # Returns


file1 = str(argv[1])
file2 = str(argv[2])

all_input = []      # List to store the tag/word-sets from an input file

freq_word_tag = {}  # Dictionary of frequencies of a tag given a word 
freq_prev_tag = {}  # Dictionary of frequencies of a tag given a previous tag 

prob_dict = {}

length = 2
holder = []  # Array to hold the word and tag
tag_history = []  # Array to hold the previous tag

output = []

# BEGIN MAIN
with open(file1) as filehandle:
    # Read in the .txt file
    text = filehandle.read()

    # Remove brackets
    text = re.sub(r'[\[\]]', '', text)
    text = re.sub(r'\|\S+', '', text)

    # Split the preprocessed text on spaces
    all_input = re.split('\s+', text)

    # Remove instances of NULL strings
    all_input = list(filter(None, all_input))
        
# Iterate over every word/tag-set in the training corpus
for each_word in all_input:
    
    # Split up the tag/word-set on the / character
    holder = re.split('\/', each_word)
    
    # Ensure there is just one word and one tag
    if len(holder) == length:
        
        # If word not in the dictionary, initialize the word with a Dictionary
        if holder[0] not in freq_word_tag:
            freq_word_tag[holder[0]] = {}
        
        # If tag not in the dictionary, initialize the tag with a count
        if holder[1] not in freq_word_tag[holder[0]]:
            freq_word_tag[holder[0]][holder[1]] = 1  
        else:
            # Increment the count  
            freq_word_tag[holder[0]][holder[1]] += 1
        
        # If there is a tag in history
        if tag_history:
            
            # If previous tag not in the dict, initialize the tag with a dict
            if tag_history[0] not in freq_prev_tag:
                freq_prev_tag[tag_history[0]] = {}
            
            # If tag given the previous tag not in the dictionary, initalize
            if holder[1] not in freq_prev_tag[tag_history[0]]:
                freq_prev_tag[tag_history[0]][holder[1]] = 1
            else:
                # Increment the count
                freq_prev_tag[tag_history[0]][holder[1]] += 1

        # Clear and Send current TAG-holding to history
        tag_history.clear()
        tag_history.append(holder[1])

        # Reset the holder
        holder = []
        
# File Closed, Reset History
tag_history.clear()

with open(file2) as filehandle:
    # Read in the .txt file
    text = filehandle.read()
    # Remove brackets
    text = re.sub(r'[\[\]]', '', text)

    # Split the preprocessed text on spaces
    all_input = re.split('\s+', text)
    
    # Remove instances of NULL strings
    all_input = list(filter(None, all_input))
    
for each_word in all_input:

    temp_prob = 0.0         # Reset temporary probability
    probability = 0.0       # Reset stored probability
    predicted_tag = 'NN'    # Unknown Words get a noun tag
    
    # Known Word
    if each_word in freq_word_tag:
        # Once we have a tag history
        if tag_history:
            # For all possible tags for the current word
            for tag, the_freq in freq_word_tag[each_word].items():
                # Except those that break learned rules
                if tag not in freq_prev_tag[tag_history[0]]:
                    continue
                
                # Calculate the Probability
                temp_prob = (the_freq / freq_count(freq_word_tag[each_word])) * (freq_prev_tag[tag_history[0]][tag] / freq_count(freq_prev_tag[tag_history[0]]))
                
                # Greedy Probability
                if temp_prob > probability:
                    probability = temp_prob
                    predicted_tag = tag
                    
        # First word only
        else:
            # For all possible tags for the current word
            for tag, the_freq in freq_word_tag[each_word].items():
                
                # Calculate the Probability with no given history
                temp_prob = (the_freq / freq_count(freq_word_tag[each_word]))
                
                # Greedy Probability
                if temp_prob > probability:
                    probability = temp_prob
                    predicted_tag = tag
        
    # Add the Word\Tag to an output list
    output.append(each_word + "/" + predicted_tag)
    
    # Clear and Send current TAG-holding to history
    tag_history.clear()
    tag_history.append(predicted_tag)

for x in output:
    print(x + ' ')
