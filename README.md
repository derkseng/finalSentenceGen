# finalSentenceGen
Sentence Generator
This project generates a sentence based on probability of words appearing frequently together starting with a randomly selected word. The python file requires the following modules be installed:
import Counter which uses collections,
import random,
import requests,
import re,
import nltk,
import csv. 

Also, it uses a dictionary set of words to check against the parts of speech and catagorize the articles (start word).
This is likely too large a module just for the 15 words in the set however, the intention is to build these out to collect the other parts of speech and use them in place of the middle 'word'(s). Earlier versions of this included the other parts of speech lists.
Connection to the internet is also required to pull text from the LA city council meeting transcripts.
