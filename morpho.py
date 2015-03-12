from itertools import combinations
import re

import Graph


def formatWord(word):
    ''' This takes a string and adds word beginning and end symbols.
        * is word beginning and # is word end
    '''
    return "*"+word+"#"


def getTotalLetters(dataset):
    ''' Returns total number of letters in data set and the number of distinct
        letters.
    '''
    letter_count = 0
    distinct_letters = set()
    for word in dataset:
        for letter in word:
            letter_count+=1
            distinct_letters.add(letter)
    return letter_count, len(distinct_letters)


def possibleMorphemes(word):
    ''' Finds all possible morphemes for a word. Stored in a set, aka a list 
        with no repeating entries.
    '''
    breakups = set()
    # Add beginning and end of word symbols
    word = formatWord(word)
    # Create dictionary of all possible segments
    for i in range(len(word)):
        for j in range(i, len(word)+1):
            breakups.add(word[i:j])
    return breakups
    

def generatePowerSet(number):
    ''' Returns the power set of the set of integers from 1 to number.
        Used to divide a word into every possible segmentation.
    '''
    powerSet = []
    for i in range(number+1):
        # itertools.combinations
        q = combinations(range(1, number+1), i)
        for p in q:
            powerSet.append(list(p))
    return powerSet


def possibleSegments(word, mode="Normal"):
    ''' Returns a list. Each item in the list is a list of segments, which when 
        concatenated sequentially, should be equivalent to the original word.
    '''
    if mode == "Normal":
        # In 'scoring' mode, segment word without beginning and end symbols
        word = formatWord(word)
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
        # create a segmentation of word between indices x and y, where x and y
        # are all adjacent entries in newlist
        for s in range(len(newlist)-1):
            segmentation.append(word[newlist[s]:newlist[s+1]])
        segments.append(segmentation)
    # return final list of segmentation lists
    return segments


def countMorphemes(dataset):
    ''' Produces a dictionary of all observed morphemes as keys. Values are observed
        frequency of morpheme with correction for shorter morphemes being more likely
        to occur by pure chance
    '''
    freq_dict = {}
    total_letters, distinct_letters = getTotalLetters(dataset)
    # For each word, find all possible morphemes
    for word in dataset:
        morphemes = possibleMorphemes(word)
        for m in morphemes:
            if m not in freq_dict.keys():
                freq_dict[m] = 1
            else: freq_dict[m] += 1
    for m in freq_dict.keys():
        mcount = freq_dict[m]
        freq_dict[m] = correct_for_length(m, mcount, total_letters, distinct_letters)
    return freq_dict


def correct_for_length(m, mcount, total_letters, distinct_letters):
    # Expected frequency for m is probability of occurence (based just on number 
    # of letters in m) multiplied by total size of dataset (in letters)
    # Returns a new value for mcount, adjusted for length of m
    A = distinct_letters
    expected = float(total_letters)/(A**len(m))
    actual = mcount
    if expected > 0.1:
        return round((actual-expected)/expected)
    elif expected != 0:
        return round((actual-expected)/0.1)
    # expected frequency should never be 0 in float, unless error
    else: raise ZeroDivisionError("String has expected value 0: "+str(m))


def createGraph(dataset):
    ''' Takes a list of words, 'dataset' and returns a graph object with possible
        morphemes as nodes, and weighted edges between each possible morpheme.
    '''
    letter_count, distinct_letters = getTotalLetters(dataset)
    possible_morphemes = set()
    for word in dataset:
        for x in possibleMorphemes(word):
            possible_morphemes.add(x) 
    graph = Graph.Directed_Graph(possible_morphemes)
    for word in dataset:
        segments_list = possibleSegments(word)
        for segmentation in segments_list:
            for i in range(len(segmentation)-1):
                graph.add_edge(segmentation[i],segmentation[i+1])
    graph = weightEdges(graph, letter_count, distinct_letters)
    # Also weight each edge by the weight of each node it connects
    node_dict = countMorphemes(dataset)
    edge_dict = graph.edges()
    for edge in graph.edges().keys():
        start_value = edge_dict[edge]
        value = start_value*node_dict[edge[0]]*node_dict[edge[1]]
        graph.define_edge(edge[0], edge[1], value)
    return graph

def weightEdges(graph, letter_count, distinct_letters):
    ''' Longer sequences of letters should receive higher weight since they are 
        less likely occur by pure chance.
    '''
    for edge in graph.edges().keys():
        value = correct_for_length(edge[1],graph.edges()[edge], letter_count, distinct_letters)
        graph.define_edge(edge[0], edge[1], value)
    return graph


def scoreSegmentation(word, graph):
    ''' Returns the highest score from a list of segments which are the possible
        morphemes of a word. Score is the sum of each edge between two possible
        morphemes in 'graph'.
    '''
    segmentations = possibleSegments(word, "scoring")
    best_choice = (None,0)
    edges = graph.edges()
    for possibility in segmentations:
        score = 0
        for i in range(len(possibility)-1):
            if (possibility[i], possibility[i+1]) in edges.keys():
                score += edges[(possibility[i], possibility[i+1])]
        if score > best_choice[1]:
            best_choice = (possibility, score)
    return best_choice
