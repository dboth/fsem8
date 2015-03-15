#verbontologization
#WSD ALGORITHM
#Both/Lohse/Weidler

import numpy
import json
from nltk.corpus import wordnet as wn

class OntologyWSD():
    def __init__(self, file_occ, file_gold=""):
        #gold standard File is optional to make feature functions accessable for other files (e.g. chooseSense.py) to just calculate features
        try:
            self.gold = self.readFile(file_gold)
        except:
            pass
        
        self.occurances = self.readFile(file_occ)
        
    def getInfo(self):
        """ Returns all features and their possible states for WeKa implementation"""
        return [["cooc","NUMERIC"],["lesk","NUMERIC"],["relation",["ant","tmp","ent","pre"]],["correct",["+","-"]]]

    #DATA PREPERATION METHODS
    def readFile(self, filename):
        """ Reads json files (gold/ooc) """
        return json.loads(open(filename, "r").read())

    #METHODS TO CALC FEATURES
    def findTroponymAssociation(self, combs):
        """ Takes a list of combined senses of two verbs and returns the overall occurance of all combinations of troponyms of the pairs.
        Function is meant to be used by getAssociationMeasures for further depth of analysis. """
        print("ENTERING Troponym Calculation")
        troponyms = {}
        for orig_pair in combs:
            tuple_of_troponyms = ()
            for sense in orig_pair:
                tuple_of_troponyms += (wn.synset(sense).hyponyms(),)
            troponyms.update({orig_pair: tuple_of_troponyms})    
        
        for pair in troponyms:
            troponym_combinations = [tuple(sorted((a.name(),b.name()))) for a in troponyms[pair][0] for b in troponyms[pair][1]]
            if troponym_combinations != []:
                occurances_extract = {}
                for el in self.occurances:
                    element = tuple(sorted(el.split(",")))
                    if element in troponym_combinations:
                        occurances_extract.update({element: self.occurances[el]})
            
            occ_trop = 0
            occ_of_other_combs = 0
            for trop_pair in troponym_combinations:
                if trop_pair in occurances_extract:
                    occ_trop += occurances_extract[trop_pair]
                    for el in occurances_extract: #divident_calc
                        if trop_pair[0] in el or trop_pair[1] in el:
                            occ_of_other_combs += occurances_extract[el]
            
            troponyms[pair] = [occ_trop, occ_of_other_combs]
            if troponyms[pair] != [0,0]:
                print(troponyms[pair])
            
        print("FINISHED Troponym Calculation")
        return troponyms
    
    def getAssociationMeasures(self, verb_a, verb_b):
        """ Takes two verbs and return a dictionary with the possible sense pairs for those two verbs as keys and their cooccurance divided by the occurances of
        all possible pairs for the verbs that have one sense in common with the key pair. """
        verb_sense_combinations = [tuple(sorted((a.name(),b.name()))) for a in wn.synsets(verb_a, wn.VERB) for b in wn.synsets(verb_b, wn.VERB)]
        troponyms = self.findTroponymAssociation(verb_sense_combinations)

        #reducing the given data to relevant information about all pairs in verb_sense_combinations
        occurances_extract = {}
        for el in self.occurances:
            element = tuple(sorted(el.split(",")))
            if element in verb_sense_combinations:
                occurances_extract.update({element: self.occurances[el]})                

        #assign the single pairs to their association measure by dividing their occurance by the overall occurance of the elements as a pair with another sense
        occ = {}
        for pair in verb_sense_combinations:
            if pair in occurances_extract:
                occ_of_other_combs = 0
                for el in occurances_extract:
                    if pair[0] in el or pair[1] in el:
                        occ_of_other_combs += occurances_extract[el]
                occ.update({pair: ((occurances_extract[pair] + troponyms[pair][0])/(occ_of_other_combs+troponyms[pair][1]))})
            else:
                try:
                    occ.update({pair: (troponyms[pair][0]/troponyms[pair][1])})
                except:
                    occ.update({pair: troponyms[pair][0]})
        return occ

    def getLesk(self, synset1, synset2):
        """ Takes two SENSES (not verbs) and returns their Lesk, meaning the congruence of their descriptions in wordnet (natural positive number value increasing with common words in both definitions)."""
        return sum([1 if x in wn.synset(synset1).definition().split() else 0 for x in wn.synset(synset2).definition().split()])

    #FINALIZATION METHODS              
    def processData(self):
        """ Only usable if GoldStandard File is provided! Returns a dictionary that contains all sense pairs for all verb pairs in the gold standard as keys and their feature vector. Decides if a sense is predicted correctly with those features
        based on the gold standard annotation and provides this information as last feature respectively the classification label. """
        out={}
        for pair in self.gold:
            print("---------\nPROCESSING: "+str(self.gold[pair][1]))
            assoc_measures = self.getAssociationMeasures(self.gold[pair][1][0],self.gold[pair][1][1])
            for i in assoc_measures:
                if i == tuple(sorted(self.gold[pair][0])):
                    class_pred = "+"
                else:
                    class_pred = "-"
                out.update({i:[assoc_measures[i], self.getLesk(i[0], i[1]), self.gold[pair][3], class_pred]})
        return out


if __name__ == "__main__":
    a = OntologyWSD("dictionarybuilder/all_verbs.json","goldbuilder/goldstandard.json")
    print(a.processData())


