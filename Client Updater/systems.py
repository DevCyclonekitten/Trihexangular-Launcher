import platform
import os
import network
import json
import subprocess




urls = {
    "launcher_data":r"https://github.com/DevCyclonekittenTriHex/Trihexangular-Launcher/raw/main/Server/data/launcher_data.json",
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
def GetOperatingSystemName():
    n= "Windows"
    n = platform.system()
    
    c =""
    if(n=="Linux"):
        return "Linux"
    elif(n=="Darwin"):
        return "Mac"
    elif(n=="Windows"):
        return "Windows"
    elif(n=="Java" or n=="FreeBSD"):
        return "Java"




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

        print(path)
        subprocess.Popen([path])
    def InstallLauncher(self):
        self.GetLauncherData()
        self.GetPackages()
        print(self.data)
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
            print("KeyError")
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
            self.packages = {
                "launcher":{
                    "version":0.94
                },
                "system":"None",
                "eula":"false",
                "repository":"None",
                "messages":[]
            }
            with open(os.path.join(self.paths["data"],"packages.json"),"w") as f:
                json.dump(self.packages, f)
            self.GetPackages()
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

