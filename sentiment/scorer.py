"""
@author: Tyler Griggs
@classwork: VCU CMSC416 Introduction to Natural Language Processing in Spring 2020.

@model: Naive Bayes
@accuracy: 66.81 %

This program compares two text files of answer-instance-id and predicted sense
    information and shows the performance.

This algorithm opens two texts files passed in by command-line arguments, and
    compares each entry of answer-instance-id and predicted sense to check 
    if the predicted file matches the gold-standard file (second file).
The imported library pandas, creates a series from the list of predicted senses 
    from the first and second files. Pandas can then create a binary confusion
    matrix showing the counts of when the True sense matched the Predicted
    sense. The resulting confusion matrix is printed to STDOUT.
    
Instructions:
    Users will run the scorer.py from command-line and pass two filenames as
        arguments.
        
    python scorer.py my-sentiment-answers.txt sentiment-test-key.txt
    
    True: 155
    False: 77
    Total: 232
    Accuracy: 66.81%
    
    True       negative  positive
    Predicted
    negative         30        35
    positive         42       125
    
Sources:
    Pandas Confusion Matrix - pandas-ml.readthedocs.io/en/latest/conf_mat.html
    Some Syntax - VCU CMSC 416 Assignment 3 scorer.py @author: Tyler Griggs
    Regex Testing - regex101.com
"""

from sys import argv
import pandas as pd
import re

predicted_file = str(argv[1])   # File 1 Passed in arguments
true_file = str(argv[2])        # File 2 Passed in arguments

pred_sentiment = []                 # List of predicted sentiments
true_sentiment = []                 # List of actual (true) sentiments

# Open Predicted Word/Tag text file
with open(predicted_file) as filehandle:
    
    # Read in the .txt file
    pred_lines = filehandle.readlines()
    for line in pred_lines:
        tokens = re.search('sentiment=\"(.*?)\"\/\>', line)
        sentiment = tokens.group(1)
        pred_sentiment.append(sentiment)
    

# Open Gold-Standard Test text file
with open(true_file) as filehandle:
    
    # Read in the .txt file
    true_lines = filehandle.readlines()
    for line in true_lines:
        tokens = re.search('sentiment=\"(.*?)\"\/\>', line)
        sentiment = tokens.group(1)
        true_sentiment.append(sentiment)
    
count_true = 0
count_false = 0

# Count number of correct predictions
for x in range(len(true_sentiment)):
    if true_sentiment[x] == pred_sentiment[x]:
        count_true += 1
    else:
        count_false += 1
total = count_true + count_false

# Print Out Performance Information
print('True: ' + str(count_true))
print('False: ' + str(count_false))
print('Total: ' + str(total))
print('Accuracy: ' + str(round(count_true * 100 / (count_true + count_false), 2) ) + '%' )

# Create Pandas Series given dictionary entries
x_true = pd.Series(true_sentiment, name='True')
y_pred = pd.Series(pred_sentiment, name='Predicted')

# Generate the confusion matrix from two Series
df_confusion = pd.crosstab(y_pred, x_true)

# Required flag to not truncate output for STDOUT
pd.set_option('display.expand_frame_repr', False)

# Print the confusion matrix to STDOUT
print("\n%s" % df_confusion)