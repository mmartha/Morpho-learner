import wiki
import morpho
from dataset import data, solutions

# Wikipedia articles in multiple languages
english = "http://en.wikipedia.org/wiki/World_War_II"
turkish = "http://tr.wikipedia.org/wiki/II._D%C3%BCnya_Sava%C5%9F%C4%B1"
french = "http://fr.wikipedia.org/wiki/Seconde_Guerre_mondiale"
german = "http://de.wikipedia.org/wiki/Zweiter_Weltkrieg"
boarisch = "http://bar.wikipedia.org/wiki/Wean"

def main():

    choice = raw_input("\nEnter 1 for Data Set or 2 for Wikipedia analysis\n")
    if int(choice) == 1:
        # Analyze morphology from a data set
        lang = raw_input("\nEnter Turkish, Swahili, Zulu, or English\n")
        if lang in solutions.keys:
            A, B = morpho.findAB(data[lang], solutions[lang])
            affixes = morpho.getAffixDict(data[lang], A, B)
        else:
            affixes = morpho.getAffixDict(data[lang])

        # Print all morphemes from top scored to lowest
        morpho.printByMax(affixes)
    else: print "Choice not recognized, try again"


    # To analyze the morphology from a Wikipedia page
    '''USE_THIS_URL = url2
    content = wiki.getContent(USE_THIS_URL)
    text = wiki.cleanContent(content)
    words, wordcount = wiki.getDictionary(text)'''
   
'''
    # Analyze morphology from a data set
    A, B = morpho.findAB(data["Turkish"], solutions["Turkish"])
    print 
    print "A = ", A, "B = ", B
    affixes = morpho.getAffixDict(data["Turkish"], A, B)

    # Print all morphemes from top scored to lowest
    morpho.printByMax(affixes)
'''

    # Print top ranked possible segmentations
'''for word in Zulu:
        segments = morpho.possibleSegments(word)
        ratings = {tuple(s):morpho.scoreSegmentation(list(s), affixes) for s in segments}
        print word
        morpho.printByMax(ratings, 5)
        print "-------------------------------"
        print
'''


if __name__ == '__main__':
    main()


