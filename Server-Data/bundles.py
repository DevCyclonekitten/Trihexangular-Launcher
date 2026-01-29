import json,glob
def Get(string):
    r = input(string + "\n>>> ")
    return r



class Creator():
    def __init__(self):
        launcher_manifestversion = 2
        launcher_currentversion = 0.96
        self.filedata = {
            "manifest":launcher_manifestversion,
            "launcher":{
                "version":launcher_currentversion,
                "maintainer":{
                    "messages":{}
                }
            },
            "content":{
                
            }
        }

    def AddLauncherMessage(self):
        bid = Get("Id (int)")
        

        data = {
            "id":bid,
            "name":"temp",
            "content":"temp2",
            "flags":"3000",
            "images":[],
            "json-modify":{},
            "interactions":[]
        }
        path = "ServerFiles/content/messages"
        with open(f"{path}/{bid}.json","w+") as fs:
            json.dump(data,fs,indent=4)
    def AddCollection(self):
        bid = Get("Id (int)")
        name = Get("Name (string)")
        des = Get("Description (string)")
        games = Get("GameIDs (int split(,))").split(',')
        sb = Get("Sortby (string -> id,alphabetical)")

        data = {
            "id":bid,
            "name":name,
            "description":des,
            "games":games,
            "sortby":sb
        }
        path = "ServerFiles/content/collections"
        with open(f"{path}/{bid}.json","w+") as fs:
            json.dump(data,fs,indent=4)
    def AddBundle(self):
        bid = Get("Id (int)")
        name = Get("Name (string)")
        des = Get("Description (string)")
        games = Get("GameIDs (int split(,))").split(',')
        price = Get("Price Total (double)")
        images = Get("Extra Images (string split(,))")

        data = {
            "id":bid,
            "name":name,
            "description":des,
            "games":games,
            "price":price,
            "images":images
        }
        path = "ServerFiles/content/bundles"
        with open(f"{path}/{bid}.json","w+") as fs:
            json.dump(data,fs,indent=4)
    def CompileGames(self):
        files = glob.glob("ServerFiles/content/games/*.json")

        data = []
        for file in files:
            with open(file, "r") as f:
                d = json.load(f)
                data.append(d)

        self.filedata["content"]["games"] = data
    def CompileBundles(self):
        files = glob.glob("ServerFiles/content/bundles/*.json")

        data = []
        for file in files:
            with open(file, "r") as f:
                d = json.load(f)
                data.append(d)

        self.filedata["content"]["bundles"] = data
    def CompileCollections(self):
        files = glob.glob("ServerFiles/content/collections/*.json")

        data = []
        for file in files:
            with open(file, "r") as f:
                d = json.load(f)
                data.append(d)

        self.filedata["content"]["collections"] = data
    def CompileMessages(self):
        files = glob.glob("ServerFiles/content/messages/*.json")

        data = []
        for file in files:
            with open(file, "r") as f:
                d = json.load(f)
                data.append(d)

        self.filedata["content"]["messages"] = data
    def CompileFile(self):
        self.CompileGames()
        self.CompileBundles()
        self.CompileCollections()
        self.CompileMessages()
        with open("Server/data/launcher_data.json","w") as f:
            json.dump(self.filedata,f,indent=4)
    def AskLoop(self):
        while True:
            m = input(">>> ")
            if(m=="compile"):
                self.CompileFile()
            if(m=="message"):
                self.AddLauncherMessage()
            if(m=="bundle"):
                self.AddBundle()
            if(m=="collection"):
                self.AddCollection()
c = Creator()
c.AskLoop()