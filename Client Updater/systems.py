import platform
import os
import network
import json




urls = {
    "launcher_data":r"https://github.com/DevCyclonekittenTriHex/trihexangulargamesrepo/raw/main/data/launcher_data.json",
    "launcher":r"https://github.com/DevCyclonekittenTriHex/trihexangulargamesrepo/releases/download/main_update_0.95/Launcher_2.0.zip"
}
def GetOperatingSystem():
    n= "Windows"
    n = platform.system()
    
    c =""
    if(n=="Linux"):
        c=Linux()
    elif(n=="Darwin"):
        c=Mac()
    elif(n=="Windows"):
        c=Windows()
    elif(n=="Java" or n=="FreeBSD"):
        c=Java()
    
    return c






class Linux():
    def __init__(self):
        print("Operating System: Linux\nStatus: Supported")
        self.network = network.NetworkManager()
        self.data = {}
        self.paths = {
            "folder":os.path.expanduser("~")+"/.trihexangular-launcher",
            "bin": os.path.join(os.path.expanduser("~")+"/.trihexangular-launcher","bin"),
            ".temp": os.path.join(os.path.expanduser("~")+"/.trihexangular-launcher",".temp"),
            "data": os.path.join(os.path.expanduser("~")+"/.trihexangular-launcher","data"),
            "games": os.path.join(os.path.expanduser("~")+"/.trihexangular-launcher","games"),
        }

    def HasInstalled(self):
        if(os.path.isdir(self.paths["folder"])):
            return True
        else:
            return False
    def SetupLauncherDirectory(self):
        for path in self.paths.keys():
            os.makedirs(self.paths[path],exist_ok=True)
    
    def GetLauncherData(self):
        #self.network.InstallFile(urls["launcher_data"],self.paths[".temp"],self.paths["data"],"launcher_data.json")
        with open(os.path.join(self.paths["data"],"launcher_data.json"), "r") as f:
            self.data = json.load(f)
    def InstallLauncher(self):
        url = urls["launcher"]
        self.network.InstallZip(url,os.path.join(self.paths[".temp"],"launcher_download_linux_x86_64"),self.paths["bin"])

    def CheckForUpdates(self):
        
        self.GetLauncherData()
        self.GetPackages()
        
        if(self.packages["launcher"]["version"]<self.data["launcher"]["version"]):
            self.InstallLauncher()
            self.packages["launcher"]["version"]=self.data["launcher"]["version"]
            self.SetPackages()
    

    
    def GetPackages(self):
        try:
            with open(os.path.join(self.paths["data"],"packages.json"), "r") as f:
                self.packages = json.load(f)
        except FileNotFoundError:
            self.packages = {
                "launcher":{
                    "version":0.94
                }
            }
            with open(os.path.join(self.paths["data"],"packages.json"),"w") as f:
                json.dump(self.packages, f)
            self.GetPackages(self)
            return
    def SetPackages(self):
        with open(os.path.join(self.paths["data"],"packages.json"),"w") as f:
            json.dump(self.packages, f)


class Mac():
    def __init__(self):
        print("Operating System: MacOS\nStatus: Not Supported")

class Windows():
    def __init__(self):
        print("Operating System: Windows\nStatus: Not Supported")

class Java():
    def __init__(self):
        print("Operating System: Java?\nStatus: Not Supported, why are you using java?")

