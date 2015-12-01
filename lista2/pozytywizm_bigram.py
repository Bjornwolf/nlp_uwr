#!/usr/bin/python
# -*- coding: UTF-8 -*-

from math import log

def clear(word):
    characters = 'qwertyuiopasdfghjklzxcvbnmęóąśłżźćń'
    word = word.decode('utf-8').lower().encode('utf-8')
    return filter(lambda c: c in characters, word)

def build_grams_from_file(in_file):
    with open('../data/dane_pozytywistyczne/' + in_file, 'r') as f:
        lines = map(lambda x: x[:-1], f.readlines())
    lines = filter(lambda x: x != '', lines)
    lines = map(lambda x: x.split(' '), lines)
    line = reduce(lambda x, y: x + y, lines)
    line = map(clear, line)
    line = filter(lambda x: x != '', line)
    print line[146:172]
    bigrams = {}
    for i in range(len(line)-1):
        word1 = line[i]
        word2 = line[i+1]
        try:
            (n, options) = bigrams[word1]
            try:
                options[word2] += 1
            except KeyError:
                options[word2] = 1
            bigrams[word1] = (n+1, options)
        except KeyError:
            bigrams[word1] = (1, {word2: 1})

    return bigrams

def prepare_file(in_file):
    with open('../data/dane_pozytywistyczne/' + in_file, 'r') as f:
        lines = map(lambda x: x[:-1], f.readlines())
    lines = filter(lambda x: x != '', lines)
    lines = map(lambda x: x.split(' '), lines)
    line = reduce(lambda x, y: x + y, lines)
    line = map(clear, line)
    line = filter(lambda x: x != '', line)
    return line

def judge_file(line, bi):
    V = len(bi.keys())
    nll = 0.0
    read = line[0]
    for word in line[1:]:
        try:
            (N, opts) = bi[read]
            try:
                C = opts[word]
            except KeyError:
                C = 0
            p = float(C + 1) / float(N + V)
        except KeyError:
            p = 1e-8
        nll -= log(p)
    return nll

def judge_files(orzeszkowa_list, prus_list, sienkiewicz_list):
    o2 = build_grams_from_file('korpus_orzeszkowej.txt')
    p2 = build_grams_from_file('korpus_prusa.txt')
    s2 = build_grams_from_file('korpus_sienkiewicza.txt')
    success_o = 0
    for name in orzeszkowa_list:
        t_file = 'testy1/' + name
        line = prepare_file(t_file)
        o = judge_file(line, o2)
        p = judge_file(line, p2)
        s = judge_file(line, s2)
        print o, p, s
        if o < p and o < s:
            success_o += 1
    print "ORZESZKOWA"
    print success_o, "/", len(orzeszkowa_list)
    success_p = 0
    for name in prus_list:
        t_file = 'testy1/' + name
        line = prepare_file(t_file)
        o = judge_file(line, o2)
        p = judge_file(line, p2)
        s = judge_file(line, s2)
        print o, p, s
        if p < o and p < s:
            success_p += 1
    print "PRUS"
    print success_p, "/", len(prus_list)
    success_s = 0
    for name in sienkiewicz_list:
        t_file = 'testy1/' + name
        line = prepare_file(t_file)
        o = judge_file(line, o2)
        p = judge_file(line, p2)
        s = judge_file(line, s2)
        print o, p, s
        if s < o and s < p:
            success_s += 1
    print "SIENKIEWICZ"
    print success_s, "/", len(sienkiewicz_list)

orzeszkowa_list = ['test_orzeszkowej' + str(i) + '.txt' for i in [''] + range(1, 22, 2)]
prus_list = ['test_prusa' + str(i) + '.txt' for i in range(0, 41, 2)]
sienkiewicz_list = ['test_sienkiewicza' + str(i) + '.txt' for i in range(1, 54, 2)]

judge_files(orzeszkowa_list, prus_list, sienkiewicz_list)
