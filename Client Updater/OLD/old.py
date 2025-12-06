
import sys


import os ,subprocess,json,data,shutil,zipfile
import urllib.request
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

Roaming = "Roaming"

class GUI():
    def __init__(self):
        #Configure Home Directory

        self.home_dir = os.path.expanduser("~")
        if not self.home_dir:
            exit()

        #Configure Updater Settings

        try:
            self.data = data.Data(False)
            print("Updater Settings Loaded")
        except Exception as e:
            print("Updater Settings Created")
            try:
                os.makedirs(os.path.join(self.home_dir, "AppData", Roaming,"Trihexangular Launcher","updater"))
            except Exception as r:
                pass
            f=open(os.path.join(self.home_dir, "AppData", Roaming,"Trihexangular Launcher","updater","settings.json"),"w")
            f.write(json.dumps({"version":-1,"run-after-update":True},indent=4))
            f.close()
            self.data = data.Data(False)

        #Get LPData From Internet to Compare with 

        self.jsonDataLink = "https://github.com/DevCyclonekittenTriHex/trihexangulargamesrepo/raw/main/data/launcher_data.json"
        self.extractionPath = os.path.join(self.home_dir, "AppData", Roaming,"Trihexangular Launcher","updater")
        response = self.InstallJsonFile(self.jsonDataLink,self.extractionPath)
        self.lpdata = data.Data(os.path.join(self.extractionPath,"launcher_data.json"))
            
    def InstallLauncher(self): 
        global home_dir

        version = self.lpdata.GetVersion()
        print(version)
        link = f"https://github.com/DevCyclonekittenTriHex/trihexangulargamesrepo/releases/download/main_update_{version}/Launcher_2.0.zip"


        self.download_zip_path = os.path.join(self.home_dir, "AppData", Roaming,"Trihexangular Launcher","updater","bin","temp")
        self.extract_zip_path = os.path.join(self.home_dir, "AppData", Roaming,"Trihexangular Launcher","bin","launcher")

        try:
            os.makedirs(self.download_zip_path)
        except Exception as r:
            pass

        try:
            os.makedirs(self.extract_zip_path)
        except Exception as r:
            pass
        self.InstallGameZip(link,self.download_zip_path+"/launcher.zip",self.extract_zip_path)
        self.data.SetVersion(self.lpdata.GetVersion())
        print("InstalledGame")

    def RunLauncher(self):

        self.launcher_path = project_path = os.path.join(self.home_dir, "AppData", Roaming,"Trihexangular Launcher")

        #os.makedirs(launcher_path, exist_ok=True)
        #os.makedirs(os.path.join(launcher_path,"bin"), exist_ok=True)

        try:
            self.executable_path = os.path.join(self.launcher_path,"bin","launcher","Trihexangular Launcher.exe")
            subprocess.Popen([self.executable_path])
        except Exception as e:
            self.ErrorMessageBox("77: Couldn't Find Exe and start the launcher. Have you downloaded it?")

    def GetLauncherVersion(self):
        if(self.data.GetVersion()<self.lpdata.GetVersion()): #Outdated
            return True
        else:
            return False

    def CheckForUpdate(self):
        __update__ = self.GetLauncherVersion()
        if __update__ :
            response = self.UpdateMessageBox()
            if(response==2):
                self.InstallLauncher()
                if(self.data.RunAfterUpdate()):
                    self.RunLauncher()
                    sys.exit(0)()
            elif(response==1):
                self.RunLauncher()
                sys.exit(0)()
            else:
                sys.exit(0)()
        else:
            self.RunLauncher()
    def UpdateMessageBox(self):
        rt = ctk.CTk()
        rt.geometry("1x1")
        msg = CTkMessagebox(title="Launcher Outdated", message="Trihexangular Launcher outdated or not installed, do you want to download the latest version.",
                        icon="question", option_1="Update", option_2="Run", option_3="Exit")
        response = msg.get()
        
        if response=="Update":
            return 2
        elif response=="Run":
            return 1
        elif response=="Exit":
            return 0


        if response=="Run":
            return 1

    def ErrorMessageBox(self,text):
        print(text)
        rt = ctk.CTk()
        rt.geometry("1x1")
        msg = CTkMessagebox(title="Error", message=text,
                        icon="cancel", option_1="Ok")
        response = msg.get()

        if response=="Ok":
            return 1

    def InstallGameZip(self,url,zip_path,extract_path):
        try:
            
            project_path = os.path.join(self.home_dir, "AppData", Roaming,"Trihexangular Launcher","updater")
            
            launcher_path = project_path = os.path.join(self.home_dir, "AppData", Roaming,"Trihexangular Launcher")
            download_path = os.path.join(project_path, "temp")
            os.makedirs(download_path, exist_ok=True)
            os.makedirs(extract_path, exist_ok=True)
            if os.path.exists(zip_path):
                try:
                    os.remove(zip_path)
                    print("Deleted existing zip file.")
                except Exception as e:
                    self.ErrorMessageBox(f"141: Error deleting existing zip: {e}")
                    return False
            try:
                urllib.request.urlretrieve(url, zip_path)
            except Exception as e:
                self.ErrorMessageBox(f" 146: Download Error: {e}")
                return False
            try:
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
            except zipfile.BadZipFile as e:
                self.ErrorMessageBox(f"152: Extraction failed: Invalid zip file - {e}")
                return False
            except Exception as e:
                self.ErrorMessageBox(f"155: Extraction failed with an unexpected error: {e}")
                return False
            try:
                os.remove(zip_path)
            except Exception as e:
                self.ErrorMessageBox(f"160: Error deleting zip after extraction: {e}")
                return True
        except Exception as e:
            self.ErrorMessageBox(f"163: An unexpected error occurred: {e}")
            return False

    def InstallJsonFile(self,url,extract_path):
        try:

            project_path = os.path.join(self.home_dir, "AppData", Roaming, "Trihexangular Launcher", "updater")

            launcher_path = os.path.join(self.home_dir, "AppData", Roaming, "Trihexangular Launcher")
            download_path = os.path.join(project_path)
            json_file_name="launcher_data.json"
            json_file_path = os.path.join(download_path)
            os.makedirs(download_path, exist_ok=True)
            try:
                urllib.request.urlretrieve(url, os.path.join(json_file_path,json_file_name))
                #if os.path.exists(json_file_path):
                #    try:
                #        os.remove(json_file_path)
                #    except Exception as r:
                #        self.ErrorMessageBox(f"Error deleting existing JSON file: {r}")
                #        return False

                #shutil.move(os.path.join(json_file_path,"temp",json_file_name), os.path.join(json_file_path,json_file_name))

                
            except Exception as a:
                self.ErrorMessageBox(f"189: Couldn't connect to internet to check for updates. Running in offline mode: \n{a}")
                return False
            return True
        except Exception as e:
            self.ErrorMessageBox(f"193: An unexpected error occurred: {e}")
            return False

