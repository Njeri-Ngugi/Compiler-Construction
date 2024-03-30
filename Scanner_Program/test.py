import nltk
import re

def exclude_comments(text):
    lines = text.split('\n')
    lines_without_comments = []
    for line in lines:
        line = re.sub(r'//.*','', line)
        lines_without_comments.append(line)
    return '\n'.join(lines_without_comments)

#Comparing different tokenization options
program = input("Enter file name to compile: ") #try with main.txt
with open(program, 'r') as file:
    contents = file.read()
    contents = exclude_comments(contents)
    print("--Without comments: ")
    print(contents)
    print("----Split result: ")
    program_tokens = contents.split() #doesn't handle non-spaced lines very well
    print(program_tokens)
    print("----nltk result: ")
    program_tokens = nltk.wordpunct_tokenize(contents)
    print(program_tokens)
    print("-----re.split result: ")
    program_tokens = re.split(r'\W+', contents) #splits text on any non-word characters
    print(program_tokens) #excludes the special characters/punctuators
