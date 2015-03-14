import verb_ontologization as v

class Chooser():
    def __init__(self, verb_a, verb_b, relation):
        self.va = verb_a
        self.vb = verb_b
        self.relation = relation

        self.OWSD = v.OntologyWSD("dictionarybuilder/all_verbs.json")

    def calc(self):
        all_values = {}
        assoc = self.OWSD.getAssociationMeasures(self.va, self.vb)
        for sense_pair in assoc:
            lesk = self.OWSD.getLesk(sense_pair[0], sense_pair[1])
            rel_value = {"ant":0.63,"tmp":-0.28,"ent":0.39,"pre":0}[self.relation]
            all_values.update({sense_pair: 0.13 + assoc[sense_pair] * -0.19 + lesk * -0.24 + rel_value})
        return max(all_values, key= lambda key: all_values.get(key))

a = Chooser("win", "play", "pre")
print(a.calc())
