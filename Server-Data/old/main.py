import _package,_create,_asset,_upload

folder = "OUTPUT\\"
end = False

while not end:
    command = input(">>> ")
    if(command == "exit" or command == "quit"):
        end = True
    else:
        args = command.replace("git ","").split(" ")
        if(args[0]=="add"):
            if(args[1]=="game"):
                name = _package.Args(args,2)
                print(name)
                _create.Create(name,folder)
                _asset.Asset(name,folder)
                print(f"- Added Game for {name}")
            if(args[1]=="json"):
                name = _package.Args(args,2)
                _create.Create(name,folder)
                _asset.Asset(name,folder)
                print(f"- Added Json for {name}")
            if(args[1]=="asset"):
                name = _package.Args(args,2)
                _asset.Asset(name,folder)
                print(f"- Added Asset for {name}")
        elif(args[0]=="package"):
            _package.Package()
        elif(args[0]=="commit"):
            print("- Committing Files to Githup Repository")
            _upload.Commit(folder)
                
        else:
            print("- Unknown Command")