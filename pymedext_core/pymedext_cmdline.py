#!/usr/bin/env python3

from pymedext_core import pymedext
import argparse

# @click.command()
# # @click.option('--count', default=1, help='Number of greetings.')
# @click.option('--itype',default='txt', type=click.Choice(['txt', 'pymedext','bioc','fhir','brat']), help="input type")
# @click.option('--otype',default='pymedext', type=click.Choice(['omop','pymedext','bioc','fhir','brat']), help = "output type")
# @click.option('--output',default="input",
#               help='enter the outputfile name.')

# @click.option('--inp', prompt='input file',
#               help='The input file name.')




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
    elif itype=="biocxml":
        thisDoc=pymedext.BioC.load_collection(inputfile)
        return(thisDoc)
    elif itype=="biocjson":
        thisDoc= pymedext.BioC.load_collection(pathTofile_json,1)
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
  
def main():
    """Simple program that greets NAME for a total of COUNT times."""

    README = '''example:

     python test.py -i template/test.py
     python test.py -i template/test -c conf/test.conf
     python test.py -i test.py'''
    parser = argparse.ArgumentParser(prog='pymedext',
                                     description='toolkit for Medical Informatics',
                                     epilog=README,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    parser = argparse.ArgumentParser()
    # parser.add_argument("-i","--inputFolder", help="input annotationsFiles")
    parser.add_argument('-i', '--inputFile', help='path to input folder', type=str)
    parser.add_argument('-o', '--output', default="input",  help='enter the output file name', type=str)

    parser.add_argument('--itype',default='txt', choices=['txt', 'pymedext','biocxml','biocjson','fhir','brat'], help="input type")
    parser.add_argument('--otype',default='pymedext', choices=['omop','pymedext','bioc','fhir','brat'], help = "output type")
    #parser.add_argument('-i', '--inputFile', help='path to input folder', type=str)
    # parser.add_argument('-s', '--source', help='if set, switch to english rxnorm sources, if not french  romedi source' ,action="store_true" )
    parser.add_argument('-v','--version', action='version', version='%(prog)s 0.1')
    args = parser.parse_args()

    print(args.inputFile)
    print(args.itype)
    print(args.output)
    print(args.otype)
    rawFileName="".join(args.inputFile.split("/")[-1].split(".")[:-1])
    thisDoc = loadFile(args.inputFile,rawFileName,args.itype)
    if type(thisDoc) is not list:
        export(thisDoc,args.output,args.otype,rawFileName)
    else:
        for data in range(len(thisDoc)):
            export(thisDoc[data],args.output,args.otype,rawFileName+str(data+1))


if __name__ == '__main__':
    main()
