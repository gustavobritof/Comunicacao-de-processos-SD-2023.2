import pickle

def serialize(obj) -> bytes:
    return pickle.dumps(obj)

def deserialize(serialized):
    return pickle.loads(serialized)