#!/usr/bin/env python3

import click
from pymedext_core import pymedext

@click.command()
@click.option('--count', default=1, help='Number of greetings.')

@click.option('--i', prompt='input file',
              help='The input file name.')

@click.option('--output',default="input",
              help='enter the outputfile name.')

@click.option('--itype',default='txt', type=click.Choice(['txt', 'pymedext','bioc','fhir','brat'], help="input type"))
@click.option('--otype',default='pymedext', type=click.Choice(['omop','pymedext','bioc','fhir','brat'], help = "output type"))

@click.option('--name', prompt='Your name',
              help='The person to greet.')
@click.option('--count', default=1, help='Number of greetings.')

# def main(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('main %s!' % name)

def loadFile(inputfile,rawFileName):
     if itype=="txt":
        thisFile=open(inputfile,"r").read()
        thisDoc=Document(raw_text=thisFile, ID=rawFileName)
        return(thisDoc)
     else:
         return(Document(raw_text="thisFile", ID=rawFileName))

def export(thisDoc,output,otype,rawFileName):
     if otype=="pymedext":
         if output=="input":
             thisDoc.writeJson(rawfileName+".json")
        else:
             thisDoc.writeJson(output+".json")
    return(0)
  
def main(i,output,itype,otype):
    """Simple program that greets NAME for a total of COUNT times."""
    rawFileName=i.split("/")[-1].replace(itype,"")
    thisDoc = loadFile(i,rawFileName)
    export(thisDoc,output,otype,rawFileName)


if __name__ == '__main__':
    main()
