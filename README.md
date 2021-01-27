
# PyMedExt - a library to process clinical text

PyMedExt is a library designed to process clinical text.
PyMedExt includes basic data wrangling functions to transform
text input formated as txt, pymedext,biocxml,biocjson,fhir, or brat
into pymedext, biocxml, biocjson, omop or brat.

PyMedExt also includes an easy way to define Annotator.
## Requirements
### Installation
#### Using pip

```bash

pip3 install git+https://github.com/equipe22/pymedext_core.git

```

# Tutorials


## Add an Annotator
if you want to expand PyMedExt and add a new Annotator.
First you need create a new class which extend the annotators.Annotator class.
After that you will need to extend two functions.

- __init__
- annotate_function


### the GREP use case

grep is a linux command-line which allow you to search into plain-text data sets
for lines that match a regular expression.
The script grepWrapperAnnotator.py located on the src
directory, is a wrapper around grep.

this wrapper takes as resources two files :
- regexResource.txt --> a one column list of words to search in a text
- pivotResource.csv --> a two columns list of words: pattern, normalizewords

#### Define the Grep Annotator

##### __init__()

The init function must contains
- key_input --> the type of Annotation's input used by the Annotator, here  "raw_text"
- key_output --> the type of the Annotation's output by the Annotator, here "regex_fast"
- ID --> the tool ID, eventually the tool git repository address and version
- other arguments are specific to the type of the defined Annotator


```python
from pymedextcore import annotators
class regexFast(annotators.Annotator):
    """
    Annotator based on linux grep to search regex from a source file
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

The annotate_function must contains
- _input --> Annotations associated with the Document to annotate
- returns --> Annotations ( a list of annotations object )

```python

def annotate_function(self, _input):
    """ main annotation function
    :param _input: in this case raw_text
    :returns: a list of annotations
    :rtype:
    """
    logger.debug(_input)
    #get_key_input: return the annotations oF Documents.annotations which have
    # the same type of the i th key_input element
    inp = self.get_key_input(_input,0)[0]
    fileAnnotation,countValue=self.makeMatch(inp)
    countValue=self.setPivot(countValue)
    logger.debug(countValue)
    annotations=[]
    for matchPos in list(fileAnnotation.keys()):
        for thisMatch in fileAnnotation[matchPos]:
            ID = str(uuid.uuid1())
            attributes={"ngram":thisMatch}
            annotations.append(annotators.Annotation(type= self.key_output,
                                          value=countValue[thisMatch]["normalized"], #thisMatch,
                                          span=(int(matchPos), int(matchPos)+len(thisMatch)),
                                          source=self.ID,
                                          isEntity=True,
                                          ID=ID,
                                          attributes=attributes,
                                          source_ID = inp.ID))
    return(annotations)
```



##### Use the Annotator in a python script
First, clone the pymedext_core git repository and go to the src directory

``` bash
git clone https://github.com/equipe22/pymedext_core.git
cd pymedext_core/src

# go in python interactive mode
python3
```

``` python

#import dependencies
from grepWrapperAnnotator import regexFast # contains your local annotator
from pymedextcore import pymedext # contains all pymedextcore  objects
import os
import logging

logging.basicConfig(level=logging.DEBUG)
resourcePath=os.getcwd().replace("src","ressources/")
thisDoc=pymedext.Document(raw_text= " a document demo you want to work with and contains evidence of. covid 19, sras, sars ", ID="ID01")


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
#write your annotation in PymedExt json
thisDoc.writeJson("outputfile.json")

```




## PyMedExt commandline (in progress)

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
