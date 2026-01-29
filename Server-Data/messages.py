import glob,json

def GetMessages():
    path = "ServerFiles/data/messages"
    files = glob.glob(path+"/.json")
    print(files)

def Get(string):
    r = input(string + "\n>>> ")
    return r
def AddMessage():
    path = "ServerFiles/data/messages"


    print("############## flags #############\n")

    id = input("ID (int) \n>>> ")
    print("")

    #flags
    icon = input("Icon (string) \n>>> ")
    perm = input("Perminance (y/n) \n>>> ")
    quil = input("Exit after (y/n) \n>>> ")
    invi = input("Invisible (y/n) \n>>> ")
    prio = input("Priority (y/n) \n>>> ")

    #text
    print("############## Texts ##############\n")

    title = input("Title (string) \n>>> ")
    maintex = input("Text Main (string) \n>>> ")
    stex = input("Text Secondary (string) \n>>> ")
    ttex = input("Text Tertiary (string) \n>>> ")

    print("############## Interactions ##############\n")

    perm = title.replace("y",True).replace("n",False)
    quil = title.replace("y",True).replace("n",False)
    invi = title.replace("y",True).replace("n",False)
    prio = title.replace("y",True).replace("n",False)

    con = [
        {"text":maintex,"position":0,"font":("Helvetica",15)}
    ]
    if(stex !=""):
        con.append({"text":stex,'position':25,"font":("Helvetica",10)})
    if(ttex !=""):
        con.append({"text":ttex,'position':25,"font":("Helvetica",10)})
    data = {
        f"{id}":{
            "name":title,
            "content":con,
            "icon":icon,
            "flags":{
                "perminance":perm,
                "exit-after":quil,
                "invisible":invi,
                "priority":prio
            },
            "interactions":{}

        }
    }
    with open(f"{path}/{id}.json","w+") as fs:
        json.dump(data,fs,indent=4)



AddGame()