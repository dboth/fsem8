#Goldstandardgenerator
#Both/Lohse/Weidler

import numpy
import nltk
import json
from collections import Counter



class Annotation():
    def __init__(self, filename):
        self.filename = filename
        self.file = self.readFile(self.filename)[2:-2].split("], [")
        self.categories = self.createDictOfCategories()

    #METHODS
    def readFile(self, filename):
        file = open(filename, "r")
        out = file.read()
        file.close()
        return out
    def createDictOfCategories(self):
        ''' <cat_number>: [verb1, verb2, relation, relation_specification, available_contexts, v1_sense, v2_sense] '''
        categories = {}
        for cat in self.file:
            single_cat = cat[1:-1].split('", "')
            categories.update({single_cat[0] : single_cat[1:]})
        return categories
    
class Goldstandard():
    def __init__(self, list_of_annotations):
        self.annotations = [annot.categories for annot in list_of_annotations]
        self.gold = self.calcGold()
        self.average_confidence = self.calcAverageConfidence()

    def readFile(self, filename):
        return json.loads(open(filename).read())
        
    def calcGold(self):
        all_tupels = {}
        for ann in self.annotations:
            for cat in ann:
                try:
                    all_tupels[cat] += [(ann[cat][-2], ann[cat][-1])]
                except:
                    all_tupels.update({cat: [(ann[cat][-2], ann[cat][-1])]})

        gold = {}
        for cat in all_tupels:
            most_common_tuple = Counter(all_tupels[cat]).most_common(1)[0]
            most_common_tuple = [most_common_tuple[0], self.annotations[0][cat][:2], most_common_tuple[1]/len(self.annotations), self.annotations[0][cat][2]]
            gold.update({cat: most_common_tuple})

        return gold
    
    def calcAverageConfidence(self):
        additive_conf = 0
        for cat in self.gold:
            additive_conf += self.gold[cat][2]
        return additive_conf/len(self.gold)
    
    def getProblematicDecisions(self):
        return sorted([int(i) for i in self.gold if self.gold[i][1] < 0.75])

    def fixGold(self, filename):
        fixed = self.readFile(filename)
        for i in fixed:
            self.gold[i[0]][0]=i[-2:]
        
    def writeIntoFile(self):
        f = open("goldstandard.json", "w")
        f.write(json.dumps(self.gold))
        f.close()
    

if __name__ == "__main__":
    a = Annotation("train_wundi.json")
    b = Annotation("train_svenja.json")
    c = Annotation("train_dominik.json")
    d = Annotation("train_tonio.json")

    g = Goldstandard([a,b,c,d])
    g.fixGold("train_golden_gold.json")
    g.writeIntoFile()
