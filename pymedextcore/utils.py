"""Utility functions"""

import uuid

def generate_id(_id):
    """Generates a new id
    params: _id If _id is not None, a new id is generated else returns _id
    """
    if _id is not None:
        return _id
    return str(uuid.uuid1()).replace('-','')
