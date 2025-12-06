import os

def Asset(nm,folder):
    try:
        os.mkdir(folder+"Assets\\"+nm)
    except Exception as e:
        pass
