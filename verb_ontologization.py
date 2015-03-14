#verbontologization
#WSD ALGORITHM

import numpy
import json
from nltk.corpus import wordnet as wn

class OntologyWSD():
    def __init__(self, file_occ, file_gold=""):
        try:
            self.gold = self.readFile(file_gold)
        except:
            pass
        self.occurances = self.readFile(file_occ)
        
    def getInfo(self):
        return [["cooc","NUMERIC"],["lesk","NUMERIC"],["relation",["ant","tmp","ent","pre"]],["correct",["+","-"]]]

    def readFile(self, filename):
        if filename.split(".")[1] == "json":
            read = json.loads(open(filename).read())
        else:
            file = open(filename, "r")
            read = [line for line in file.readlines()]
            file.close
        return read

    #METHODS TO CALC FEATURES
    def findTroponymAssociation(self, combs):
        ''' Takes a list of combined senses of two verbs and returns the overall occurance of all combinations of troponyms of the pairs. ''' 
        troponyms = {}
        for pair in combs:
            tuple_of_troponyms = ()
            for sense in pair:
                tuple_of_troponyms += (wn.synset(sense).hyponyms(),)
            troponyms.update({pair: tuple_of_troponyms})
        
        for pair in troponyms:
            troponym_combinations = [(a,b) for a in troponyms[pair][0] for b in troponyms[pair][1]]
            occ_trop = 0
            for trop_pair in troponym_combinations:
                pair_string = pair[0]+","+pair[1]
                if pair_string in self.occurances:
                    occ_trop += self.occurances[pair_string]
            troponyms[pair] = occ_trop
            
        return troponyms
    
    def getAssociationMeasures(self, verb_a, verb_b):
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
                occ.update({pair: ((occurances_extract[pair] + troponyms[pair])/occ_of_other_combs)})
            else:
                occ.update({pair: 0})

        return occ

    def getLesk(self, synset1, synset2):
        return sum([1 if x in wn.synset(synset1).definition().split() else 0 for x in wn.synset(synset2).definition().split()])

    #FINALIZATION METHODS              
    def processData(self):
        out={}
        for pair in self.gold:
            assoc_measures = self.getAssociationMeasures(self.gold[pair][1][0],self.gold[pair][1][1])
            for i in assoc_measures:
                if i == tuple(sorted(self.gold[pair][0])):
                    class_pred = "+"
                else:
                    class_pred = "-"
                out.update({i:[assoc_measures[i], self.getLesk(i[0], i[1]), self.gold[pair][3], class_pred]})
        return out


if __name__ == "__main__":
    a = OntologyWSD("dictionarybuilder/all_verbs.json","goldstandard.json")
    print(a.processData())


