def Get(string):
    r = input(string + "\n>>> ")
    return r

def AddGame():
    
    gid = Get("ID (int)")
    name = Get("Name (string)")
    pgname = Get("Programming Name (string)")
    author = Get("Authors (string split(,))").split(",")


    print("######## Content ########")
    icoim = Get("Icon images (string split(,))").split(",")
    disim = Get("Display Images (string split(,))").split(",")
    disvi = Get("Display Video (string split(,))").split(",")


    print("######## Store ########")
    des = Get("Description (string)")
    pri = Get("Price (double)")

    print("####### Builds ########")
    windows = Get("Windows builds (string split(,))").split(",")
    linux = Get("Linux builds (string split(,))").split(",")
    #mac = Get("Windows builds (string split(,))").split(",")
    data = {
        "id":gid,
        "name":name,
        "programmingname":pgname,
        "author":author,
        "content":{
            "general":{
                "iconimages":icoim,
                "displayimages":disim,
                "displayvideo":disvi
            },
            "store":{
                "storedescription":[{"type":"text","content":[des]}],
                "storecontent":[],
                "storefaq":[]
            }
        },
        "purchasing":{
            "price":pri
        },
        "builds":{
            "linux":linux,
            "windows":windows
        }
    }
    path = "ServerFiles/json/games"
    with open(f"{path}/{bid}.json","w+") as fs:
        json.dump(data,fs,indent=4)
