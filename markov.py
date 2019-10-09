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

    #for the whole list
    for idx in range(len(f_list)-n-1):
        #for n length
        for word_to_clean in range(f_list[idx:idx+n]):
            for char in unwanted_char:
                word_to_clean = word_to_clean.replace(char, '')
            list_to_be_tuple.append(word_to_clean)
        tup = tuple(list_to_be_tuple)
        chains[tup] = chains.get(tup, []) + [third_word]

    return chains


def make_text(chains):
    """Return text from chains."""

    words = []
    tup = choice(list(chains.keys()))

    #get the first word (must start with a capital letter)
    while tup[0] != tup[0].capitalize():
        tup = choice(list(chains.keys()))

    word_count = 0

    #get the paragraph
    while tup in chains and word_count < 100:
        words.append(tup[0])
        next_word = choice(chains[tup])
        tup = (tup[1], next_word)
        word_count += 1

    #end the sentence
    while (tup in chains 
        and not tup[0].endswith('.') 
        and not tup[0].endswith('?') 
        and not tup[0].endswith('!')):
        words.append(tup[0])
        next_word = choice(chains[tup])
        tup = (tup[1], next_word)

    # print(f'\nIN?{tup in chains}\n')
    # print(f'\nLAST:{tup}\n')
    words.append(tup[0])

    return " ".join(words)

global_chains = {}

#Assuming no invalid input
gram_length = int(input('How long do you want your n-gram sequence to be? '))

for file in sys.argv[1:]:
    input_path = file
    # Open the file and turn it into one long string
    input_text = open_and_read_file(input_path)
    # Get a Markov chain
    global_chains.update(make_chains(input_text), gram_length)


# Produce random text
random_text = make_text(global_chains)

print(random_text)
