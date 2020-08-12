
# pymedext_core
Based on the work of Antoine Neuraz !

pymedext core to extend in order to add new annotators.

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
- implement Bioc output by extending datatransform
- implement Fhir wrangling by extending datatransform
- implment Fhir source by extending source

demo
# Example
- text to pymedext
- bioc to pymedext
- fhir to pymedext
- brat to pymedext
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
