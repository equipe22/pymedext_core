from pymedext_core import pymedext

import sys
import time


def usage(): print(
    """
    add_users_roles.py :

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
        set_roles = argv[argv.index("--setroles") + 1]
    except ValueError:
        try:
            set_roles = argv[argv.index("-roles") + 1]
        except ValueError:
            set_roles = "Hippolyte:annotation_approver;Laure:annotation_approver"

    for_projects = "--project_names" in argv


    # Création du client Doccano
    doccano_client = pymedext.DoccanoSource(entrypoint, username, password)


    if for_projects :

        try:
            project_names = argv[argv.index("--project_names") + 1]
        except ValueError:
            print("Please precise the names of the projects separated by ';' or don't put this option if you want set the roles in all projects.'")
            sys.exit()

        list_project_names=project_names.split(";")

        user_role_couple_list = set_roles.split(";") # [Laure:annotation_approver,Hippolyte:annotator]

        for project_name in list_project_names :

            project_id = doccano_client.get_project_id(project_name=project_name)

            for user_role_couple in user_role_couple_list:

                user_role_couple = user_role_couple.split(":")

                username = user_role_couple[0]
                role = user_role_couple[1]

                if role == "annotator":
                    role_id = '2'
                elif role == "annotation_approver":
                    role_id = '3'
                else:
                    print("The role " + role + " does not exist. Please chose between annotator and annotation_approver.")
                    sys.exit()

                user_id = doccano_client.get_user_id(username=username)
                if type(user_id) == str:
                    print(user_id)
                    sys.exit()
                else:
                    time.sleep(timesleep)
                    doccano_client.set_rolemapping_list(project_id=project_id, user_id=user_id, role_id=role_id, username=username,
                                                        rolename=role)


    else :


        list_id_projects=[el['id'] for el in doccano_client.get_project_list().json()]

        user_role_couple_list = set_roles.split(";") # [Laure:annotation_approver,Hippolyte:annotator]
        print("listusercouple",user_role_couple_list)

        for project_id in list_id_projects :


            for user_role_couple in user_role_couple_list :


                user_role_couple = user_role_couple.split(":")

                username = user_role_couple[0]
                role = user_role_couple[1]

                print("username",username)

                if role == "annotator" :
                    role_id = '2'
                elif role == "annotation_approver":
                    role_id = '3'
                else :
                    print("The role " + role + " does not exist. Please chose between annotator and annotation_approver.")
                    sys.exit()

                user_id = doccano_client.get_user_id(username=username)
                if type(user_id) == str:
                    print(user_id)
                    sys.exit()
                else :
                    time.sleep(timesleep)
                    doccano_client.set_rolemapping_list(project_id=project_id, user_id=user_id, role_id=role_id, username=username,rolename=role)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))