import wiki
import morpho
from dataset import data, solutions

# Wikipedia articles in multiple languages
links = {
    "English" : "http://en.wikipedia.org/wiki/World_War_II",
    "Turkish" : "http://tr.wikipedia.org/wiki/Y%C3%BCz_(organ)",
    "French" : "http://fr.wikipedia.org/wiki/Seconde_Guerre_mondiale",
    "German" : "http://de.wikipedia.org/wiki/Zweiter_Weltkrieg",
    "Boarisch" : "http://bar.wikipedia.org/wiki/Wean"
}


def main():
    
    choice = raw_input("\nEnter 1 for Data Set or 2 for Wikipedia analysis\n")
    if int(choice) == 1:
        # Analyze morphology from a data set
        lang = raw_input("\nEnter Turkish, Swahili, Zulu, or English\n")
        dataset = data[lang]

    elif int(choice) ==2:
        lang = raw_input("\nEnter English, Turkish, French, or German\n")
        dataset, wordcount = wiki.get_dataset(links[lang])
    else: print "Choice not recognized, try again"

    mygraph = morpho.createGraph(dataset)
    for word in dataset:
        print word, morpho.scoreSegmentation(word, mygraph)[0]
    


if __name__ == '__main__':
    main()


