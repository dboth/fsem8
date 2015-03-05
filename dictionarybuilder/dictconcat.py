import json
from collections import Counter
json.dump(open("all_verbs.json","w"),Counter(json.load(open("cooc_semcor_verbs.json"))) + Counter(json.load(open("ontonote.json"))))