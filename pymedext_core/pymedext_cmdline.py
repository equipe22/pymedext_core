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
        thisDoc= pymedext.BioC.load_collection(inputfile,1)
        return(thisDoc)
    elif itype=="fhir":
        thisDoc= pymedext.FHIR.load_xml(inputfile)
        return(thisDoc)

    else:
        return(pymedext.Document(raw_text="thisFile", ID=rawFileName))

def export(thisDoc,otype,rawFileName):
    if otype=="pymedext":
        thisDoc.writeJson(rawFileName+".json")
    if otype=="brat":
        pymedext.brat.save(thisDoc,rawFileName+".ann",["raw_text","drwh_cleantext"])

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
    parser.add_argument('--otype',default='pymedext', choices=['omop','pymedext','bioc','brat'], help = "output type")
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
        if args.output=="input":
            export(thisDoc,args.otype,rawFileName)
        else:
            export(thisDoc,args.otype,rawFileName)
    else:
        for data in range(len(thisDoc)):
            if args.output=="input":
                export(thisDoc[data],args.otype,rawFileName+"_"+str(data+1)+"_"+thisDoc[data].ID.replace("/","_"))
            else:
                export(thisDoc[data],args.otype,args.output+"_"+str(data+1)+"_"+thisDoc[data].ID.replace("/","_"))


if __name__ == '__main__':
    main()
