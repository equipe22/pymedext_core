from source import Source
from connector import *

class DoccanoSource(Source,APIConnector):
    """
    Connection to DoccanoClient
    """

    def __init__(self, baseurl, username, password):
        """

        :param baseurl:
        :param username:
        :param password:
        """
        super().__init__(baseurl, username, password)

    def get_me(self) -> requests.models.Response:
        """
        Gets this account information.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/me')

    def get_features(self) -> requests.models.Response:
        """
        Gets features.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/features')

    def get_project_list(self) -> requests.models.Response:
        """
        Gets projects list.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/projects')

    def get_user_list(self) -> requests.models.Response:
        """
        Gets user list.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/users')

    def get_roles(self) -> requests.models.Response:
        """
        Gets available Doccano user roles.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/roles')

    def get_project_detail(
            self,
            project_id: int
    ) -> requests.models.Response:
        """
        Gets details of a specific project.

        Args:
            project_id (int): A project ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}'.format(
                project_id=project_id
            )
        )

    def get_project_statistics(
            self,
            project_id: int
    ) -> requests.models.Response:
        """
        Gets project statistics.

        Args:
            project_id (int): A project ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/statistics'.format(
                project_id=project_id
            )
        )

    def get_label_list(
            self,
            project_id: int
    ) -> requests.models.Response:
        """
        Gets a list of labels in a given project.

        Args:
            project_id (int): A project ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/labels'.format(
                project_id=project_id
            )
        )

    def get_label_detail(
            self,
            project_id: int,
            label_id: int
    ) -> requests.models.Response:
        """
        Gets details of a specific label.

        Args:
            project_id (int): A project ID to query.
            label_id (int): A label ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/labels/{label_id}'.format(
                project_id=project_id,
                label_id=label_id
            )
        )

    def get_document_list(
            self,
            project_id: int,
            url_parameters: dict = {}
    ) -> requests.models.Response:
        """
        Gets a list of documents in a project.

        Args:
            project_id (int):
            url_parameters (dict): `limit` and `offset`

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/docs{url_parameters}'.format(
                project_id=project_id,
                url_parameters=self.build_url_parameter(url_parameters)
            )
        )

    def get_document_detail(
            self,
            project_id: int,
            doc_id: int
    ) -> requests.models.Response:
        """
        Gets details of a given document.

        Args:
            project_id (int): A project ID to query.
            doc_id (int): A document ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/docs/{doc_id}'.format(
                project_id=project_id,
                doc_id=doc_id
            )
        )

    def get_annotation_list(
            self,
            project_id: int,
            doc_id: int
    ) -> requests.models.Response:
        """
        Gets a list of annotations in a given project and document.

        Args:
            project_id (int): A project ID to query.
            doc_id (int): A document ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/docs/{doc_id}/annotations'.format(
                project_id=project_id,
                doc_id=doc_id
            )
        )

    def get_annotation_detail(
            self,
            project_id: int,
            doc_id: int,
            annotation_id: int
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/docs/{doc_id}/annotations/{annotation_id}'.format(
                project_id=project_id,
                doc_id=doc_id,
                annotation_id=annotation_id
            )
        )

    def get_doc_download(
            self,
            project_id: int,
            file_format: str = 'json'
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/docs/download?q={file_format}'.format(
                project_id=project_id,
                file_format=file_format
            )
        )

    def get_rolemapping_list(
            self,
            project_id: int,
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/roles'.format(
                project_id=project_id
            )
        )

    def get_rolemapping_detail(
            self,
            project_id: int,
            rolemapping_id: int,
    ) -> requests.models.Response:
        """
        Currently broken!
        """
        return self.get(
            'v1/projets/{project_id}/roles/{rolemapping_id}'.format(
                project_id=project_id,
                rolemapping_id=rolemapping_id
            )
        )

    def post_doc_upload(
            self,
            project_id: int,
            file_format: str,
            file_name: str,
            file_path: str = './',
    ) -> requests.models.Response:
        """
        Uploads a file to a Doccano project.

        Args:
            project_id (int): The project id number.
            file_format (str): The file format, ex: `plain`, `json`, or `conll`.
            file_name (str): The name of the file.
            file_path (str): The parent path of the file. Defaults to `./`.

        Returns:
            requests.models.Response: The request response.
        """
        files = {
            'file': (
                file_name,
                open(os.path.join(file_path, file_name), 'rb')
            )
        }
        data = {
            'file': (
                file_name,
                open(os.path.join(file_path, file_name), 'rb')
            ),
            'format': file_format
        }
        return self.post(
            'v1/projects/{project_id}/docs/upload'.format(
                project_id=project_id
            ),
            files=files,
            data=data
        )

    def post_approve_labels(
            self,
            project_id: int,
            doc_id: int
    ) -> requests.models.Response:
        """
        """
        return self.post(
            'v1/projects/{project_id}/docs/{doc_id}/approve-labels'.format(
                project_id=project_id,
                doc_id=doc_id
            )
        )

    def _get_any_endpoint(
            self,
            endpoint: str
    ) -> requests.models.Response:
        """
        """
        # project_id: int,
        # limit: int,
        # offset: int
        return self.get(endpoint)

    def exp_get_doc_list(
            self,
            project_id: int,
            limit: int,
            offset: int
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/docs?limit={limit}&offset={offset}'.format(
                project_id=project_id,
                limit=limit,
                offset=offset
            )
        )


###########################################
###########################################
########################################### Méthodes construites

    def create_project(self,
                       name: str,
                       description: str,
                       project_type: str,
                       guidelines: str) -> requests.models.Response:
        """
        Créee un projet
        :param name:
        :param description:
        :param project_type:
        :return:
        """
        mapping = {'SequenceLabeling': 'SequenceLabelingProject',
                   'DocumentClassification': 'TextClassificationProject',
                   'Seq2seq': 'Seq2seqProject'}
        data = {
            'name': name,
            'project_type': project_type,
            'description': description,
            'guideline': guidelines,
            'resourcetype': mapping[project_type]
        }
        return self.post(
            'v1/projects',
            data=data
        )

    def create_label(self,
                     project_id: str,
                     label_name: str,
                     color: str,
                     prefix : str,
                     suffix : str) -> requests.models.Response:
        """
        Créé un label
        :param self:
        :param project_id:
        :param label_name:
        :return:
        """

        if color is None :
            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())
        elif color == "rouge":
            color = "#E84B3C"
        elif color == "vert":
            color = "#2ECC70"
        elif color == "orange":
            color = "#F39C19"
        elif color == "violet":
            color = "#8E43AD"
        elif color == "jaune":
            color = "#F2C511"
        elif color == "bleu":
            color = "#3398DB"
        else :
            r = lambda: random.randint(0, 255)
            color = '#%02X%02X%02X' % (r(), r(), r())


        data = {
            'text': label_name,
            'background_color': color,
            'prefix_key': prefix,
            'suffix_key': suffix
        }

        return self.post(
            'v1/projects/{project_id}/labels'.format(
                project_id=project_id),
            data=data
        )



    def set_rolemapping_list(self,
            project_id: str,
            user_id: str,
            role_id: str,
            username: str,
            rolename: str
    ) -> requests.models.Response:
        """
        """

        data = {
            #'id':rolemapping_id,
            'user': user_id,
            'role': role_id,
            'username': username,
            'rolename': rolename
        }


        return self.post(
            'v1/projects/{project_id}/roles'.format(
                project_id=project_id
            ),
            data=data
        )


    def get_user_id(self,
                    username: str
                    ) :
        user_list = self.get_user_list().json()

        i=0
        el = user_list[i]

        while el['username'] != username and i < len(user_list) :
            el = user_list[i]
            i += 1

        if el['username'] == username :
            return el['id']
        else :
            return "No such a username (" + username +  ") exists."


    def get_project_id(self,
                       project_name :str
                       ):
        project_list = self.get_project_list().json()

        i=0
        el=project_list[i]

        while el['name'] != project_name and i < len(project_list) :
            el = project_list[i]
            i +=1

        if el['name'] == project_name :
            return el['id']
        else :
            return "No such a project name (" + project_name +  ") exists."



    def get_label_id(self,
                     project_id: int,
                     label_name: str
                     ):

        labels_list = self.get_label_list(project_id).json()
        i=0
        el=labels_list[i]

        while el['text'] != label_name and i < len(labels_list):
            el = labels_list[i]
            i += 1

        if el['text'] == label_name :
            return el['id']
        else :
            return "No such a label name (" + label_name + ") exists in project " + str(project_id) + "."


    def find_project_id(self,
                        regex : str,
                        date : str,
                        time : str):
        list_of_matches = []
        list_project_names = [dict_project['name'] for dict_project in self.get_project_list().json()]
        for name in list_project_names :
            if re.search(regex, name) is not None:
                list_of_matches.append(self.get_project_id(name))

        if len(list_of_matches) > 0 :
            if len(list_of_matches) > 1 :
                if date is None:
                    print("Several projects exist with this regex expression (" + regex + "). Please enter the date and/or the time to select the good one.")
                else :
                    list_of_matches_with_date = []
                    for id in list_of_matches :
                        if re.search(str(date), self.get_project_detail(id).json()['name']) is not None :
                            list_of_matches_with_date.append(id)
                    if len(list_of_matches_with_date) > 0 :
                        if len(list_of_matches_with_date) > 1 :
                            if time is None :
                                print("Several projects exist with this regexp expression (" + regex + ") and this date (" + str(date) +"). Please enter the time to select the good one.")
                            else :
                                list_of_matches_with_date_and_time=[]
                                for id in list_of_matches_with_date:
                                    if re.search(time, self.get_document_detail(id).json()['name']) is not None :
                                        list_of_matches_with_date_and_time.append(id)
                                if len(list_of_matches_with_date_and_time) > 0 :
                                    if len(list_of_matches_with_date_and_time) > 1 :
                                        return "Several projects (", list_of_matches_with_date_and_time, ") with exactly the same name"
                                    else :
                                        return list_of_matches_with_date_and_time[0]
                                else :
                                    return "No project found."
                        else :
                            return list_of_matches_with_date[0]
                    else :
                        return "No project found."
            else :
                return list_of_matches[0]
        else :
            return "No project found."