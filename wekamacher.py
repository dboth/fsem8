from weka import Wekabuilder
from verb_ontologization import OntologyWSD
a = OntologyWSD("original_data/train_48.txt", "dictionarybuilder/all_verbs.json","goldstandard.json")
w = Wekabuilder(a.processData(),a.getInfo(),"ontolo")
w.processData()
w.saveArff()
