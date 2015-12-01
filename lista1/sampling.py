import random
import pickle

def sample_2gram(word, dictionary, dist, totals=None):
    if dist == "uniform":
        return random.choice(dictionary[word])[0]
    elif dist == "proportional":
        options = dictionary[word]
        ch = random.randint(0, totals[word] - 1)
        for w, f in options:
            if ch < f:
                return w
            else:
                ch -= f

def gen_2gram(dictionary, word_limit = 100, dist="uniform", totals=None):
    words = []
    words.append(random.choice(dictionary.keys()))
    total_words = 1
    while total_words < word_limit:
        try:
            words.append(sample_2gram(words[-1], dictionary, dist, totals))
        except KeyError:
            words.append("\nNo choice, start again\n")
            words.append(random.choice(dictionary.keys()))
        total_words += 1
    return ' '.join(words)



dic, totals = pickle.load(open('2gram_from5.pkl', 'rb'))

print "UNIFORM"
for i in range(5):
    print "Sample ", i, ":"
    print gen_2gram(dic)

print "PROPORTIONAL"
for i in range(5):
    print "Sample ", i, ":"
    print gen_2gram(dic, dist = "proportional", totals = totals)
