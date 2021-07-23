from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string
from collections import Counter

def cleanSentence(sentence):
    sentence = sentence.split(' ')
    sentence = [word.strip(string.punctuation+string.whitespace) for word in sentence]
    sentence = [word for word in sentence if len(word) > 1 or (word.lower() == 'a' or word.lower() == 'i')]
    return sentence

def cleanInput(content):
    content = content.upper()
    content = re.sub('\n', ' ', content)
    content = bytes(content, 'UTF-8')
    content = content.decode('ascii', 'ignore')
    sentences = content.split('. ')
    return [cleanSentence(sentence) for sentence in sentences]

def getNgramsFromSentence(content, n):
    output = []
    for i in range(len(content)-n+1):
        output.append(content[i:i+n])
    return output
  
 
def getNgrams(content, n):
  content = cleanInput(content)
  ngrams = Counter()
  ngrams_list = []
  for sentence in content:
    newNgrams = [' '.join(ngram) for ngram in getNgramsFromSentence(sentence, n)]
    ngrams_list.extend(newNgrams)
    ngrams.update(newNgrams)
  return(ngrams)


content = str(
      urlopen('https://www.yelp.com/search?find_desc=Delivery&find_loc=San+Francisco%2C+CA').read(),
              'utf-8')
ngrams = getNgrams(content, 3)
print(ngrams)

def isCommon(ngram):
    commonWords = ['  rating','price',]
    for word in ngram:
        if word in commonWords:
            return True
    return False

def getNgramsFromSentence(content, n):
    output = []
    for i in range(len(content)-n+1):
        if not isCommon(content[i:i+n]):
            output.append(content[i:i+n])
    return output

ngrams = getNgrams(content, 3)
print(ngrams)

def getFirstSentenceContaining(ngram, content):
    #print(ngram)
    sentences = content.upper().split(". ")
    for sentence in sentences: 
        if ngram in sentence:
            return sentence+'\n'
    return ""
  
  from urllib.request import urlopen
from random import randint

def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum

def retrieveRandomWord(wordList):
    randIndex = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word

def buildWordDict(text):
    # Remove newlines and quotes
    text = text.replace('\n', ' ');
    text = text.replace('"', '');
punctuation = [',','.',';',':']
    for symbol in punctuation:
        text = text.replace(symbol, ' {} '.format(symbol));

    words = text.split(' ')
    # Filter out empty words
    words = [word for word in words if word != '']

    wordDict = {}
    for i in range(1, len(words)):
        if words[i-1] not in wordDict:
                # Create a new dictionary for this word
            wordDict[words[i-1]] = {}
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
        wordDict[words[i-1]][words[i]] += 1
    return wordDict

text = str(urlopen('https://www.yelp.com/search?find_desc=Delivery&find_loc=San+Francisco%2C+CA')
          .read(), 'utf-8')
wordDict = buildWordDict(text)
#Generate a Markov chain of length 100
length = 100
chain = ['I']
for i in range(0, length):
    newWord = retrieveRandomWord(wordDict[chain[-1]])
    chain.append(newWord)

print(' '.join(chain))

!pip install pymysql
import pymysql

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd='root', db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute('USE yelp')

def getUrl(pageId):
    cur.execute('SELECT url FROM review_name WHERE id = %s', (int(pageId)))
    return cur.fetchone()[0]

def getLinks(fromPageId):
    cur.execute('SELECT toPageId FROM links WHERE location = %s', (string(fromPageId)))
    if cur.rowcount == 0:
        return []
    return [x[0] for x in cur.fetchall()]

def searchBreadth(targetPageId, paths=[[1]]):
    newPaths = []
    for path in paths:
        links = getLinks(path[-1])
        for link in links:
            if link == targetPageId:
                return path + [link]
            else:
                newPaths.append(path+[link])
    return searchBreadth(targetPageId, newPaths)
                
nodes = getLinks(1)
targetPageId = 28624
pageIds = searchBreadth(targetPageId)
for pageId in pageIds:
    print(getUrl(pageId))
    
 !pip install -U spacy
!python -m spacy download en_core_web_sm
import spacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Process whole documents
text = (pageIds)
doc = nlp(text)

# Analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)
