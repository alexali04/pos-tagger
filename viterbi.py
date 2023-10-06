#!/usr/bin/python3

'''
viterbi HMM POS Tagger

emission probability: probability a word is assigned a specific state
    - likelihood['DT'] = {'the': 0.5, 'a': 0.5}

transition probability: P(curr state = verb | prev state = noun)
    - transition_table['Begin_State'] = {'DT': 0.5, 'NNP': 0.5}
    
viterbi algorithm:
    - P(curr word is curr state) = P(curr word | curr state) * P(curr state | prev state) * P(prev state)
    = emission prob * transition prob * prev viterbi
    = P(curr word is verb) = likelihood[state][curr word] * transition_table[prev state][curr state] * prev viterbi
'''

import sys
import json

if len(sys.argv) != 2:
    print("Usage: viterbi.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

with open('likelihood.json', 'r', encoding='utf-8') as file_1:
    likelihood = json.load(file_1)

with open('transition_table.json', 'r', encoding='utf-8') as file_2:
    transition_prob = json.load(file_2)

def tag(corpus_name):
    with open(corpus_name, 'r') as text, open(output_name, 'w') as output_file: ## read, write at same time
        first_val = text.readline().strip()

        while first_val:
            sentence_tokens = get_sent(text, first_val)
            pos_tags = get_tags(sentence_tokens)
            for token, tag in zip(sentence_tokens, pos_tags):
                output_file.write(f"{token}\t{tag}\n") ## tag to output file
            
            output_file.write("\n")

            first_val = text.readline()  ## increment over \n to get to start of next sentence
            if first_val == "" or first_val == "\n":
                first_val = text.readline().strip() 

def get_sent(text, first_token):
    first_token = first_token.replace("\n", "")
    sentence = [first_token] 
    while True:
        token = text.readline().strip()
        if not token or token == "\n":
            break
        
        token = token.replace("\n", "")
        sentence.append(token)

    return sentence
    

output_name = "submission.pos"


""" 
hidden states cluster / categorize observed instances

Viterbi:
    viterbi algorithm - uses dynamic programming to find optimal hidden sequence
    P(word is tag) = max(P(prev word is prev tag) * P(tag | prev tag) * P(word | tag)) for prev tag in tags
        - prevents exponential number of paths - information about previous paths is contained in previous word column
        - all information about prev paths is in prev words -> works w/ markov model
            - future is indep. of past given present
    
    for each word:
        for each tag:
            P(word is tag) = max(P(prev word is prev tag) * P(tag | prev tag) * P(word | tag)) for prev_tag in tags
            O(w * t * t) = O(t^2 w)

Backpointers:
    viterbi[i][j] = probability of most likely path ending at word j with tag i

    backpointer[i][j] = which tag at word j - 1 maximizes probability of path ending at word j w/ tag i
        - we can't have a 1d array just storing argmaxes - we're not finding the global most likely path
        - we're finding the most likely path that ends in a particular state
        - can reach tag in curr col thru several paths - need a backpointer for each state at each position in the sequence
"""
def get_tags(word_sequence):
    '''
    observed sequence is set of words
    hidden sequence is set of tags
        - want most likely sequence of tags that generates observed sequence

    emission probability: probability a word is assigned a specific state
        - likelihood['DT'] = {'the': 0.5, 'a': 0.5}

    transition probability: P(curr state = verb | prev state = noun)
        - transition_table['Begin_State'] = {'DT': 0.5, 'NNP': 0.5}

    OOV handling:
        - default probability 1e-7 - seems to generate best results via hyperparameter tuning
    '''
    
    tags = likelihood.keys()
    ## includes end_sent, excludes begin_sent
    ## this is OK since begin_sent is in transition_prob - and we're not actually tagging it as anything
    ## states include POS Tags + begin_sent + end_sent but we can kind of ignore begin_sent since we're doing it manually in initialization
    ## must exclude end_sent in previous tags though


    viterbi = {}
    backpointers = {}
    word_sequence = [word.lower() for word in word_sequence]
    
    ## INITIALIZATION:
    ## Nouns, Verbs, etc.
    for tag in tags:
        viterbi[tag] = {}
        viterbi[tag][0] = likelihood[tag].get(word_sequence[0], 1e-7) * transition_prob['Begin_Sent'].get(tag, 1e-7)
        ## P(token | curr tag) * P(curr tag | previous tag)
        ## P(token | curr tag) = emission probability -> P(verb emits eat)

        backpointers[tag] = {}
        backpointers[tag][0] = "Begin_Sent" ## start state is argmax for prev states
    
    ## RECURSION:
    for j in range(1, len(word_sequence)):
        for tag in tags:

            max_prob, best_prev_tag = max(
                (
                    viterbi[prev_tag][j - 1] * transition_prob[prev_tag].get(tag, 1e-7) * likelihood[tag].get(word_sequence[j], 1e-7),
                    prev_tag
                ) 
                for prev_tag in tags - ["End_Sent"]
            )

            ## P(curr word is curr state) = P(prev word is prev state) * P(curr word | curr state) * P(curr state | prev state)
            
            viterbi[tag][j] = max_prob
            backpointers[tag][j] = best_prev_tag
        

    ## TRACE
    best_prob_for_last_word, best_prev_tag = max(
    (viterbi[tag][len(word_sequence) - 1], tag) for tag in tags
    )
    
    ## backpointers[i][j] = which tag at j - 1 maximizes probability of path ending at word j w/ tag i
    ## best_prev_tag is held at backpointers[curr tag][word number]
    ## we get current tag by moving backwards to get best_prev_tag
    ## then we insert that in tag_sequence at the 0th position

    tag_seq = [best_prev_tag]
    for q in range(len(word_sequence) - 1, 0, -1):
        best_prev_tag = backpointers[tag_seq[0]][q]
        tag_seq.insert(0, best_prev_tag)

    return tag_seq



        
    



    
   


tag(filename)



