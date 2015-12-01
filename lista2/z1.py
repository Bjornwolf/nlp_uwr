#!/usr/bin/python
# -*- coding: UTF-8 -*-

import cPickle as pickle
from math import log

data_loc = '../data/'
latin = 'qwertyuiopasdfghjklzxcvbnm'
polish = 'ęóąśłżźćń'
acceptable_signs = set(latin + polish)
test_sentence = 'astronomia ajmuje sie badsaniem procesów dotyczących tsych cial'

def depolonise(word):
    word = word.replace('ę', 'e').replace('ó', 'o').replace('ą', 'a')
    word = word.replace('ś', 's').replace('ł', 'l').replace('ż', 'z')
    return word.replace('ź', 'z').replace('ć', 'c').replace('ń', 'n')

def generate_all_errors(word):
    n = len(word)
    if n < 3:
        return [word]
    options = [word]
    options += [word[:i] + c + word[i+1:] for i in range(n) for c in latin]
    options += [word[:i] + word[i+1] + word[i] + word[i+2:] for i in range(n-1)]
    options += [word[:i] + word[i+1:] for i in range(n)]
    options += [word[:i] + c + word[i:] for i in range(n+1) for c in latin]
    return options

def get_viable_editions(word, corrector):
    options = generate_all_errors(word)
    viables = []
    for option in options:
        try:
            _ = corrector[option]
            viables.append(option)
        except KeyError:
            pass
    return list(set(viables))

def unravel(line, version=None):
    if version == '2g':
        line = line[:-1].split(' ')
        number = line[-3]
        word1 = line[-2]
        word2 = line[-1]
        return (number, word1, word2)
    elif version == '1g':
        line = line[:-1].split(' ')
        number = line[-2]
        word = line[-1]
        return (number, word)
    elif version == 's':
        return line[:-1]

def purify_2grams(in_file, out_file):    
    out_gram = open(data_loc + out_file, 'w+')
    for line in open(data_loc + in_file, 'r'):
        # line = ['', numerek, slowo1, slowo2]
        (number, word1, word2) = unravel(line, '2g')
        if len(set(word1 + word2) - acceptable_signs) == 0:
            out_gram.write(' '.join([number, word1, word2]) + '\n')

def purify_dict(in_file, out_file):
    out_dict = open(data_loc + out_file, 'w+')
    for line in open(data_loc + in_file, 'r'):
        # line = ['slowo\n']
        word = unravel(line, 's')
        if len(set(word) - acceptable_signs) == 0:
            out_dict.write(line)

def build_correction_option_dict(in_file, pickle_loc):
    result = {}
    for line in open(data_loc + in_file, 'r'):
        word = unravel(line, 's')
        depolon = depolonise(word)
        try:
            result[depolon].append(word)
        except KeyError:
            result[depolon] = [word]
    pickle.dump(result, open(data_loc + pickle_loc, 'wb'))
    return result

def count_log_likelihood(word1, word2, depolon_dict, word_count):
    try:
        (n, v, inner_dict) = depolon_dict[word1]
        try:
            numerator = inner_dict[word2] + 1
        except KeyError:
            numerator = 1
        ll = log(numerator) - log(n + v)
    except KeyError:
        ll = -log(word_count)
    return ll

def dynamic_depolonised(sentence, depolon_dict, corrector):
    wc = len(corrector)
    options = get_sentence_options(sentence, corrector)
    prefices = [([], 0.0)]
    for word_options in options:
        new_prefices = []
        for option in word_options:
            new_prefices_cands = []
            for (prefix, nll) in prefices:
                new_prefix = prefix + [option]
                ll = count_log_likelihood(prefix[-1], option, depolon_dict, wc)
                new_prefices_cands.append(new_prefix, nll - ll)
            best_nll = new_prefices_cands[0][1]
            best_prefix = new_prefices_cands[0][0]
            for (prefix, nll) in new_prefices_cands:
                if nll < best_nll:
                    best_nll = nll
                    best_prefix = prefix
            new_prefices.append( (best_prefix, best_nll) )
        prefices = new_prefices
    return prefices

def build_2gram_dict(in_file, pickle_loc):
    result = {}
    for line in open(data_loc + in_file, 'r'):
        (number, word1, word2) = unravel(depolonise(line), '2g')
        try:
            (n, v, inner_dict) = result[word1]
            try:
                inner_dict[word2] += int(number)
                result[word1] = (n + int(number), v, inner_dict) 
            except KeyError:
                inner_dict[word2] = int(number)
                result[word1] = (n + int(number), v + 1, inner_dict)
        except KeyError:
            inner_dict = {word2: int(number)}
            result[word1] = (int(number), 1, inner_dict)
    pickle.dump(result, open(data_loc + pickle_loc, 'wb'))
    return result

def build_pruned_datasets():
    print 'pruning 2grams...'
    purify_2grams('2grams', '2grams_zepsute')
    print 'pruning dict...'
    purify_dict('slownik_do_literowek.txt', 'slownik')

def build_depolonised_datasets():
    print 'building grams'
    gram_dict = build_2gram_dict('2grams_zepsute', 'depolon_grams.pkl')
    print 'building dict...'
    corrections = build_correction_option_dict('slownik', 'corrections.pkl')
    return gram_dict, corrections, len(corrections)

def get_sentence_options(sentence, corrections):
    depolon_sentence = depolonise(sentence).split(' ')
    options = map(lambda x: get_viable_editions(x, corrections), depolon_sentence)
    return options

build_depolonised_datasets()
# test_options(pickle.load(open(data_loc + 'corrections.pkl', 'rb')), None)
depolon_dict = pickle.load(open(data_loc + 'depolon_grams.pkl', 'rb'))
corrections = pickle.load(open(data_loc + 'corrections.pkl', 'rb'))
print "SENTENCE NOW"
print dynamic_depolonised(test_sentence, depolon_dict, corrections)
