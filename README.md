## Overview
The model is based on a Hidden Markov Model and uses the Viterbi algorithm to compute the most likely sequence of hidden states (POS tags) for a set of words. 

For training, it is assumed that the words are pre-tokenized. The train.py file generates two hashmaps of hashmaps which it stores in json files. First, likelihood.json stores the emission probabilities $P(word \mid tag)$ and transition_table.json stores the transition probabilities $P(state \mid prev \, state)$. 

## OOV

For handling OOV words, the current implementation is just the constant $1-e7$. Some hyperparameter tuning revealed that accuracy goes from ~$65\%$ at $1-e4$  to ~$94\%$ with $1-e7$. Other potential future implementations include Laplace Smoothing and potential applications of other N-gram smoothing techniques. 

## Usage
run `python3 train.py labeled_corpus.txt` to generate the emission probability matrix and the transition probability matrix. Then, run `python3 viterbi.py unlabeled_corpus.txt` to generate a file submission.pos which tags each word in the corpus. 

If the labeled corpus and unlabeled corpus are from very different sources, i.e. one is an academic journal, and the other is a series of tweets, the model will likely not perform as well.
