#Ressorces: ontonotes in database in localhost, root:root
#Ontonotes wordnet xml sense_inventories directory in same folder

#changes on ontonotes database:
#add column lang_id to sentence
#fill lang_id by getting the value out of document using key sentence.document_id on document.id

#load mysql.connector, nltk.corpus.wordnet, xml.minidom, sys.stdout, json, time and os
import mysql.connector as cn
from nltk.corpus import wordnet as wn
from xml.dom import minidom
from sys import stdout
import json
import time, os

#function takes a list of synsets, counts their cooccurence and adds it to the given dictionary
def addSentenceToDictionary(synsets, dictionary):
		num_sets = len(synsets)
		for x in range(num_sets): #last element does not have to be called, because it has no partner
			for y in range(x+1,num_sets): #gives us for an array 0,1,2,3,4 tuples of 01,02,03,04,12,13,14,23,24,34
				key = synsets[x]+","+synsets[y]
				if key in dictionary:
					dictionary[key] += 1
				else:
					dictionary[key] = 1
		return dictionary

#init dictionary and mysql connection		
dictionary = {}
cd = cn.connect(user="root", password="root", host='127.0.0.1', database='ontonotes',buffered=True)
cnx = cd.cursor()
#select all english sentences. for this query the lang_id column must have been manually added to the sentence table!
query = "SELECT id FROM sentence WHERE lang_id = 'en'"
cnx.execute(query)
#initialize the clock getting a remaining time counter
c = 1
begintime = time.clock()
#iterate through all sentences
for (id) in cnx:
	#calculate remaining time
	now = time.clock()
	vg = now-begintime
	os.system('cls' if os.name == 'nt' else 'clear')
	print("Satz "+str(c)+" von 115.812") #115812 is the number of english sentences in the ontonotes database. this has to be changed if another ontonotes db is used.
	seconds = vg/(float(c)/115812*100)*100
	#subtract elapsed time to get remaining time
	seconds -= vg
	#calculate minutes and hours out of seconds
	m, s = divmod(seconds, 60)
	h, m = divmod(m, 60)
	#print remaining 
	print "Remaining: %02d:%02d:%02d hours" % (h, m, s)
	#get all senses of the words in this sentence out of the on_sense table.
	cnx2 = cd.cursor()
	query = "SELECT lemma, sense FROM on_sense WHERE id LIKE '%"+id[0]+"' AND pos = 'v'"
	cnx2.execute(query)
	senselist = []
	#iterate through sentence senses
	for (lemma, sense) in cnx2:
		#get the sense information out of ontonote's sense inventory files
		xmldoc = minidom.parse("sense-inventories/"+lemma+"-v.xml")
		itemlist = xmldoc.getElementsByTagName('sense')
		#search the wordnet sense in the xml model
		for s in itemlist:
			if (s.attributes['n'].value == sense):
				for i in s.getElementsByTagName('wn'):
					if (i.firstChild and not i.hasAttribute('lemma')):
						if (i.firstChild.nodeValue != ""):
							senses = i.firstChild.nodeValue.split(",")
							for sens in senses:
								senselist += [wn.synset(lemma+".v."+sens).name()]
	#add the senselist to the dictionary
	dictionary = addSentenceToDictionary(sorted(senselist),dictionary)					
	cnx2.close()
	c+=1
#close the mysql connections
cnx.close()
cd.close()
#save the dictionary as json
f = open("ontonote.json","w")
dct = json.dump(dictionary,f)
f.close()