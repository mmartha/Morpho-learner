#import relevant modules
import urllib2
from urllib2 import urlopen
import cookielib
from cookielib import CookieJar
import re


# Build opener and change header so we don't look like a bot
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent','Mozilla5.0')]

def getContent(url):
	sourceCode = opener.open(url).read()
	# Select everything marked as paragraph text
	pattern = re.compile(r'<p>(.*)</p>')
	# findall returns a list, select first element which is a string
	content = " ".join(re.findall(pattern, sourceCode))
	return content

def cleanContent(text):
    # Get rid of <HTML code between pointy brackets>
    htmlcode = re.compile(r'<[^>]*>')
    newtext = re.sub(htmlcode, "", text)
    # Get rid of Wikipedia style references e.g. [184]
    references = re.compile(r'\[\d+\]')
    newtext = re.sub(references, '', newtext)
    # Get rid of $#180; code - up to 4 symbols between & and ;
    andhearts = re.compile(r'\&.{,4}\;')
    newtext = re.sub(andhearts, '', newtext)
    # Get rid of numbers
    numbers = re.compile(r'\d+')
    newtext = re.sub(numbers, '', newtext)
    return newtext


def getParagraphs(text):
    '''Find all sentences using Regex and join them together to make 
    paragraphs. Match made with English in mind, update for other languages.
    '''
    pattern = re.compile(r'(.*\b.?(?<!Mr|Dr|Jr|Sr)(?<!Mrs|Drs)(?<![A-Z])\.\s(?![a-z]))')
    paragraphs = re.findall(pattern, text)
    return "".join(paragraphs)

def getDictionary(text):
    ''' Find all word breaks marked with spaces and returns a dictionary of each
        unique word in the article with raw frequency. Also returns an int of 
        total words (wordcount)
    '''
    words = {}
    word = re.compile(r'(?!\d)\b(\S+)\b')
    foundWords = re.findall(word, text)
    for w in foundWords:
        w = w.lower()
        if w not in words.keys():
            words[w] = 1
        else:
            words[w] += 1
    wordcount = sum(words.values())
    return words, wordcount

def get_dataset(link):
    content = cleanContent(getContent(link))
    word_dict, wordcount = getDictionary(getParagraphs(content))
    return word_dict.keys(), wordcount
