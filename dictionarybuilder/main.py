#!/usr/bin/env python
print("Initializing..")	
from nltk.corpus import semcor as s
from builder import SemcorDictionaryBuilder				
builder = SemcorDictionaryBuilder(s.tagged_sents(tag="sem"))
builder.buildDictionary()
builder.saveDictionary()
raw_input()