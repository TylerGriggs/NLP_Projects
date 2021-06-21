"""
@author: Tyler Griggs
@classwork: VCU CMSC416 Introduction to Natural Language Processing in Spring 2020.

@model: Naive Bayes
@accuracy: 66.81 %

This program determines the sentiment of an tweet - or any supervised binary+ 
    classification - from the context words contained in the short online message.
    
My implementation for Twitter sentiment analysis uses a Naive Bayes
    approach to calculate the most probable sense given a bag of words.
    The entirety of the context is processed to remove stop words
    and unimportant contextual information for the learning task. The
    algorithm takes tagged training data from an input text file, and records 
    the words used. The learned model can then be applied tweets in other files.
    
As predictions on the sentiment of a tweet are being made, the program stores
    logs into a third text file, showing which words in the given context were
    found in the model and the associated score with those context-features, 
    as well as the overall predicted sense of, and, the surrounding context.
    Finally, the predicted answers along with the instance ID, are printed out
    to STDOUT for user or automatic comparison.
    
Instructions:
    Users will run the sentiment.py program from command line and pass 3 arguments:
        tagged training filename
        tagged test filename
        model output log filename
    
    Example: python sentiment.py sentiment-train.txt sentiment-test.txt my-model.txt
    
Example Model Output:
    Instance ID:620979391984566272 
    {'<context>': ' on another note it seems greek pm tsipras married angela merkel to francois hollande on sunday <#> <url>', 'another': {'negative': 0.0136986301369863}, 'seems': {'negative': 0.0136986301369863}, 'angela': {'negative': 0.1917808219178082, 'positive': 0.018867924528301886}, 'merkel': {'negative': 0.1780821917808219, 'positive': 0.018867924528301886}, 'sunday': {'negative': 0.0273972602739726, 'positive': 0.018867924528301886}, '<#>': {'negative': 0.136986301369863, 'positive': 0.37735849056603776}, '<url>': {'negative': 0.3424657534246575, 'positive': 0.5094339622641509}, 'pm': {'positive': 0.012578616352201259}, 'negative': -19.77087923305767, 'positive': -18.313480619308653, '<Predicted_Sentiment>': 'negative'}
    ...
    
    
Example Answer Output:
    answer instance="620979391984566272" sentiment="negative"/>
    <answer instance="621340584804888578" sentiment="positive"/>
    <answer instance="621351052047028224" sentiment="positive"/>
    <answer instance="621357165211742208" sentiment="positive"/>
    <answer instance="621392677519540224" sentiment="negative"/>
    
    
Resources Used:
    VCU CMSC416 Powerpoint Slides (formulas)
    regex101.com (testing)
    VCU CMSC 416 Assignment 4 wsd.py @author: Tyler Griggs (Syntax)
    VCU CMSC 416 Assignment 4 scorer.py @author: Tyler Griggs (Syntax)
    geeksforgeeks.org/removing-stop-words-nltk-python (NLTK Stop Word Removal)
"""

from sys import argv
import re
import math
from nltk.corpus import stopwords

def process_text(text):
    """ Returns a string of text that has been processed. Certain special
            characters and features are removed. Others are tagged to save
            stop word removal. Other processing includes basic abbreiviation
            extension (b4 u - > before you)
            
            Learnable Tags
                <$>             Money Symbol $
                <%>             Percent Symbol %
                <elipsis>       Elipsis...
                <curse>         Curse Words
                <why>           Why
                <exclaimation>  !!+
                <question>      ??+
                <ord_num>       Ordered Number (4th, 52nd, etc.)
            
            Spaces after . are reduced to only one
            
    Parameter:
        text        a string containing text to be processed
    """
    
    text = text.lower()                                 # Lowercase
    text = re.sub(r'https?.*?[\s\n]', ' ', text)        # Hyperlinks removed
    text = re.sub(r'\@.*?\W', ' <@> ', text)            # Replace @persons
    text = re.sub(r'\#.*?\W', ' <#> ', text)            # Replace #hashtags
    text = re.sub(r'\.\.+', '<elipsis> ', text)         # Elipsis tag
    text = re.sub(r'\!\!+', ' <exclaimation> ', text)   # Exclaimation Intensifier
    text = re.sub(r'\?\?+', ' <question_marks> ', text) # Question Intensifier
    text = re.sub(r'\bwhy\b', ' <why> ', text)          # Question Intensifier
    
    text = re.sub(r'\bfuck', ' <curse> fuck', text)     # Curse Tag
    text = re.sub(r'\bdamn', ' <curse> damn', text)     # Curse Tag
    text = re.sub(r'\bshit', ' <curse> shit', text)     # Curse Tag
    text = re.sub(r'\bpenis', ' <curse> penis', text)   # Curse Tag
    text = re.sub(r'\bsuck', ' <curse> suck', text)     # Curse Tag
    text = re.sub(r'\bcrap', ' <curse> crap', text)     # Curse Tag
    text = re.sub(r'\bbutt', ' <curse> butt', text)     # Curse Tag
    
    text = re.sub(r'\,', ' ', text)                     # Comma
    text = re.sub(r'\.+', ' ', text)                    # Period (not elipsis)
    
    text = re.sub(r'\!', ' <!> ', text)                 # Exclaimation
    text = re.sub(r'\?', ' <?> ', text)                 # Question
    text = re.sub(r'\(', '', text)                      # Left-Parenthesis
    text = re.sub(r'\)', '', text)                      # Right-Parenthesis
    
    text = re.sub(r'\<\.\>', ' . ', text)               # Period tag
    text = re.sub(r'\$', ' <$> ', text)                 # Money Tag
    text = re.sub(r'\%', ' <%> ', text)                 # Percent Tag
    text = re.sub(r'\&amp\;', ' and ', text)            # Ampersand
    
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s\"\s', ' ', text)
    text = re.sub(r'\.\s+', '. ', text)
    
    text = re.sub(r'\bi\'m\b', 'i am', text)        # I'm -> I am
    text = re.sub(r'\bi\'ll\b', 'i will', text)     # I'll -> I will
    text = re.sub(r'\bw\/\b', 'with', text)         # w/ -> with
    text = re.sub(r'\b4 u\b', ' for you', text)     # 4 u -> for you
    text = re.sub(r'\bb4\b', 'before', text)        # b4 -> before
    text = re.sub(r'\bu\b', 'you', text)            # u -> you
    text = re.sub(r'\b\+\b', 'and', text)           # + -> and
    text = re.sub(r'\'', '', text)                  # Apostrophe
    
    
    text = re.sub(r'i have', ' ive ', text)
    text = re.sub(r'i would', ' id ', text)
    text = re.sub(r'they have', ' theyve ', text)
    text = re.sub(r'\b1st\b', 'first', text)      # Apostrophe
    text = re.sub(r'\b2nd\b', 'second', text)     # Apostrophe
    text = re.sub(r'\b3rd\b', 'third', text)      # Apostrophe
    text = re.sub(r'\b\dth\b|\b\drd\b|\b\dnd\b|\b\dst\b', '<ord_num>', text)   # Apostrophe
    
    return text


def process_context(full_context):
    """ Returns a list of word-features composing the context of the tweet. 
            Numbers and digits are removed, as well as special characters.
            
            A list of stop words imported from NLTK clean out potentially
                useless words from being recorded in the model's dictionary
            
            Special Characters Removed: ( ) , { } [ ] - @person #hashtag
            
    Parameter:
        full_context        a string containing context before a target word
    """
    
    # Remove numbers, Special Characters, utf-8 encoded > < <= >= signs
    full_context = re.sub(r'\b\d+.*?\d*\-?', '', full_context)
    full_context = re.sub(r'\(|\)|\"|\:|\;|\'|\/|\`|\~|\{|\}|\[|\]','', full_context)
    full_context = re.sub(r'\&gt;|\&lt|\&le|\&ge','', full_context)
    
    # Tokenize context into Bag of Words
    context_features = re.split('\s+', full_context)
    
    # Remove stop words using NLTK list
    context_features = [word for word in context_features if not word in stop_words]
        
    
    return context_features


def count_entries(aDictEntry):
    """ Returns the total count from the entries in a given dictionary entry
    Parameter:
        aDictEntry      an entry of a dictionary, containing frequencies of occurrence
    """
    total = 0           # Sum of all frequencies
    for x in aDictEntry:
        total += aDictEntry[x]  # Add to the total
    return total        # Returns


# Command line arguments
file1 = str(argv[1])
file2 = str(argv[2])
file3 = str(argv[3])

# NLTK Stop Words
stop_words = set(stopwords.words('english'))

sentiment_dict = {}     # Dictionary of frequencies of sense given a context given an ambiguous word
model_dict = {}         # Dictionary of learned model
answer_dict = {}        # Answer instance information
count_dict = {}         # Math Couting Dictionary


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
    tokens = re.search(r'\<instance\>\n\<id\>(\d+)\<\/id\>\n\<sentiment\>(\w+)\<\/sentiment\>\n\<context\>(.*)\<\/context\>', instance)
    
    # Initialze from groups
    inst_id = tokens.group(1)
    answ_id = tokens.group(2)
    sentiment = tokens.group(3)
    context = tokens.group(4)
    
    # Create entry in model dictionary of ID, Sentiment, and Context
    model_dict[inst_id] = {
        'sentiment' : sentiment,
        'context' : context
        }
    
    # Store total count for that sentiment
    if sentiment not in count_dict:
        count_dict[sentiment] = 1
    else:
        count_dict[sentiment] += 1
    
    # Bag of Words features extraction from context
    context_features = process_context(context)
    
    
    for word in context_features:
        if word is not None and word != '':
            if word not in sentiment_dict:
                sentiment_dict[word] = {}
            if sentiment not in sentiment_dict[word]:
                sentiment_dict[word][sentiment] = 1
            else:
                sentiment_dict[word][sentiment] += 1
    

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

sentiment_types = count_dict.keys()

# Each Instance of Context from Testing source
for instance in instances:
    
    # Tokenize each instance into groups with Regular Expression
    tokens = re.search(r'\<instance id\=\"(.*?)\"\>\s+\<context\>(.*?)\s*\<\/context\>', instance)
    
    # Initialze from groups
    inst_id = tokens.group(1)
    context = tokens.group(2)
    
    # Store total sense count and the ID, Sense and Context in memory
    answer_dict[inst_id] = {}
    answer_dict[inst_id]['<context>'] = context
    
    # Bag of Words features extraction from context
    context_features = process_context(context)
    
    argmax_dict = {} # Store Scores for each sense
    
    # For Positive / Negative sentiment
    for sentiment in sentiment_types: 
        
        # Set Sigma to 0, to sum over each sense
        sigma = 0
        
        for word in context_features:
            # If the current word exsists in our dictionary with feature 
            #   and sense, otherwise continue to the next word
            if word is not None and word != '':
                if word in sentiment_dict:
                    if sentiment in  sentiment_dict[word]:
                       
                        # Probability of current word with feature and sense
                        prob_feature = sentiment_dict[word][sentiment] / count_dict[sentiment]
                        
                        # Add Probability to Sigma
                        sigma += math.log(prob_feature)
                    
                        # Store Probability in Model Log dictionary
                        if word not in answer_dict[inst_id]:
                            answer_dict[inst_id][word] = {}
                            answer_dict[inst_id][word][sentiment] = prob_feature
                        else:
                            answer_dict[inst_id][word][sentiment] = prob_feature
                    else:
                        continue
                else:
                    continue
            else:
                continue
    
        # Calculated Probability of current sense
        prob_sense = count_dict[sentiment] / total_answers
        
        # Bayes Score
        argmax_dict[sentiment] = math.log(prob_sense) + sigma
    
    sentiment0 = list(sentiment_types)[0]
    sentiment1 = list(sentiment_types)[1]
    
    # Create and Store the Bayes score for both labels
    score0 = argmax_dict[sentiment0]
    score1 = argmax_dict[sentiment1]
    answer_dict[inst_id][sentiment0] = score0
    answer_dict[inst_id][sentiment1] = score1
    
    # Unfortunetly have to invert the desicion for negative number answers
    if score0 > score1:
        answer = sentiment1
    else:
        answer = sentiment0
    
    # Store Prediction in answer dictionary
    answer_dict[inst_id]['<Predicted_Sentiment>'] = answer
    
    # Record Prediction information in the Model Log file
    f.write('Instance ID:' + str(inst_id) + ' \n' + str(answer_dict[inst_id]) + '\n\n')
        
    # Print predicted answer with the instance identifier to STDOUT
    print('<answer instance="' + inst_id + '" sentiment="' + answer + '"/>')

f.close()




















