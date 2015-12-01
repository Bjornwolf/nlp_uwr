#!/usr/bin/python
# -*- coding: UTF-8 -*-

def filter_ngrams_with_suffices(ngram_loc, interesting_words, suffices, out_loc):
    grams = open(ngram_loc, 'r')
    out = open(out_loc, 'w+')
    for line in grams:
        matched = False
        words = line[:-1].split(' ')
        for word in words[1:]:
            for suffix in suffices:
                if word[-len(suffix):] == suffix:
                    matched = True
        if matched:
            out.write(line)
        elif reduce(lambda x, y: x or y, map(lambda x: x in line, interesting_words)):
            out.write(line)

def filter_ngrams(ngram_loc, interesting_words, out_loc):
    grams = open(ngram_loc, 'r')
    out = open(out_loc, 'w+')
    for line in grams:
        if reduce(lambda x, y: x or y, map(lambda x: x in line, interesting_words)):
            out.write(line)

judyta = 'judyta dała wczoraj stefanowi czekoladki'.split(' ')
babulenka = 'babuleńka miała dwa rogate koziołki'.split(' ')

for grams in ['../data/2grams', '../data/3grams']:
    for sentence in [judyta, babulenka]:
        filter_ngrams(grams, sentence, grams[-6:] + '_' + sentence[0])
