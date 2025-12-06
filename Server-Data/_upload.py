import os,shutil,subprocess,time


def Commit(folder):
    json = os.getcwd()+"\\"+folder + "launcher_data.json"
    json_destination = "C:\\Users\\isaac\\Desktop\\Trihexangular Studios\\trihexangulargamesrepo\\data\\launcher_data.json"
    try:
        os.remove(json_destination)
    except Exception as e:
        pass
    shutil.copyfile(json,json_destination)


    assets = os.getcwd() +"\\"+folder+"Assets.zip"
    assets_destination = "C:\\Users\\isaac\\Desktop\\Trihexangular Studios\\trihexangulargamesrepo\\data\\Assets.zip"
    try:
        os.remove(assets_destination)
    except Exception as e:
        pass
    shutil.copyfile(assets,assets_destination)


    filestorun = [r"C:\Users\isaac\Desktop\Trihexangular Studios\trihexangulargamesrepo\bin\!add.bat"]
    for file in filestorun:
        p=subprocess.Popen(file, cwd=r"C:\Users\isaac\Desktop\Trihexangular Studios\trihexangulargamesrepo",creationflags=subprocess.CREATE_NO_WINDOW)
        while p.poll() is None:
            time.sleep(10)
            print("- Committing...")
    print("- Completed Committing")
