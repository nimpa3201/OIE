import pickle


def pickle_dump(path,text):
    with open(path,"wb") as r:
        pickle.dump(text,r)
            
            
def pickle_load(path):
    with open(path,"rb") as w:
        return pickle.load(w)
