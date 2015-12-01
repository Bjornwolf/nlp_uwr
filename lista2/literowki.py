#!/usr/bin/python
# -*- coding: UTF-8 -*-
from difflib import ndiff

# TODO dodac sprawdzanie slownikowe opcji poprawnych
keyboard = ['###qwertyuiop###','###asdfghjkl###', '###zxcvbnm###']
latin = 'qwertyuiopasdfghjklzxcvbnm'
polish = 'ęóąśłżźćń'
chars = set(latin + polish)

def depolonise(word):
    word = word.replace('ę', 'e').replace('ó', 'o').replace('ą', 'a')
    word = word.replace('ś', 's').replace('ł', 'l').replace('ż', 'z')
    return word.replace('ź', 'z').replace('ć', 'c').replace('ń', 'n')



def build_smaller_grams():
    f = open('../data/1grams', 'r')
    out = open('../data/1grams_letters', 'w+')
    for line in f:
        number, word = line[:-1].split(' ')[-2:]
        if len(set(word) - chars) == 0:
            out.write(line)
    f.close()
    out.close()


def possible_typos(sign):
    # znajdz pozycje w stringu i ktorym
    if sign in keyboard[0]:
        i = keyboard[0].find(sign)
        options = [keyboard[0][j] for j in [i-1, i, i+1]]
        options += [keyboard[1][j] for j in [i-1, i]]
    elif sign in keyboard[1]:
        i = keyboard[1].find(sign)
        options = [keyboard[0][j] for j in [i, i+1]]
        options += [keyboard[1][j] for j in [i-1, i, i+1]] 
        options += [keyboard[2][j] for j in [i-1, i]] 
    else:
        i = keyboard[2].find(sign)
        options = [keyboard[1][j] for j in [i, i+1]]
        options += [keyboard[2][j] for j in [i-1, i, i+1]]
    return filter(lambda x: x != '#', options)

def is_typo(word, number, correct, correct_number):
    if number > correct_number:
        return False, 'numbers', None

    errors = []
    for (i, c) in enumerate(ndiff(word, correct)):
        if c[0] in ['-', '+']:
            errors.append( (i, c) )
    # print errors
    if len(errors) == 1:
        pass
        if errors[0][1][0] == '+':
            return True, 'del', None
        else:
            i = errors[0][0]
            letter = errors[0][1][-1]
            typos = []
            if i > 0:
                typos += possible_typos(word[i-1])
            if i < len(word) - 1:
                typos += possible_typos(word[i+1])
            # print typos
            if letter in typos:
                return True, 'ins', None
            else:
                return False, 'n/a', None
 
    elif len(errors) == 2:
        
        if errors[0][1][-1] == errors[1][1][-1] and errors[0][1][0] != errors[1][1][0] and abs(errors[0][0] - errors[1][0]) == 2:
            another = word[(errors[0][0] + errors[1][0]) / 2 - 1]
            return True, 'trans', (another, errors[0][1][-1])

        if abs(errors[0][0] - errors[1][0]) == 1 and errors[0][1][0] != errors[1][1][0] and errors[0][1][-1] in possible_typos(errors[1][1][-1]):
            return True, 'repl', (errors[0][1][-1], errors[1][1][-1])
    elif len(errors) == 3 and depolonise(word) == depolonise(correct):
        if len(word) > len(correct):
            return True, 'alt_plus', None
        else:
            return True, 'alt_minus', None
    return False, 'n/a', None

    # insert musi byc ktores z possible_typos
    # replace podobnie

def build_structure():
    words = {}
    for line in open('../data/1grams_letters', 'r'):
        number, word = line[:-1].split(' ')[-2:]
        word_length = len(word)
        try:
            words[word_length].append( (word, number) )
        except KeyError:
            words[word_length] = [(word, number)]
    return words

def build_dictionary():
    dictionary = {}
    for line in open('../data/slownik', 'r'):
        word = line[:-1]
        dictionary[word] = True
    return dictionary

def find_all_typos(word, word_count, correct_dictionary, grams_by_length):

    word_length = len(word)
    typos = []
    error_count = {'del': 0, 'ins': 0, 'trans': 0, 'repl': 0, 'alt_plus': 0, 'alt_minus': 0}
    repl_stats = []
    trans_stats = []
    try:
        _ = correct_dictionary[word]
    except KeyError:
        return typos, error_count, repl_stats, trans_stats
    for i in [word_length - 1, word_length, word_length + 1]:
        try:
            for (typo, number) in grams_by_length[i]:
                number = int(number)
                is_ok, err_type, err_details = is_typo(typo, number, word, word_count)
                if is_ok:
                    typos.append(typo)
                    error_count[err_type] += number
                    if err_type == 'repl':
                        repl_stats.append(err_details)
                    if err_type == 'trans':
                        trans_stats.append(err_details)
        except KeyError:
            pass
    return typos, error_count, repl_stats, trans_stats

def build_typos(print_no):
    words = build_dictionary()
    grams_by_length = build_structure()

    all_repl = {}
    all_trans = {}
    for l in latin:
        for k in latin:
            all_repl[ (l, k) ] = 0
            all_trans[ (l, k) ] = 0
    total_typoable_words = 0
    total_printed = 0
    total_errors = {'del': 0, 'ins': 0, 'trans': 0, 'repl': 0, 'alt_plus': 0, 'alt_minus': 0}
    for (i, line) in enumerate(open('../data/1grams_letters', 'r')):
        if i % 10000 == 0:
            print i
        number, word = line[:-1].split(' ')[-2:]
        number = int(number)
        typos, errors, repl, trans = find_all_typos(word, number, words, grams_by_length)
        if len(typos) > 0:
            total_typoable_words += 1
            if total_printed < print_no:
                print word, typos
                total_printed += 1
            total_typo_cnt = sum(errors.values())
            # przeskaluj bledy do ppb (podziel przez total_typo_cnt)
            for key in errors.keys():
                total_errors[key] += float(errors[key]) / total_typo_cnt
            for key in repl:
                all_repl[key] += 1
            for key in trans:
                all_trans[key] += 1

# print find_all_typos('się', 100000, words, grams_by_length)

build_smaller_grams()
total_errors, all_repl, all_trans = build_typos(10)
for key in total_errors.keys():
    print key, total_errors[key] / total_typoable_words

total_repl = sum(all_repl.values())
total_trans = sum(all_trans.values())
repl_out = open('../data/repl.csv', 'w+')
trans_out = open('../data/trans.csv', 'w+')
for k in latin:
    repl_out.write(k + ';')
    trans_out.write(k + ';')
repl_out.write('\n')
trans_out.write('\n')
for k in latin:
    repl_out.write(k + ';')
    trans_out.write(k + ';')
    for l in latin:
        repl_out.write(str(float(all_repl[(k, l)]) / total_repl) + ';')
        trans_out.write(str(float(all_trans[(k, l)]) / total_trans) + ';')
    repl_out.write('\n')
    trans_out.write('\n')

