from itertools import combinations
import re


def getAffixDict(words, A = 5, B = 1):
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
                # for Turkish use A = 10
                # for English use A = 2-5
                # for Swahili use A ~ 5
                # for Zulu use A ~ 5
                affixDict[a] *= (1 - (1/(A*float(len(a)**B))))
    return affixDict


def findAB(data, solutions):
    '''Attempt to implement 'Supervised Learning' to find best parameters, given 
    a solution set.
    '''
    X = False
    min_score = (999999, (0,0))
    for a in range(1,20):
        for b in range(1,5):
            score = 0
            mylist = [x for (x, y) in listByMax(getAffixDict(data, a, b))]
            for i in solutions.keys():
                for morpheme in solutions[i]:
                    k = mylist.index(morpheme)
                    score += (k-i)
            if score < min_score[0]:
                min_score = (score, (a,b))
    return min_score[1]
    

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
    '''Returns a score for a list of segments which are the possible
    morphemes of a word. Score is the sum of each possible morpheme asstored 
    in the 'scoreDict'
    '''
    score = 0
    for part in segmentationList:
        if len(part) > 0:
            score += scoreDict[part]
    if len(segmentationList) > 0:
        score /= len(segmentationList)
    return score


def listByMax(mydict, stopAt = None):
    '''Returns the key, value pairs in order from highest value to lowest
    value. If stopAt has a value, only prints that many results.
    '''
    returnlist = []
    copy = mydict
    if stopAt == None:
        stopAt = len(mydict.keys())
    # 'printed' to keep track of how many top items have been found
    printed = 0
    while len(copy.values()) > 0:
        for key in copy.keys():
            if copy[key] == max(copy.values()):
                returnlist.append((key, copy[key]))
                printed += 1
                del copy[key]
            if printed == stopAt:
                break
        if printed == stopAt:
            break
    return returnlist

def printByMax(mydict, stopAt = None):
    # Prints a dictionary sorted by maximum value
    for x, y in listByMax(mydict, stopAt = None):
        print x, y




