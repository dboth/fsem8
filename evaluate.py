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
        return json.loads(open(filename, "r").read())
    
    def calcCongruence(self):
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
        print(amount_predictions)
        return correct/amount_predictions*100
    
    def calcFScore(self):
        pass
    

if __name__ == "__main__":
    e = Evaluation("goldbuilder/goldstandard.json", "train_data_calculated_3.json")
    print(e.calcCongruence())
