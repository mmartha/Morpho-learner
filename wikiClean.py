import re

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