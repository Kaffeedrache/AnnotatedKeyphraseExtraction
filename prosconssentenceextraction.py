#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 9.12.11

#  This code is distributed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported license
#  [http://creativecommons.org/licenses/by-nc-sa/3.0/]

#  Please cite:
#  Wiltrud Kessler and Hinrich Schütze (2012)
#  Classification of Inconsistent Sentiment Words Using Syntactic Constructions.
#  In Proceedings of the 24th International Conference on Computational Linguistics (COLING 2012), Mumbai, India, 10.-14. December 2012, pages 569-578.

"""
Use pros and cons to automatically label sentences with
polarity information.
Assumption: A sentence that contains an aspect mentioned
in a pro (con) is positive (negative).

All string parameters should be passed as unicode and they
are written to a file in UTF-8.
"""

import nltk
import nltk.data

import dictionaryWWH


class ProsConsSentenceExtraction:
   """
   Use pros and cons to automatically label sentences with
   polarity information.
   Assumption: A sentence that contains an aspect mentioned
   in a pro (con) is positive (negative).
   """
   
   labelPositive = "1"
   labelNegative = "-1"
   maxLength = 3
   noSentences = 0
   extractionLimit = 200
   maxTokens = 100


   # Set this to false if you don't want to print it out
   extractSentences = True
   extractKeyphrases = True
   
   
   
   def __init__(self, outputfile):
      """
      Initialize sentence splitter.
      Open output file.
      Create sentiment words dictionary.
      """
      # Load sentence splitting of content
      self.sentenceSplitter = nltk.data.load('nltk:tokenizers/punkt/english.pickle')

      # Open output file
      self.outputFileHandle = open(outputfile, "w")
      
      # Create sentiment words dictianary
      dictfile = "../../Data/subjclueslen1-HLTEMNLP05.tff"
      posExcludeList = [] # don't exclude anything
      strongsubj = False # include strong and weak subjective
      self.dictionaryPositive = dictionaryWWH.makeDictionaryPOS (dictfile, self.labelPositive,strongsubj,posExcludeList)
      self.dictionaryNegative = dictionaryWWH.makeDictionaryPOS (dictfile, self.labelNegative,strongsubj,posExcludeList)

   
   def setWhatToExtract(self, extractSentences, extractKeyphrases):
      """
      Which part to extract sentences (argument 1) or keyphrasese (argument 2).
      Defaults both to True if nothing is set.
      """
      self.extractSentences = extractSentences
      self.extractKeyphrases = extractKeyphrases


   def write (self, label, tokenlist, flag):
      """
      Write sentence and label to file.
      """
      # Flag is a hack, set to true if it should be really written.
      # Allows to distinguish between keyphrase extraction and
      # content sentences -> just for debugging purposes.
      if flag:
         sentence = ""
         # The parser has a problem with sentences that are too long,
         # therefor sentences are just cut off after a certain number of tokens.
         # This is a bit of a hack, because it might be, that the keyword
         # where the label comes from is actually in a later part of the sentence
         # and is cut off.
         for token in tokenlist[:self.maxTokens]:
            sentence = sentence + " " + token
         sentence = sentence.strip()
         content = sentence.encode('utf-8') # UTF-8
         self.outputFileHandle.write(label + ":\t" + content + "\n")
         self.noSentences = self.noSentences + 1 # needed for cleanup
   
   
   def addToKeyphraseDict(self, keyphraseDictionary, keyphraselist, label):
      """
      Create a dictionary from a keyphrase list.
      Key = keyphrase as string, tokens separated with spaces.
      Value = label to assign the sentence
      """
      for keyphrase in keyphraselist:
         tokens = nltk.word_tokenize(keyphrase)
         if len(tokens) > self.maxLength:
            self.write(label, tokens, self.extractKeyphrases) 
         else:
            for token in tokens:
               if self.dictionaryPositive.get(token) != None:
                  tokens.remove(token)
               elif self.dictionaryNegative.get(token) != None:
                  tokens.remove(token)
            if len(tokens)>0:
               key = ""
               for token in tokens:
                  key = key + " " + token
               key = key.strip()
               keyphraseDictionary[key] = label

   
   def checkDict (self, keyphraseDictionary, token, tokens):
      """
      Check if token in dictionary.
      If yes, write to file.
      """
      label = keyphraseDictionary.get(token)
      if label != None:
         self.write (label,  tokens, self.extractSentences)  
         return True
      return False

   
   def extract (self, proslist, conslist, content):
      """
      Use pros and cons to automatically label sentences with
      polarity information.
      Assumption: A sentence that contains an aspect mentioned
      in a pro (con) is positive (negative).
      """
      
      # Create a dictionary from pros and cons lists.
      # positive label if it is a pro, negative if it is a con.
      keyphraseDictionary = {}
      self.addToKeyphraseDict(keyphraseDictionary, proslist, self.labelPositive)
      self.addToKeyphraseDict(keyphraseDictionary, conslist, self.labelNegative)
      
      # If there are no keyphrases, nothing can be found in content -> give up
      if not keyphraseDictionary:
         return
         
      # Split sentences in content
      # Tokenize sentences.
      # Check all tokens for ocurrence in dictionary.
      # Assumption: A sentence that contains an aspect mentioned
      # in a pro (con) is positive (negative).
      # Assign the sentence the corresponding label.
      # TODO: Remove HTML tags
      sents = self.sentenceSplitter.tokenize(content)
      for sentence in sents:
         tokens = nltk.word_tokenize(sentence)
         
         # HACK: consider up to three tokens for keyphrase
         previousToken = ""
         prepreviousToken = ""
         for token in tokens:
            check = self.checkDict(keyphraseDictionary, token, tokens)
            if previousToken != "" and not check:
               check = self.checkDict(keyphraseDictionary, previousToken + " " + token, tokens)
            if prepreviousToken != "" and not check:
               check = self.checkDict(keyphraseDictionary, prepreviousToken + " " + previousToken + " " + token, tokens)
            if check: # Extract each sentence only once
               break
            prepreviousToken = previousToken
            previousToken = token
            


   def cleanup(self):
      """ 
      Cleanup - close output file.
      """
      print "Written " + str(self.noSentences) + " sentences."
      try:
         self.outputFileHandle.close()
      except AttributeError:
         # ignore
         pass


