import os
import random
import pickle

c = input()
if c % 2 == 0:
   file_2 = open('../data/2grams', 'r')
   os.mkdir('../data/filedb_2gram')
   
   file_translator = {}
   next_word = 1
   
   for line in file_2:
      tokenised = line[:-1].split(' ')[-3:]
      try:
         no = file_translator[tokenised[1]]
      except KeyError:
         file_translator[tokenised[1]] = next_word
         no = next_word
         next_word += 1 
      fname = '../data/filedb_2gram/word#' + str(no)
      with open(fname, 'a') as my_file:
         my_file.write(tokenised[2] + ' ' + tokenised[0] + '\n')
   pickle.dump(file_translator, open("word_numbers.pkl", 'wb'))

elif c % 3 == 0:
   file_3 = open('../data/3grams', 'r')
   os.mkdir('../data/filedb_3gram')
   
   file_translator = pickle.load(open("word_numbers.pkl", 'rb'))
   next_word = len(file_translator) + 1
   
   for line in file_3:
      tokenised = line[:-1].split(' ')[-4:]
      try:
         no = file_translator[tokenised[1]]
      except KeyError:
         file_translator[tokenised[1]] = next_word
         no = next_word
         next_word += 1 
      dirname = '../data/filedb_3gram/word#' + str(no)
      if not os.path.isdir(dirname):
         os.mkdir(dirname)
      try:
         no = file_translator[tokenised[2]]
      except KeyError:
         file_translator[tokenised[2]] = next_word
         no = next_word
         next_word += 1 
      fname = dirname + '/word#' + str(no)
      with open(fname, 'a') as my_file:
         my_file.write(tokenised[3] + ' ' + tokenised[0] + '\n')
   pickle.dump(file_translator, open("word_numbers.pkl", 'wb'))

