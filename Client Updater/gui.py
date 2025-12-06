import systems
import customtkinter as ctk
import tkinter


class GUI():
    def __init__(self,system):
        if(system==False):
            self.system = systems.GetOperatingSystem()
            self.TryFreshInstall()
        else:
            self.system = systems.GetForcedOperatingSystem(system)
        
        
    def TryFreshInstall(self):
        if(self.system.HasInstalled == False):
            self.GetUserLauncherVersionType("Linux")
        else:
            self.GetUserLauncherVersionType("Linux")
    def GetUserLauncherVersionType(self,suggested):
        order = ["Windows","Mac","Linux"]
        order.remove(suggested)
        rt = tkinter.Tk()
        rt.geometry("1x1")
        msg = tkinter.messagebox.Message(title="Install Launcher", message=f"Trihexangular Launcher hasn't been installed on this device. \n Detected operating system: {suggested}",
                        icon="question", option_1=suggested, option_2=order[0], option_3=order[1],option_4="Exit")
        #response = msg.get()
        response = "hi"
        if response==suggested:
            return
        elif response==order[0]:
            self = GUI(order[0])
        elif response==order[1]:
            self = GUI(order[1])


        if response=="Exit":
            exit()

GUI(False)