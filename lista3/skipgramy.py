import numpy as np
import matplotlib.pyplot as plt
import codecs

def read_1grams(unigram_handle):
    dictionary = {}
    for line in unigram_handle:
        parts = line[:-1].split(' ')
        word = parts[-1]
        number = int(parts[-2])
        dictionary[word] = number
    return dictionary

def read_2grams(bigram_handle):
    dictionary = {}
    for line in bigram_handle: 
        parts = line[:-1].split(' ')
        word2 = parts[-1]
        word1 = parts[-2]
        number = int(parts[-3])
        try:
            dictionary[word1][word2] = number
        except KeyError:
            dictionary[word1] = {word2: number}
    return dictionary


def count_trig_probs(trigram_handle, unigrams, bigrams):
    results = {}
    for line in trigram_handle:
        parts = line[:-1].split(' ')
        word3 = parts[-1]
        word2 = parts[-2]
        word1 = parts[-3]
        number = int(parts[-4])
        p_trig = 1.0 * number / bigrams[word1][word2]
        p_big = 1.0 * bigrams[word1][word2] * bigrams[word2][word3]
        p_big /= unigrams[word1] * unigrams[word2]
        try:
            results[(word1, word3)] += p_trig - p_big
        except KeyError:
            results[(word1, word3)] = p_trig - p_big
    print 

with codecs.open('../data/1grams', 'r') as unig:
    unigrams = read_1grams(unig)

with codecs.open('../data/2grams', 'r') as big:
    bigrams = read_2grams(big)

with codecs.open('../data/3grams', 'r') as trig:
    skips = count_trig_probs(trig, unigrams, bigrams)

plt.hist(np.array(skips.values()))
plt.show()

