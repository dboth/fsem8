Relationsontologisierungsalgorithmus (Relation Ontologizating Algorithm)
========================================================================

Authors
-------
Dominik Both, Svenja Lohse and Tonio Weidler  
(both|lohse|weidler)@cl.uni-heidelberg.de  
Institute of Computational Linguistics  
Heidelberg University, Germany  

Outline
----
Goal of this project was to conceptionalize an algorithm that takes a given set of semantically related verbs and computes the most probable wordnet sense pair.
In the first step the algorithm takes the cooccurence measure of the senses in two corpora and the lesk measure of the wordnet sense glosses as indicators for sense probability.
It turned out, that this is not enough to get a satisfying ontologization algorithm, which reflects in the evaluation of the current algorithm.
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

The third, fourth and fifth are only needed once to generate the verb cooccurence database files and are not needed in the runtime of the ontologizating algorithm.

Structure and Usage of the Single Program Parts - Preprocessing
---------------------------------------------------------------
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

**Gold Standard Generator**  
*./goldbuilder/gold_gen.py*  
Holds classes to generate one gold standard out of a variable number of human annotation holding json files.  
Human annotations are loaded by instantiating the `Annotation` class.  
The `Goldstandard` class takes a list of `Annotation` instances and holds a method to save the calculated  gold standard into a json file.
See the comments in the file for more information regarding other methods of the named classes.

**Semcor Verb Cooccurence Extractor**  
*./dictionarybuilder/semcorreader.py*  
Iterates through all sentences in the Semcor corpus and counts cooccurences of verb wordnet senses inside the sentence.  
Saves the cooccurence into a json dictionary, where the key is composed of the two wordnet senses names separated by comma in alphabetical order.  
See the comments in the file for more information regarding other methods of the Class.

**Ontonotes Verb Cooccurence Extractor**  
*./dictionarybuilder/ontonotesreader.py*  
The corpus has to be loaded into a MySQL database. Login details have to be specified within the code.  
Further alterations to the Ontonotes database have to be made, for the sentences in the database are not annotated with their language.  
To only get english sentences only, first the language information has to be added by updating a new lang_id column inside the sentence table with data selected out of the document table by matching the documents id and the sentences document_id column.  
Iterates through all english sentences in the Ontonotes corpus and counts cooccurences of verb wordnet senses inside the sentence.  
Saves the cooccurence into a json dictionary, where the key is composed of the two wordnet senses names separated by comma in alphabetical order.  

**Verb Cooccurence Extractor Merger**  
*./dictionarybuilder/dictconcat.py*  
Merges the two built json cooccurence dictionary into ones by adding the value of verb pairs that happen to exist in both corpora. Saves the resulting dictionary as a json dictionary.

Structure and Usage of the Single Program Parts - Main Algorithm
----------------------------------------------------------------
**Verb Ontologization Main Class**  
*./verb_ontologization.py*  
This class is the calculation main class for the relation ontologization algorithm.  
The constructor takes a cooccurence dictionary and optionally the gold standard file.  
Calling the `processData` method returns a dictionary a list of the cooccurence measure and the lesk value for every possible sense pair.   
See the comments in the file for more information regarding other methods of the Class.  

**Weka ARFF Builder**  
*./weka.py*  
This class processes the data processed by the verb ontologization main class into a ARFF-file readable by WEKA.
The constructor takes a data dictionary of data points with the feature as a list and a options list containing information regarding the features.  
See the comments in the file for more information regarding other methods of the Class.  
Example:  

    data = {0:[1,2,"+"],1:[1,3,"-"]}  
    options = [["cooc","NUMERIC"],["lesk","NUMERIC"],["gold",["+","-"]]]  
    name = "relation_ontologization"  
    builder = Wekabuilder(data,options,name)  
    builder.processData()  
    builder.saveArff()  

**ARFF Data Multiplicator**  
*./arff_duplicator.py*  
This is a helper file, multiplying the positive datapoints by a given value to get an equal proportion. 
Change the factor inside the file and start the script without any arguments.

**Verb Ontologization Sense Chooser**  
*./choseSense.py*  
This class calculates the most probable sense pair for given test data using the calculations in the verb ontologization main class.  
The constructor takes the cooccurence file for the verb ontologization class.  
By calling the `writeIntoFile` method the algorithm writes the results for the given test data file into a json file, which can be evaluated to the goldstandard with the following evaluation class.  
See the comments in the file for more information regarding other methods of the Class. 

**Verb Ontologization Evaluator**  
*./evaluate.py*  
Evaluates the calculations of the sense chooser on a given gold standard.  
The constructor takes the path to the named files.  
By using the `calcCongruence` method the evaluator prints the accuracy.
See the comments in the file for more information regarding other methods of the Class. 
