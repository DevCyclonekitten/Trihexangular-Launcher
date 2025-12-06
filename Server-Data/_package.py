import json,glob,os,shutil
folder = "OUTPUT\\"
def AddComponent(path,array):
    with open(path,"r") as file:
        data = json.load(file)
    array.append(data)
    return array

def GetPathJsons(path):
    global folder
    pattern = os.path.join(folder+path,"*.json")
    json_files = glob.glob(pattern)
    return json_files
def ZipFolder(folder_path, output_path):
    """Zips a folder and its contents.

    Args:
        folder_path: The path to the folder to zip.
        output_path: The path to save the zipped folder.
    """
    shutil.make_archive(output_path, 'zip', folder_path)
def Args(string,value):
    loop = len(string)-value
    r = []
    for i in range(loop):
        r.append(string[i+value])
    s = ""
    for item in r:
        s = s + item +" "
    s = s + "easdeaeda"
    s = s.replace(" easdeaeda", "")
    return s

def Package():
    global folder
    

    with open(folder+"data.json", 'r') as file:
        data = json.load(file)

    data["games"]=[]
    data["messages"]=[]

    for item in GetPathJsons("Games"):
        data["games"]=AddComponent(item,data["games"])

    for item in GetPathJsons("Messages"):
        data["messages"]=AddComponent(item,data["messages"])

    with open(folder +"\\launcher_data.json", 'w') as f:
        json.dump(data, f,indent=4)

    print("Created 'launcher_data.json' file")


    # Example usage:
    folder_to_zip = folder+"Assets"
    zip_file_path = folder+"Assets"
    ZipFolder(folder_to_zip, zip_file_path)
    print("Created 'Assets.zip'")




