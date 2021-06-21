# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 13:45:09 2020
@author: Tyler Griggs
@classwork: VCU CMSC416 Introduction to Natural Language Processing in Spring 2020.

VCU CMSC416 A1 eliza.py

This program intends to imitate a Rogerian Therapist or person-centered therapy.
    The program requests USER to input a complete sentence for the anthropomorphized
    entity ELIZA. ELIZA will respond to it with a question posed to the USER.
    The question posed by ELIZA will have to do with the response provided previously.
    The USER is expected to enter complete sentences, using punctuation at their
    discretion. ELIZA responses will be in ALL CAPS, but USERs can submit any
    format-case. The USER is expected to exit the program by entering nothing
    for ELIZA to respond to. ELIZA responds viably to any text.
    
My Algorithm to accomplish this searches the USER input for a number of
    common terms, verbs, and other words to generate a viable response for
    ELIZA. After finding the groups of words found in the input, responses
    can be fired according to the weights I have assigned them (the order 
    the IF statements occur). When no word groups are caught, the USER's message
    is sent to reformat() to substitute words in the sentence, in that function
    if no words are substituted, ELIZA's response will be a random neutral 
    question to clarify further. The fired responses are often sent to 
    randomize_response() to concatenate a neutral message before or after the
    calculated response.
    
Example:
    HELLO, IM ELIZA. WHATS YOUR NAME?
    My name is Tyler Griggs.
    NICE TO MEET YOU TYLER!
    
    WHAT SORT OF PROBLEMS ARE YOU HAVING?
    I can not believe it is not butter.
    
    INTERESTING. WHY DO YOU THINK YOU CAN NOT BELIEVE IT IS NOT BUTTER?
    I want it to taste really good.
    
    HOW DO YOU FEEL ABOUT YOUR DIET?
    ...
    
    ...
    WHY DO YOU THINK YOU LIKE TO WRITE PROGRAMS?
    **USER enters nothing**
    
    [system exit]
    
    Resources:
        VCU CMSC416 Powerpoint Slides
        regex101.com (testing)
        
    
"""

import re
import random


def remove_punctuation(sent):
    """Attempts to removes punctuation from an input String.
    
    Args:
        sent (str): The sentence parameter sent with the function call
        
    Returns:
        sent (str): The edited sentence parameter
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


def randomize_response(sent):
    """Receives the resonse for ELIZA and randomizes an additional personal 
        message before or after.
    
    Example:
        'WHY DO YOU THINK YOU LIKE CATS' 
        -> 
        "INTERESTING. WHY DO YOU THINK YOU LIKE CATS?"
    
    Args:
        sent (str): The sentance parameter sent with the function call
        
    Returns:
        sent (str): The edited sentance parameter
    """
    remove_punctuation(sent)
    # Random conversational formatting applied
    random_options = {1:name + ", ",2: "INTERESTING. ",3: "REALLY? ",4: "HMMM. ",5:" " + name}
    random_key = random.randint(1,10)
    
    # Return a random response base on a random number
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
        locate their (first) name. The regex searches for a word that doesn't 
        match a long regex that I made to capture all the different ways I know
        how to introduce oneself.
        
    Example:
        My name is Tyler -> "Tyler"
        I go by Tyler G -> "Tyler"
        Mom calls me Tyler -> "Tyler"
        
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
    
    Example:
        You -> ME
        Your -> MY
        My -> WHY DID YOUR (at the start of a sentance)
        I am -> WHY DO YOU THINK YOU ARE (at the start of a sentance)
        I -> WHY DO YOU THINK YOU (at the start of a sentance)
        I -> YOU
        You're -> I AM
    
    Args:
        sent (str): The sentance parameter sent with the function call
        
    Returns:
        sent (str): The edited sentance parameter
    """
    remove_punctuation(sent)
    input_sent = sent
    
    sent = re.sub(r'\b[Yy]ou\b', "ME", sent)
    sent = re.sub(r'\b[Yy]our\b', "MY", sent)
    sent = re.sub(r'^[Mm]y\b', "WHY DID YOUR", sent) 
    sent = re.sub(r'^[Ii]\s+am\b', "WHY DO YOU THINK YOU ARE", sent)
    sent = re.sub(r'^[Ii]\b', "WHY DO YOU THINK YOU", sent)
    sent = re.sub(r'\b[Ii]\b', "YOU", sent)
    sent = re.sub(r'\b[Yy]ou\'?re\b|[Yy]oure', "I AM", sent)
    
    #If no changes are made to the USER input, then provide a neutral 'I dont know' response
    random_options = {1:"CAN YOU ELABORATE ON THAT",2: "PLEASE, CAN YOU ELABORATE",3: "WILL YOU PLEASE EXPLAIN THAT FURTHER",4: "COULD YOU TELL ME MORE ABOUT THAT"}
    random_key = random.randint(1,4)
    if sent == input_sent:
        sent = random_options[random_key]
    
    #Randomize the output with a human-like additional response before or after
        # the ELIZA response
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
    global name # User given name
    
    remove_punctuation(sent)
    
    # Regular Expression searches for potential topics for response
    question    = re.search(r'^what|^why|^who|^where|^when|^how|^will\s+you|^have\s+you', sent, re.IGNORECASE)
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
    
    # The USER began with a word that indicates they are asking a question
    if question is not None:
        string = "I'LL BE THE ONE ASKING THE QUESTIONS. WHAT PROBLEMS ARE YOU HAVING"
        return randomize_response(string)
    
    # The USER mentions forms of not allowed curse words
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
    
    # The USER mentions forms of the word kill, murder
    elif violent is not None:
        string = "FOCUS ON HAPPY THOUGHTS. WHAT MAKES YOU FEEL PEACEFUL"
        return randomize_response(string)
    
    # The USER says something is 'hard/difficult/not easy to' do
    # Directly turns the input into a question for open ended context
    elif hard is not None:
        tokens = re.search(r'(.*?)\s(hard(ship)?|difficulty?|tough(er)?|not\s+easy)(\s+to\s+)?(.*?)$', sent, re.IGNORECASE)
        verb = tokens.group(6)
        string = "WHAT IS SO HARD ABOUT " + verb.upper()
        return randomize_response(string)
    
    # The USER says something is 'easy/simple/not hard to' do
    # Directly turns the input into a question for open ended context
    elif easy is not None:
        tokens = re.search(r'(.*?)\s(eas(y|ier)|simpl(e|ify)?|not\s+hard)(\s+to\s+)?(.*?)$', sent, re.IGNORECASE)
        verb = tokens.group(6)
        string = "WHAT IS SO EASY ABOUT " + verb.upper()
        return randomize_response(string)
    
    # The USER says they 'like/wamt to, wanna' do something
    # Directly turns the input into a question for open ended context
    elif like_to is not None:
        tokens = re.search(r'(.*?)\s(like\s+to|wants?\s+to|wanna)?\s+(.*?)$', sent)
        match = tokens.group(2)
        action = remove_punctuation(tokens.group(3))
        
        string = name + ", WHY YOU DO YOU THINK YOU " + match.upper() + " " + action.upper() + "?"
        return string
    
    # The USER says they're 'looking/searching/scanning for' something
    # Directly turns the input into a question for open ended context
    elif looking_for is not None:
        tokens = re.search(r'(.*?)\s(looking\s+for|searching\s+for|scanning\s+for|lost\s+my)?\s+(.*?)$', sent)
        match = remove_punctuation(tokens.group(3))
        string = "WHY ARE YOU LOOKING TO FIND "+ match.upper() +"?"
        return randomize_response(string)
    
    # The USER mentions forms of the word happy
    elif happy is not None:
        string = "WHAT DO YOU LIKE ABOUT BEING HAPPY"
        return randomize_response(string)
    
    # The USER mentions forms of the word happy
    elif mad is not None:
        string = "I PREFER WHEN EVERYONE IS HAPPY. WHAT DO YOU LIKE ABOUT BEING HAPPY"
        return randomize_response(string)
    
    # The USER mentions forms of the word feel or feelings
    elif feeling is not None:
        string = "HOW IMPORTANT ARE FEELINGS FOR YOU"
        return randomize_response(string)
    
    # The USER mentions forms of the word crave
    elif craving is not None:
        string = "WHY DONT YOU TELL ME MORE ABOUT YOUR CRAVINGS"
        return randomize_response(string)
    
    # The USER mentions forms of the word excite
    elif exciting is not None:
        string = "WHAT IS SO EXCITING ABOUT THAT"
        return randomize_response(string)
    
    # The USER mentions forms of the word stress
    elif stress is not None:
        string = "RELAX. HOW DO YOU UNWIND IN YOUR FREE TIME"
        return randomize_response(string)
    
    # The USER mentions forms of the word love
    # Directly turns the input into a question for open ended context
    elif love is not None:
        tokens = re.search(r'(.*?)(love|like\-like|have\s+feelings\s+for)\s+(.*?)$', sent, re.IGNORECASE)
        match = tokens.group(2)
        action = remove_punctuation(tokens.group(3))
        string = name + ", WHY DO YOU THINK YOU " + match.upper() + " " + action.upper() + "?"
        return string
    
    # The USER mentions forms of the word dream or nightmare
    elif dream is not None:
        string = "WHY DO YOU THINK THAT DREAM MATTERS"
        return randomize_response(string)
    
    # The USER mentions forms of the word think, and ELIZA tries to sound human
    elif think is not None:
        string = "I THINK ALL THE TIME. CAN YOU EXPAND ON YOUR THOUGHTS"
        return randomize_response(string)
    
    # The USER mentions forms of the word work
    elif work is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR OWN WORK"
        return randomize_response(string)
    
    # The USER mentions forms of the word try
    elif tried is not None:
        string = "DO OR DO NOT, THERE IS NO TRY. HOW DOES THAT MAKE YOU FEEL"
        return randomize_response(string)
    
    # The USER mentions forms of the word eat, or food related terms
    elif eat is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR DIET"
        return randomize_response(string)
    
    # The USER mentions forms of the word see or saw
    elif see is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR VISON"
        return randomize_response(string)
    
    # The USER mentions forms of the word hear
    elif hear is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR HEARING"
        return randomize_response(string)
    
    # The USER mentions forms of the word touch
    elif touch is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR DEXTERITY"
        return randomize_response(string)
    
    # The USER mentions forms of the word smell
    elif smell is not None:
        string = "HOW DOES YOUR FAVORITE SMELL MAKE YOU FEEL"
        return randomize_response(string)
    
    # The USER mentions forms of the word taste
    elif taste is not None:
        string = "HOW DO YOU FEEL YOUR ABOUT YOUR DIET"
        return randomize_response(string)
    
    # The USER mentions forms of the word time, or any kind of time units
        # Examples: Timing, picoseconds, century, day
    elif time is not None:
        string = "HOW DO YOU FEEL ABOUT THE CONTINUOUS PASSAGE OF TIME"
        return randomize_response(string)
    
    # The USER mentions word relating to a family
    elif family is not None:
        string = "HOW DO YOU FEEL ABOUT YOUR FAMILY"
        return randomize_response(string)
    
    # If no words are matched then simply reformat the sentance.
    sent = reformat(sent)
    return sent
    

# BEGIN MAIN
print("You may type complete sentances to your therapist ELIZA. Enter nothing to exit therapy.")

# Introduction
intro = input("HELLO, IM ELIZA. WHATS YOUR NAME? \n")
name = catch_name(intro) # User given name

# Greeting after name capture
greeting = ("NICE TO MEET YOU " + name + "! ")
print(greeting)

# Conversation Catalyst
sentance = input("WHAT SORT OF PROBLEMS ARE YOU HAVING?\n")

# As long as the USER enters something
while sentance!="":
    
    sentance = analyze_sentance(sentance)
    sentance = input(sentance.upper() + "\n")
    
    