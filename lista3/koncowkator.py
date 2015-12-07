# -*- coding: UTF-8 -*-
import cPickle as pickle

class Trie:
    def __init__(self):
        self.sons = {}
        self.bases = {}

    def add(self, word, base, weight):
        if word != '':
            if word[-1] not in self.sons:
                self.sons[word[-1]] = Trie()
            self.sons[word[-1]].add(word[:-1], base, weight)
        else:
            self.bases[base] = weight

    def trim(self):
        to_delete = []
        for s in self.sons:
            if not self.sons[s].is_leaf():
                self.sons[s].trim()
            if self.sons[s].is_leaf():
                all_bases = self.sons[s].bases.keys()
                if min(map(len, all_bases)) > 0:
                    prefices = list(set(map(lambda x: x[0], all_bases)))
                else:
                    prefices = ['a', 'b']
                if len(prefices) == 1 and prefices[0] == s:
                    for base in all_bases:
                        try:
                            self.bases[base[1:]] += self.sons[s].bases[base]
                        except KeyError:
                            self.bases[base[1:]] = self.sons[s].bases[base]
                    to_delete.append(s)
        for td in to_delete:
            del self.sons[td]

    def move_weights(self, word, base, weight, history=''):
        self.modify_first_fit(word, base, weight, '')
        self.modify_best_fit(word, base, weight, '')

    def modify_first_fit(self, word, base, weight, history=''):
        for new_suf in self.bases:
            if word + new_suf == base:
                self.bases[new_suf] += weight
                return
        new_hist = word[-1] + history
        self.sons[word[-1]].modify_first_fit(word[:-1], base, weight, new_hist)

    def modify_best_fit(self, word, base, weight, history):
        succ = False
        if word != '':
            if word[-1] in self.sons:
                new_hist = word[-1] + history
                succ = self.sons[word[-1]].modify_best_fit(word[:-1], base, 
                                                       weight, new_hist)
        if succ:
            return True

        for new_suf in self.bases:
            if word + new_suf == base:
                self.bases[new_suf] -= weight
                if self.bases[new_suf] == 0:
                    del self.bases[new_suf]
                return True
        return False
        
    def find_all(self, word):
        results = []
        if word[-1] in self.sons:
            results = self.sons[word[-1]].find_all(word[:-1])
        for base in self.bases:
            results.append( (word + base, self.bases[base]) )
        return results

    def query(self, word):
        final_results = []
        results = self.find_all(word)
        final_results = {}
        for base, weight in results:
            if base in final_results:
                final_results[base] += weight
            else: 
                final_results[base] = weight
        total_weights = sum(final_results.values())
        for key in final_results:
            final_results[key] /= total_weights
        return final_results


    def is_leaf(self):
        return len(self.sons) == 0


# odczytaj_morfeusza
morfeusz_data = {}
known_words = {}
with open('../data/morfeuszNKJP.txt', 'r') as morfeusz:
    for line in morfeusz:
        parts = line.split(' ')
        word = parts[0]
        base = parts[1]
        pos = base.rfind(':')
        if pos != -1:
            base = base[:pos]
        if word in morfeusz_data:
            morfeusz_data[word].append(base)
        else:
            morfeusz_data[word] = [base]
        known_words[base] = True

print "LOADED"

words_bases = []
for word in morfeusz_data:
    n = len(morfeusz_data[word])
    for base in morfeusz_data[word]:
        words_bases.append( (word, base, 1.0 / n) )

print "PROCESSED"

# words_bases = []
# words_bases += [('miał', 'miał', 0.5)]
# words_bases += [('miał', 'mieć', 0.5)]
# words_bases += [('workami', 'worek', 1.0)]
# words_bases += [('korkami', 'korek', 1.0)]

trie = Trie()

for word, base, weight in words_bases:
    if word != base:
        trie.add(word, base, weight)

print "ADDED"

trie.trim()

print "TRIMMED"

for word, base, weight in words_bases:
    if word != base:
        trie.move_weights(word, base, weight)

print "OPTIMISED"

# query = 'cyckami'
queries = 'szmukwijne jaszwije wężały na zegwniku'.split(' ')

pickle.dump(trie, open('trie.p', 'wb'))

for query in queries:
    print query
    if query in known_words:
        print "**KNOWN WORD**"
    else:
        res = trie.query(query)
        for key in res:
            print key, res[key]
