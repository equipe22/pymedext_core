from pymedext_core import pymedext

import sys
import time
import os
import re


def usage(): print(
    """
    annot_in_doccano.py :

    Ajoute des documents à des projets sous doccano.

    usage :
    add_documents_to_projects.py 
    -ent <url du serveur doccano> par défaut
    -us <username> 'admin' par défaut
    -pas <password> 'password' par défaut
    -time <timesleep> 2 secondes par défaut, temps donné pour que le serveur réponde
    -dir <répertoire du fichier à annoter> '../examples_input_doccano/classification/' par défaut
    -format <format> format du fichier d'entrée ('conll', 'plain', 'json') 'json' par défaut
    -regex <le nom de la regex du projet dans lequel on veut ajouter des documents>
    -dateproj <la date du projet dans lequel on veut ajouter des documents>
    -timeproj <l'heure du projet dans lequel on veut ajouter des documents>

    """
)


def main(argv=None):
    if "-h" in argv or "--help" in argv:
        usage()
        sys.exit()

    try:
        entrypoint = argv[argv.index("--entrypoint") + 1]
    except ValueError:
        try:
            entrypoint = argv[argv.index("-ent") + 1]
        except ValueError:
            entrypoint = "http://127.0.0.1:8000"

    try:
        timesleep = int(argv[argv.index("--timesleep") + 1])
    except ValueError:
        try:
            timesleep = int(argv[argv.index("-time") + 1])
        except ValueError:
            timesleep = 1

    try:
        username = argv[argv.index("--username") + 1]
    except ValueError:
        try:
            username = argv[argv.index("-us") + 1]
        except ValueError:
            username = "admin"

    try:
        password = argv[argv.index("--password") + 1]
    except ValueError:
        try:
            password = argv[argv.index("-pas") + 1]
        except ValueError:
            password = "password"

    try:
        project_type = argv[argv.index("--project_type") + 1]
    except ValueError:
        try:
            project_type = argv[argv.index("-type") + 1]
        except ValueError:
            project_type = "DocumentClassification"

    try:
        dir = argv[argv.index("--directory") + 1]
    except ValueError:
        try:
            dir = argv[argv.index("-dir") + 1]
        except ValueError:
            dir = "/home/alice/04-06_nextflow_ima_neg_hyp_fam_evaluations/evaluations_files/"


    try:
        format = argv[argv.index("--file_format") + 1]
    except ValueError:
        try:
            format = argv[argv.index("-format") + 1]
        except ValueError:
            format = "json"

    try:
        regex = argv[argv.index("--regex") + 1]
    except ValueError:
        try:
            regex = argv[argv.index("-reg") + 1]
        except ValueError:
            regex = "ISCOVID"

    try:
        regex = argv[argv.index("--dateproject") + 1]
    except ValueError:
        try:
            dateproj = argv[argv.index("-dateproj") + 1]
        except ValueError:
            dateproj = None

    try:
        regex = argv[argv.index("--timeproject") + 1]
    except ValueError:
        try:
            timeproj = argv[argv.index("-timeproj") + 1]
        except ValueError:
            timeproj = None


    # Création du client Doccano
    doccano_client = pymedext.DoccanoSource(entrypoint, username, password)

    list_new_eval = os.listdir(dir)
    i=0

    print("hééého")


    # Trouver le fichier eval avec la regex
    while re.search(regex,list_new_eval[i]) is None and i < len(list_new_eval) + 1 :
        print("i",i)
        print(list_new_eval[i])
        i += 1

    if re.search(regex, list_new_eval[i]) is not None :

        eval_file = list_new_eval[i]
        print("There is", eval_file)

        # Trouver le projet dans doccano avec la regex
        project_id = doccano_client.find_project_id(regex=regex, date=dateproj, time=timeproj)
        time.sleep(timesleep)

        # Poster les docs en plus dans le bon projet
        doccano_client.post_doc_upload(project_id=project_id, file_format="json", file_name=eval_file, file_path=dir)

    else :
        print("There is no eval file with this regex (" + regex + ") in " + dir)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))









