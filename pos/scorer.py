# -*- coding: utf-8 -*-
"""
@author: Tyler Griggs
@classwork: VCU CMSC416 Introduction to Natural Language Processing in Spring 2020.

@model_type: frequency of Tag-given-Word, or frequency[word][tag]

This program compares two text files of words with their part-of-speech tag to 
    determine the how well a trained model worked.

This algorithm opens two texts files passed in by command-line arguments, and
    compares each entry of a word/tag-set to check if one match the true answer
    from the second. Once the correctly predicted sets are tallied, the word
    in the set is removed, leaving only the tag.
The imported library pandas, creates a series from the list of tags from the
    first and second files. Pandas can then create a non-binary confusion
    matrix showing the counts of when the True tag matched the Predicted tag.

Examples:
    ____TRUE___________Predicted________Answer____
        it/PRP      == it/PRP           Correct
        would/MD    == would/MD         Correct
        succeed/VB  == succeed/VB       Correct
        stock/NN    == stock/VB         Incorrect
    
    Correct:    3
    Total:      4
    Accuracy:   75.0000
    
    True       PRP  MD   VB  NN
    Predicted                 
    PRP        1    0    0   0   
    MD         0    1    0   0 
    VB         0    0    1   1
    NN         0    0    0   0
    
Sources:
    Pandas Confusion Matrix - pandas-ml.readthedocs.io/en/latest/conf_mat.html
    Some Syntax - VCU CMSC 416 Assignment 3 ngram.py @author: Tyler Griggs
    Regex Testing - regex101.com
"""

from sys import argv
import re
import pandas as pd

predicted_file = str(argv[1])   # File 1 Passed in arguments
true_file = str(argv[2])        # File 2 Passed in arguments

pred_tags = []      # List of Predicted tags
true_tags = []      # List of True or actual tags

# Open Predicted Word/Tag text file
with open(predicted_file) as filehandle:
    
    # Read in the .txt file
    text = filehandle.read()
    
    # Split the preprocessed text on space
    pred_tags = re.split(r'\s+', text)
    
    # Remove instances of NULL strings
    pred_tags = list(filter(None, pred_tags))

# Open Gold-Standard Test text file
with open(true_file) as filehandle:
    
    # Read in the .txt file
    text = filehandle.read()
    
    # Remove brackets and extra tags
    text = re.sub(r'[\[\]]', '', text)
    text = re.sub(r'\|\S+', '', text)
    
    # Split the preprocessed text on spaces
    true_tags = re.split(r'\s+', text)
    
    # Remove instances of NULL strings
    true_tags = list(filter(None, true_tags))

# Compare the two files for exact matches
correct = 0                 # Count of number correct
total = len(pred_tags)      # Count of total predictions
for x in range(len(pred_tags)):         # for all predicted tags
    if pred_tags[x] == true_tags[x]:    # If exact match
        correct += 1                    # Add to the count
        
# Remove the word, from the predicted word/tag-set
for x in range(len(pred_tags)):
    
    # regex: replace string with with group2 of match
    pred_tags[x] = re.sub(r'(.*)\/(.*)', r'\g<2>', pred_tags[x])
    
# Remove the word, from the true word/tag-set
for x in range(len(true_tags)):
    
    # regex: replace string with with group2 of match
    true_tags[x] = re.sub(r'(.*)\/(.*)', r'\g<2>', true_tags[x])

# Print Statistics about general accuracy
print("Correct: " + str(correct))
print("Total: " + str(len(pred_tags)))
print("Accuracy: " + str(round((correct/x)*100, 4)) + "%") # 4 decimal places

# Create Pandas Series given dictionary entries
x_true = pd.Series(true_tags, name='True')
y_pred = pd.Series(pred_tags, name='Predicted')

# Generate the confusion matrix from two Series
df_confusion = pd.crosstab(y_pred, x_true)

# Required flag to not truncate output for STDOUT
pd.set_option('display.expand_frame_repr', False)

# Print the confusion matrix to STDOUT
print("\n%s" % df_confusion)
