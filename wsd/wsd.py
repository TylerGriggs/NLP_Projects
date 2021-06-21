"""
@author: Tyler Griggs
@classwork: VCU CMSC416 Introduction to Natural Language Processing in Spring 2020.

@model: Naive Bayes
@Accuracy: 88.89%

This program determines the sense of an ambiguous word - the understood meaning
    - from the context in which the word was used.
    
My implementation for Word-Sense-Disambiguation (WSD) uses a Naive Bayes
    approach to calculate the most probable sense of an ambiguous word.
    Context surrounding the target word is processed to remove stop words
    and unimportant contextual information for the learning task. The
    algorithm takes tagged training data from an input text file, and records 
    six context-feature-types to assess the context in which the ambiguous word
    was used. The learned model can then be applied target words in other files.
    The context-feature-types are: 
        preceding word,
        following word,
        surrounding words in a window of size 20
        two preceding words,
        word before, and word after
        two following words
        
As predictions on the sense of a target word are being made, the program stores
    logs into a third text file, showing which words in the given context were
    found in the model and the associated score with those context-features, 
    as well as the overall predicted sense and the surrounding context.
    Finally, the predicted answers along with the instance ID, are printed out
    to STDOUT for user or automatic comparison.
    
Instructions:
    Users will run the wsd.py program from command line and pass 3 arguments:
        tagged training filename
        tagged test filename
        model output log filename
    
    Example: python wsd.py line-train.txt line-test.txt my-model.txt
    
Example Model File:
    <instance>line-n.art7} aphb 45903907:
    <sense>phone
    <phone>-40.77193475028964
    <product>-30.42282420934801
    {'<context>': ' yes " if you still have that open <line> to the white house 
    youd better notify the president of the situation', 'open': 
    {'phone': 0.016853932584269662, 'product': 0.00510204081632653}, 
    'yes': {'phone': 0.0056179775280898875}, '"': {'phone': 0.0449438202247191,
    'product': 0.0663265306122449}, 'still': {'phone': 0.03932584269662921, 
    'product': 0.05102040816326531}...
    
Example Output:
    <answer instance="line-n.art7} aphb 05601797:" senseid="phone"/>
    <answer instance="line-n.w8_119:2964:" senseid="product"/>
    <answer instance="line-n.w7_040:13652:" senseid="product"/>
    <answer instance="line-n.w7_122:2194:" senseid="phone"/>
    
Resources Used:
    VCU CMSC416 Powerpoint Slides (formulas)
    regex101.com (testing)
    Some Syntax - VCU CMSC 416 Assignment 3 tagger.py @author: Tyler Griggs
    Some Syntax - VCU CMSC 416 Assignment 3 scorer.py @author: Tyler Griggs
"""

from sys import argv
import re
import math

def process_text(text):
    """ Returns a string of text that has been processed. The following
            characters are removed throughout a text file passed as a string:
            <@> <s> </s> <p> </p> , 's ' ; ( ) -- . "
            Money Symbol is seperated as a learnable "word"
            Percent Symbol is seperated as a learnable "word"
            Spaces after . are reduced to only one
            
    Parameter:
        text        a string containing text to be processed
    """
    text = re.sub(r'<@>\s+|<s>\s+|</s>\s+|<p>\s+|</p>\s+|\s+\,|\'s|\'|\;|\(|\)|\-\-\s+|\s+\.', '', text)
    text = re.sub(r'\.\,', '. ,', text)
    text = re.sub(r'\,', '', text)
    text = re.sub(r'\$', '$ ', text)
    text = re.sub(r'\%', ' %', text)
    text = re.sub(r'\s\"\s', ' ', text)
    text = re.sub(r'\.\s+', '. ', text)
    text = text.lower()
    return text


def process_context_features(before, after):
    """ Returns a list of lists which contain either one word, or a list of
            words after processing the context surrounding a target word,
            to identidy a set of predetermined features. 
            
            Ex: preceding 2 words, window of 1, etc.
            
    Parameter:
        before      a string containing context before a target word
        after       a string containing context after a target word
    """
    
    # Remove custom stop words
    before = re.sub(r'\bhers?\b|\bhes?|\bh(a|i)s\b|\b(b|m)y\b|\bgot(ten)?\b|\bat\b|\bit?s\b|\bnow\b|\bif?\b|\bbecause\b|\bdid(nt)?\b|\bnot\b|\babout\b|\bi\b|\bwas\b|\byou\b|\ba(nd?)?\b|\bof\b|\bt(hey?|o)\b|\bare(n?t)?|\bbut\b|\bhave(nt)?|\bdo(nt)?\b|\bcan(nt)?\b|\bbe(en)?\b|\bin(ner)?\b|taken?\b|\bf?or\b|\bon\b|\bthat\b|\bth(ere|is)\b|\bc(o|a)me\b|\bfrom\b|\bwith(in|out)?\b|\bout(er)?\b|\bso(me)?', '', before)
    after = re.sub(r'\bhers?\b|\bhes?|\bh(a|i)s\b|\b(b|m)y\b|\bgot(ten)?\b|\bat\b|\bit?s\b|\bnow\b|\bif?\b|\bbecause\b|\bdid(nt)?\b|\bnot\b|\babout\b|\bi\b|\bwas\b|\byou\b|\ba(nd?)?\b|\bof\b|\bt(hey?|o)\b|\bare(n?t)?|\bbut\b|\bhave(nt)?|\bdo(nt)?\b|\bcan(nt)?\b|\bbe(en)?\b|\bin(ner)?\b|taken?\b|\bf?or\b|\bon\b|\bthat\b|\bth(ere|is)\b|\bc(o|a)me\b|\bfrom\b|\bwith(in|out)?\b|\bout(er)?\b|\bso(me)?', '', after)
    
    # Remove numbers
    before = re.sub(r'\b\d+.?\d*\-?', '', before)
    after = re.sub(r'\b\d+.?\d*\-?', '', after)
    
    # Tokenize context before and after ambigous word
    before = re.split('\s+', before)
    if '' in after:
        before.remove('')
    after = re.split('\s+', after)
    if '' in after:
        after.remove('')
    
    # Handle missing features at beginning or end of context
    len_b = len(before)
    len_a = len(after)
    while len_b < 20:
        before.insert(0, None)
        len_b += 1
    while len_a < 20:
        after.append(None)
        len_a += 1
    
    # Extract Feature Types
    f1 = before[-1]
    f2 = after[0]
    f3 = [before[-20], before[-19], before[-18], before[-17], before[-16], before[-15], before[-14], before[-13], before[-12], before[-11], before[-10], before[-9], before[-8], before[-7], before[-6], before[-5], before[-4], before[-3], before[-2], before[-1], after[0], after[1], after[2], after[3], after[4], after[5], after[6], after[7], after[8], after[9], after[10], after[11], after[12], after[13], after[14], after[15], after[16], after[17], after[18], after[19]]
    f4 = [before[-2], before[-1]]
    f5 = [before[-1], after[0]]
    f6 = [after[0], after[1]]
    context_features = [f1, f2, f3 ,f4, f5, f6]
    
    return context_features


def count_entries(aDictEntry):
    """ Returns the total number of tags for a given word, given the dictionary of tag frequencies for that word
    Parameter:
        aDictEntry      # an entry of a dictionary, containing a dictionary of tags with frequencies of occurrence
    """
    total = 0           # Sum of all frequencies
    for x in aDictEntry:
        total += aDictEntry[x]  # Add to the total
    return total        # Returns


# Command line arguments
file1 = str(argv[1])
file2 = str(argv[2])
file3 = str(argv[3])

# Create context indetifing features
feature_list = ['-w', 'w+', 'k', '--w', '-w+', 'w++']
wsd_dict = {}  # Dictionary of frequencies of sense given a context given an ambiguous word
model_dict = {}
answer_dict = {}

# Count the total number of training samples for each label
count_dict = {'phone' : 0, 'product' : 0}

# Create first level of dictionary using feature types
for feature in feature_list:
    if feature not in wsd_dict:
        wsd_dict[feature] = {}

# Training
with open(file1) as filehandle:
    # Read in the .txt file
    text = filehandle.read()
    
    # Remove special tags and characters from text
    text = process_text(text)
    
    # Split the tagged text by the end tag into a list, remove last empty-tag
    instances = re.split('\<\/instance\>', text)
    instances.pop()

# Each Instance of Context from Training source
for instance in instances:
    
    # Tokenize each instance into groups with Regular Expression
    tokens = re.search(r'\<instance id\=\"(.*?)\"\>\n\<answer instance=\"(.*?)\" senseid=\"(.*?)\"\/\>\n\<context\>\n(.*?)\s*\<head\>(.*?)\<\/head\>\s*(.*?)\s*\<\/context\>', instance)
    
    # Initialze from groups
    inst_id = tokens.group(1)
    answ_id = tokens.group(2)
    sense = tokens.group(3)
    before = tokens.group(4)
    after = tokens.group(6)
    
    # Store total sense count and the ID, Sense and Context in memory
    count_dict[sense] += 1
    model_dict[inst_id] = {
        'sense' : sense,
        'context' : before + ' ' + after
        }
    
    # Feature Type word-extraction from context
    context_features = process_context_features(before, after) # List of Lists
    
    # For Each of the designated features
    for x in range(len(feature_list)):
        feature  = feature_list[x]
        
        # Single Word Features
        if x == 0 or x == 1:
            word = context_features[x]
            if word is not None and word != '':
                if word not in wsd_dict[feature]:
                    wsd_dict[feature][word] = {}
                if sense not in wsd_dict[feature][word]:
                    wsd_dict[feature][word][sense] = 1
                else:
                    wsd_dict[feature][word][sense] += 1
        
        # Multiple Word Features
        else:
            for word in context_features[x]:
                if word is not None and word != '':
                    if word not in wsd_dict[feature]:
                        wsd_dict[feature][word] = {}
                    if sense not in wsd_dict[feature][word]:
                        wsd_dict[feature][word][sense] = 1
                    else:
                        wsd_dict[feature][word][sense] += 1

# Store the total number of answers and probabilities in memory
total_answers = count_entries(count_dict)

# Testing
with open(file2) as filehandle:
    # Read in the .txt file
    text = filehandle.read()
    
    # Remove special tags and characters from text
    text = process_text(text)
    
    # Split the tagged text by the end tag into a list, remove last empty-tag
    instances = re.split('\<\/instance\>', text)
    instances.pop()
    
# Model Output Log File
f = open(file3, 'w+')

# Each Instance of Context from Testing source
for instance in instances:
    
    # Tokenize each instance into groups with Regular Expression
    tokens = re.search('\<instance id\=\"(.*?)\"\>\n\<context\>\n(.*?)\s*\<head\>(.*?)\<\/head\>\s*(.*?)\s*\<\/context\>', instance)
    
    # Initialze data from groups
    inst_id = tokens.group(1)
    before = tokens.group(2)
    after = tokens.group(4)
    
    # Store total sense count and the ID, Sense and Context in memory
    answer_dict[inst_id] = {}
    answer_dict[inst_id]['<context>'] = before + ' <' + tokens.group(3) + '> ' + after
    
    # Feature Type word-extraction from context, List of Lists
    context_features = process_context_features(before, after)
    
    argmax_dict = {} # Store Scores for each sense
    
    """ I THINK THIS MIGHT BE WHERE IT FUCKS UP """
    # For Both Senses (Phone/Product)
    for sense in count_dict.keys(): 
        
        # Set Sigma to 0, to sum over each sense
        sigma = 0
        
        # For Each of the designated features
        for x in range(len(feature_list)):
            
            # Load Feature Type
            feature  = feature_list[x]
            
            # Single Word Features
            if x == 0 or x == 1:
                
                # Current word from context
                word = context_features[x]
                
                # If the current word exsists in our dictionary with feature 
                #   and sense, otherwise continue to the next word
                if word is not None and word != '':
                    if word in wsd_dict[feature]:
                        if sense in  wsd_dict[feature][word]:
                            
                            # Probability of current word with feature and sense
                            prob_feature = wsd_dict[feature][word][sense] / count_dict[sense]
                            
                            # Add Probability to Sigma
                            sigma += math.log(prob_feature)
                            
                            # Store Probability in Model Log dictionary
                            if word not in answer_dict[inst_id]:
                                answer_dict[inst_id][word] = {}
                                answer_dict[inst_id][word][sense] = prob_feature
                            else:
                                answer_dict[inst_id][word][sense] = prob_feature
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            
            # Multiple Word Features
            else:
                # Each Word in the list of words for the current feature
                for word in context_features[x]:
                    
                    # If the current word exsists in our dictionary with feature 
                    #   and sense, otherwise continue to the next word
                    if word is not None and word != '':
                        if word in wsd_dict[feature]:
                            if sense in  wsd_dict[feature][word]:
                                
                                # Probability of current word with feature and sense
                                prob_feature = wsd_dict[feature][word][sense] / count_dict[sense]
                                
                                # Add Probability to Sigma
                                sigma += math.log(prob_feature)
                                
                                # Store Probability in Model Log dictionary
                                if word not in answer_dict[inst_id]:
                                    answer_dict[inst_id][word] = {}
                                    answer_dict[inst_id][word][sense] = prob_feature
                                else:
                                    answer_dict[inst_id][word][sense] = prob_feature
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
        
        # Calculated Probability of current sense
        prob_sense = count_dict[sense] / total_answers
        
        # Bayes Score
        argmax_dict[sense] = math.log(prob_sense) + sigma
        
    # Create and Store the Bayes score for both labels
    score_phone = argmax_dict['phone']
    score_product = argmax_dict['product']
    answer_dict[inst_id]['s_phone'] = score_phone
    answer_dict[inst_id]['s_product'] = score_product
    
    # Unfortunetly have to invert the desicion here at the very end
    if argmax_dict['phone'] > argmax_dict['product']:
        answer = 'product'
    else:
        answer = 'phone'
    
    # Record Prediction information in the Model Log file
    f.write('<instance>' + inst_id + '\n<sense>' + answer + '\n<phone>' + str(score_phone) + '\n<product>' + str(score_product) + '\n' + str(answer_dict[inst_id]) + '\n\n')
        
    # Print predicted answer with the instance identifier to STDOUT
    print('<answer instance="' + inst_id + '" senseid="' + answer + '"/>')
    
f.close()