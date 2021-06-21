# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 13:45:09 2020
@author: Tyler Griggs
@classwork: VCU CMSC416 Introduction to Natural Language Processing in Spring 2020.
"""

import re
import random
import os
# Import the required module for text  
# to speech conversion 
from gtts import gTTS 
  
# This module is imported so that we can  
# play the converted audio 
language = 'en-au'

# Attempt to remove any punctuation symbols from the end of the string input
def remove_punctuation(sent):
    """Attemps to removes punctuation from an input String.
    
    Args:
        sent (str): The sentance parameter sent with the function call
        
    Returns:
        sent (str): The edited sentance parameter
    """
    # Remove any punctuation and add Question Mark at the end of ELIZA response
    if re.search(r'(\.|\!|\?|\:|\;|\,|\'|\\|\[|\])$', sent) is not None:
        sent = sent[:-1]
    return sent.upper()



def punctuate_response(sent):
    """Attemps to removes punctuation and add a question mark from an input 
        String.
    
    Args:
        sent (str): The sentance parameter sent with the function call
        
    Returns:
        sent (str): The edited sentance parameter
    """
    # Remove any punctuation and add Question Mark at the end of ELIZA response
    if re.search(r'(\.|\!|\?|\:|\;|\,|\'|\\|\[|\])$', sent) is not None:
        sent = sent[:-1] + "?"  
    else: 
        sent = sent + "?"
    return sent


def swap_words(sent):
    """Attemps to substitute certain words from the user's input to make sense.
    
    Args:
        sent (str): The sentance parameter sent with the function call
        
    Returns:
        sent (str): The edited sentance parameter with a random response
    """
    sent = sent.upper()
    for word in sent.split():
        sent = re.sub(r'YOU', "I", sent)
        sent = re.sub(r'YOUR', "MY", sent)
        sent = re.sub(r'\b[Yy]ou\'?re|[Yy]ou\s+are', "I AM", sent)
        sent = re.sub(r'\b[Aa]m', "ARE", sent)
        #sent = re.sub(r'^I', "YOU", sent)
        sent = re.sub(r'^I', "WHY DO YOU THINK YOU", sent)

    
    return randomize_response(sent)


def randomize_response(sent):
    """Receives the resonse for ELIZA and randomizes a personal message before
        or after.
    
    Args:
        sent (str): The sentance parameter sent with the function call
        
    Returns:
        sent (str): The edited sentance parameter
    """
    remove_punctuation(sent)
    # Random conversational formatting applied
    random_options = {1:name + ", ",2: "INTERESTING. ",3: "REALLY? ",4: "HMMM. ",5:" " + name}
    random_key = random.randint(1,10)
    if random_key < 5:
        sent = random_options[random_key] + sent + "?"
        punctuate_response(sent)
    elif random_key == 5:
        remove_punctuation(sent)
        sent = sent + random_options[random_key] + "?"
    elif random_key > 5:
        remove_punctuation(sent)
        sent = sent + "?"
    return sent


def catch_name(sent):
    """Receives the input from the user containing their name and attempts to 
        locate their (first) name.
    
    Args:
        sent (str): The sentance parameter sent with the function call
        
    Returns:
        name (str): The first word not recognized in common name-introductions 
    """
    global name  # User given name
    
    tokens = re.split('\s+', sent)
    # Catch the words associated with common introduction phrases
    for token in tokens:
        if re.match(r'my|name|is|nickname|i|am|named|called|go|by|calls?|g(i|a)ven?|me|they?|you|can|say|all|friends|full|first|last|middle|initial|so|f?or|a|and?|have|but|about|mom|dad|twin|brother|sister|whole', token, re.IGNORECASE) is None:
            # ELIZA picks the first name that isn't commonly used
            name = remove_punctuation(token.upper()) # Store name in ALL-CAPS
            break
    return name


def reformat(sent):
    """Receives a sentance that did not match during analyzing. Certain words
        are swapped so the ELIZA response makes more sense. If no words are 
        swapped, then a general randomized neutral response is given.
    w
    Args:
        sent (str): The sentance parameter sent with the function call
        
    Returns:
        sent (str): The edited sentance parameter
    """
    remove_punctuation(sent)
    input_sent = sent
    sent = re.sub(r'\b[Yy]ou\b', "ME", sent)
    sent = re.sub(r'\b[Yy]our\b', "MY", sent)
    sent = re.sub(r'^[Ii]\s+am\b', "WHY DO YOU THINK YOU ARE", sent)
    sent = re.sub(r'^[Ii]\b', "WHY DO YOU THINK YOU", sent)
    sent = re.sub(r'\b[Ii]\b', "YOU", sent)
    sent = re.sub(r'\b[Yy]ou\'?re\b|[Yy]oure', "I AM", sent)
    
    random_options = {1:"CAN YOU ELABORATE ON THAT",2: "PLEASE, CAN YOU ELABORATE",3: "WILL YOU PLEASE EXPLAIN THAT FURTHER",4: "COULD YOU TELL ME MORE ABOUT THAT"}
    random_key = random.randint(1,4)
    if sent == input_sent:
        sent = random_options[random_key]
    
    sent.upper()
    sent = randomize_response(sent)
    
    return sent


def analyze_sentance(sent):
    """Receives the input from the user containing their answer to ELIZA and 
        searches for a number of words using regular expressions, with order-
        weighted if-else statements for responses. If nothing is triggered the
        sentance is sent to "reformat()"
    
    Args:
        sent (str): The user input parameter sent with the function call
        
    Returns:
        str: response for ELIZA, randomized reponse for ELIZA
    """
    global name
    remove_punctuation(sent)
    
    question    = re.search(r'^what|^why|^who|^where|^how|^will\s+you|^have\s+you', sent, re.IGNORECASE)
    correct     = re.search(r'^correct\b|^ye(s|p)*\b|^yeah*\b', sent, re.IGNORECASE)
    negative    = re.search(r'^no\b|^nope\b|^wrong\.\b', sent, re.IGNORECASE)
    sorry       = re.search(r'^sorry\b|\bi\'m\s+sorry\b|\bim\s+sorry\b|\b(my\s+)?apolog(y|ies)?\b', sent, re.IGNORECASE)
    explict     = re.search(r'\bdamn\b|\bass\b|\basshole|\bpussy\b|\bdick\b|sh(a|i)t*\b|\bf.ck*|\bc.ck*', sent, re.IGNORECASE)
    violent     = re.search(r'\bmurder(ed|ing)?|\bkill(er|ed|ing)?\b|\bhat(e|er|ing)?\b|\bdespise\b|\bloath(e|ing)?\b|\bdied?\b|\bdead\b|\bdying\b', sent, re.IGNORECASE)
    hard        = re.search(r'\bhard(ship)?\b|\bdifficulty?\b|\btough(er)?\b|\bnot\s+easy\b', sent, re.IGNORECASE)
    easy        = re.search(r'\beas(y|ier)\b|\bsimpl(e|ify)?\b|\bnot\s+hard\b', sent, re.IGNORECASE)
    like_to     = re.search(r'\bi\s+like\s+to\b|\bi\s+want\s+to\b|\bi\s+wanna\b', sent, re.IGNORECASE)
    looking_for = re.search(r'\blooking\s+for\b|\bsearching\s+for\b|\bscanning\s+for\b|\blost\s+my\b', sent, re.IGNORECASE)
    mad         = re.search(r'\bmad(denning)?\b|\bangry\b|\bupset(ting)?\b', sent, re.IGNORECASE)
    happy       = re.search(r'\bhappy\b|\bjoy\b', sent, re.IGNORECASE)
    craving     = re.search(r'\bcraves?|\bcravings?\b|\bdesire', sent, re.IGNORECASE)
    exciting    = re.search(r'\bexcit(e|es|ing)?\b', sent, re.IGNORECASE)
    stress      = re.search(r'\bstress(ful|ed)?\b|\bbus(y|ier)?\b', sent, re.IGNORECASE)
    change_name = re.search(r'\bchange\s+my\s+name\b', sent, re.IGNORECASE)
    love        = re.search(r'\blove\b|\blike\-like\b|\bhave\s+feelings\s+for\b', sent, re.IGNORECASE)
    dream       = re.search(r'\bdreams?\b|\bnightmares?\b', sent, re.IGNORECASE)
    think       = re.search(r'\bi\s+think?\b|\bthinking?|\bthoughts?', sent, re.IGNORECASE)
    work        = re.search(r'\bi\s+work\b|\bwork(s|ed)?', sent, re.IGNORECASE)
    tried       = re.search(r'\btried\b|\btrys?\s+to\b|\btry', sent, re.IGNORECASE)
    eat         = re.search(r'\beats?\b|\beating\b|\bate\b|\bcook(s|ed)?\b|\bchefs?\b', sent, re.IGNORECASE)
    feeling     = re.search(r'\bfeeling|\bi\s+feel\b|\bfeels?', sent, re.IGNORECASE)
    see         = re.search(r'\bsees?\b|\bi\s+saw\b|\bseen|\blook(ed)?\s+at\b', sent, re.IGNORECASE)
    touch       = re.search(r'\btouch(ing)?\b', sent, re.IGNORECASE) 
    hear        = re.search(r'\bhear(ing)?\b|\bheard\b|\blisten(ing)?\b', sent, re.IGNORECASE)
    smell       = re.search(r'\bsmell(s|ing|ed)?\b', sent, re.IGNORECASE) 
    taste       = re.search(r'\btaste(s|d)?\b|\bflavor(s|ed)?\b', sent, re.IGNORECASE)
    family      = re.search(r'\bfamil(y|ies)\b|\bbrothers?\b|\bbro\b|\bsis\b|\bsisters?\b|\bm(o|u)m\b|\bmothers?\b|\bfathers?|\bdad\b', sent, re.IGNORECASE)
    time        = re.search(r'\btime(s|d)?\b|\bcentur(y|ies)?\b|\bdecades?\b|\byears?\b|\bmonths?\b|\bdays?\b|\bhours?\b|\bminutes?\b|\b(centi|milli|micro|pico)?seconds?\b', sent, re.IGNORECASE)
    
    if question is not None:
        string = "I'LL BE THE ONE ASKING THE QUESTIONS. WHAT PROBLEMS ARE YOU HAVING"
        return randomize_response(string)
    
    elif explict is not None:
        string = "YOU DONT NEED TO USE THAT LANGUAGE. WHAT MAKES YOU SPEAK THAT WAY"
        return randomize_response(string)
    
    # If the user input contains 'change my name'
    elif change_name is not None:
        #Ask for confirmation
        answer = input("DID YOU WANT ME TO CALL YOU SOMETHING ELSE?\n")
        #If yes
        if re.match(r'^y*', answer) is not None:
            answer = input("WHAT DID YOU WANT ME TO CALL YOU?\n")
            name = catch_name(answer)
            string = name + ", FANTASTIC! WHAT PROBLEMS CAN I HELP YOU WITH " + name + "?"
            return string
        #If no
        else:
            string = "I WILL KEEP CALLING YOU " + name + " THEN. WHAT PROBLEMS ARE YOU HAVING " + name + "?"
            return string
    
    # If the user input starts with positive affirmation
    elif correct is not None:
        string = "I AGREE. IS THERE A REASON WHY"
        return randomize_response(string)
    
    # If the user input starts with negative word
    elif negative is not None:
        string = "NO? CAN YOU PLEASE EXPLAIN WHY"
        return randomize_response(string)
    
    # If the user mentions 'I'm sorry/sorry/my bad/apologies'
    elif sorry is not None:
        string = "WHY WOULD YOU BE SORRY FOR THAT"
        return randomize_response(string)
    
    elif violent is not None:
        string = "FOCUS ON HAPPY THOUGHTS. WHAT MAKES YOU FEEL PEACEFUL"
        return randomize_response(string)
    
    # The USER says something is 'hard/difficult/not easy to' do
    elif hard is not None:
        tokens = re.search(r'(.*?)\s(hard(ship)?|difficulty?|tough(er)?|not\s+easy)(\s+to\s+)?(.*?)$', sent, re.IGNORECASE)
        verb = tokens.group(6)
        string = "WHAT IS SO HARD ABOUT " + verb.upper()
        return randomize_response(string)
    
    # The USER says something is 'easy/simple/not hard to' do
    elif easy is not None:
        tokens = re.search(r'(.*?)\s(eas(y|ier)|simpl(e|ify)?|not\s+hard)(\s+to\s+)?(.*?)$', sent, re.IGNORECASE)
        verb = tokens.group(6)
        string = "WHAT IS SO EASY ABOUT " + verb.upper()
        return randomize_response(string)
    
    # The USER says they 'like/wamt to, wanna' do something
    elif like_to is not None:
        tokens = re.search(r'(.*?)\s(like\s+to|wants?\s+to|wanna)?\s+(.*?)$', sent)
        match = tokens.group(2)
        action = remove_punctuation(tokens.group(3))
        
        string = name + ", WHY YOU DO YOU THINK YOU " + match.upper() + " " + action.upper() + "?"
        return string
    
    # The USER says they're 'looking/searching/scanning for' something
    elif looking_for is not None:
        tokens = re.search(r'(.*?)\s(looking\s+for|searching\s+for|scanning\s+for|lost\s+my)?\s+(.*?)$', sent)
        match = remove_punctuation(tokens.group(3))
        string = "WHY ARE YOU LOOKING TO FIND "+ match.upper() +"?"
        return randomize_response(string)
    
    elif happy is not None:
        string = "WHAT DO YOU LIKE ABOUT BEING HAPPY"
        return randomize_response(string)
    
    elif mad is not None:
        string = "I PREFER WHEN EVERYONE IS HAPPY. WHAT DO YOU LIKE ABOUT BEING HAPPY"
        return randomize_response(string)
        
    elif feeling is not None:
        string = "HOW IMPORTANT ARE FEELINGS FOR YOU"
        return randomize_response(string)
        
    elif craving is not None:
        string = "WHY DONT YOU TELL ME MORE ABOUT YOUR CRAVINGS"
        return randomize_response(string)
    
    elif exciting is not None:
        string = "WHAT IS SO EXCITING ABOUT THAT"
        return randomize_response(string)
    
    elif stress is not None:
        string = "RELAX. HOW DO YOU UNWIND IN YOUR FREE TIME"
        return randomize_response(string)
    
    elif love is not None:
        tokens = re.search(r'(.*?)(love|like\-like|have\s+feelings\s+for)\s+(.*?)$', sent, re.IGNORECASE)
        match = tokens.group(2)
        action = remove_punctuation(tokens.group(3))
        string = name + ", WHY DO YOU THINK YOU " + match.upper() + " " + action.upper() + "?"
        return string
    
    elif dream is not None:
        string = "WHY DO YOU THINK THAT DREAM MATTERS"
        return randomize_response(string)
    
    elif think is not None:
        string = "I THINK ALL THE TIME. CAN YOU EXPAND ON YOUR THOUGHTS"
        return randomize_response(string)
    
    elif work is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR OWN WORK"
        return randomize_response(string)
    
    elif tried is not None:
        string = "DO OR DO NOT, THERE IS NO TRY. HOW DOES THAT MAKE YOU FEEL"
        return randomize_response(string)
    
    elif eat is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR DIET"
        return randomize_response(string)
    
    elif see is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR VISON"
        return randomize_response(string)
    
    elif hear is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR HEARING"
        return randomize_response(string)
    
    elif touch is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR DEXTERITY"
        return randomize_response(string)
    
    elif smell is not None:
        string = "HOW DOES YOUR FAVORITE SMELL MAKE YOU FEEL"
        return randomize_response(string)
    
    elif taste is not None:
        string = "HOW DO YOU FEEL YOUR ABOUT YOUR DIET"
        return randomize_response(string)
    
    elif time is not None:
        string = "HOW DO YOU FEEL ABOUT THE CONTINUOUS PASSAGE OF TIME"
        return randomize_response(string)
    
    elif family is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR FAMILY"
        return randomize_response(string)
    
    sent = reformat(sent)
    return sent


def text_to_speech(sent):
    # Passing the text and language to the engine,  
    # here we have marked slow=False. Which tells  
    # the module that the converted audio should  
    # have a high speed 
    myobj = gTTS(text=sent, lang=language, slow=False)
    
    # Saving the converted audio in a mp3 file named 
    # welcome  
    myobj.save("welcome.mp3")
    
    # Playing the converted file 
    os.system("welcome.mp3")


# BEGIN 
print("You may type complete sentances to your therapist ELIZA. Enter nothing to exit therapy.")
record = ""
# Introduction
welcome = "HELLO, IM ELIZA. WHATS YOUR NAME?\n"
record =record + welcome
text_to_speech(welcome)
intro = input(welcome)
record =record + intro
name = catch_name(intro)

# Greeting after name capture
greeting = ("NICE TO MEET YOU " + name + "! ")
record = record + " " + greeting
print(greeting)

question = "WHAT SORT OF PROBLEMS ARE YOU HAVING?\n"
record = record + question
text_to_speech(greeting + question)
sentance = input(question)

# AS long as the user inputs something
while sentance!="":
    record = record + " \n" + sentance
    sentance = analyze_sentance(sentance)
    record = record + " \n" + sentance
    
    text_to_speech(sentance)
    
    sentance = input(sentance.upper() + "\n")
    
