# TREE REPRESENTATION USING NLTK

import nltk
from nltk import CFG
from nltk.parse import RecursiveDescentParser

# Define a simple context-free grammar
grammar = CFG.fromstring("""
    S -> NP VP
    NP -> Det N | Det N PP
    VP -> V NP | V NP PP
    PP -> P NP
    Det -> 'the' | 'a'
    N -> 'cat' | 'dog' | 'man' | 'park'
    V -> 'chased' | 'saw'
    P -> 'in' | 'on' | 'by'
""")

# Create a parser
parser = RecursiveDescentParser(grammar)

# Input sentence
sentence = "the dog chased the cat in the park"

# Tokenize the sentence
tokens = nltk.word_tokenize(sentence)

print(tokens)

# Parse the sentence
for tree in parser.parse(tokens):
    tree.pretty_print()
