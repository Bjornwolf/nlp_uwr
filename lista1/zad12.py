import os
import random
import pickle

def get_2():
    if not (os.path.isfile("dict_2.pkl") and os.path.isfile("totals_2.pkl")):
        file_2 = open('../data/2grams', 'r')
        dict_2 = {}
        totals_2 = {}
        for line in file_2:
            tokenised = line[:-1].split(' ')[-3:]
            try:
                dict_2[tokenised[1]].append( (tokenised[2], tokenised[0]) )
                totals_2[tokenised[1]] += int(tokenised[0])
            except KeyError:
                dict_2[tokenised[1]] = [ (tokenised[2], tokenised[0]) ]
                totals_2[tokenised[1]] = int(tokenised[0])

        pickle.dump(dict_2, open("dict_2.pkl", 'wb'))
        pickle.dump(totals_2, open("totals_2.pkl", 'wb'))
    else:
        dict_2 = pickle.load(open("dict_2.pkl", 'rb'))
        totals_2 = pickle.load(open("totals_2.pkl", 'rb'))
    return dict_2, totals_2

def get_3():
    if not (os.path.isfile("dict_3.pkl") and os.path.isfile("totals_3.pkl")):
        file_3 = open('../data/3grams', 'r')
        dict_3 = {}
        totals_3 = {}
        for line in file_3:
            tokenised = line[:-1].split(' ')[-4:]
            try:
                dict_3[(tokenised[1], tokenised[2])].append( (tpokenised[3], tokenised[0]) )
                totals_3[(tokenised[1], tokenised[2])] += int(tokenised[0])
            except KeyError:
                dict_3[(tokenised[1], tokenised[2])] = [ (tokenised[3], tokenised[0]) ]
                totals_3[(tokenised[1], tokenised[2])] = int(tokenised[0])

        pickle.dump(dict_3, open("dict_3.pkl", 'wb'))
        pickle.dump(totals_3, open("totals_3.pkl", 'wb'))
    else:
        dict_3 = pickle.load(open("dict_3.pkl", 'rb'))
        totals_3 = pickle.load(open("totals_3.pkl", 'rb'))
    return dict_3, totals_3

def generate_2(steps_no, dictionary, total_numbers, random_version="uniform"):
    word = random.choice(dictionary.keys())
    print word + " ",
    words_written = 1
    while words_written <= steps_no:
        options = dictionary[word]
        if options is None:
            print "\nOd nowa!"
            word = random.choice(dictionary.keys())
            print word + " ",
            words_written = 1
            options = dictionary[word]
        n = total_numbers[word]
        if random_version == "uniform":
            (word, _) = random.choice(options)
        elif random_version == "proportional":
            sample = random.randint(1, n)
            i = 0
            while sample > options[i][1]:
                sample -= options[i][1]
                i += 1
            word = options[i][0]
        else:
            raise NotImplemented

        print word + " ",
        words_written += 1

def generate_3(steps_no, dictionary, total_numbers, random_version="uniform"):
    (word1, word2) = random.choice(dictionary.keys())
    print word1 + " " + word2 + " ",
    words_written = 2
    while words_written <= steps_no:
        options = dictionary[word]
        if options is None:
            print "\nOd nowa!"
            (word1, word2) = random.choice(dictionary.keys())
            print word1 + " " + word2 + " ",
            words_written = 2
            options = dictionary[word]
        n = total_numbers[word]
        if random_version == "uniform":
            (word, _) = random.choice(options)
        elif random_version == "proportional":
            sample = random.randint(1, n)
            i = 0
            while sample > options[i][1]:
                sample -= options[i][1]
                i += 1
            word = options[i][0]
        else:
            raise NotImplemented

        print word + " ",
        words_written += 1

print "Laduje model 2-gramowy..."
dict_2, totals_2 = get_2()
print "Zaladowalem model 2-gramowy."

print "2-gram, jednostajnie"
generate_2(2000, dict_2, totals_2)

print "2-gram, proporcjonalnie"
generate_2(2000, dict_2, totals_2, "proportional")

print "Laduje model 3-gramowy..."
dict_3, totals_3 = get_3()
print "Zaladowalem model 3-gramowy."

print "3-gram, jednostajnie"
generate_3(2000, dict_3, totals_3)

print "3-gram, proporcjonalnie"
generate_3(2000, dict_3, totals_3, "proportional")
