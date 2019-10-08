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


def make_chains(text_string):
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

    chains = {}
    f_list = text_string.split()
    for idx, word in enumerate(f_list):
        if idx == len(f_list) - 2:
            break
        tup = (word, f_list[idx+1])
        chains[tup] = chains.get(tup, []) + [f_list[idx+2]]

    return chains
    # for key, value in chains.items():
    #     print(f"{key}: {value}")


def make_text(chains):
    """Return text from chains."""

    words = []
    tup = choice(list(chains.keys()))

    #get the first word (must start with a capital letter)
    while tup[0] != tup[0].capitalize():
        tup = choice(list(chains.keys()))

    word_count = 0

    #get the paragraph
    while tup in chains and word_count < 50:
        words.append(tup[0])
        next_word = choice(chains[tup])
        tup = (tup[1], next_word)
        word_count += 1

    #end the sentence
    while not tup[0].endswith('.') and not tup[0].endswith('?'):
        words.append(tup[0])
        next_word = choice(chains[tup])
        tup = (tup[1], next_word)
    words.append(tup[0])

    return " ".join(words)

global_chains = {}

for file in sys.argv[1:]:
    input_path = file
    # Open the file and turn it into one long string
    input_text = open_and_read_file(input_path)
    # Get a Markov chain
    global_chains.update(make_chains(input_text))
    # for key, value in global_chains.items():
    #     print(f"{key}: {value}")
    # print('\n\n')


# Produce random text
random_text = make_text(global_chains)

print(random_text)
