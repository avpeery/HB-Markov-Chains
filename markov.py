"""Generate Markov text from text files."""

from random import choice
import sys


def open_and_read_file(file_path):
    """Take file path as string; return text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    # your code goes here
    f_object = open(file_path)
    f_string = f_object.read()
    f_object.close()

    return f_string


def make_chains(text_string, n):
    """Take input text as string; return dictionary of Markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.
    f
    For example:

        >>> chains = make_chains("hi there mary hi there juanita")

    Each bigram (except the last) will be a key in chains:

        >>> sorted(chains.keys())
        [('hi', 'there'), ('mary', 'hi'), ('there', 'mary')]

    Each item in chains is a list of all possible following words:

        >>> chains[('hi', 'there')]
        ['mary', 'juanita']
        
        >>> chains[('there','juanita')]
        [None]
    """
    unwanted_char = ['--', '[', ']', '(', ')', '/', '*', '_', '\\', '&']
    chains = {}
    list_to_be_tuple = []
    f_list = text_string.split()

    #to get first tuple
    for word_to_clean in f_list[:n]:
        for char in unwanted_char:
            word_to_clean = word_to_clean.replace(char, '')
        list_to_be_tuple.append(word_to_clean)
    #for rest of string
    for idx in range(n, len(f_list)-1):
        #make tuple
        tup = tuple(list_to_be_tuple)
        #clean next_word
        next_word = f_list[idx]
        for char in unwanted_char:
            next_word = next_word.replace(char, '')
        #add value to key(tup)
        chains[tup] = chains.get(tup, []) + [next_word]
        #create next tuple
        list_to_be_tuple = list_to_be_tuple[1:] + [next_word]

    return chains


def make_text(chains):
    """Return text from chains."""

    words = []
    tup = choice(list(chains.keys()))

    #get the first word (must start with a capital letter)
    while tup[0] != tup[0].capitalize():
        tup = choice(list(chains.keys()))

    tup_count = 0

    #get the paragraph
    while tup in chains and tup_count < 100:
        words.append(tup[0])
        next_word = choice(chains[tup])
        tup = tup[1:] + (next_word,)
        tup_count += 1

    #end the sentence
    while (tup in chains 
        and not tup[0].endswith('.') 
        and not tup[0].endswith('?') 
        and not tup[0].endswith('!')):
        words.append(tup[0])
        next_word = choice(chains[tup])
        tup = tup[1:] + (next_word,)

    if tup not in chains:
        words.extend(tup)
    else:
        words.append(tup[0])
    # print(words)
    return " ".join(words)

global_chains = {}

#Assuming no invalid input
gram_length = int(input('How long do you want your n-gram sequence to be? (min 2) '))

for file in sys.argv[1:]:
    input_path = file
    # Open the file and turn it into one long string
    input_text = open_and_read_file(input_path)
    # Get a Markov chain
    global_chains.update(make_chains(input_text, gram_length))


# Produce random text
random_text = make_text(global_chains)

print(random_text)
