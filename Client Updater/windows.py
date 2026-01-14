import platform,os,network,json,subprocess,webbrowser

import logging
logging.basicConfig(filename='error.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


class Windows():
    def __init__(self):
        
        self.nm = "Windows"
        self.network = network.NetworkManager()
        self.data = {}
        base = "/AppData/roaming/trihexangular-launcher"
        self.paths = {
            "folder":os.path.expanduser("~")+base,
            "bin": os.path.join(os.path.expanduser("~")+base,"bin"),
            ".temp": os.path.join(os.path.expanduser("~")+base,".temp"),
            "data": os.path.join(os.path.expanduser("~")+base,"data"),
            "games": os.path.join(os.path.expanduser("~")+base,"games"),
        }
    def SetOS(self):
        self.GetPackages()
        self.packages["system"]="Windows"
        self.SetPackages()
    def ISActiveUser(self):
        
        self.GetPackages()
        try:
            if(self.packages["system"]=="Windows"):
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
    def ConfirmLauncherData(self):
        p = self.packages["repository"] + "/raw/main/Server/data/launcher_data.json"

        succeded = self.network.InstallFile(p,self.paths[".temp"],self.paths["data"],"launcher_data.json")

        if(succeded):
            self.master.Message("Connected","Successfully connected to alternate repository!","check",["Continue"])
            
            with open(os.path.join(self.paths["data"],"launcher_data.json"), "r") as f:
                self.data = json.load(f)
            
            logging.debug(f"NETWORK - successfully configured alternate repository '{self.packages["repository"]}'")
        else:
            self.master.Message("Couldn't connect","Could not get repository data, is the link valid, and are you conencted to the internet\n","cancel",["Back"])
            logging.error(f"NETWORK - could not connect to alternate repository '{self.packages["repository"]}'")
            self.packages["repository"] = "None"
            self.SetPackages()
            exit()
    def GetLauncherData(self):
        p = self.packages["repository"] + "/raw/main/Server/data/launcher_data.json"
        try:
            
            succeded = self.network.InstallFile(p,self.paths[".temp"],self.paths["data"],"launcher_data.json")
        except Exception as e:
            logging.error(e)
            succeded = False
        if(succeded):
            
            logging.debug(f"NETWORK - successfully downloaded launcher data '{self.packages["repository"]}'")
        
            with open(os.path.join(self.paths["data"],"launcher_data.json"), "r") as f:
                self.data = json.load(f)
            
            logging.debug(self.data)
        else:

            try:
                with open(os.path.join(self.paths["data"],"launcher_data.json"), "r") as f:
                    self.data = json.load(f)
                logging.debug(f"NETWORK - could not connect to repository to download data '{self.packages["repository"]}'")
                logging.debug(f"STATE - attempting to run in offline mode")
            except Exception as e:
                logging.debug(f"NETWORK - could not connect to repository to donwload data '{self.packages["repository"]}'")
                logging.debug(f"STATE - attempting to run in offline mode")
                logging.error(f"NETWORK - no previous launcher data loaded and cannot continue ")
                exit()
            


    def StartLauncher(self):
        
        path = os.path.join(self.paths["bin"],"launcher",("Trihexangular Launcher"+".exe"))

        logging.debug(f"LAUNCH - starting '{path}'")
        
        try:
            l = subprocess.Popen([path])
        except Exception as e:
            logging.error(f"LAUNCH - error {e}")
            exit()
        
        exit()
    def InstallLauncher(self):
        self.GetPackages()
       
        self.packages["launcher"]["installed"] = False
        launcher_number = self.data["launcher"]["version"]

        self.SetPackages()
        
        status = self.network.InstallZip(self.packages["repository"]+f"/releases/download/main_{launcher_number}/launcher_windows.zip",os.path.join(self.paths[".temp"],"launcher_download_windows_exe.zip"),self.paths["bin"]+"\\launcher")
        
        if(status==False):
            
            logging.error(f"ERROR - failed installing launcher")
            
            try:
                v=self.master.Message("Error: ",f"Error installing launcher. See error.log for details","cancel",["Open","Exit"])
                if(v==0):
                    webbrowser.open_new(r"C:\Users\Administrator\Desktop\Trihexangular-Launcher\Client Updater\error.log")
                
            except Exception as e:
                print(e)
            
            exit()

        self.packages["launcher"]["installed"] = True
        self.packages["launcher"]["version"] = launcher_number
        self.SetPackages()
        self.StartLauncher()
    def CheckForUpdates(self):
        logging.debug("LAUNCH - Checking for updates")
        self.GetPackages()
        try:
            if(self.packages["launcher"]["version"]<self.data["launcher"]["version"]):
                logging.debug("LAUNCH - Updating launcher")
                
                self.InstallLauncher()
                
                self.packages["launcher"]["version"]=self.data["launcher"]["version"]
                self.SetPackages()
        except KeyError:
            print("KeyError")
            self.packages["launcher"]={
                "version":-1
            }
            self.SetPackages()
            self.CheckForUpdates()
    def AddKey(self,dict,key,value):
        if dict.get(key) is not None:
            return
        else:
            dict[key]=value
    def GetPackages(self):
        try:
            with open(os.path.join(self.paths["data"],"packages.json"), "r") as f:
                self.packages = json.load(f)
        except Exception as e:
            try:
                self.AddKey(self.packages,"launcher",{})
            except AttributeError:
                self.packages = {"launcher":{}}
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