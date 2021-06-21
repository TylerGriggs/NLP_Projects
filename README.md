# Natural Language Processing Projects
NLP algorithms for training, testing and saving models.

Many of the Python scripts involve command line arguments to read text files or retrieve text information from API requests. Supervised training samples are provided in some cases, and the ability to create new supervised data from Twitter and YouTube is provided in the /sentiment directory, provided by [twitter-scraper](https://github.com/bisguzar/twitter-scraper) and [youtube-data-api](https://github.com/mabrownnyu/youtube-data-api) packages.

Projects inspired by Introduction to Natural Language Processing coursework.
##
### Eliza Chatbot
A simple Rogerian psychotherapist chatbot designed to technically satisfy the Turing Test. Using the words provided in the user's answer, the chatbot can provide a feasible response as long as the user follow's the "game's" rules.
##
### N-gram Predictive Text
Generates brand new sentences after reading a book or books, provided to it as text files. Based on the words used in the books, a number of words used before each word, the program is able the generate a number of sentences. Using the probabilities of words with previous words the program can choose a potential next word, or conclude the sentence with punctuation.
##
### Part-of-Speech (POS) Tagging
This program takes text file of words with their part of speech tag as input (supervised training), and attempts to tag a separate file containing only words with their correct part-of-speech, based on what it learned from the first supervised training file.
##
### Sentiment Classifiction
This program determines the sentiment of a Tweet, YouTube comment or snippent of text from the context words contained in the message based on supervised training on context words.
Scripts to create new supervised training data from API requests to Twitter and YouTube.
##
### Word-Sense-Disambiguation (WSD)
This program determines the sense of an ambiguous word - the understood meaning - from the context in which the word was used in supervised training. (Example in English: "bank, line, cool")

