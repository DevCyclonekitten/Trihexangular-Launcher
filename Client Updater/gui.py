import systems
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import webbrowser
import time

runn = True

import logging,os
logging.basicConfig(filename='error.log', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)


logging.getLogger('PIL').setLevel(logging.WARNING)

class GUI():
    def __init__(self,system):
        #os.remove(r"C:\Users\Administrator\AppData\Roaming\trihexangular-launcher")
        logging.debug("############################################")
        if(system==False):
            
            self.system = systems.GetOperatingSystem()
            logging.debug(f"loading auto-detected-system '{self.system.nm}'")
            self.system.master = self
            self.TryFreshInstall()
        else:
            logging.debug(f"loading forced-callback-system '{system}'")
            self.system = systems.GetForcedOperatingSystem(system)
        
    def GetUserBoxInput(self,message):
        global runn
        runn = True
        result = {"completed":False,"result":""}

        root = ctk.CTk()
        root.geometry("300x200")

        
        title = ctk.CTkLabel(root,text=message,height=30,width=200)
        title.place(x=50,y=20)

        entry = ctk.CTkEntry(root,width=200,height=30)
        entry.place(x=50,y=65)

        button = ctk.CTkButton(root,text="Submit",width=75,height=30,command=lambda: [result.__setitem__('result', entry.get()),self.RunFalse()])
        button.place(x=112.5,y=115)

        back_button = ctk.CTkButton(root,text="Back",width=50,height=30,command=self.RunFalse)
        back_button.place(x=125,y=160)

        while runn:
            root.update()
        root.destroy()
       
        return result["result"]
    def RunFalse(self):
        global runn
        runn = False
    def DestroyRoot(self,root):
        root.destroy()
    def TryFreshInstall(self):
        
        try:
            self.system.GetPackages()
        except Exception as e:
            pass
            

        
        self.GetOS()

        try:
            if(self.system.packages.get("repository") == "None"):
                logging.debug("SYSTEM - loading fresh install")
                self.PollEULA()
                self.FreshInstall()
                
            else:
                logging.debug("SYSTEM - detected completed launcher install")
                self.ConfirmEverythingIsGood()
                self.system.GetLauncherData()
                
                self.CheckMessages()
                self.system.CheckForUpdates()
                self.StartLauncher()

        except Exception as e:
            
            #self.system.packages["repository"]="None"
            self.system.SetPackages()
            #self.TryFreshInstall()
    def ConfirmEverythingIsGood(self):
        g = True
        self.system.GetPackages()
        if(self.system.packages.get("repository") == "None"):
            logging.error("ERROR-DETECT repository is none. running repository configuring")
            self.GetRepository()
            g=False
        if(self.system.packages.get("eula") != "true"):
            logging.error("ERROR-DETECT - eula is set to false. running eula configuring")
            self.PollEULA()
            g=False
        if(g):
            logging.debug("DETECT - system detects no abnormalities")
        
        

    def GetOS(self):
        self.system.SetupLauncherDirectory()
        
        self.system.GetPackages()
        
        if(self.system.ISActiveUser()==True):
            return
        else:
            self.GetUserLauncherVersionType(systems.GetOperatingSystemName())
            
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
            webbrowser.open_new('https://devcyclonekitten.github.io/Trihexangular-Launcher/eula.html')
            self.ConfirmEULA()
        if(i==1):
            self.FinishEULA()
        if(i==2):
            self.DenyEULA()
    def FinishEULA(self):
        self.system.GetPackages()
        self.system.packages["eula"] = "true"
        self.system.SetPackages()
        logging.debug("EULA - user agreed to eula")
    def DenyEULA(self):
        self.Message("Cannot Install","Cannot install without agreeing to EULA","cancel",["Exit"])
        logging.error("EULA - user denied eula")
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
        self.system.GetLauncherData()
        self.RemoveAllMessages()
        self.CheckMessages()

        try:
            self.system.CheckForUpdates()
        except Exception as e:
            print(f"Fresh: {e}")
    def GetRepository(self):
        
        if(self.system.packages["repository"] != "None"):
            return


        i = self.Message("Launcher Repository","Do you want to install from the main repository 'https://github.com/DevCyclonekitten/Trihexangular-Launcher'","question",["Main","Custom","Exit"])
        docustom = i
        customlink = "https://github.com/DevCyclonekitten/Trihexangular-Launcher"
        if(docustom==1):
            r = self.GetUserBoxInput("Enter custom repository link (experimental): ")
            if(r==""):
                self.GetRepository()
                return
            customlink = r
            
            self.system.GetPackages()
            self.system.packages["repository"] = customlink
            self.system.SetPackages()
            self.system.ConfirmLauncherData()
            #self.Message("Custom Repository", "Custom repositories are currently not supported","cancel",["Back","Exit"])
            #self.GetRepository()
            return
        self.system.GetPackages()
        self.system.packages["repository"] = customlink
        self.system.SetPackages()
        

    def RunMessage(self,message,ID):
        
        logging.debug("MESSAGES - running message {" + str(ID) + "}")
        flags = self.GetMessageFlags(message)
        
        self.system.GetPackages()
        if(flags[3]==1):
            return
        
        if(message.get("json-modify") != None):
            
            for key in message["json-modify"].keys():
                logging.debug("MESSAGES - message {"+str(ID)+"}"+f" modifying json propery '{key}' to '{message["json-modify"][key]}")
                self.system.packages[key]=message["json-modify"][key]
            self.system.SetPackages()
        
        i = self.Message(message["name"],message["content"],flags[0],flags[4])

        interactor = message["interactions"][i]

    
        
        if(interactor["type"]=="accept"):
            pass

        elif(interactor["type"]=="url"):
            webbrowser.open_new(interactor["content"])
        elif(interactor["type"]=="messagebuilder"):
            
            logging.debug("MESSAGES - message builder started")
            
            
            self.RunMessage(interactor["content"],-1)
            
        
        if(not flags[2]==1):
            if(not ID ==-1):
                logging.debug("MESSAGES - message {"+ID+"} cleared")
                self.system.GetPackages()
                self.system.packages["messages"].append(ID)
                self.system.SetPackages()
        else:
            logging.debug("MESSAGES - message {"+ID+"} is permanent")
        if(flags[1]==1):
            time.sleep(0.1)
            logging.debug("MESSAGES - message {"+ID+"} has flag 2 at state 1 (exit)")
            logging.debug("EXIT")
            exit()
    def GetMessageFlags(self,message):
        #0 = iconflag
        #1 = exitflag, so exit after
        #2  perminance flag
        #3 = invisible
        # Message Flags
        icons = ["check","cancel","info","question","warning"]
        try:
            iconflag = icons[int(message["flags"][0])]
            exitflag = int(message["flags"][1])
            perminance = int(message["flags"][2])
            invisible = int(message["flags"][3])
        except Exception as e:
            iconflag = 4
            exitflag = 0
            perminance = 0
            invisible = 1
        

        buttons = message["interactions"]
        buttonnames = []
        for button in buttons:
            buttonnames.append(button["name"])


        return [iconflag,exitflag,perminance,invisible,buttonnames]
    def CheckMessages(self):
        logging.debug("MESSAGES - checking messages")
        
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
        logging.debug("MESSAGES - adding viewed flags to all previous messages")
        self.system.GetPackages()
        try:
            print(self.system.data)
            for item in self.system.data["launcher"]["maintainer"]["messages"].keys():
                viewed = False
                for viewedItem in self.system.packages["messages"]:
                    if(item==viewedItem):
                        viewed = True
                if(not viewed):
                    self.system.packages["messages"].append(item)
                    print(f"Append: {item}")
        except Exception as e:
            print(f"RM :{e}")
        self.system.SetPackages()
    def StartLauncher(self):
        self.system.GetPackages()
        if(self.system.packages.get("launcher").get("installed")==True):
            self.system.StartLauncher()
        else:
            logging.debug("LAUNCHER - attempted to start launcher without installed, installing.")
            self.system.InstallLauncher()
        
GUI(False)