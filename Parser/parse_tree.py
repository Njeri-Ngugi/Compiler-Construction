import nltk
from nltk import CFG

# Define grammar rules using a dictionary
grammar_dict = {
    "S": ["NP VP"],
    "NP": ["Det N", "Det N PP"],
    "VP": ["V NP", "V NP PP"],
    "PP": ["P NP"],
    "Det": ["'the'", "'a'"],
    "N": ["'cat'", "'dog'", "'man'", "'park'"],
    "V": ["'chased'", "'saw'"],
    "P": ["'in'", "'on'", "'by'"]
}

# Convert dictionary to string representation of the grammar
grammar_string = "\n".join(f"{key} -> {' | '.join(value)}" for key, value in grammar_dict.items())

# Create CFG from string representation
grammar = CFG.fromstring(grammar_string)
# print(grammar)

# Example usage: parsing a sentence
parser = nltk.ChartParser(grammar)
sentence = "the cat chased the dog in the park"  # Corrected sentence
tokens = nltk.word_tokenize(sentence)

for tree in parser.parse(tokens):
    tree.pretty_print()
