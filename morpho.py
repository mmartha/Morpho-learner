from itertools import combinations

def getDictionary(text):
    '''Find all word breaks marked with spaces and returns a list of each
    unique word in the article. Also returns an int of total words (wordcount)
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
    return words.keys(), wordcount


def getAffixDict(words):
    '''Takes the words from a list and finds all possible morphemes from
    each word. Then all morphemes from all words are tallyed. Finally, each
    morpheme count is scaled by a constant so that shorter morphemes are
    decreased, since they are statistically more likely to be random.
    '''
    affixDict = {}
    for word in words:
        breakups = set()
        for i in range(len(word)):
            for j in range(i, len(word)+1):
                breakups.add(word[i:j])
        for b in breakups:
            if b in affixDict.keys():
                affixDict[b] += 1
            else:
                affixDict[b] = 1
        for a in affixDict.keys():
            if len(a) < 1:
                del affixDict[a]
            else:
                # for Turkish use X = 10
                # for English use X = 2-5
                # for Swahili use X ~ 5
                # for Zulu use X ~ 5
                X = 4.9
                affixDict[a] *= (1 - (1/(X*float(len(a)))))
    return affixDict


def generatePowerSet(number):
    '''Returns the power set of the set of integers from 1 to number.'''
    powerSet = []
    for i in range(number+1):
        q = combinations(range(1, number+1), i)
        for p in q:
            powerSet.append(list(p))
    return powerSet


def possibleSegments(word):
    '''Returns a list. Each item in the list is a list of segments, which when 
    concatenated sequentially, should be equivalent to the original word.
    '''
    segments = []
    for split in generatePowerSet(len(word)-1):
        # segmentation will be a list of each part, which together make 
        # the whole word, eg ["to", "g", "ethe", "r"]
        segmentation = []
        # Generate a new list containing 0 and len(word) as the first and
        # final indices for the first and final splits
        newlist = [0]
        newlist.extend(split)
        newlist.append(len(word))
        for s in range(len(newlist)-1):
            segmentation.append(word[newlist[s]:newlist[s+1]])
        segments.append(segmentation)
    return segments


def scoreSegmentation(segmentationList, scoreDict):
    score = 0
    for part in segmentationList:
        if len(part) > 0:
            score += scoreDict[part]
    if len(segmentationList) > 0:
        score /= len(segmentationList)
    return score


def printByMax(dict, stopAt = None):
    '''Prints the key, value pairs in order from highest value to lowest
    value. If stopAt has a value, only prints that many results.
    '''
    copy = dict
    if stopAt == None:
        stopAt = len(dict.keys())
    printed = 0
    while len(copy.values()) > 0:
        for key in copy.keys():
            if copy[key] == max(copy.values()):
                print key, copy[key]
                printed += 1
                del copy[key]
            if printed == stopAt:
                break
        if printed == stopAt:
            break



