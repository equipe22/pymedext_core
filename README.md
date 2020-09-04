
# Description pymedext_core

pymedext_core contains basic data wrangling function to transform 
input data format txt, pymedext,biocxml,biocjson,fhir,brat
into another one pymedext,biocxml,biocjson,omop,brat.
pymedext core to extend in order to add new annotators.

# Dataset

based on the QUAERO dataset

``` tex
Névéol A, Grouin C, Leixa J, Rosset S, Zweigenbaum P. The QUAERO French Medical Corpus: A Ressource for Medical Entity Recognition and Normalization. Fourth Workshop on Building and Evaluating Ressources for Health and Biomedical Text Processing - BioTxtM2014. 2014:24-30 

wget https://quaerofrenchmed.limsi.fr/QUAERO_FrenchMed_BioC.zip

wget https://quaerofrenchmed.limsi.fr/QUAERO_FrenchMed_brat.zip

```

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

1) create a file config/.git-credentials based on the config/.git-credentials_template 
 http:user:pass@github.com
2) run make build. If you are under proxy modify the bin/build.sh script.
3) execute bash bin/runInteractive.sh to test it in a docker container 

# Documentation (in progress)
 firefox html/modules.html

# Examples

## pymedext command line

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


## call PubTator

``` python
from pymedext_core import pymedext
pub = pymedext.PubTatorSource()
doc = pub.GetPubTatorAnnotations(["27940449","28058064","28078498"])


```


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
