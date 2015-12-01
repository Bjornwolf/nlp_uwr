import random
import pickle

def sample_3gram(key, dictionary, dist, totals=None):
    if dist == "uniform":
        return random.choice(dictionary[key])[0]
    elif dist == "proportional":
        options = dictionary[key]
        ch = random.randint(0, totals[key] - 1)
        for w, f in options:
            if ch < f:
                return w
            else:
                ch -= f

def gen_3gram(dictionary, word_limit = 100, dist="uniform", totals=None):
    words = []
    (w1, w2) = random.choice(dictionary.keys())
    words.append(w1)
    words.append(w2)
    total_words = 2
    while total_words < word_limit:
        try:
            words.append(sample_3gram( (words[-2], words[-1]), dictionary, dist, totals))
        except KeyError:
            words.append("\nNo choice, start again\n")
            (w1, w2) = random.choice(dictionary.keys())
            words.append(w1)
            words.append(w2)
        total_words += 2
    return ' '.join(words)



dic, totals = pickle.load(open('3gram_from5.pkl', 'rb'))

print "UNIFORM"
for i in range(5):
    print "Sample ", i, ":"
    print gen_3gram(dic)

print "PROPORTIONAL"
for i in range(5):
    print "Sample ", i, ":"
    print gen_3gram(dic, dist = "proportional", totals = totals)
