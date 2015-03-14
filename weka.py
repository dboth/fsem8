class Wekabuilder:
	data = {}
	options = []
	output = ""
	name = ""
	
	def __init__(self, data, options, name):
		self.data = data
		self.options = options
		self.name = name
		
	def processData(self):
		#hihi list comprehension fun. wow being so readable wow.
		self.output = "\n".join(["@RELATION "+self.name,""]+["@ATTRIBUTE " + rel[0]+" "+rel[1] if isinstance(rel[1],str) else "@ATTRIBUTE " + rel[0] + " {" + ",".join(["\""+str(x)+"\"" for x in rel[1]]) + "}" for rel in self.options]+["","","@DATA"]+[",".join(str(x) for x in line) for line in self.data.values()])
		return self
		
	def returnArff(self):
		return self.output
	
	def saveArff(self):
		if self.output != "":
			try:
				handler = open(self.name+".arff","w")
				handler.write(self.output)
				handler.close()
				return self
			except:
				raise IOError("File could not be written")
		else:
			raise ValueError("Data was never processed. Use processData method first.")
			
if __name__ == "__main__":			
	from verb_ontologization import OntologyWSD
	a = OntologyWSD("original_data/train_48.txt", "dictionarybuilder/all_verbs.json","goldstandard.json")
	w = Wekabuilder(a.processData(),a.getInfo(),"ontolo")
	w.processData()
	w.saveArff()
