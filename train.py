#!/usr/bin/python3

import sys

if len(sys.argv) != 2:
    print("Usage: tagging.py <filename>")
    sys.exit(1)

corpus = sys.argv[1]

def get_frequencies(curr_tag, prev_tag, word): 
    '''
    creates likelihood table
        - likelihood['DT'] = {'the':30, 'an':100}
        - table of frequencies of words given POS
        - {'DT': {}, }
    
    also creates transition probabilities table
        - transition['Begin_State'] = {'DT':100, 'NNP':100}
        - relates states to frequencies
        - freq: t2 | t1
    '''
    if curr_tag in likelihoods:
        if word in likelihoods[curr_tag]:
            likelihoods[curr_tag][word] += 1
        else:
            likelihoods[curr_tag][word] = 1
    else:
        likelihoods[curr_tag] = {word: 1}

    ## don't compute if beginning of sent
    if prev_tag is None:
        return

    if prev_tag in transition_table:
        if curr_tag in transition_table[prev_tag]: ## begin_state & DT
            transition_table[prev_tag][curr_tag] += 1
        else: # begin_state but no DT
            transition_table[prev_tag][curr_tag] = 1
    else: ## no begin_state, no DT or begin_state but no DT
        transition_table[prev_tag] = {curr_tag: 1}

def freq_to_prob():
    '''
    likelihood['DT'] = {'the':30, 'an':100} ->
    likelihood['DT'] = {'the': 30/130, 'an':100/130}
    
    transition['Begin_State'] = {'DT':100, 'NNP':100} ->
    transition['Begin_State'] = {'DT':100/200, 'NNP':100/200}
    '''
    
    for tag in likelihoods:
        total = sum(likelihoods[tag].values())
        for word in likelihoods[tag]:
            likelihoods[tag][word] /= total
    
    for tag in transition_table:
        total = sum(transition_table[tag].values())
        for next_tag in transition_table[tag]:
            transition_table[tag][next_tag] /= total



def train(corpus_name):
    '''
    likelihoods['DT'] = {'the': 0.5, 'a': 0.5}
    transition_table['Begin_State'] = {'DT': 0.5, 'NNP': 0.5}
    
    '''
    try:
        with open(corpus_name, 'r') as text_file:
            previous_tag = "Begin_Sent"
            
            for line in text_file:
                parts = line.strip().split('\t')

                if len(parts) < 2: 
                    curr_tag = "End_Sent"
                    get_frequencies(curr_tag, previous_tag, None)
                    previous_tag = "Begin_Sent"
                    continue
                
                word = parts[0].lower() ## The vs the is trivial difference
                vocabulary.add(word)
                curr_tag = parts[1]

                get_frequencies(curr_tag, previous_tag, word)
                previous_tag = curr_tag
            
            freq_to_prob() ## converts both likelihoods and transition_table to probabilities

            print(likelihoods)
            print('\n')
            print(transition_table)

    except FileNotFoundError:
        print(f"corpus not found: {corpus_name}")
        sys.exit(1)

likelihoods = {}
transition_table = {}
vocabulary = set()

train(corpus)













