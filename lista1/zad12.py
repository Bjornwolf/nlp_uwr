import os
import random
import pickle

def generate_2_uniform(words, file_translator, out_file):
   base_location = "../data/filedb_2gram/word#"
   of = open(out_file, 'wb')
   word = random.choice(file_translator.keys())
   of.write(word + ' ')
   total_words = 1
   while total_words <= words:
      f = open(base_location + str(file_translator[word]), 'rb')
      options = f.readlines()
      if options == []:
         of.write("\nOd nowa!\n")
         word = random.choice(file_translator.keys())
         of.write(word + ' ')
         total_words = 1
         f = open(base_location + str(file_translator[word]), 'rb')
         options = f.readlines()
      n = len(options)
      word = random.choice(options).split(' ')[0]
      of.write(word + ' ')
      total_words += 1
   of.close()

file_translator = pickle.load(open("word_numbers.pkl", 'rb'))

def generate_3_uniform(words, file_translator, out_file):
   base_location = "../data/filedb_3gram"
   prefix = "/word#"
   of = open(out_file, 'wb')
   word1 = random.choice(file_translator.keys())
   of.write(word1 + ' ')
   word2 = random.choice(file_translator.keys())
   of.write(word2 + ' ')
   total_words = 2
   while total_words <= words:
      location = base_location + prefix + str(file_translator[word1]) + prefix + str(file_translator[word2])
      if os.path.isfile(location):
         f = open(location, 'rb')
         options = f.readlines()
      else:
         options = []
      while options == []:
         of.write("\nOd nowa!\n")
         word1 = random.choice(file_translator.keys())
         of.write(word1 + ' ')
         word2 = random.choice(file_translator.keys())
         of.write(word2 + ' ')
         total_words = 2
         location = base_location + prefix + str(file_translator[word1]) + prefix + str(file_translator[word2])
         if os.path.isfile(location):
            f = open(location, 'rb')
            options = f.readlines()
      word1 = word2
      word2 = random.choice(options).split(' ')[0]
      of.write(word2 + ' ')
      total_words += 1
   of.close()

file_translator = pickle.load(open("word_numbers.pkl", 'rb'))
# for i in range(20):
#    generate_2_uniform(50, file_translator, '2gu' + str(i))

for i in range(20):
   generate_3_uniform(50, file_translator, '3gu' + str(i))

'''
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
'''
