# Released into the Public Domain by fpgaminer@bitcoin-mining.com


import hashlib
import math
import sys


def load_dictionary(dictionary_file=None):
    """Load a dictionary file - words separated by newlines"""
    if dictionary_file is None:
        dictionary_file = "words.txt"

    with open(dictionary_file, 'rb') as f:
        dictionary = f.read().splitlines()

    return dictionary


def default_hasher(data):
    """Simple md5 hash operation"""
    m = hashlib.md5()
    m.update(data.encode())
    return m.hexdigest()


def hash_phrase(data, minimum_entropy=64, dictionary=None, hashfunc=default_hasher, separator='-'):
    """Hash a phrase into words"""
    if dictionary is None:
        dictionary = load_dictionary()

    dict_len = len(dictionary)
    entropy_per_word = math.log(dict_len, 2)
    num_words = int(math.ceil(minimum_entropy / entropy_per_word))

    # Hash the data and convert to a big integer (converts as Big Endian)
    hash_str = hashfunc(data)
    available_entropy = len(hash_str) * 4
    hash_str = int(hash_str, 16)

    # Check entropy
    if num_words * entropy_per_word > available_entropy:
        raise Exception(
            "The output entropy of the specified hashfunc (%d) is too small." % available_entropy)

    # Generate phrase
    phrase = []

    for _ in range(num_words):
        remainder = int(hash_str % dict_len)
        hash_str = hash_str / dict_len
        phrase.append(dictionary[remainder])

    return separator.join([p.decode().lower().capitalize() for p in phrase])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("USAGE: hash-phrase.py DATA")
        sys.exit(-1)

    print(hash_phrase(sys.argv[1]))
