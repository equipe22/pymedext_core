
# Automatic PyMedExt Documentation from sources

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

also to a use case of Documentation example for the Annotation class --> https://equipe22.github.io/pymedext_core/pymedextcore.html?highlight=annotation#pymedext_core.annotators.Annotation




# Examples

## Datasets

All the datasets used in the examples can be found in the data folder

### PubTator (biocxml)
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

### QUAERO french corpus (biocxml)
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


# How to use
## Makefile

```bash

make help
build                          Build dinstance
demo                           start a demo pymdext container to run it
help                           Display available commands in Makefile
install                        local install of pymedext packages
uninstall                      uninstall local pymedext packages


```
## interactive

3) execute bash bin/runInteractive.sh to test it in a docker container




# ROADMAP
## TODO

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

## RELEASED
- implement a generic APIConnector with the request function
- add the whole api of Doccano as a Source in an other file called DoccanoSource.py
- Extend datatransform to perform the data wrangling for Doccanotransform.py
- implement datatransform to perform data wrangling for brattransform.py
- implement Bioc output by extending datatransform (done)
- implement Fhir wrangling by extending datatransform (done)

# REFERENCES

## BIOC
input data from article:
https://www.ncbi.nlm.nih.gov/research/bionlp/APIs/BioC-PMC/

example of file in json:
https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/17299597/unicode

http://bioc.sourceforge.net/

https://pypi.org/project/bioc/

https://www.ncbi.nlm.nih.gov/research/pubtator/api.html

## FHIR

https://github.com/smart-on-fhir/client-py

https://github.com/smart-on-fhir/sample-patients

https://docs.smarthealthit.org/client-py/

https://github.com/smart-on-fhir/fhir-parser

https://github.com/smart-on-fhir/client-py/blob/master/fhirclient/models/documentmanifest.py

## BRAT format
https://brat.nlplab.org/standoff.html
