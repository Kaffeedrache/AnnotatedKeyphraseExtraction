# Annotated Keyphrase Extraction

Code for creating the annotated sentences that were used in the paper (Kessler and Schütze, 2012).

__WARNING__: This is research code, it was not written with anybody else in mind nor with the goal of applying it "in real life". So it is hacky and may not be usable at all.


## Content of this repository

* `README.md`: this file.
* `prosconsXMLreader.py`: The main progamm that parses the XML file.
* `prosconssentenceextraction.py`: Called by `prosconsXMLreader.py` to extract automatically annotated sentences from the XML.
* `dictionaryWWH.py`: Called by `prosconssentenceextraction.py` to read sentiment words from the MPQA dictionary.

You will need NLTK and the [MPQA Subjectivity Lexicon](http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/).


## Usage

You need an XML file in the format specified below. You can use the optional parameters to extract annotated sentences from the keyphrases (pros and cons), from the review text or both.

    python prosconsXMLreader.py <inputfile> <outputfile> <[extract sentences: 0/1]> <[extract keyphrases: 0/1]>



## XML file format

Read the XML files in format from [(Branavan, Chen, Eisenstein, Barzilay 2009)](http://groups.csail.mit.edu/rbg/code/precis/). 

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

The file must be in UTF-8.



## Licence and References

(c) Wiltrud Kessler

This code is distributed under a Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported license
[http://creativecommons.org/licenses/by-nc-sa/3.0/](http://creativecommons.org/licenses/by-nc-sa/3.0/)

Please cite:
Wiltrud Kessler and Hinrich Schütze (2012)
Classification of Inconsistent Sentiment Words Using Syntactic Constructions.
In Proceedings of the 24th International Conference on Computational Linguistics (COLING 2012), Mumbai, India, 10.-14. December 2012, pages 569-578.


