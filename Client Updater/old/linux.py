import platform,os,network,json,subprocess

class Linux():
    def __init__(self):
        
        self.network = network.NetworkManager()
        self.data = {}
        self.paths = {
            "folder":os.path.expanduser("~")+"/.trihexangular-launcher",
            "bin": os.path.join(os.path.expanduser("~")+"/.trihexangular-launcher","bin"),
            ".temp": os.path.join(os.path.expanduser("~")+"/.trihexangular-launcher",".temp"),
            "data": os.path.join(os.path.expanduser("~")+"/.trihexangular-launcher","data"),
            "games": os.path.join(os.path.expanduser("~")+"/.trihexangular-launcher","games"),
        }
    def SetOS(self):
        self.GetPackages()
        self.packages["system"]="Linux"
        self.SetPackages()
    def ISActiveUser(self):
        
        self.GetPackages()
        try:
            if(self.packages["system"]=="Linux"):
                return True
            else:
                return False
        except Exception as e:
            return False
    def HasInstalled(self):
        if(os.path.isdir(self.paths["folder"])):
            return True
        else:
            return False
    def SetupLauncherDirectory(self):
        for path in self.paths.keys():
            os.makedirs(self.paths[path],exist_ok=True)
    def GetLauncherData(self):
        p = self.packages["repository"] + "/raw/main/Server/data/launcher_data.json"


        self.network.InstallFile(p,self.paths[".temp"],self.paths["data"],"launcher_data.json")

        with open(os.path.join(self.paths["data"],"launcher_data.json"), "r") as f:
            self.data = json.load(f)
    def StartLauncher(self):
        path = os.path.join(self.paths["bin"],("Trihexangular Launcher"+""))

        
        subprocess.Popen([path])
    def AddKey(self,dict,key,value):
        if dict.get(key) is not None:
            return 1
        else:
            dict[key]=value
            return 0
    def InstallLauncher(self):
        self.GetLauncherData()
        self.GetPackages()
        
        launcher_number = self.data["launcher"]["version"]
        self.network.InstallZip(self.packages["repository"]+f"/releases/main_{launcher_number}/launcher_linux",os.path.join(self.paths[".temp"],"launcher_download_linux_x86_64"),self.paths["bin"])
    def CheckForUpdates(self):
        
        self.GetLauncherData()
        self.GetPackages()
        try:
            if(self.packages["launcher"]["version"]<self.data["launcher"]["version"]):
                self.InstallLauncher()
                self.packages["launcher"]["version"]=self.data["launcher"]["version"]
                self.SetPackages()
        except KeyError:
           
            self.packages["launcher"]={
                "version":-1
            }
            self.SetPackages()
            self.CheckForUpdates()
    def GetPackages(self):
        try:
            with open(os.path.join(self.paths["data"],"packages.json"), "r") as f:
                self.packages = json.load(f)
        except Exception as e:
            
            self.AddKey(self.packages,"launcher",{})
            self.AddKey(self.packages,"system","None")
            self.AddKey(self.packages,"eula","false")
            self.AddKey(self.packages,"repository","None")
            self.AddKey(self.packages,"messages",[])
            with open(os.path.join(self.paths["data"],"packages.json"),"w") as f:
                json.dump(self.packages, f,indent=4)
            self.GetPackages()
            return
    def SetPackages(self):
        with open(os.path.join(self.paths["data"],"packages.json"),"w") as f:
            json.dump(self.packages, f,indent=4)
