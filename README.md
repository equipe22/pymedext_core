
# Description pymedext_core

pymedext_core contains basic data wrangling function to transform 
input data format txt, pymedext,biocxml,biocjson,fhir,brat
into another one pymedext,biocxml,biocjson,omop,brat.
pymedext core to extend in order to add new annotators.

# Install

## package 
### pip install
```bash

pip3 install git+https://github.com/equipe22/pymedext_core.git


```

### make
```bash

#local install of pymedext packages
make install 


```

## docker image
first create a file config/.git-credentials based on the config/.git-credentials_template 
 http:user:pass@github.com

## docker command line
```bash

docker build -t pymedext-core:v0.0.2 .


```

### make
```bash

#build docker instance
make build 

```

# Examples

## Datasets

all dataset used are on located on the data folder

### PubTator (biocxml)
We have implemented Pubtator as a resource for pymedext

### QUAERO french corpus (biocxml)
based on the QUAERO dataset

``` tex
Névéol A, Grouin C, Leixa J, Rosset S, Zweigenbaum P. 
The QUAERO French Medical Corpus: A Ressource for Medical Entity
Recognition and Normalization. Fourth Workshop on Building and
Evaluating Ressources for Health and Biomedical Text Processing 
- BioTxtM2014. 2014:24-30 

```
download the dataset

``` bash
cd data
wget https://quaerofrenchmed.limsi.fr/QUAERO_FrenchMed_BioC.zip
#wget https://quaerofrenchmed.limsi.fr/QUAERO_FrenchMed_brat.zip

unzip QUAERO_FrenchMed_BioC.zip

```


### CellFinder corpus
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

### Get Data from PubTator
``` python
from pymedextcore import pymedext
pub = pymedext.PubTatorSource()
docs = pub.GetPubTatorAnnotations(["27940449","28058064","28078498"])


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

## pymedext commandline

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
