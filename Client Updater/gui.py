import systems
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import webbrowser
import time

class GUI():
    def __init__(self,system):
        if(system==False):
            self.system = systems.GetOperatingSystem()
            self.TryFreshInstall()
        else:
            self.system = systems.GetForcedOperatingSystem(system)
        
    
    def TryFreshInstall(self):
        self.GetOS()
        self.system.GetPackages()
        try:
            if(self.system.packages["repository"] == "None"):
                    
                self.PollEULA()
                self.FreshInstall()
                self.RemoveAllMessages()
                self.CheckMessages()
                
            else:
                self.CheckMessages()
                self.StartLauncher()
        except KeyError:
            self.system.packages["repository"]="None"
            self.system.SetPackages()
            self.TryFreshInstall()
    def GetOS(self):
        self.system.SetupLauncherDirectory()
        if(self.system.ISActiveUser()==True):
            return
        else:
            self.GetUserLauncherVersionType(systems.GetOperatingSystemName())
            self.system.SetupLauncherDirectory()
            self.system.SetOS()
    def GetUserLauncherVersionType(self,suggested):
        order = ["Windows","Mac","Linux"]
        order.remove(suggested)
        i = self.Message("Select OS", "Detected operating system: "+suggested,"question",[suggested,order[0],order[1]])
        
        if(i==0):
            return
        elif(i==1):
            self = GUI(order[0])
        elif(i==2):
            self = GUI(order[1])
        else:
            exit()
    def ConfirmEULA(self):
        i = self.Message("End User Licence Agreement", ("Have you read and do you agree to the END USER LICENCE AGREEMENT (EULA)."),"question",["View Eula","Agree","Disagree"])
        if(i==0):
            webbrowser.open_new('https://www.example.com')
            self.ConfirmEULA()
        if(i==1):
            self.FinishEULA()
        if(i==2):
            self.DenyEULA()
    def FinishEULA(self):
        self.system.GetPackages()
        self.system.packages["eula"] = "true"
        self.system.SetPackages()
    def DenyEULA(self):
        self.Message("Cannot Install","Cannot install without agreeing to EULA","cancel",["Exit"])
        exit()
    def PollEULA(self):
        self.system.GetPackages()
        try:
            r=self.system.packages["eula"]
            if(r=="true"):
                return
            else:
                self.ConfirmEULA()
        except KeyError:
            self.system.packages["eula"] = "false"
            self.system.SetPackages()
            self.PollEULA()
        
    
    def Message(self,title,message,icon,options):
        root = ctk.CTk()
        root.geometry("1x1")
        msg = CTkMessagebox(title=title,message=message,icon=icon,options=options)
        response = msg.get()
        if(response =="Exit"):
            
            exit()
        for i in range(len(options)):
            if(response==options[i]):
                return i
        else:
            exit()

    def FreshInstall(self):
        self.GetRepository()
        self.system.InstallLauncher()
    def GetRepository(self):
        i = self.Message("Launcher Repository","Do you want to install from the main repository 'https://github.com/DevCyclonekitten/Trihexangular-Launcher'","question",["Main","Custom","Exit"])
        docustom = i
        customlink = "https://github.com/DevCyclonekitten/Trihexangular-Launcher"
        if(i==1):
            self.Message("Custom Repository", "Custom repositories are currently not supported","cancel",["Back","Exit"])
            self.Install()
            return
        self.system.GetPackages()
        self.system.packages["repository"] = customlink
        self.system.SetPackages()

    def RunMessage(self,message,ID):
        flags = self.GetMessageFlags(message)

        if(flags[3]==1):
            return

        i = self.Message(message["name"],message["content"],flags[0],flags[4])

        interactor = message["interactions"][i]


        if(message["jsonmodify"]!={}):
            for key in message["jsonmodify"].keys():
                self.system.packages[key]=message["jsonmodify"][key]

        if(interactor["type"]=="accept"):
            pass
        elif(interactor["type"]=="url"):
            webbrowser.open_new(interactor["content"])
        elif(interactor["type"]=="messagebuilder"):
            self.RunMessage(interactor["content"],-1)
        
        if(not flags[2]==1):
            if(not ID ==-1):
                self.system.GetPackages()
                self.system.packages["messages"].append(ID)
                self.system.SetPackages()
        if(flags[1]==1):
            time.sleep(0.1)
            exit()
    def GetMessageFlags(self,message):
        # Message Flags
        icons = ["check","cancel","info","question","warning"]
        iconflag = icons[int(message["flags"][0])]
        exitflag = int(message["flags"][1])
        perminance = int(message["flags"][2])
        #invisible = int(message["invisible"])
        invisible = 0

        buttons = message["interactions"]
        buttonnames = []
        for button in buttons:
            buttonnames.append(button["name"])


        return [iconflag,exitflag,perminance,invisible,buttonnames]
    def CheckMessages(self):
        self.system.GetLauncherData()
        self.system.GetPackages()
        for item in self.system.data["launcher"]["maintainer"]["messages"].keys():
            viewed = False
            for viewedItem in self.system.packages["messages"]:
                if(item==viewedItem):
                    viewed = True
            if(not viewed):
                m = self.system.data["launcher"]["maintainer"]["messages"][item]
                self.RunMessage(m,item)
    def RemoveAllMessages(self):
        self.system.GetPackages()
        for item in self.system.data["launcher"]["maintainer"]["messages"].keys():
            viewed = False
            for viewedItem in self.system.packages["messages"]:
                if(item==viewedItem):
                    viewed = True
            if(not viewed):
                self.system.packages["messages"].append(item)
        self.system.SetPackages()
    def StartLauncher(self):
        self.system.StartLauncher()
        
        
GUI(False)  