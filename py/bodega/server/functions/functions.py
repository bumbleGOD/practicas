import uuid

# generar id's automaticas 
def create_id():
    return str(uuid.uuid4().hex)