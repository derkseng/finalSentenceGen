from collections import Counter
import random
import requests
import re
import nltk
import csv

dWord = []
unknown =[]
input_text = []
urlNum = []
count = 15000

# I was hoping to add more files to work with and that is why I added a counter to this, but ended up using only the first page
url = 'http://lacity.granicus.com/TranscriptViewer.php?view_id=130&clip_id='
while (count < 17000):     
    count = count + 1
    strCount = str(count)
    newStrUrl = url + strCount
    urlNum.append(newStrUrl)

readWords = requests.get(urlNum[0])
dirtyText = readWords.text

# cleans out the set of symbols and punctuation which I could have done in the remove_tag function but... time and know how?
def clean_word(word):
    for ch in ".;,[]\t\n°()\"'“”":
        word = word.replace(ch, "")
    return word.lower()

# a little regex to strip out the tags and css
def remove_tags(tag):
    p = re.compile(r'<.*?>+' '|{.*?}')
    tag = p.sub('', tag)
    
    return tag
        
input_text = remove_tags(dirtyText)

# set dictionary from text file
with open('assets/DictionaryNW.txt', mode='r') as infile:
    reader = csv.reader(infile)
    myWords = {k:v for k, v in reader}

# words are the relation between a word and the next word
prev_word = None
pairs = []
for word in input_text.split():
    type = myWords.get(word,"unknown") 
    if (type == 'DT') and (word not in dWord):
        dWord.append(word)
    else:
        unknown.append(word)
    end_word = word[-1] == "."
    word = clean_word(word)
    if len(word) == 0:
        continue
    if prev_word is not None:
        pair = (prev_word, word, end_word)
        pairs.append(pair)
    prev_word = word

word_count = len(pairs) + 1

# count the frequency a word appears and build a tuple of words based on the probablity of the previous word and the
# next word appearing in the original text.
count = Counter(pairs)
network = {}
for item, times in count.items():
    prev_word, word, end_word = item
    if prev_word not in network:
        network[prev_word] = {}
    next_words = network[prev_word]
    next_words[(word, end_word)] = times/word_count

# build the sentence with a max word count of 30 words
m = random.choice(dWord)
word = m
sentence = [word]
while len(sentence) < 30:
    next_values = network[word]
    next_words = list(next_values.keys())
    next_item = random.choices(next_words, next_values.values())[0]
    word, is_end = next_item
    sentence.append(word)

    if is_end:
        break
newSentence = " ".join(sentence) + "."
mySentence = newSentence.capitalize()
print(mySentence)

