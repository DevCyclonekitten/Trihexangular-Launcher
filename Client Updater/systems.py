import platform
import os
import network
import json
import subprocess

from linux import *
from windows import *



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






class Mac():
    def __init__(self):
        print("Operating System: MacOS\nStatus: Not Supported")

class Java():
    def __init__(self):
        print("Operating System: Java?\nStatus: Not Supported, why are you using java?")

