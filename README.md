
# PyMedExt - a library to process clinical text

PyMedExt is a library designed to process clinical text.
PyMedExt includes basic data wrangling functions to transform
text input formated as txt, pymedext,biocxml,biocjson,fhir, or brat
into pymedext, biocxml, biocjson, omop or brat.

PyMedExt also includes
pymedext core to extend in order to add new annotators.

## Requirements

### Installation
#### Using pip
```bash

pip3 install git+https://github.com/equipe22/pymedext_core.git


```

# Tutorial Add an annotator


# Add an Annotator
if you want to expand PyMedExt and add a new local annotator.

first you will have to

```python
from pymedextcore import annotators

```
### the use case of grep

grep is a linux command-line which allow you to search into plain-text data sets
for lines that match a regular expression.
The script grepWrapperAnnotator.py located on the src
directory, is a wrapper around grep.

#### resources
It takes as input two files :
- regexResource.txt --> a one column list of words to search in a text
- pivotResource.csv --> a two columns list of words: pattern,normalizewords

#### Define the Annotator

In order to define a new annotator, first you need to extend the annotators.Annotator class.
After that you will need at list two linux functions.
- __init__
- annotate_function


##### __init__()

The initialise function must contains
- key_input --> the type of Annotation to be used by the annotator, in that case the raw_text
- key_output --> the type of the Annotation output by the Annotator
- ID --> the tooo id, preferencially the the tool github repository and version tag
- other arguments are specific to the type of annotator

```python
class regexFast(annotators.Annotator):
    """
    Annotator based on linux grep to search regext from a source file
    """
    def __init__(self, key_input, key_output, ID, regexResource, pathToPivot, ignore_syntax=False):
        """FIXME! initialize the annotator
        :param key_input: input [raw_text']
        :param key_output: either regex_fast or the normalized regex value need to discuss
        :param ID: regex_fast.version
        :param regexResource: path to regex value file
        :param pathToPivot: pivot table between regex and the normalized value
        :param ignore_syntax: not used yet
        :returns:
        :rtype:

        """
        super().__init__(key_input, key_output, ID)
        self.ignore_syntax=ignore_syntax
        self.fileAnnotation=None
        self.countValue=None
        self.pathToPivot=pathToPivot
        self.pivot=dict()
        self.cmds=["fgrep -iow -n -b -F -f "+regexResource]
        self.loadPivot()

```

##### annotate_function()

```python

def annotate_function(self, _input):
    """ main annotation function
    :param _input: in this case raw_text
    :returns: a list of annotations
    :rtype:
    """
    logger.debug(_input)
    inp = self.get_key_input(_input,0)[0]
    fileAnnotation,countValue=self.makeMatch(inp)
    countValue=self.setPivot(countValue)
    logger.debug(countValue)
    annotations=[]
    for matchPos in list(fileAnnotation.keys()):
        for drug in fileAnnotation[matchPos]:
            ID = str(uuid.uuid1())
            attributes={"ngram":drug}
            annotations.append(annotators.Annotation(type= self.key_output,
                                          value=countValue[drug]["normalized"], #drug,
                                          span=(int(matchPos), int(matchPos)+len(drug)),
                                          source=self.ID,
                                          isEntity=True,
                                          ID=ID,
                                          attributes=attributes,
                                          source_ID = inp.ID))
    return(annotations)
```



##### Use the Annotator in a python script
For this demo clone  the pymedext_core git repository and go to the src directory

``` bash
git clone https://github.com/equipe22/pymedext_core.git
cd pymedext_core/src

# go in python interactive mode
python3
```

``` python
#import dependencies
from grepWrapperAnnotator import regexFast # contains your local annotator
from pymedextcore import pymedext # contains Document and other pymed connector object
import os
import logging

logging.basicConfig(level=logging.DEBUG)
resourcePath=os.getcwd().replace("src","ressources/")

dataPath=os.getcwd().replace("src","data/frenchReport/letter.txt")


thisDoc=pymedext.Document(raw_text= " a document demo you want to work with and contains evidence of. covid 19, sras, sars ", ID="dataPath")


getRegex = regexFast(key_input = ['raw_text'],
                     key_output = 'regex_fast',
                     ID = "regex_fast.v1",
                     regexResource=resourcePath+"regexResource.txt ",
                     pathToPivot=resourcePath+"pivotResource.csv"
                     )

# add all your annotators in a list
annotators =[getRegex]
# annotate your document


thisDoc.annotate(annotators)
thisDoc.to_dict()

#write your annotation in pymedext json
thisDoc.writeJson("outputfile.json")

```




# PyMedExt conversion tutorial

## PyMedExt commandline

``` bash

pymedext -h
usage: pymedext [-h] [-i INPUTFILE] [-o OUTPUT]
                [--itype {txt,pymedext,biocxml,biocjson,fhir,brat}]
                [--otype {omop,pymedext,bioc,brat}] [-f] [-be BRATEXCLUDE]
                [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUTFILE, --inputFile INPUTFILE
                        path to input folder
  -o OUTPUT, --output OUTPUT
                        enter the output file name
  --itype {txt,pymedext,biocxml,biocjson,fhir,brat}
                        input type
  --otype {omop,pymedext,bioc,brat}
                        output type
  -f, --folder          if set, the input is consider to be a folder of json
                        pymedext
  -be BRATEXCLUDE, --bratexclude BRATEXCLUDE
                        list of annotations to exclude from brat
  -v, --version         show program's version number and exit
```




### text to pymedext

``` python

    pymedext -i demo.txt --itype txt -otype pymedext
```


### fhir to pymedext

``` python

    pymedext -i patient-2169591.fhir-bundle.xml  --itype fhir -otype pymedext
    pymedext -i patient-99912345.fhir-bundle.xml  --itype fhir -otype pymedext

```


### bioc to pymedext


### text to pymedext

``` bash

    pymedext -i demo.txt --itype txt -otype pymedext
```


### fhir to pymedext

``` bash

    pymedext -i patient-2169591.fhir-bundle.xml  --itype fhir -otype pymedext
    pymedext -i patient-99912345.fhir-bundle.xml  --itype fhir -otype pymedext

```


### bioc to pymedext

``` bash
    cd data
    wget https://quaerofrenchmed.limsi.fr/QUAERO_FrenchMed_BioC.zip
    unzip QUAERO_FrenchMed_BioC.zip
    pymedext -i 7382743.xml --itype biocxml -otype pymedext
    pymedext -i biocformat.json --itype biocjson -otype pymedext
    pymedext -i QUAERO_BioC/corpus/train/MEDLINE_train_bioc --itype biocjson -otype pymedext
    pymedext -i QUAERO_BioC/corpus/train/EMEA_train_bioc --itype biocjson -otype pymedext
    #pymedext to bioc, need to be able to construct collection



```


### brat to pymedext (no example)

``` bash
 no example
 brat to bioc

```
### require annotation
It will be done on pymedext_public
  - pymedext to omop
  - fhir to omop
  - fhir to bioc
  - brat to omop
  - pymedext to doccano





### Other Install mode

#### Using GNU Make
```bash

#local install of pymedext packages
make install

```

#### Deploying PyMedExt as Docker image

##### Install as Docker Image
check on 21 January 2021

###### Linux
https://docs.docker.com/engine/install/#server

###### Mac Intel Processor
https://docs.docker.com/docker-for-mac/install/#system-requirements

###### Mac M1 Processor
https://docs.docker.com/docker-for-mac/install/#system-requirements
trouble to make it work

#### Build Image

##### fullfill configuration
first create a file config/.git-credentials based on the config/.git-credentials_template
 http:user:pass@github.com

##### Docker in command line
```bash

docker build -t pymedext-core:v0.0.2 .


```

##### Using GNU Make
```bash
#build docker instance
make build

```



# PyMedExt Documentation

PyMedExt Documentation is generated automatically with
sphinx-doc https://github.com/equipe22/sphinx_doc. AS an example to generate the documentation you can have a look at
the following links,

--> https://www.sphinx-doc.org/en/master/usage/restructuredtext/domains.html#the-python-domain

--> https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html

```python


class Annotation:
    """
    Based object which contains Annotation
    """

    def __init__(self, type:str, value:str, source:str, source_ID:str,
                 span:Optional[Tuple[int,int]] = None, attributes:Optional[List] = None,
                 isEntity:bool=False, ID:Optional[str] = None, ngram:Optional[str] = None):
        """Intialize an Annotation object
        :param type: annotation type define by the user (linked to the Annotator)
        :param value: the annotation value, has to be a string
        :param source: the name of the Annotator
        :param source_ID: the Annotator id
        :param span: the (start, end) position of the annotators
        :param attributes: In some cases, the value is not enough so other key elements could be saved as dict in attributes
        :param isEntity: if the Annotation is an entity define as an annotation which can be normalized  (e.g. by a specific uri from an ontology) not the case for segment
        :param ID: Annotation ID of this specific annotation
        :returns: Annotation
        :rtype: Annotation
        """

```

also to a use case of Documentation example for the Annotation class --> https://equipe22.github.io/pymedext_core/pymedext_core.html?highlight=annotation#pymedext_core.annotators.Annotation
## Installation of PyMedExt




## Examples

### Datasets

All the datasets used in the examples can be found in the data folder

#### PubTator (biocxml)
Users can retrieve pre-annotated PubMed files using PubTator.

**Get Data from PubTator**
``` python
from pymedextcore import pymedext

pub = pymedext.PubTatorSource()
docs = pub.getPubTatorAnnotations(["27940449","28058064","28078498"])
counter=1
for doc in docs:
    doc.writeJson("pubtator_"+str(counter)+".json")
    counter+=1

docs = pub.getPubTatorAnnotations(["27940449","28058064","28078498"],returnFormat=1)

outData=open("pubtator_all.xml","w")
outData.write(docs)
outData.close()

```

#### QUAERO french corpus (biocxml)
In the example, we also used the QUAERO dataset:

``` tex
Névéol A, Grouin C, Leixa J, Rosset S, Zweigenbaum P.
The QUAERO French Medical Corpus: A Ressource for Medical Entity
Recognition and Normalization. Fourth Workshop on Building and
Evaluating Ressources for Health and Biomedical Text Processing
- BioTxtM2014. 2014:24-30

```
To download the dataset

``` bash
cd data
wget https://quaerofrenchmed.limsi.fr/QUAERO_FrenchMed_BioC.zip
#wget https://quaerofrenchmed.limsi.fr/QUAERO_FrenchMed_brat.zip

unzip QUAERO_FrenchMed_BioC.zip

```
#### CellFinder corpus
 Mariana Neves, Alexander Damaschun, Andreas Kurtz, Ulf Leser. Annotating and evaluating text for stem cell research. Third Workshop on Building and Evaluation Resources for Biomedical Text Mining (BioTxtM 2012) at Language Resources and Evaluation (LREC) 2012. [workshop] [paper]
https://www.informatik.hu-berlin.de/de/forschung/gebiete/wbi/resources/cellfinder

``` bash
cd data
wget https://www.informatik.hu-berlin.de/de/forschung/gebiete/wbi/resources/cellfinder/cellfinder1_brat.tar.gz
mkidr cellfinder
mv cellfinder1_brat.tar.gz cellfinder
tar -zxf cellfinder1_brat.tar.gz

```

### FHIR examples

data are generated from

https://github.com/smart-on-fhir/sample-patients

## library pymedext Usage





# Makefile

```bash

make help
build                          Build dinstance
demo                           start a demo pymdext container to run it
help                           Display available commands in Makefile
install                        local install of pymedext packages
uninstall                      uninstall local pymedext packages


```
# How to used

3) execute bash bin/runInteractive.sh to test it in a docker container

# Documentation (in progress)
 firefox html/modules.html




# TODO

- implement a BratSource.py which open an ssh Connector to a brat Server
- Pymedext to BIOC and specify which annotation are passage
- brat to pymedext
- implement Fhir source by extending source
- It will be done on pymedext_public
  - pymedext to omop
  - fhir to omop
  - fhir to bioc
  - brat to omop
  - pymedext to doccano
  - add omop as (csv) output and furthermore to a db

# DONE
- implement a generic APIConnector with the request function
- add the whole api of Doccano as a Source in an other file called DoccanoSource.py
- Extend datatransform to perform the data wrangling for Doccanotransform.py
- implement datatransform to perform data wrangling for brattransform.py
- implement Bioc output by extending datatransform (done)
- implement Fhir wrangling by extending datatransform (done)

# BIOC
input data from article:
https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/BioC-PMC/

example of file in json:
https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/17299597/unicode

http://bioc.sourceforge.net/

https://pypi.org/project/bioc/

https://www.ncbi.nlm.nih.gov/research/pubtator/api.html

# FHIR

https://github.com/smart-on-fhir/client-py

https://github.com/smart-on-fhir/sample-patients

https://docs.smarthealthit.org/client-py/

https://github.com/smart-on-fhir/fhir-parser

https://github.com/smart-on-fhir/client-py/blob/master/fhirclient/models/documentmanifest.py

---
# BRAT format
https://brat.nlplab.org/standoff.html
