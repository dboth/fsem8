class Lesk:
	def __init__(self):
		return None
		
	def lesk(self, synset1, synset2):
		return sum([1 if x in synset1.definition().split() else 0 for x in synset2.definition().split()])

if __name__ == "__main__":
	d = Lesk();
	from nltk.corpus import wordnet as wn
	dreams = wn.synsets("dream",wn.VERB)
	sleeps = wn.synsets("sleep",wn.VERB)
	print(d.lesk(dreams[0],sleeps[0]))
	print(d.lesk(dreams[0],sleeps[1]))
	print(d.lesk(dreams[1],sleeps[1]))
	print(d.lesk(dreams[1],sleeps[0]))		