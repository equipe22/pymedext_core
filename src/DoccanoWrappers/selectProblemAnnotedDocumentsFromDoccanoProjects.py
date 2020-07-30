from pymedext_core import pymedext

import sys
import os

import os.path
import re
import time
import random
import csv


import sys



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
        project_name = argv[argv.index("--project_name") + 1]
    except ValueError:
        try:
            project_name = argv[argv.index("-pro") + 1]
        except ValueError:
            project_name = "projetZ"

    try:
        project_description = argv[argv.index("--project_description") + 1]
    except ValueError:
        try:
            project_description = argv[argv.index("-desc") + 1]
        except ValueError:
            project_description = "description"

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
            dir = "../examples_input_doccano/classification/"

    try:
        file = argv[argv.index("--file_name") + 1]
    except ValueError:
        try:
            file = argv[argv.index("-fname") + 1]
        except ValueError:
            file = "neg_pos_test.jsonl"

    try:
        format = argv[argv.index("--file_format") + 1]
    except ValueError:
        try:
            format = argv[argv.index("-format") + 1]
        except ValueError:
            format = "json"

    try:
        labels = argv[argv.index("--add_labels") + 1]
    except ValueError:
        try:
            labels = argv[argv.index("-labels") + 1]
        except ValueError:
            labels = None

    try:
        guidelines = argv[argv.index("--guidelines") + 1]
    except ValueError:
        try:
            guidelines = argv[argv.index("-guide") + 1]
        except ValueError:
            guidelines = "Veuillez à nouveau cliquer sur l'un des labels pour signaler une extraction correcte incorrecte ou partiellement correcte."

    try:
        problem_dir = argv[argv.index("--problem_dir") + 1]
    except ValueError:
        try:
            problem_dir = argv[argv.index("-pbdir") + 1]
        except ValueError:
            problem_dir = "../../pb_doccano/"


    # Création du client Doccano
    doccano_client = pymedext.DoccanoSource(entrypoint, username, password)

    dict_doc_with_problem={}

    for project in doccano_client.get_project_list().json():
        problem_id = doccano_client.get_label_id(project_id=project['id'], label_name="probleme")
        if type(problem_id) == int :
            for doc in doccano_client.get_document_list(project_id=project['id']).json()['results'] :
                labels_list_of_the_project = [el['label'] for el in doccano_client.get_annotation_list(project_id=project['id'], doc_id=doc['id']).json()]
                if problem_id in labels_list_of_the_project :
                    regexp = re.search("_ima_([A-Z]+)", doccano_client.get_project_detail(project['id']).json()['name']).group(1)
                    pymedext_name=eval(doc['meta'])['pymedext_name']
                    dict_doc_with_problem[pymedext_name]=regexp



    for pymedext_name in dict_doc_with_problem :

        project_description = "Voici les textes des comptes-rendus qui ont été annotés probleme pour " + dict_doc_with_problem[pymedext_name]

        name_doc_pb = "PROBLEME_" + dict_doc_with_problem[pymedext_name] + "_" + os.path.basename(pymedext_name)

        project_name = name_doc_pb

        docFromJsonPb = Document.loadFromJson(pymedext_name)
        dictToDoccanoPb = Document.to_doccano_pb(docFromJsonPb, path_to_doc = pymedext_name, regexp = dict_doc_with_problem[pymedext_name])
        thisDoccanoPb = Document.docForDoccanoPb(dict_doccano_pb=dictToDoccanoPb)


        if problem_dir[-1] != "/":
            problem_dir = problem_dir + "/"

        if not os.path.isdir(problem_dir):
            os.mkdir(problem_dir)

        thisDoccanoPb.writeJson_doccano(problem_dir + name_doc_pb)

        # Création d'un projet
        time.sleep(timesleep)
        project = doccano_client.create_project(name=project_name, description=project_description,
                                                project_type=project_type, guidelines=guidelines)

        # Téléchargement d'un fichier annoté (json) ou non (texte brut)
        time.sleep(timesleep)
        project_id = project.json()['id']
        r_json_upload = doccano_client.post_doc_upload(project_id=project_id, file_format=format, file_name=name_doc_pb,
                                                       file_path=problem_dir)

        doccano_client.create_label(project_id=project_id, label_name="correct", color="vert", prefix=None,
                                    suffix="c")

        doccano_client.create_label(project_id=project_id, label_name="incorrect", color="rouge", prefix=None,
                                    suffix="i")

        doccano_client.create_label(project_id=project_id, label_name="partiellement correct", color="orange", prefix=None,
                                    suffix="p")

        doccano_client.create_label(project_id=project_id, label_name="probleme", color="jaune", prefix=None,
                                    suffix="o")





if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))