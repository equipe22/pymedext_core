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