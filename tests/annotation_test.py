import pytest
import json
from pymedextcore.annotators import Annotation


@pytest.fixture
def content(): 
    return {
        "type": "annotation_type",
        "value": "ok",
        "source": "annotation1", 
        "source_ID": "1",
        "span": [0,10],
        "attributes": {"CUI": "CUI0001", "label": "Cui 0001"},
        "isEntity": True,
        "ID": '946c8559-90a8-11eb-93d0-3c7d0a00025d',
        "ngram": "bla bla"
    }


class TestEmpty:

    def test_init_empty(self):
        with pytest.raises(TypeError):
            ann = Annotation()

    def test_init_missing_type(self,content):
        with pytest.raises(TypeError):
            ann = Annotation(value = content["value"],
                            source = content["source"],
                            source_ID = content["source_ID"])

    def test_init_missing_value(self,content):
        with pytest.raises(TypeError):
            ann = Annotation(type = content["type"], 
                            source = content["source"],
                            source_ID = content["source_ID"])


    def test_init_missing_source(self,content):
        with pytest.raises(TypeError):
            ann = Annotation(type = content["type"], 
                            value = content["value"],
                            source_ID = content["source_ID"])

    def test_init_missing_source_ID(self,content):
        with pytest.raises(TypeError):
            ann = Annotation(type = content["type"], 
                            value = content["value"],
                            source = content["source"])



def test_new(content): 
    ann = Annotation(**content)

    assert ann.type == content["type"]
    assert ann.value == content["value"]
    assert ann.source == content["source"]
    assert ann.source_ID == content["source_ID"]
    assert ann.span == content["span"]
    assert ann.attributes == content["attributes"]
    assert ann.isEntity == content["isEntity"]
    assert ann.ID == content["ID"]
    assert ann.ngram == content["ngram"]


def test_to_dict(content):

    ann = Annotation(**content)
    ann_dict = ann.to_dict()

    assert ann_dict == content

def test_to_json(content):

    ann = Annotation(**content)
    ann_json = ann.to_json()

    ann_json == json.dumps(content)