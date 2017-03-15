#!/usr/bin/env python
# encoding: utf-8

# (c) Wiltrud Kessler, 7.12.11

#  This code is distributed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported license
#  [http://creativecommons.org/licenses/by-nc-sa/3.0/]

#  Please cite:
#  Wiltrud Kessler and Hinrich Schütze (2012)
#  Classification of Inconsistent Sentiment Words Using Syntactic Constructions.
#  In Proceedings of the 24th International Conference on Computational Linguistics (COLING 2012), Mumbai, India, 10.-14. December 2012, pages 569-578.

"""
Read the XML files in format
(Branavan, Chen, Eisenstein, Barzilay 2009)

<review>
   <id>20</id>
   <title>&quot;Entry Level&quot;</title>
   <date>2006/8/25</date>
   <feature_ranks>
      <feature>Battery Life</feature><rank>5.0</rank>
      <feature>Portability</feature><rank>4.0</rank>
      <feature>Clarity</feature><rank>5.0</rank>
      <feature>Durability</feature><rank>4.0</rank>
      <feature>Product Rating</feature><rank>5.0</rank>
   </feature_ranks>
   <procons>
      <pro>carl zeiss lens</pro>
      <con>minolta would have attracted more photographers</con>
   </procons>
   <text>
   Using the Sony name will probably give it an "entry level" status. It's a great toy for people who will buy their first DSLR. But dont expect the camera to attract Canon or Nikon enthusiasts.
   </text>
</review>

Extract pros, cons and text and pass it to prosconssentenceextraction.py

The file must be in UTF-8.

"""

import sys
import xml.sax as sax

import prosconssentenceextraction as pcs



class ReviewXMLHandler(sax.handler.ContentHandler):
   """
   SAX XML Content handler for files in format
   (Branavan, Chen, Eisenstein, Barzilay 2009).
   """
   # Take care that everything is unicode
   # -> pretty silly, but needed

   def __init__(self, outputFile, extractSentences, extractKeyphrases): 
      """
      Constructor.
      Set self.extraction for class that does the actual processing
      of sentences.
      """
      print "Output to file " + outputFile
      if extractSentences:
         print "extract annotated sentences from review text"
      if extractKeyphrases:
         print "extract annotated sentences from review keyphrases"         
      self.pros = []
      self.cons = []
      self.numberReviews = False
      self.inReview = False
      self.inPros = False
      self.inCons = False
      self.inText = False
      self.text = unicode("")
      # In this the actual extraction of the sentences happens
      self.extraction = pcs.ProsConsSentenceExtraction(outputFile)
      self.extraction.setWhatToExtract(extractSentences, extractKeyphrases)

   def startElement(self, name, attrs):
      """
      Called at the start of an element.
      """
      # Set flags, reset/update variables
      if name == "review":
         self.pros = []
         self.cons = []
         self.inReview = True
         self.numberReviews  += 1
         self.text = unicode("")
         self.keyphrasetext = unicode("")
      elif name == "pro":
         self.inPros= True
      elif name == "con":
         self.inCons = True
      elif name == "text":
         self.inText = True

   def endElement(self, name):
      """
      Called at the end of an element.
      """
      # Delete flags
      if name == "review": 
         # Have read everything in a review,
         # pass on to further processing.
         self.inReview = False
         content = self.text # Unicode
         self.extraction.extract(self.pros, self.cons, content)
         self.text = unicode("")
      elif name == "pro":
         self.inPros = False
         self.pros.append(self.keyphrasetext) # Unicode
         self.keyphrasetext = unicode("")
      elif name == "con": 
         self.inCons = False
         self.cons.append(self.keyphrasetext) # Unicode
         self.keyphrasetext = unicode("")
      elif name == "text": 
         self.inText = False

   def characters(self, content):
      """
      Called with the contents of an element.
      """
      # Append to corresponding variable,
      # Pros/cons or text
      # Take care that it stays unicode!
      # Don't add empty lines, but otherwise don't do strip() to preserve
      # spaces at the end of a set of characters that is read.
      if content.strip() != "":
         if self.inPros or self.inCons:
            if self.keyphrasetext == "":
               self.keyphrasetext = content
            else:
               self.keyphrasetext = self.keyphrasetext + content
         elif self.inText:
            if self.text == "":
               self.text = content
            else:
               self.text = self.text + content

   def cleanup(self):
      print "Processed " + str(self.numberReviews) + " reviews."
      self.extraction.cleanup()


def getBoolean(v):
   return v.lower() in ("yes", "true", "t", "1")


## MAIN ##

# Get arguments
if len(sys.argv) < 2:
   sys.stderr.write('Usage: sys.argv[0] inputfile outputfile [extract sentences: 0/1] [extract keyphrases: 0/1]\n')
   sys.exit(1)
   
inputFile = sys.argv[1]
outputFile = sys.argv[2]
if len(sys.argv) > 3:
   extractSentences = getBoolean(sys.argv[3])
else: 
   extractSentences = True
if len(sys.argv) > 4:
   extractKeyphrases = getBoolean(sys.argv[4])
else: 
   extractKeyphrases = True

# Just read the file!
handler = ReviewXMLHandler(outputFile, extractSentences, extractKeyphrases)
parser = sax.make_parser() 
parser.setContentHandler(handler)
parser.parse(inputFile)
handler.cleanup()
