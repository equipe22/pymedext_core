import json



class DoccanoAnnotation:
    """
    Annotation object specific to Doccano
    """

    def __init__(self, text, labels, meta):
        """Initialize a DoccanoAnnotation object

        :param text: a short text that contains enough context to evaluate the annotation
        :param labels: annotation extracted (ex : "negative"/"not negative" to evaluate DrWH negation)
        :param meta: the path of the corresponding pymedext file that contains the annotation
        :return: DoccanoAnnotation
        :rtype: DoccanoAnnotation
        """
        self.text = text
        self.labels = labels
        self.meta = meta

    def to_json(self):
        """Transform DoccanoAnnotation to json

        :return: a json
        :rtype: json
        """
        return json.dump(self.to_dict())

    def to_dict(self):
        """Transform DoccanoAnnotation to dict

        :return: a dict
        :rtype: dict
        """
        return {'text':self.text,
                'labels':self.labels,
                'meta':self.meta}