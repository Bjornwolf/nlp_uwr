#!/usr/bin/python
# -*- coding: UTF-8 -*-

def summarise(gram):
    den = 0
    for n,v in gram:
        if v == 0:
            den += 1
        else:
            den = den + n + v
    return den

def match(x, words, suffices):
    for word in words:
        if x == word:
            return word
    for suffix in suffices:
        if x[-len(suffix):] == suffix:
            return '<SUF>' + suffix
    return '<NONE>'


def build_3judge(grams, words, suffices):
    translator = dict(zip(['<NONE>'] + words + map(lambda x: '<SUF>' + x, suffices), range(len(words) + len(suffices) + 1)))
    n = len(translator)
    result_grid = [[[(0, 0) for _ in range(n)] for _ in range(n)] for _ in range(n)]
    with open(grams, 'r') as f:
        for line in f:
            cut = line[:-1].split(' ')[-4:]
            freq = int(cut[0])
            vals = map(lambda x: translator[match(x, words, suffices)], cut[1:])
            a = vals[0]
            b = vals[1]
            c = vals[2]
            (total, records) = result_grid[a][b][c]
            result_grid[a][b][c] = (total + freq, records + 1)
    return result_grid, translator

def grade_sentence(sentence, model, translator, words, suffices):
    import math
    words = map(lambda x: translator[match(x, words, suffices)], sentence.split(' '))
    trigrams = [words[i:i+3] for i in range(len(words) - 2)]
    nll = 0
    for a, b, c in trigrams:
        if model[a][b][c] == (0, 0):
            numerator = 1.
        else:
            x, y = model[a][b][c]
            numerator = float(x + y)
        denominator = summarise(model[a][b])
        nll -= math.log(numerator / denominator)
    return nll


words = ["dała", "wczoraj"]
suffices = ["a", "owi", "adki"]

#res,translator = build_3judge('../data/3grams', ["dała", "wczoraj"], ["a", "owi", "adki"])
#sentences = open('zad3_judyta', 'r')
#judyta_out = open('zad5_judyta', 'w+')
#for sentence in sentences:
#    grade = grade_sentence(sentence[:-1], res, translator, words, suffices)
#    judyta_out.write(str(grade) + " " + sentence + "\n")


words = ["miała", "dwa"]
suffices = ["a", "te", "ołki"]

res,translator = build_3judge('../data/3grams', ["miała", "dwa"], ["a", "te", "ołki"])
sentences = open('zad3_babulenka', 'r')
babulenka_out = open('zad5_babulenka', 'w+')
for sentence in sentences:
    grade = grade_sentence(sentence[:-1], res, translator, words, suffices)
    babulenka_out.write(str(grade) + " " + sentence + "\n")


