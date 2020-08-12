#!/usr/bin/env python3

import click
from pymedext_core import pymedext

@click.command()
# @click.option('--count', default=1, help='Number of greetings.')
@click.option('--itype',default='txt', type=click.Choice(['txt', 'pymedext','bioc','fhir','brat']), help="input type")
@click.option('--otype',default='pymedext', type=click.Choice(['omop','pymedext','bioc','fhir','brat']), help = "output type")
@click.option('--output',default="input",
              help='enter the outputfile name.')

@click.option('--inp', prompt='input file',
              help='The input file name.')



# @click.option('--name', prompt='Your name',
              # help='The person to greet.')
# @click.option('--count', default=1, help='Number of greetings.')

# def main(count, name):
#     """Simple program that greets NAME for a total of COUNT times."""
#     for x in range(count):
#         click.echo('main %s!' % name)

def loadFile(inputfile,rawFileName,itype):
    if itype=="txt":
        thisFile=open(inputfile,"r").read()
        thisDoc=pymedext.Document(raw_text=thisFile, ID=rawFileName)
        return(thisDoc)
    else:
        return(pymedext.Document(raw_text="thisFile", ID=rawFileName))

def export(thisDoc,output,otype,rawFileName):
    if otype=="pymedext":
        if output=="input":
            thisDoc.writeJson(rawFileName+".json")
        else:
            thisDoc.writeJson(output+".json")
    return(0)
  
def main(itype, otype, output , inp):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo("go in main function %s!" % inp)
    click.echo("go in main function %s!" % itype)
    click.echo("go in main function %s!" % otype)
    click.echo("go in main function %s!" % output)

    print(inp)
    print(itype)
    print(output)
    print(otype)
    rawFileName=inp.split("/")[-1].replace(itype,"")
    thisDoc = loadFile(inp,rawFileName,itype)
    export(thisDoc,output,otype,rawFileName)


if __name__ == '__main__':
    main()
