import random
import codecs
from math import log
import numpy as np

class Symbol:
    def __init__(self, name, is_terminal=False, pos=None, case=None,
                 number=None, person=None, content=None, gender=None):
        self.is_terminal = is_terminal
        self.name = name
        self.pos = pos
        self.case = case
        self.number = number
        self.person = person
        self.content = content
        self.gender=gender

def produce_sentence():
    sentence = [Symbol("Z")]
    all_terminals = False
    while all_terminals == False:
        all_terminals = True
        new_sentence = []
        for symbol in sentence:
            if not symbol.is_terminal:
                all_terminals = False
            new_sentence += produce(symbol)
        sentence = new_sentence
    result = flatten_sentence(sentence)
    return result

def flatten_sentence(sentence):
    result = []
    for symbol in sentence:
        if symbol.content is not None:
            result.append(symbol.content)
        else:
            tag = [symbol.pos, symbol.number, symbol.case, symbol.gender]
            if symbol.pos == "adj":
                tag += ["pos"]
            tag = ":".join(tag)
            result.append(tag)
    return result

def produce(symbol):
    gender = ["m1", "m2", "m3", "f", "n1", "n2"]
    nums = ["sg", "pl"]
    if symbol.is_terminal:
        return [symbol]
    if symbol.name == "Z":
        p = np.random.uniform(0, 1)
        if p < 0.5:
            return [Symbol("GR", case="nom", number="sg", 
                           gender=random.choice(gender)),
                    Symbol("GC", number="sg")]
        else:
            with open('../data/trans_form', 'r') as tf:
                lines = tf.readlines()
            chosen = random.choice(lines)[:-1].split(' ')
            word = chosen[0]
            tag = chosen[1]
            if "sg" in tag:
                number = "sg"
            else:
                number = "pl"
            my_gender = tag.split(':')[-2]

            res = [Symbol("GR", case="nom", number=number, 
                          gender=my_gender),
                   Symbol(None, is_terminal=True, content=word)]
            p = np.random.uniform(0, 1)
            if p < 0.5:
                res += [Symbol("GR", case="dat", number=random.choice(nums),
                               gender=random.choice(gender))]

            p = np.random.uniform(0, 1)
            if p < 0.5:
                res += [Symbol("GR", case="acc", number=random.choice(nums), 
                               gender=random.choice(gender))]
            return res

    elif symbol.name == "GC":
        p = np.random.uniform(0, 1)

        if p < 0.2:
            return [Symbol(None, is_terminal=True, content="opowiada o"),
                    Symbol("GR", case="loc", number=random.choice(nums),
                           gender=random.choice(gender))]
        if p < 0.4:
            return [Symbol(None, is_terminal=True, content="pracuje z"),
                    Symbol("GR", case="inst", number=random.choice(nums), 
                           gender=random.choice(gender))]
        if p < 0.6:
            return [Symbol(None, is_terminal=True, content="je"),
                    Symbol("GR", case="acc", number=random.choice(nums), 
                           gender=random.choice(gender))]
        if p < 0.8:
            return [Symbol(None, is_terminal=True, content="idzie do"),
                    Symbol("GR", case="gen", number=random.choice(nums),
                           gender=random.choice(gender))]
        else:
            return [Symbol(None, is_terminal=True, content="lubi"),
                    Symbol("GR", case="acc", number=random.choice(nums),
                           gender=random.choice(gender))]
    elif symbol.name == "GR":
        p = np.random.uniform(0, 1)
        if p < 0.05:
            return [Symbol("GR", case=symbol.case, number=symbol.number,
                           gender=symbol.gender),
                    Symbol(None, is_terminal=True, content="i"),
                    Symbol("GR", case=symbol.case, number=symbol.number,
                           gender=symbol.gender)]
        else:
            return [Symbol("GP", case=symbol.case, number=symbol.number,
                           gender=symbol.gender),
                    Symbol(None, is_terminal=True, pos="subst", case=symbol.case,
                            number=symbol.number, gender=symbol.gender),
                    Symbol("D")]
    elif symbol.name == "GP":
        p = np.random.uniform(0, 1)
        if p < 0.2:
            return [Symbol("GP", case=symbol.case, number=symbol.number,
                           gender=symbol.gender),
                    Symbol(None, is_terminal=True, pos="adj", case=symbol.case,
                            number=symbol.number, gender=symbol.gender)]
        elif p < 0.5:
            return [Symbol(None, is_terminal=True, pos="adj", case=symbol.case,
                            number=symbol.number, gender=symbol.gender)]
        else:
            return []
    elif symbol.name == "D":
        p = np.random.uniform(0, 1)
        if p < 0.1:    
            return [Symbol(None, is_terminal=True, content="na"),
                    Symbol("GRN", case="loc", number="sg", 
                           gender=random.choice(gender))]
        elif p < 0.4:
            return [Symbol(None, is_terminal=True, content="w"),
                    Symbol("GRN", case="loc", number="sg",
                           gender=random.choice(gender))]
        elif p < 0.7:
            return [Symbol(None, is_terminal=True, content="z"),
                    Symbol("GRN", case="inst", number="sg",
                           gender=random.choice(gender))]
        else:
            return []
    elif symbol.name == "GRN":
        return [Symbol("GP", case=symbol.case, number=symbol.number, 
                       gender=symbol.gender),
                Symbol(None, is_terminal=True, pos="subst", case=symbol.case,
                       number=symbol.number, gender=symbol.gender)]
    else:
        return [symbol]

def find_best(list_of_pairs):
    low = min(map(lambda x: x[1], list_of_pairs))
    return filter(lambda x: x[1] == low, list_of_pairs)[0]

def sample_from(domain, total):
    sample = random.randint(0, total)
    for (word, current) in domain:
        if sample < current:
            return word
        else:
            sample -= current
    return domain[-1][0]

def pick_unigram(words, unigrams):
    total = 0
    for word in words:
        try:
            total += unigrams[word]
        except KeyError:
            pass
    choice = random.randint(0, total)
    for word in words:
        try:
            current = unigrams[word]
            if choice < current:
                return word, current, total
            else:
                choice -= current
        except KeyError:
            pass

def build_unigram(sentence, tags_to_words, unigrams):
    result = []
    for word in sentence:
        if ':' in word:
            result.append(pick_unigram(tags_to_words[word], unigrams)[0])
        else:
            result.append(word)
    return result

def build_bigram(sentence, tags_to_words, unigrams, bigrams, words_to_tags,
                 skipgrams):
    so_far = []
    tag_word = sentence[0]
    if ':' in tag_word:
        options = tags_to_words[tag_word]
        options = filter(lambda x: x in unigrams, options)
        counts = [unigrams[word] for word in options]
        so_far = [sample_from(zip(options, counts), sum(counts))]
    else:
        so_far = [tag_word]

    for tag_word in sentence[1:]:
        second_last_word = None
        last_word = so_far[-1]
        try: 
            acceptables = bigrams[last_word]
            if len(so_far) > 2:
                second_last_word = so_far[-2]
                if second_last_word in skipgrams:
                    new_acceptables = {}
                    for word in acceptables:
                        if word in skipgrams[second_last_word]:
                            new_acceptables[word] = acceptables[word]
                    acceptables = new_acceptables
        except KeyError:
            acceptables = {}
        if ':' in tag_word:
            potential_words = []
            total = 0
            for word in acceptables:
                if word in words_to_tags and tag_word in words_to_tags[word]:
                    num = acceptables[word]
                    total += num
                    potential_words.append( (word, num) )
            if total == 0:
                new_word = random.choice(tags_to_words[tag_word])
                so_far.append(new_word)
            else:
                so_far.append(sample_from(potential_words, total))
        else:
            so_far.append(tag_word)
    return so_far

def read_morfeusz_nkjp(morfeusz_handle):
    lines = morfeusz_handle.readlines()
    dictionary = {}
    dictionary2 = {}
    for line in lines:
        parts = line[:-1].split(' ')
        word = parts[0]
        tags = parts[2:]
        dictionary2[word] = tags
        for tag in tags:
            try:
                dictionary[tag].append(word)
            except KeyError:
                dictionary[tag] = [word]
    return dictionary, dictionary2

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

def read_skipgrams(skipgram_handle):
    dictionary = {}
    for line in skipgram_handle:
        line = line[:-1].split(' ')
        number = float(line[0])
        w1 = line[1]
        w2 = line[2]
        if number > 20.:
            if w1 in dictionary:
                dictionary[w1].append(w2)
            else:
                dictionary[w1] = [w2]
    return dictionary





with codecs.open('../data/1grams', 'r') as unig:
    unigrams = read_1grams(unig)

with codecs.open('../data/2grams_zepsute', 'r') as big:
    bigrams = read_2grams(big)

with codecs.open('../data/morfeuszNKJP.txt', 'r') as morf:
    tags_to_words, words_to_tags = read_morfeusz_nkjp(morf)

with codecs.open('../data/skipgramy', 'r') as skip:
    skipgrams = read_skipgrams(skip)

sentences = [produce_sentence() for _ in range(10)]
for tags in sentences:
    print tags
    for _ in range(5):
        unigres = build_unigram(tags, tags_to_words, unigrams)
        print 'UNIGRAM: ', ' '.join(unigres)

        bigres = build_bigram(tags, tags_to_words, unigrams, bigrams, words_to_tags, skipgrams)
        print 'BIGRAM: ', ' '.join(bigres)


