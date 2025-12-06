import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from shutil import rmtree
from os.path import join
import os
import sys
rt = ctk.CTk() 
rt.geometry("1x1")
Roaming = "Roaming"
msg = CTkMessagebox(title="Uninstall", message="Do you really want to uninstall Trihexangular Launcher",
                        icon="cancel", option_2="Ok",option_1="Cancel")
response = msg.get()

if(response=="Ok"):
    try:
        print("Uninstalling")
        home_dir = os.path.expanduser("~")
        updater_path = os.path.join(home_dir, "AppData", Roaming,"Trihexangular Launcher","updater")
        launcher_path = os.path.join(home_dir, "AppData", Roaming,"Trihexangular Launcher")
        rmtree(launcher_path)
        print("BMF")
        try:
            print("Before message box")
            msg2 = CTkMessagebox(title="Uninstall", message="Successfully Uninstalled", icon="success", option_2="Ok")
            r = msg2.get()  # Ensure this is a blocking call
            print("After message box")
            print("Value of r:", r)
            if r != "Ok":
                print("ok")
        except Exception as e:
            print(f"An error occurred: {e}")
                        
    except Exception as e:
        updater_path = join(home_dir, "AppData", Roaming,"Trihexangular Launcher","updater")
        launcher_path = join(home_dir, "AppData", Roaming,"Trihexangular Launcher")
        print("HI")
        msg = CTkMessagebox(title="Uninstall", message=f"""Couldn't uninstall due to an error, Files are at: {launcher_path}""",
            icon="cancel", option_2="Ok")
        msg.get()
        msg2 = CTkMessagebox(title="Uninstall", message=f"Error: {e}",
            icon="cancel", option_2="Ok")

        msg2.get()
    sys.exit(0)()
else:
    sys.exit(0)()