import wikiGet
import wikiClean
import morpho


Swahili = ["ninasema", "ninaona", "wunasema", "wunaona", "anasema", 
            "niliona", "wanasema", "ninawaona", "nilisema", "niliwuona", 
            "wulisema", "wunaniona", "alisema", "waliniona", "walisema", 
            "wanawuona"]

Zulu = ["abafundisi", "ababazi", "umfundisi", "umbazi", "fundisa", "baza",
        "umlimi", "umfundi", "abalimi", "abafundi", "lima", "funda"]

Turkish = ["geldim", "geldin", "geldi", "geldik", "geldiniz", "geldiler", 
            "gelmedim", "gelmedin", "gelmedi", "gelmedik", "gelmediniz", 
            "gelmediler", "yedim", "yedin", "yedi", "yedik", "yediniz", 
            "yediler", "yemedim", "yemedin", "yemedi", "yemedik", "yemediniz", 
            "yemediler"]

English = ["nation", "civilization", "civilized", "creation", "create", 
            "nationalist", "nationalize", "socialist", "socialize", 
            "civilize", "society", "proper", "propriety", "property", 
            "locality", "local", "nationalization", "civil", "social",
            "nationality", "moral", "morality"]

# Wikipedia articles in multiple languages
url1 = "http://en.wikipedia.org/wiki/World_War_II"
url2 = "http://tr.wikipedia.org/wiki/II._D%C3%BCnya_Sava%C5%9F%C4%B1"
url3 = "http://fr.wikipedia.org/wiki/Seconde_Guerre_mondiale"
url4 = "http://de.wikipedia.org/wiki/Zweiter_Weltkrieg"
url5 = "http://bar.wikipedia.org/wiki/Wean"

def main():
    # To analyze the morphology from a Wikipedia page
    USE_THIS_URL = url2
    content = wikiGet.getContent(USE_THIS_URL)
    text = wikiClean.cleanContent(content)
    words, wordcount = morpho.getDictionary(text)

    affixes = morpho.getAffixDict(Zulu)
    for word in Zulu:
        segments = morpho.possibleSegments(word)
        ratings = {tuple(s):morpho.scoreSegmentation(list(s), affixes) for s in segments}
        print word
        morpho.printByMax(ratings, 5)
        print "-------------------------------"
        print

    return affixes


if __name__ == '__main__':
    main()


