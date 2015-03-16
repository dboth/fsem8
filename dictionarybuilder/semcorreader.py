#!/usr/bin/env python
from nltk.tree import Tree
from sys import stdout
import json

'''
Cooccurence counter class for the semcor corpus
Requires nltk with semcor
returns cooccurence dictionary of all verbs over all sentences
'''
class SemcorDictionaryBuilder:
	semcor = []
	dictionary = {}
	
	#init with empty corpus
	def __init__(self, semcor=[]):
		self.semcor = semcor
		print("Ready.")
	
	#setter for the corpus, where each sentence is an element in a list
	def setCorpus(self, dict):
		self.semcor = dict
		print("Ready.")
	
	#iterates through the dictionary and processes the sentence
	def buildDictionary(self):
		num = 1
		stdout.write("\rPreparing...")
		stdout.flush()
		for i in self.semcor:
			stdout.write("\rProcessing sentence %d" % num)
			stdout.flush()
			self.addSentenceToDictionary(self.getOccuringSynsets(i))
			num += 1
		print("\n\rProcessing completed.")
	
	#prints out statistics after the dictionary is created
	def statistics(self):
		d = {}
		for t_n in self.dictionary.values():
			if t_n not in d:
				d[t_n] = 0
			d[t_n] += 1
		for x in sorted(d.keys(),reverse=True):
			print(str(x)+"\t"+str(d[x]))
	
	#saves the dictionary to a json file
	def save(self,filename):
		try:
			f = open(filename,"w")
			dct = json.dump(self.dictionary,f)
			f.close()
			print("Saving successful")
		except:
			print("Error while saving")
	
	#reads a dictionary out of a file for adding sentences or showing statistics
	def read(self,filename):
		try:
			f = open(filename,"r")
			self.dictionary = json.load(f)
			f.close()
			print("Reading successful")
		except:
			print("Error while saving")
	
	#ui for read
	def loadDictionary(self):
		filename = raw_input("Path to load the dictionary from: ")
		self.read(filename)
	
	#ui for save
	def saveDictionary(self):
		filename = raw_input("Path to save the dictionary into: ")
		self.save(filename)
		
	#returns the corpus
	def returnSemcor(self):
		return self.semcor
		
	#returns the sentence with the given id
	def returnSentence(self,id):
		try:
			return self.semcor[id]
		except:
			raise IndexError('Sentence with the specified id unknown.')
			
	#returns the dictionary
	def returnDictionary(self):
		return self.dictionary
		
	#processes a sentence and gives out a list of verb synsets in this sentence
	def getOccuringSynsets(self,sentence):
		synsets = []
		for chunk in sentence:
			if isinstance(chunk,Tree):
				if not isinstance(chunk.pos()[0][1],basestring):
					if chunk.label().synset().pos() == "v":
						synsets += [chunk.label().synset().name()]
		return sorted(synsets)
		
	#takes a list of synsets and builds cooccurence pairs to add them to the dictionary
	def addSentenceToDictionary(self,synsets):
		num_sets = len(synsets)
		for x in range(num_sets): #last element does not have to be called, because it has no partner
			for y in range(x+1,num_sets): #gives us for an array 0,1,2,3,4 tuples of 01,02,03,04,12,13,14,23,24,34
				key = synsets[x]+","+synsets[y]
				if key in self.dictionary:
					self.dictionary[key] += 1
				else:
					self.dictionary[key] = 1
					
					
if __name__ == "__main__":
	print("Initializing..")	
	from nltk.corpus import semcor as s
	from builder import SemcorDictionaryBuilder				
	builder = SemcorDictionaryBuilder()
	builder.setCorpus(s.tagged_sents(tag="sem"))
	builder.buildDictionary()
	builder.saveDictionary()