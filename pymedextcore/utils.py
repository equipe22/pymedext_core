import uuid

def generate_id(ID):
    if ID is not None:
        return ID
    return str(uuid.uuid1()).replace('-','')
