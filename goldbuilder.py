#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Dominik Both
#3125763

inputname = "train_48.txt"
outputname = "train.json"
def header(x,y,verb1,verb2):
	os.system('cls' if os.name == 'nt' else 'clear')
	print "Heidelberg University, Insitute of Computational Linguistics"
	print "Dominik Both, Svenja Lohse, Tonio Weidler"
	print "Gold Standard Annotator for Relation Ontologization" 
	print str(int(round(y*100/x)))+"% (Relation "+str(y)+" of "+str(x)+")"
	print "Relation: "+verb1+" > "+verb2+" ("+rel+")"

import os, json
from nltk.corpus import wordnet as wn
output = []
x = sum(1 for line in open(inputname))
with open(inputname) as fileobject:
	y = 1;
	for line in fileobject:
		linedat = line.strip().split("\t");
		verb1 = linedat[1]
		verb2 = linedat[2]
		rel = linedat[3]
		if (rel == "none"):
			optline = [linedat + ["",""]]
			continue
		header(x,y,verb1,verb2)
		print "Senses for "+verb1+":"
		zuordnung = {}
		i = 1
		for synset in wn.synsets(verb1,pos=wn.VERB):
			print str(i)+": "+synset.definition()
			zuordnung[i] = synset.name()
			i+=1
		sensea = input("Correct Sense (Number): ")	
		sense1 = zuordnung[sensea]
		header(x,y,verb1,verb2)
		print "Senses for "+verb2+":"
		zuordnung = {}
		i = 1
		for synset in wn.synsets(verb2,pos=wn.VERB):
			print str(i)+": "+synset.definition()
			zuordnung[i] = synset.name()
			i+=1
		sensea = input("Correct Sense (Number): ")	
		sense2 = zuordnung[sensea]
		optline = [linedat + [sense1,sense2]]
		output += optline
		y+=1
print "Thank you very much!"
f = open(outputname,"w")
f.write(json.dumps(output))
f.close()