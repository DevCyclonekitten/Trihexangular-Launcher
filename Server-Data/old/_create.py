import json,os
def Create(__displayname__,folder):
    #os.system("cls")

    __packageversion__ = 0.1
    print("")
    __author__ = input("- Author \n> ")
    print("")
    __description__ = input("- Description \n> ")
    print("")
    __images__ = input("- Store Images \n> ").split(",,,")
    print("")
    __video__ = input("- Store Video \n> ")
    print("")
    __price__ = int(input("- Price \n> "))
    print("")

    __buildsdata__={}
    finished = False
    print("- Build Adding ----------")
    __builds__ = []
    while not finished:
        
        g = input("> ")
        print("")
        if(g !="exit"):
            l = "https://github.com/DevCyclonekittenTriHex/trihexangulargamesrepo/raw/main/bin/"+__displayname__.replace(" ","%20")+"_"+g
            print("")
            __buildsdata__[g]=l
            __builds__.append(g)
        else:
            finished=True


    


    data = {
        "name":__displayname__,
        "version":__packageversion__,
        "builds":__buildsdata__,
        "displayname":__displayname__,
        "displaydescription":__description__,
        "displayimages":__images__,
        "displayvideo":__video__,
        "avaliablebuilds":__builds__,
        "price":__price__,
        "author":__author__
    }
    #os.system("cls")
    cl = folder+"\\Games\\"+__displayname__+".json"
    with open(cl, 'w') as f:
        json.dump(data, f,indent=4)