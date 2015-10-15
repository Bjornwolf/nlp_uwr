import os
import random
import pickle

def build_bigram():
   file_2 = open('../data/2grams', 'r')
   dict_2 = {}
   totals_2 = {}
   for line in file_2:
      tokenised = line[:-1].split(' ')[-3:]
      number = int(tokenised[0])
      if number < 5:
         pickle.dump( (dict_2, totals_2), open("2gram_from5.pkl", 'wb'))
         return
      word_1 = tokenised[1]
      word_2 = tokenised[2]
      try:
         dict_2[word_1].append( (word_2, number) )
         totals_2[word_1] += number
      except KeyError:
         dict_2[word_1] = [ (word_2, number) ]
         totals_2[word_1] = number

def build_trigram():
   file_3 = open('../data/3grams', 'r')
   dict_3 = {}
   totals_3 = {}
   for line in file_3:
      tokenised = line[:-1].split(' ')[-4:]
      number = int(tokenised[0])
      if number < 5:
         pickle.dump( (dict_3, totals_3), open("3gram_from5.pkl", 'wb'))
         return
      word_1 = tokenised[1]
      word_2 = tokenised[2]
      word_3 = tokenised[3]
      try:
         dict_3[(word_1, word_2)].append( (word_3, number) )
         totals_3[(word_1, word_2)] += number
      except KeyError:
         dict_3[(word_1, word_2)] = [ (word_3, number) ]
         totals_3[(word_1, word_2)] = number


print "Building bigrams"
build_bigram()

print "Building trigrams"
build_trigram() 
