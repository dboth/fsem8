import json, operator
from nltk.corpus import wordnet as wn
d = json.load(open("cooc_semcor.json","r"))
while True:
	s1 = raw_input("Verb 1: ")
	s2 = raw_input("Verb 2: ")
	ss1 = wn.synsets(s1,wn.VERB)
	ss2 = wn.synsets(s2,wn.VERB)
	res = {}
	for x in ss1:
		for y in ss2:
			l = ",".join(sorted([x.name(),y.name()]))
			if l in d:
				res[(x,y)] = d[l]
			else:
				res[(x,y)] = 0
	print "Out of "+str(len(res))+" combinations this is the most likely one:"
	a,b = max(res.iteritems(), key=operator.itemgetter(1))[0]
	print a.definition()
	print b.definition()
	print