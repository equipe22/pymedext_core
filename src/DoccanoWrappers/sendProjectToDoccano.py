from pymedext_core import pymedext
import sys
import time
import random
import csv


def usage(): print(
    """
    annot_in_doccano.py :

    Annote sous doccanno le fichier mis en entrée sous le bon format.

    usage :
    annot_in_doccano.py 
    -ent <url du serveur doccano> par défaut
    -us <username> 'admin' par défaut
    -pas <password> 'password' par défaut
    -time <timesleep> 2 secondes par défaut, temps donné pour que le serveur réponde
    -pro <nom du projet> 'projetZ' par défaut
    -des <description du projet> 'description' par défaut
    -type <type de projet> trois types possibles : SequenceLabeling', 'DocumentClassification' ou 'Seq2seq','DocumentClassification' par défaut
    -dir <répertoire du fichier à annoter> '../examples_input_doccano/classification/' par défaut
    -fname <nom du fichier à annoter> 'neg_pos_test.jsonl' par défaut
    -format <format> format du fichier d'entrée ('conll', 'plain', 'json') 'json' par défaut
    -labels <noms des labels séparés par des ';'> Vaut 'None' par défaut. 


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
            guidelines = "guidelines"

    # Création du client Doccano
    doccano_client = pymedext.DoccanoSource(entrypoint, username, password)

    # Création d'un projet
    if project_description == "precision":

        project_description = "Évaluation de la précision de l'extracteur pour les compte-rendus d'imagerie."
        guidelines = "On recherche ici à savoir si l'extracteur a extrait la bonne information. \n L'information extraite est stipulée après 'valeur extraite' et concerne l'item ci-dessus (EN-DESSOUS de l'encadré bleu). Son context est présent dans le snippet. Veuillez préciser si la valeur extraite de l'item est correcte, incorrecte ou partiellement correcte en cliquant sur le label correspondant (ou en tapant sur les raccourcis clavier)."

    elif project_description == "rappel":
        project_description = "Évaluation du rappel de l'extracteur pour les comptes-rendus d'imagerie"
        guidelines = "Dans l'encadré bleu, la liste des items absents possibles. \n Au-dessus du compte-rendu, le ou les terme(s) manquant(s) trouvé(s).\n Retirez-le(s) s'ils est/sont présent(s) dans le compte-rendu. \n Si d'autres items sont également absents du compte-rendu, ajoutez-les."
    project = doccano_client.create_project(name=project_name, description=project_description,
                                            project_type=project_type, guidelines=guidelines)

    # Téléchargement d'un fichier annoté (json) ou non (texte brut)
    time.sleep(timesleep)
    project_id = project.json()['id']
    r_json_upload = doccano_client.post_doc_upload(project_id=project_id, file_format=format, file_name=file,
                                                   file_path=dir)

    # Ajouts des labels spécifiés
    if labels is not None:

        time.sleep(timesleep)
        FILE = False

        # lire les labels à partir d'un fichier
        if "/" in labels:
            try:
                with open(labels, 'r') as csvfile:
                    csvreader = csv.reader(csvfile, delimiter=',')
                    list_labels = [rows[0] for rows in csvreader]
                    FILE = True

            except ValueError:
                print("The labels file ", labels, "does not exist")
                sys.exit()

        if FILE:

            if len(list_labels) < 37:

                shortcuts = random.sample(
                    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z',
                     '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], len(list_labels))

                i = 0

                for label in list_labels:
                    shortcut = shortcuts[i]

                    i += 1

                    time.sleep(timesleep)
                    doccano_client.create_label(project_id=project_id, label_name=label, color=None, prefix=None,
                                                suffix=shortcut)

            elif len(list_labels) < 109:  # 36 * 3
                shortcuts = random.sample(
                    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                     'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'], 36)

                i = 0
                j = 0
                k = 0

                for label in list_labels:

                    i += 1
                    if i < 36:
                        shortcut = shortcuts[i]
                        time.sleep(timesleep)
                        doccano_client.create_label(project_id=project_id, label_name=label, color=None, prefix=None,
                                                    suffix=shortcut)
                    elif j < 36:
                        shortcut = shortcuts[j]
                        time.sleep(timesleep)
                        doccano_client.create_label(project_id=project_id, label_name=label, color=None, prefix="shift",
                                                    suffix=shortcut)
                        j += 1

                    elif k < 36:
                        shortcut = shortcuts[k]
                        time.sleep(timesleep)
                        doccano_client.create_label(project_id=project_id, label_name=label, color=None, prefix="ctrl",
                                                    suffix=shortcut)
                        k += 1

            else:
                print("There are too much labels.")


        # list_text_existing_label=[]
        # if len(doccano_client.get_label_list(project_id).json()) > 0:
        #     for existing_label in doccano_client.get_label_list(project_id).json() :
        #         list_text_existing_label.append(existing_label['text'])

        else:

            if ";" in labels:

                if "," in labels:  # Infos sur couleur de label +  shortcut

                    labels = labels.split("|")

                    for label in labels:
                        label = label.split(";")
                        text = label[0]
                        c_s = label[1].split(",")
                        color = c_s[0]
                        shortcut = c_s[1]
                        time.sleep(timesleep)
                        doccano_client.create_label(project_id=project_id, label_name=text, color=color, prefix=None,
                                                    suffix=shortcut)


                else:  # Info sur couleur seulement :

                    labels = labels.split("|")

                    shortcuts = random.sample(
                        ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                         't', 'u', 'v', 'w', 'x', 'y', 'z'], len(labels))
                    i = 0

                    for label in labels:
                        shortcut = shortcuts[i]
                        i += 1

                        label = label.split(";")
                        text = label[0]
                        color = label[1]
                        # if text not in list_text_existing_label :
                        time.sleep(timesleep)
                        doccano_client.create_label(project_id=project_id, label_name=text, color=color, prefix=None,
                                                    suffix=shortcut)

            elif "," in labels:  # Info sur shortcut seulement :

                labels = labels.split("|")

                i = 0

                for label in labels:
                    i += 1
                    label = label.split(",")
                    text = label[0]
                    shortcut = label[1]

                    time.sleep(timesleep)
                    doccano_client.create_label(project_id=project_id, label_name=text, color=None, prefix=None,
                                                suffix=shortcut)


            else:  # Pas d'infos sur la couleur ou le shortcut

                labels = labels.split("|")

                shortcuts = random.sample(
                    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                     't', 'u', 'v', 'w', 'x', 'y', 'z'], len(labels))

                i = 0

                for label in labels:
                    shortcut = shortcuts[i]

                    i += 1

                    time.sleep(timesleep)
                    doccano_client.create_label(project_id=project_id, label_name=label, color=None, prefix=None,
                                                suffix=shortcut)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))