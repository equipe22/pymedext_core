
# pymedext_core
Based on the work of Antoine Neuraz !

pymedext core to extend in order to add new annotators.

# Dataset

based on the QUAERO dataset

``` tex
Névéol A, Grouin C, Leixa J, Rosset S, Zweigenbaum P. The QUAERO French Medical Corpus: A Ressource for Medical Entity Recognition and Normalization. Fourth Workshop on Building and Evaluating Ressources for Health and Biomedical Text Processing - BioTxtM2014. 2014:24-30 

wget https://quaerofrenchmed.limsi.fr/QUAERO_FrenchMed_BioC.zip

wget https://quaerofrenchmed.limsi.fr/QUAERO_FrenchMed_brat.zip

```


# Annotator class
 need to implement the annotator class to expends pymedext

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

# TODO
## Alice
- implement a generic APIConnector with the request function
- add the whole api of Doccano as a Source in an other file called DoccanoSource.py
- Extend datatransform to perform the data wrangling for Doccanotransform.py 

## David
- implement a generic sshConnector with paramiko
- implement a BratSource.py which open an ssh Connector to a brat Server
- implement datatransform to perform data wrangling for brattransform.py 


# otherthings to do
- Pymedext to BIOC and specify which annotation are passage
- brat to pymedext
- add omop as (csv) output and furthermore to a db ( i think this should be done in pymedext)
- same thing for brat
- same thing for doccano (add them to the commandline
- implement Bioc output by extending datatransform (done)
- implement Fhir wrangling by extending datatransform (done)
- implment Fhir source by extending source (not done)

# Example
- no annotation
  - text to pymedext (done)
  - bioc to pymedext (done)
  - fhir to pymedext (done)
  - brat to pymedext (done)
- require annotation
  - pymedext to omop
  - fhir to omop
  - fhir to bioc
  - brat to omop
  - pymedext to doccano

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
