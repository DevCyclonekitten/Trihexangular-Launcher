import os,json
Roaming = "Roaming"
class Data():
    def __init__(self,differ):
        self.home_dir = os.path.expanduser("~")
        if self.home_dir:
            self.project_path = os.path.join(self.home_dir, "AppData", Roaming,"Trihexangular Launcher","updater")
        if(differ!=False):
            self.f = differ
        else:
            self.f = os.path.join(self.project_path,"settings.json")
        self.data = {}

        self.ReadData()

    def RunAfterUpdate(self):
        return self.data["run-after-update"]
    def ReadData(self):
        try:
            with open(self.f, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            f=open(self.f,"w")
            f.write(json.dumps({"version":-1,"run-after-update":True},indent=4))
            f.close()
    def WriteData(self):
        with open(self.f, "w") as outfile:
            outfile.write(json.dumps(self.data, indent=4))

    def GetVersion(self):
        self.ReadData()
        return self.data["version"]
    def SetVersion(self,value):
        self.ReadData()
        self.data["version"]=value
        self.WriteData()