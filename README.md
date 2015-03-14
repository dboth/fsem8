Relationsontologisierungsalgorithmus (Relation Ontologizating Algorithm)
========================================================================

Authors
-------
Dominik Both, Svenja Lohse and Tonio Weidler
(both|lohse|weidler)@cl.uni-heidelberg.de
Institut of Computational Linguistics
Heidelberg University, Germany

Goal
----
Goal of this project was to conceptionalize an algorithm that takes a given set of semantically related verbs and computes the most probable wordnet sense pair.
In the first step the algorithm takes the cooccurence measure of the senses in two corpora and the lesk measure of the wordnet sense glosses as indicators for sense propability.
Further steps to be made could be taking advantage of other measurements (wordnet path distance, wordnet antonyms etc.) and a larger set of verb cooccurence data by evaluating more corporas.

Requirements
------------
* Python > 2.6 with installed NLTK module
* Wordnet (installed in NLTK)
* Semcor Corpus installed in NLTK
* MySQL Database
* Ontonotes Corpus (installed into a MySQL Database)
* Optional: py2exe (for providing a binary of the Gold Standard Annotator to users without python)
* Optional: Inno Setup (for providing a binary of the Gold Standard Annotator to users without python)

The three latter ones are only needed once to generate the verb cooccurence database files and are not needed in the runtime of the ontologizating algorithm.

Structure and Usage of the Single Program Parts
-----------------------------------------------
**Gold Standard Annotator**
*./goldbuilder/goldbuilder.py*

Allows the annotation of a given set of related verbs with their wordnet sense by human annotators.

Takes a file with one verb relation per line separated by tabs, like the given train and test files.

The file to be loaded can be specified in the first lines of code.
Start the python script without any arguments. 
The annotation is saved as a json file in the users home directory, formatted as the input file, but with the annotated wordnet senses as two more columns.
The python script can optionally be compiled to a windows binary using the py2exe library and the setup.py script. 
The resulting files can also be comprimated in to a setup.exe by using Inno Setup an the enclosed setup.iss.
For more information regarding the build of a windows binary out of python and a installer see the documentation of py2exe and Inno Setup.




