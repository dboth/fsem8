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
		self.output = "\n".join(["@RELATION "+self.name,""]+["@ATTRIBUTE " + rel[0]+" "+rel[1] if isinstance(rel[1],basestring) else "@ATTRIBUTE " + rel[0] + " {" + ",".join(["\""+str(x)+"\"" for x in rel[1]]) + "}" for rel in self.options]+["","","@DATA"]+[",".join(str(x) for x in line) for line in self.data.values()])
		return self
		
	def returnArff(self):
		return self.output
	
	def saveArff(self):
		if self.output != "":
			try:
				handler = open(name+".arff","w")
				handler.write(self.output)
				handler.close()
				return 0
			except:
				raise IOError("File could not be written")
		else:
			raise ValueError("Data was never processed. Use processData method first.")
			
if __name__ == "__main__":			
	data = {("word1_sense1","word2_sense2"):[1,2,"+"],("word1_sense2","word2_sense3"):[1,3,"-"]}
	options = [["cooc","NUMERIC"],["lesk","NUMERIC"],["gold",["+","-"]]]
	name = "relation_ontologization"
	builder = Wekabuilder(data,options,name)
	builder.processData()
	builder.saveArff()