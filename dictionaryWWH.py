#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 11.10.11

#  This code is distributed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported license
#  [http://creativecommons.org/licenses/by-nc-sa/3.0/]

#  Please cite:
#  Wiltrud Kessler and Hinrich Schütze (2012)
#  Classification of Inconsistent Sentiment Words Using Syntactic Constructions.
#  In Proceedings of the 24th International Conference on Computational Linguistics (COLING 2012), Mumbai, India, 10.-14. December 2012, pages 569-578.


"""
Constructs a python dictionary from the MPQA dictionary file.
See Wilson, Wiebe, Hofman (2005).
"""



def makeDictionary (dictionary_file, label):
   """
   Insert all words from the file into the dictionary with sentiment "label",
   key is the word, value is 0 in all cases (useful only to check if a word
   is in the dictionary or not).
   Expected format: One word per line, word and sentiment separated with ;
   Words are not normalized.
   [this is a simplified version of the original file]
   """
   mydictionary = {}
   input_file = open(dictionary_file)
   for line in input_file:
      line = line.strip()
      parts = line.split(';')
      if parts[1]==label:
         mydictionary[parts[0]] = 0
   return mydictionary


def makeDictionaryPOS (dictionaryFile, label, onlyStrongSubj = False, notPOS = []):
   """
   Insert all words from the file into the dictionary with sentiment "label",
   key is the word, value is the part of speech.
   Expected format: Wilson, Wiebe, Hofman (2005)
   type=strongsubj len=1 word1=acrimoniously pos1=anypos stemmed1=n priorpolarity=negative
   type=weaksubj len=1 word1=youthful pos1=adj stemmed1=n priorpolarity=positive
   Words are not normalized.
   There are errors in the file, sometimes a "m" ocurrs after "stemmed1", sometimes "len" ocurrs twice, these errors are handled.
   @param dictionaryFile The file from which the dictionary will be read
   @param label The label the words should have (only words with this label
         will be inserted into the dictionary)
   @param onlyStrongSubj Extract all words or only those with 'strongSubj' set.
   @param notPOS Exclude POS tags from this list.
   """
   mydictionary = {}
   stronsubjlabel = "strongsubj"
   
   # Change internal labels to WWH labels
   mylabel = ""
   if label=="-1":
      mylabel = "negative"
   if label=="1":
      mylabel = "positive"
   
   # Read in dictionary
   input_file = open(dictionaryFile)
   for line in input_file:
      line = line.strip()
      parts = line.split(' ')
      
      # Get polarity, word and POS

      for part in parts:
         subparts = part.split("=")
         if subparts[0] == "word1":
            word = subparts[1]
         elif subparts[0] == "priorpolarity":
            polarity = subparts[1]
         elif subparts[0] == "pos1":
            pos = subparts[1]
            # Convert names to our internal names
            if pos == "noun":
               pos = "N"
            elif pos == "adj":
               pos = "ADJ"
            elif pos == "verb":
               pos = "V"
            elif pos == "adverb":
               pos = "ADV"
            elif pos == "anypos":
               pos = "*"
               
         elif subparts[0] == "type":
            type=subparts[1]
      
      # If the flag "extract only strong subjective words" is set,
      # ignore word if its type is not "strongsubj".
      if onlyStrongSubj and type != stronsubjlabel:
         continue
      
      # If the word has a POS on the exclude list, ignore word
      if pos in notPOS:
         continue
      
      # Check if it matches
      # the polarity we want
      if polarity==mylabel:
         
         # Check if word is already in dictionary
         occurrences = mydictionary.get(word)
         if occurrences != None: 
            #  word in candidates -> add POS to list
            occurrences.append(pos) # reference -> already added to mydict
         else: # not in candidates -> set POS
            mydictionary[word] = [pos]
            
   return mydictionary

