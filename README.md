# pymedext_core
Based on the work of Antoine Neuraz !

pymedext core to extend in order to add new annotators.

# Annotator class
 need to implement the annotator class to expends pymedext

# Makefile

```bash

make help
build                          Build dinstance
help                           Display available commands in Makefile

```

# TODO
## Alice
- implement a generic APIConnector with the request function
- add the whole api of Doccano as a Source in an other file called DoccanoSource
- Extend datatransform to perform the data wrangling for Doccano 

## David
- implement a generic sshConnector with paramiko
- implement a SourceBrat which open an ssh Connector to a brat Server
- implement datatransform to perform data wrangling for brat 


# otherthings to do
- implement Bioc output by extending datatransform
- implement Fhir wrangling by extending datatransform
- implment Fhir source by extending source
