"""
Created on Thu Feb  6 11:35:05 2020
@author: Tyler Griggs
@classwork: VCU CMSC416 Introduction to Natural Language Processing in Spring 2020.

This program intends to generate brand new sentences after reading a book or books, provided to it as text files. Based
    on the words used in the books, a number of words used before each word, the program is able the generate a number
    of sentences. Using the probabilities of words with previous words the program can choose a potential next word, or
    conclude the sentence with punctuation.

My algorithm to accomplish this sets the books to lowercase, turns special characters into whitespace, turn multiple
    whitespace characters into one, and splits each text file by whitespace characters or new lines into word tokens.
    A starting and ending tag are used to denote the end of once sentence, and the beginning of new sentence. The USER
    enters a single line as a command to specify values in the following order:

    number int(n) of n-grams to used to generate new words
    number int(m) of sentences to generate
    name(s) of text files to be read by the program, separated by whitespace

    Every n-gram in the input corpus is counted in a history dictionary (hash-map). All of the words used after the
    n-gram of history, and their respective frequencies, are stored in a frequency dictionary of dictionaries.
    Probabilities are calculated from the counts in the history dictionary, and the frequecies of words given a history
    in the probability dictionary.

    From the start string we can probabilistically generate words to form sentences, until the USER number is reached.
    A random number sets a threshold, and as we visit possible words given the history, the probabilities are summed
    until the random threshold is met.

Example Input Output:
    This program generates random sentences based on an Ngram model. Author: Tyler Griggs
    3 2 example_file.txt
    yes but he had finished his second term of service.
    they prayed for all for what we shall not come from a conscientious desire for anything.

    [system exit]

    This program generates random sentences based on an Ngram model. Author: Tyler Griggs
    5 3 example_file.txt
    said peter solemnly moving his forefinger upwards from his nose.
    ricky ceased speaking and turned his attention to his tea.
    her hair had begun to grow weaker it had cost him an effort to go near him.

    [system exit]

Resources:
    VCU CMSC416 Powerpoint Slides (formulas)
    regex101.com (testing)
    programiz.com/python-programming/nested-dictionary (using dictionaries)
"""

import re
import random
import time
import glob
import os

# BEGIN MAIN
# Introduction

print("This program generates random sentences based on an Ngram model. Author: Tyler Griggs")

txtfiles = []
intro = input()
start_time = time.time()

# Parse the USER commands by the whitespace characters
commands = re.split(r'\s+', intro)

# Print Command Line Settings back to the USER as required
print("Command line settings : ngram.py " + commands[0] + " " + commands[1])

# Parse numbers from commands
n = int(commands[0])
m = int(commands[1])

t = 2  # Starting Index
# Parse the text files entered by the USER
while t < len(commands):
    txtfiles.append(commands[t])
    t += 1

start_string = ""
count = 0

# Create a start string based on the USER input
while count < n - 1:
    start_string = start_string + "<start> "
    count = count + 1

all_words = []
freq_dict = {}
hist_dict = {}
prob_dict = {}

# For each file in the list
for file in txtfiles:
    with open(file, encoding='utf8') as filehandle:
        # Read in the .txt book file
        book = start_string + filehandle.read()
        # Remove apostrophes and set to lowercase
        book = re.sub(r'[\']+', '', book.lower())

        # Remove other special non-punctuation (-,":;-<>()[]{})
        book = re.sub(r'[^A-Za-z0-9\.\?\!\,\"\:\;\<\>\s+\n+]+', ' ', book)

        # Replace punctuation with "<end> <start> <start>"
        book = re.sub(r'\,', ' <comma> ', book)
        book = re.sub(r'\"', ' <quote> ', book)
        book = re.sub(r'\:', ' <colon> ', book)
        book = re.sub(r'\;', ' <scolon> ', book)
        book = re.sub(r'\.', ' <end> ' + start_string, book)
        book = re.sub(r'\!', ' <!end> ' + start_string, book)
        book = re.sub(r'\?', ' <?end> ' + start_string, book)

        # Replace multiple spaces with just one
        book = re.sub(r'[\s+]', ' ', book)

        # Split the preprocessed book on spaces and new lines
        all_words = all_words + re.split('[\s+\n+]', book)
        all_words.remove('')

# Remove instances of NULL strings
all_words = list(filter(None, all_words))

laplace_v = len(set(all_words))  # Laplace Smoothing, number of types in corpus
ngram = []  # USER sized n-gram
history = []  # n-1 sized gram
word = ""  # 1-word gram

# Iterate over every word in the training corpus
for each_word in all_words:
    ngram.append(each_word)  # add the word to the current n-gram
    length = len(ngram)  # get current n-gram length
    if length == n:
        c = 0
        while c < length - 1:  # fill the history will all but the last word in the n-gram
            history.append(ngram[c])
            c += 1
        word = ngram[length - 1]  # Specify the last word
        history_words = " ".join(history)  # Specify the n-1-gram called history

        if history_words not in hist_dict:
            hist_dict[history_words] = 1  # Initialize history dictionary count by key
        else:
            hist_dict[history_words] += 1  # Count the history by key

        if history_words not in freq_dict:
            freq_dict[history_words] = {}  # Initialize frequency dictionary of words given history

        if word not in freq_dict[history_words]:
            freq_dict[history_words][word] = 1  # Initialize frequency by word given history
        else:
            freq_dict[history_words][word] += 1  # Count frequency of words given history

        ngram.pop(0)
        history = []
        word = ""

# Iterate through the words given their history in the frequency dictionary
for history_e, values_dict in freq_dict.items():
    for the_word, its_num in values_dict.items():

        if history_e not in prob_dict:
            prob_dict[history_e] = {}  # Initialize dictionary in probability dictionary at history

        # Calculate probability of word given history
        prob_dict[history_e][the_word] = its_num / hist_dict[history_e]

# Establish generated sentence data structure
sentence_count = 0
sentences = []

# Generate the number of sentences the USER input
while sentence_count < m:
    # Establish Probability and Random Number Threshold
    probability = 0
    random_num = random.uniform(0, 1)
    quote_count = 0

    # Tokenize the starting symbols and remove NULL strings
    new_tokens = re.split(' ', start_string)
    new_tokens = list(filter(None, new_tokens))

    # Establish a Token Counter and empty sentence
    token_counter = 0
    sentence = ""

    # If the USER entered n=1-grams and we have no starting symbol
    if not new_tokens:
        new_tokens.append('<start>')

    # As long as the last generated word is not an end tag
    while new_tokens[-1] != '<end>' and new_tokens[-1] != '<!end>' and new_tokens[-1] != '<?end>':
        # Set n counter and new search key
        c = 0
        search_key = ""

        while c < n-1:
            search_key += new_tokens[token_counter]
            token_counter += 1
            c += 1
            if c < n-1:
                search_key += " "

        # Special Number (spc) is
        spc = n - 2
        if spc >= 0:
            token_counter -= spc

        # Check the possible words until and sum their probabilities to find threshold
        for a_word, the_prob in prob_dict[search_key].items():
            probability += the_prob

            # If we have met the random threshold, choose the current word
            if probability >= random_num:
                new_tokens.append(a_word)
                if a_word == '<quote>':
                    quote_count += 1
                break
        # Reset Probability
        probability = 0

        # If the sentence is longer than 100 words (Mentioned in class 2/13/2020)
        if len(new_tokens) >= 100:
            new_tokens.append('<end>')

    # Add a space after each generated word
    for element in new_tokens:
        sentence += element + " "

    # Check if there are an odd number of quotes in the sentence
    if quote_count % 2 != 0:
        sentence += '<quote>'

    # Check if the generated sentence ended immediately
    if sentence != start_string + "<end> ":
        sentences.append(sentence)
        sentence_count += 1
        
        

# For each sentence perform Start and End Symbol removal
for x in range(0, len(sentences)):
    sentences[x] = re.sub(r'<start> +', '', sentences[x])
    sentences[x] = re.sub(r'\s<comma> +', ', ', sentences[x])
    sentences[x] = re.sub(r' ?<quote> ?', '"', sentences[x])
    sentences[x] = re.sub(r' ?<colon> +', ': ', sentences[x])
    sentences[x] = re.sub(r' ?<scolon> +', '; ', sentences[x])
    sentences[x] = re.sub(r' ?<end> ?', '.', sentences[x])
    sentences[x] = re.sub(r'<!end> ?', '!', sentences[x])
    sentences[x] = re.sub(r'\<\?end> ?', '?', sentences[x])
    sentences[x] = re.sub(r'\bi\b', 'I', sentences[x])
    sentences[x] = sentences[x].capitalize()

for the_sentence in sentences:
    print(the_sentence)

print("--- %s seconds ---" % (time.time() - start_time))
print("Total Words Processed: " + str(len(all_words)))
print("Unique Words Processed: " + str(len(set(all_words))))
