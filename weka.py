#both/lohse/weidler
#WeKaBuilder

class Wekabuilder:
        """ Class converts the dictionary received by OntologyWSD class into a ARFF File readable by WeKa """   
        def __init__(self, data, options, name):
                self.data = data
                self.options = options
                self.name = name
                self.output = self.processData()
                
        def processData(self):
                """ converts provided data into string to be written into .arff file """
                output = "\n".join(["@RELATION "+self.name,""]+["@ATTRIBUTE " + rel[0]+" "+rel[1] if isinstance(rel[1],str) else "@ATTRIBUTE " + rel[0] + " {" + ",".join(["\""+str(x)+"\"" for x in rel[1]]) + "}" for rel in self.options]+["","","@DATA"]+[",".join(str(x) for x in line) for line in self.data.values()])
                return output
        
        def saveArff(self):
                """ writes processData()-string into .arff File """
                try:
                        handler = open(self.name+".arff","w")
                        handler.write(self.output)
                        handler.close()
                        return "SUCCESS"
                except:
                        raise IOError("File could not be written")
                        
if __name__ == "__main__":                      
        from verb_ontologization import OntologyWSD
        a = OntologyWSD("dictionarybuilder/all_verbs.json", "goldbuilder/goldstandard.json")
        w = Wekabuilder(a.processData(),a.getInfo(),"ontolo_new_trop")
        w.saveArff()
