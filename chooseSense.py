import verb_ontologization as v
import json

class Chooser():
    """ CLASS with methods for Files/Verb Pairs to chose correct senses by using data from verb_ontologization and goldstandard"""
    def __init__(self, cooc_file):
        self.OWSD = v.OntologyWSD(cooc_file)

    def calcVerbPair(self, verb_a, verb_b, relation):
        """ Calculation of most likely sense pair for two verbs with a relation. Feature Weights determined by Weka using the goldstandard features """
        all_values = {}
        assoc = self.OWSD.getAssociationMeasures(verb_a, verb_b)
        for sense_pair in assoc:
            lesk = self.OWSD.getLesk(sense_pair[0], sense_pair[1])
            rel_value = {"ant":0.63,"tmp":-0.28,"ent":0.39,"pre":0,"none":0}[relation]
            all_values.update({sense_pair: 0.13 + assoc[sense_pair] * -0.19 + lesk * -0.24 + rel_value})
        return [verb_a, verb_b, relation, max(all_values, key= lambda key: all_values.get(key))]

    def calcFile(self, filename):
        """ Uses calcVerbPair() to process a whole File of Verb Pairs and their Relation """
        with open(filename, "r") as f:
            pairs = [i.replace("\n","").split("\t")[1:4] for i in f.readlines()]
        out = []
        for pair in pairs:
            print("PROCESSING "+pair[0]+" "+pair[1])
            out.append(self.calcVerbPair(pair[0],pair[1],pair[2]))
        return out
    
    def writeIntoFile(self, filename, output_filename):
        """ Writes calcFile() Information into a file to prevent repeated waiting times... """
        f = open(output_filename, "w")
        f.write(json.dumps(self.calcFile(filename)))
        f.close()
        
if __name__ == "__main__":
    a = Chooser("dictionarybuilder/all_verbs.json")
    a.writeIntoFile("original_data/train_48.txt", "train_data_calculated.json")
