#Evaluation Algorithm
#Both/Lohse/Weidler

import json

class Evaluation():
    def __init__(self, gold, chosen_pairs):
        self.gold = self.readFile(gold)
        if isinstance(chosen_pairs, dict):
            self.chosen_pairs = chosen_pairs
        elif isinstance(chosen_pairs, str):
            self.chosen_pairs = self.readFile(chosen_pairs)

    def readFile(self, filename):
        """ Reads Json file """
        return json.loads(open(filename, "r").read())
    
    def calcCongruence(self):
        """ Calculates percentual congruence of prediction and gold standard """
        correct = 0
        amount_predictions = 0
        for true_label in self.gold:
            for prediction in self.chosen_pairs:
                if [self.gold[true_label][1],self.gold[true_label][3]] == [[prediction[0], prediction[1]], prediction[2]]:
                    if sorted(self.gold[true_label][0]) == sorted(list(prediction[3])):
                        correct += 1
                        amount_predictions += 1
                    else:
                        amount_predictions += 1
        return correct/amount_predictions*100
    
    def calcPartCongruence(self):
        """ Calculates Congruence of prediction and gold standard, looking at single senses, not only the pairs, s.t. (a,b) and (a,c) have
        a congruence of 1/2. Returns the percentual congruence in such way and the amount of completely correctly predicted pairs and the amount
        of partiually correctly predicted pairs """
        correct = 0
        amount_predictions = 0
        labeled_correct = 0
        labeled_part_correct = 0
        for true_label in self.gold:
            for prediction in self.chosen_pairs:
                if [self.gold[true_label][1],self.gold[true_label][3]] == [[prediction[0], prediction[1]], prediction[2]]:
                    if sorted(self.gold[true_label][0]) == sorted(list(prediction[3])):
                        correct += 2
                        amount_predictions += 2
                        labeled_correct += 1
                    elif self.gold[true_label][0][0] in prediction[3] or self.gold[true_label][0][1] in prediction[3]:
                        labeled_part_correct += 1
                        correct += 1
                        amount_predictions += 2
                    else:
                        amount_predictions += 2

        out = "Congruence: "+str(correct/amount_predictions)+"\nCompletely correctly predicted Pairs: "+str(labeled_correct)+"\nPartially correctly predicted Pairs: "+str(labeled_part_correct)
        return out

if __name__ == "__main__":
    e = Evaluation("goldbuilder/goldstandard.json", "train_data_calculated.json")
    print(e.calcPartCongruence())
