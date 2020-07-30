import json



class DoccanoAnnotation:

    def __init__(self, text, labels, meta):
        self.text = text
        self.labels = labels
        self.meta = meta

    def to_json(self):
        return json.dump(self.to_dict())

    def to_dict(self):
        return {'text':self.text,
                'labels':self.labels,
                'meta':self.meta}