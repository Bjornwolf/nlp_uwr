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
    # line = map(purify, line)
    print line[146:172]
    unigrams = {}
    for word in line:
        try:
            unigrams[word] += 1
        except KeyError:
            unigrams[word] = 1
    bigrams = {}
    for i in range(len(line)-1):
        key = (line[i], line[i+1])
        try:
            bigrams[key] += 1
        except KeyError:
            bigrams[key] = 1
    trigrams = {}
    for i in range(len(line) - 2):
        key = (line[i], line[i+1], line[i+2])
        try:
            trigrams[key] += 1
        except KeyError:
            trigrams[key] = 1
    K = len(unigrams)
    score_uni = 0
    score_bi = 0
    score_tri = 0
    read = [line[0], line[1]]
    for word in line[2:]:
        key_tri_num = (read[-2], read[-1], word)
        key_tri_den = (read[-2], read[-1])
        prob_tri = float(trigrams[key_tri_num]) / bigrams[key_tri_den]
        key_bi_num = (read[-1], word)
        key_bi_den = read[-1]
        prob_bi = float(bigrams[key_bi_num]) / unigrams[key_bi_den]
        prob_uni = float(unigrams[word]) / K
        read.append(word)
        read = read[-2:]
        if prob_tri > prob_bi and prob_tri > prob_uni:
            score_tri += float(trigrams[key_tri_num])
        elif prob_bi > prob_tri and prob_bi > prob_uni:
            score_bi += float(trigrams[key_tri_num])
        elif prob_uni > prob_bi and prob_uni > prob_tri:
            score_uni += float(trigrams[key_tri_num])
        elif prob_tri == prob_bi and prob_tri > prob_uni:
            score_tri += float(trigrams[key_tri_num]) / 2.0
            score_bi += float(trigrams[key_tri_num]) / 2.0
        elif prob_uni == prob_bi and prob_uni > prob_tri:
            score_uni += float(trigrams[key_tri_num]) / 2.0
            score_bi += float(trigrams[key_tri_num]) / 2.0
        elif prob_tri == prob_uni and prob_tri > prob_bi:
            score_tri += float(trigrams[key_tri_num]) / 2.0
            score_uni += float(trigrams[key_tri_num]) / 2.0
        else:
            score_uni += float(trigrams[key_tri_num]) / 3.0
            score_bi += float(trigrams[key_tri_num]) / 3.0
            score_tri += float(trigrams[key_tri_num]) / 3.0

    sum_score = score_uni + score_bi + score_tri
    score_uni /= sum_score
    score_bi /= sum_score
    score_tri /= sum_score
    print score_uni, score_bi, score_tri
    return unigrams, bigrams, trigrams, score_uni, score_bi, score_tri

def prepare_file(in_file):
    with open('../data/dane_pozytywistyczne/' + in_file, 'r') as f:
        lines = map(lambda x: x[:-1], f.readlines())
    lines = filter(lambda x: x != '', lines)
    lines = map(lambda x: x.split(' '), lines)
    line = reduce(lambda x, y: x + y, lines)
    line = map(clear, line)
    line = filter(lambda x: x != '', line)
    return line

def judge_file(line, uni, bi, tri, score_uni, score_bi, score_tri):
    K = len(uni)
    nll = 0.0
    read = line[:2]
    for word in line[2:]:
        key_tri_num = (read[-2], read[-1], word)
        key_tri_den = (read[-2], read[-1])
        try:
            p_tri = float(tri[key_tri_num]) / bi[key_tri_den]
        except KeyError:
            p_tri = 0.
        key_bi_num = (read[-1], word)
        key_bi_den = read[-1]
        try:
            p_bi = float(bi[key_bi_num]) / uni[key_bi_den]
        except KeyError:
            p_bi = 0.
        try:
            p_uni = float(uni[word]) / K
        except KeyError:
            p_uni = 0.
        read.append(word)
        read = read[-2:]
        p = score_uni * p_uni + score_bi * p_bi + score_tri * p_tri
        if p < 1e-8:
            p = 1e-8
        nll -= log(p)
    return nll

def judge_files(orzeszkowa_list, prus_list, sienkiewicz_list):
    o1, o2, o3, so1, so2, so3 = build_grams_from_file('korpus_orzeszkowej.txt')
    p1, p2, p3, sp1, sp2, sp3 = build_grams_from_file('korpus_prusa.txt')
    s1, s2, s3, ss1, ss2, ss3 = build_grams_from_file('korpus_sienkiewicza.txt')
    success_o = 0
    for name in orzeszkowa_list:
        t_file = 'testy1/' + name
        line = prepare_file(t_file)
        o = judge_file(line, o1, o2, o3, so1, so2, so3)
        p = judge_file(line, p1, p2, p3, sp1, sp2, sp3)
        s = judge_file(line, s1, s2, s3, ss1, ss2, ss3)
        print o, p, s
        if o < p and o < s:
            success_o += 1
    print "ORZESZKOWA"
    print success_o, "/", len(orzeszkowa_list)
    success_p = 0
    for name in prus_list:
        t_file = 'testy1/' + name
        line = prepare_file(t_file)
        o = judge_file(line, o1, o2, o3, so1, so2, so3)
        p = judge_file(line, p1, p2, p3, sp1, sp2, sp3)
        s = judge_file(line, s1, s2, s3, ss1, ss2, ss3)
        print o, p, s
        if p < o and p < s:
            success_p += 1
    print "PRUS"
    print success_p, "/", len(prus_list)
    success_s = 0
    for name in sienkiewicz_list:
        t_file = 'testy1/' + name
        line = prepare_file(t_file)
        o = judge_file(line, o1, o2, o3, so1, so2, so3)
        p = judge_file(line, p1, p2, p3, sp1, sp2, sp3)
        s = judge_file(line, s1, s2, s3, ss1, ss2, ss3)
        print o, p, s
        if s < o and s < p:
            success_s += 1
    print "SIENKIEWICZ"
    print success_s, "/", len(sienkiewicz_list)

orzeszkowa_list = ['test_orzeszkowej' + str(i) + '.txt' for i in [''] + range(1, 22, 2)]
prus_list = ['test_prusa' + str(i) + '.txt' for i in range(0, 41, 2)]
sienkiewicz_list = ['test_sienkiewicza' + str(i) + '.txt' for i in range(1, 54, 2)]

judge_files(orzeszkowa_list, prus_list, sienkiewicz_list)
