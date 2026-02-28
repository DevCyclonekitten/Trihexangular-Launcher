#import systems
import customtkinter as ctk
import asyncio,logging,os,shutil,zipfile,urllib.request,time,threading,subprocess,webbrowser,json,requests,stat,sys
import systemmessages

from PIL import Image
from PIL import ImageTk
import base64,io,sys
import sys



#with open("logo.ico", "rb") as ico:
    #bytesimage = base64.b64encode(ico.read())
    #with open("base64logo.byteimage","wb") as fs:
        #fs.write(bytesimage)


class PackageManager():
    def __init__(self,m,a):
        self.master=m
        self.alternate = a
        
        
    def CheckAdd(self,key,data):
        try:
            str(self.data[key])
        except Exception as e:
            self.data[key]=data
        
    def Append(self,key,data):
        try:
            self.data[key].append(data)
        except KeyError:
            self.data[key] = []
            self.Append(key,data)
    def Set(self,key,data):
        self.data[key]=data
    def Get(self,key):
        try:
            return self.data[key]
        except KeyError:
            
            self.Set(key,None)
    def GetFrom(self,list,key):
        try:
            return list[key]
        except KeyError:
            list[key]=None
            return list[key]
    def Clear(self):
        self.data= {}
        self.SetPackages()
        
    def Read(self):
        print(self.data)
    def GetPackages(self):
        self.master.system.DisplayError()

        v = "packages"
        if(self.alternate):
            v ="launcher data"
        logging.debug(f"PACKAGES - getting {v}")

        

        #print("DISPLAYERROR")
        p = "packages.json"
        if(self.alternate):
            p="launcher_data.json"
        try:
            with open(os.path.join(self.master.system.paths["data"],p),"r") as fs:
                self.data = json.load(fs)
            return True
        except Exception as e:
            if(self.alternate):
                logging.error("ERROR - cannot get launcher data")
                print(e)
                m = systemmessages.systemerror
                m["content"][1]["text"]="ERROR - cannot get launcher data, please make sure"
                m["content"].append({"text":"you are connected to the internet.","position":50,"font":("Helvetica",10)})
                m["interactions"]["buttons"][0]["interactor"][0]["type"] = "exit"
                self.master.currenterror = m
                self.master.system.DisplayError()
            self.data = {}
            self.SetPackages()
            return False
    def SetPackages(self):
        try:
            with open(os.path.join(self.master.system.paths["data"],"packages.json"),"w") as fs:
                json.dump(self.data,fs,indent=4)
        except Exception as e:
            os.makedirs(self.master.system.path,exist_ok=True)
            self.SetPackages()
class SystemManager():
    def __init__(self,m):
        self.master=m
        self.path = os.path.join(os.path.expanduser("~"),".trihexangular-launcher")
        
    def Configure(self):
        #self.master.pacman.GetPackages()
        os = None#self.master.pacman.Get("os")
        if(os==None):
            if sys.platform.startswith('win'):
                self.WindowsDirectory()
            elif sys.platform.startswith('linux'):
                self.LinuxDirectory()
        else:
            if os=="windows":
                self.WindowsDirectory()
            elif os=="linux":
                self.LinuxDirectory()
    def WindowsDirectory(self):
        
        self.systemname = "Windows"
        #self.path = os.path.expanduser("~")+"/.trihexangular-launcher"
        self.PathSetup()

        self.awaitpackage="windows"
    def LinuxDirectory(self):
        self.systemname = "Linux"
        

        self.PathSetup()

        self.awaitpackage="windows"
    def ApplyAwait(self):
        self.master.pacman.GetPackages()
        self.master.pacman.CheckAdd("os",self.awaitpackage)
        self.master.pacman.SetPackages()
    def DisplayError(self):
        e=self.master.currenterror
        
        if(e != {}):
            print(e)
            
            if("urlopen" in e["content"][1]["text"]):
                e = {'name': 'Error', 'content': [{'text': 'Network Error', 'position': 0, 'font': ('Helvetica', 15)}, {'text': 'Cannot connect to internet (Errno -3)', 'position': 25, 'font': ('Helvetica', 10)}], 'icon': 'cancel', 'flags': {'exit-after': 0, 'persistent': 0, 'invisible': 0, 'priority': 1}, 'interactions': {'buttons': [{'text': 'exit', 'interactor': [{'type': 'dismiss'}]}]}}
                self.master.nointernet = True
            self.SystemMessage(e)
            self.master.currenterror = {}
    def PathSetup(self):
        self.paths = {
            "folder":self.path,
            "bin": os.path.join(self.path,"bin"),
            ".temp": os.path.join(self.path,".temp"),
            "data": os.path.join(self.path,"data"),
            "games": os.path.join(self.path,"games"),
        }
        for key in self.paths.keys():
           os.makedirs(self.paths[key], exist_ok=True)
        if(os.path.exists(os.path.join(self.path,'error.log')) and 1==1):
            logging.basicConfig(filename=os.path.join(self.path,'error.log'), format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        logging.getLogger('PIL').setLevel(logging.WARNING)
        logging.debug("############################################")
        logging.debug(f"DIRECTORY - setup user directory {self.systemname}")
    def ExitWithNoRoot(self):
        time.sleep(5)
        exit()
    def ClearCurrentRoot(self):
        self.master.window.root.destroy()
    def Start(self):
        self.DisplayError()
        logging.debug("LAUNCH - starting launcher")
        version = self.master.pacman.data["launcher"]["version"]
        branch = self.master.pacman.data["branch"]
        
        self.master.window.IntermediateBarWindow(
            [
            {"text":"Starting Launcher","position":0,"font":("Helvetica",18)},
            {"text":"Loading launcher files...","position":25,"font":("Helvetica",10)},
            {"text":f"running {branch} {version}","position":50,"font":("Helvetica",10)}
            ],
            {"width":300,"height":30,"posx":0,"posy":90}
        )


        run = threading.Thread(target=self.RunLauncher)
        run.start()
        
        #clear = threading.Thread(target=self.master.window.ClearAfterDuration,args=(5,))
        #clear.start()
        try:
            self.master.window.root.after(5000,self.ClearCurrentRoot)
        except Exception as e:
            print("No Root?")
        self.master.window.Start()
        
    def RunLauncher(self):
        ending = ".exe"
        if(self.master.system.systemname=="Linux"):
            ending = ".x86_64"
        

        path = os.path.join(self.paths["bin"],"launcher","Trihexangular Launcher"+ending)
        
        subprocess.Popen([path])
        logging.debug("LAUNCH - starting game launcher exectuable")
    def DownloadData(self):
        logging.debug("NETWORK - downloading launcher data")
        self.master.window.ProgressBarWindow(
            [
                {"text":"Loading data","font":("Helvetica",18),"position":0},
                {"text":"Downloading launcher data and package files","font":("Helvetica",10),"position":25}
            ],
            {"width":300,"height":30,"posx":0,"posy":90}
        )
        
        branch = self.master.pacman.data["branch"]
        url = str(self.master.pacman.data["repository"] + f"/raw/main/Server/data/{branch}_launcher_data.json")
        
        
        d_path = self.paths[".temp"]
        f_path = self.paths["data"]
        

        
        self.master.network.ThreadDownloadFile(url,d_path,f_path,"launcher_data.json",self.master.window.DataProgressHook)
        
        self.master.window.Start()
    def Install(self):
        if(self.master.nointernet):
            self.master.window.Close()
            return
        branch = self.master.pacman.data["branch"]

        launcher_number = self.master.datman.data["launcher"]["version"]
        self.master.window.ProgressBarWindow(
            [
                {"text":"Installing","font":("Helvetica",18),"position":0},
                {"text":"Downloading neccesary launcher files and extracting","font":("Helvetica",10),"position":25},
                {"text":f"Getting {branch} {launcher_number}","font":("Helvetica",10),"position":50}
            ],
            {"width":300,"height":30,"posx":0,"posy":90}
        )

        ending = ".zip"
        if(self.master.system.systemname=="Linux"):
            ending = ".x86_64"
        if(self.master.system.systemname=="Windos"):
            ending = ".exe"
   
        
        launcher_os = (self.master.system.systemname.lower())+".zip"
        print(launcher_os)
        logging.debug("OS - OSTYPE {launcher_os} install")
        url = self.master.pacman.data["repository"] + f"/releases/download/{branch}_{launcher_number}/launcher_{launcher_os}"

        
        d_path = os.path.join(self.paths[".temp"],"launcher.zip")
        e_path = os.path.join(self.paths["bin"],"launcher")

        
        self.master.network.ThreadDownloadZIP(url,d_path,e_path,self.master.window.DataProgressHook)
        self.master.window.Start()

        self.master.pacman.CheckAdd("launcher",{})
        self.master.pacman.data["launcher"]["version"] = self.master.datman.data["launcher"]["version"]
        print(self.master.pacman.data["launcher"])
        self.master.pacman.data["launcher"]["installed"]=True
    def SystemMessage(self,message):
        logging.debug(f"MESSAGE - asking message {message['name']}")
        self.master.prompt.Message(message,-1)
    
    def CompareVersion(self):
        self.DisplayError()
        logging.debug("LAUNCH - checking for avaliable updates")
        version = 0.96
        branch = "main"
        self.master.window.IntermediateBarWindow(
            [
            {"text":"Checking for updates","position":0,"font":("Helvetica",18)},
            {"text":f"running {branch} {version}","position":25,"font":("Helvetica",10)}
            ],
            {"width":300,"height":30,"posx":0,"posy":90}
        )

        vc = self.master.pacman.data["launcher"]["version"]
        vn = self.master.datman.data["launcher"]["version"]

        updateV = False
        if(vn>vc):
            updateV = True
        

        try:
            self.master.window.root.after(500,self.master.window.ClearCurrentRoot)
        except Exception as e:
            pass
        #clear = threading.Thread(target=self.master.window.ClearAfterDuration,args=(0.5,))
        #clear.start()

        #self.master.window.Start()
        if(updateV):
            logging.debug("LAUNCH - update avaliable")
            self.Install()
        else:
            logging.debug("LAUNCH - already up to date")

            


class PromptManager():
    def __init__(self,m):
        self.master=m
    def Message(self,message,ID):


        title = message["name"]
        content = message["content"]
        icon = message["icon"]
        flags = message["flags"]
        interactions = message["interactions"]


        #interactions
        buttons = interactions["buttons"]
        json = interactions.get("json")
        web = interactions.get("webopen")
        
        if(json is not None):
            for key in json.keys():
                self.master.pacman.Set(key,json[key])
        if(web is not None):
            webbrowser.open_new(web)
        names = []
        for button in buttons:
            names.append(button["text"])

        #user
        self.master.window.root.title(title), ImageTk
        

        result = self.master.window.Messagebox(content,icon,names)
        interactor = buttons[result]["interactor"]

        #resolving
        for item in interactor:
            if(item["type"]=="dismiss"):
                if(ID!=-1):
                    self.master.pacman.Append("messages",ID)
            elif(item["type"]=="dismiss-silent"):
                pass
            elif(item["type"]=="json"):
                for key in item["content"].keys():
                    self.master.pacman.Set(key,item["content"][key])
            elif(item["type"]=="url"): ############
                webbrowser.open_new(item["content"]["target"])
            elif(item["type"]=="messagelink"):
                if(item["content"]["target"]=="repeat"):
                    self.Message(message,-1)
            elif(item["type"]=="messagebuilder"):
                content = item["content"]
                self.Message(content,-1)
            elif(item["type"]=="exit"):
                exit()
            elif(item["type"]=="inputfield"):
                btns = ["Submit"]
                if(item["content"]["returnbutton"]==True):
                    btns.append("Back")
                r = self.master.window.UserInputWindow([{"text":item["content"]["name"],"position":0,"font":("Helvetica",10)}],["Submit","Back"])
                if(r[0]==0): #success
                    self.master.pacman.Set(item["content"]["fieldname"],r[1])
                else:
                    self.Message(message,ID)
                    return
            else:
                print(f"Error, cant find interator type for {item}")

class Window():
    def __init__(self,m):
        theme = ctk.ThemeManager.theme
        theme["CTkButton"]["fg_color"] = ["#00790e","#00790e"]
        theme["CTkButton"]["hover_color"] =["#004508","#00ce18"]
        theme["CTkProgressBar"]["progress_color"] = ["#00790e","#00790e"]
        my_theme = {
            "CTk": {"fg_color": ["#f2f2f2", "#1a1a1a"]},
            "CTkButton": {
                "fg_color": ["#2CC985","#2FA572"],
                "hover_color": ["#27ae60","#219150"],
                "text_color": ["#ffffff","#ffffff"],
                "corner_radius":1,
                "border_width":3,
                "border_color": ["#ffffff","#ffffff"],
                "text_color_disabled": ["#ffffff","#ffffff"],

            },
            "CTkLabel": {
                "text_color": ["#1a1a1a","#eeeeee"],
                "fg_color": ["#2CC985","#2FA572"],
                "hover_color": ["#27ae60","#219150"],
                "corner_radius":1
            }
        }

        ctk.ThemeManager.theme = theme


        self.master=m
        self.root = ctk.CTk()
        self.root.resizable(False, False)
        self.root.geometry("300x120")
        self.root.title("Trihexangular Launcherc")






        img_bytes = base64.b64decode(systemmessages.logobytes)
        img_pil = Image.open(io.BytesIO(img_bytes))

        # 3. Convert PIL to a Tkinter-compatible PhotoImage
        # This is what root.iconphoto actually wants
        tk_icon = ImageTk.PhotoImage(img_pil)

        # 4. Set the icon
        self.root.update_idletasks()
        self.root.iconphoto(True, tk_icon)


        self.closeflag = False
        ctk.set_appearance_mode("Dark") 
    def ClearAfterDuration(self,duration):
        
        try:
            self.root.after(duration*1000, lambda: self.Close())
        
        except Exception as e:
            print(f"Cannot Exit: {e}")
            self.root.quit()
            self.root.destroy()
            sys.exit()
            os._exit(0)
    def Clear(self):
        for w in self.root.winfo_children():
            w.destroy()
    def Center(self):
        x = int((self.root.winfo_screenwidth()-300)/2)
        y = int((self.root.winfo_screenheight()-120)/2)

        self.root.geometry(f"{300}x{120}+{x}+{y}") #why does tkinter use string its painful,
    def Start(self):
        self.root.mainloop()
    def Close(self):
        self.root.quit()
        self.Clear()
    def Destroy(self):
        self.root.destroy()
    def Flags(self):
        self.root.bind("<Destroy>", self.OnUserDestroy) 
    def ProgressBarWindow(self, text, bar):
        for c in text:
            l = ctk.CTkLabel(self.root,text = c["text"],font=c["font"],width=300)
            l.place(x=0,y=c["position"])
    
            


        self.progress_bar = ctk.CTkProgressBar(self.root, width=bar["width"], height=bar["height"])
        self.progress_bar.place(x=bar["posx"],y=bar["posy"])
        self.progress_bar.set(0)
    def UserInputWindow(self,text,buttons):
        canvas = ctk.CTkCanvas(self.root,width=300,height=80,bg="#2a2a2a",bd=0,highlightthickness=0,borderwidth=0)
        canvas.place(x=0,y=0)

        for c in text:
            l = ctk.CTkLabel(self.root,text = c["text"],font=c["font"],width=300)
            l.place(x=0,y=c["position"])


        count = len(buttons)
        if(count>4):
            error("Too many buttons")

        i = 0


        e = ctk.CTkTextbox(canvas, width=250,height=60,font=("Helvetica",10))
        e.place(x=25,y=20)
        e.insert("0.0", r"https://github.com/DevCyclonekitten/Trihexangular-Launcher")

        self.result = -1
        margin = 7
        totalmargin = margin*(count+1)
        effectivewidth = 300-totalmargin
        for b in buttons:
            c = ctk.CTkButton(self.root,text=b,width=effectivewidth/count,height=40-(2*margin),command=lambda res=i: self.ButtonResult(res))
            x=margin+i*(300/count)
            c.place(x=x,y=80+margin)
            i+=1
        
        while self.result==-1:
            self.root.update()
        
        val = e.get("1.0", "end-1c")
        
        self.Close()
        return [self.result,val]
    def Messagebox(self,text,icon,buttons):
        canvas = ctk.CTkCanvas(self.root,width=300,height=80,bg="#2a2a2a",bd=0,highlightthickness=0,borderwidth=0)
        canvas.place(x=0,y=0)

        for c in text:
            l = ctk.CTkLabel(self.root,text = c["text"],font=c["font"],width=300)
            l.place(x=0,y=c["position"])


        count = len(buttons)
        if(count>4):
            error("Too many buttons")

        i = 0


        self.result = -1
        margin = 7
        totalmargin = margin*(count+1)
        effectivewidth = 300-totalmargin
        for b in buttons:
            c = ctk.CTkButton(self.root,text=b,width=effectivewidth/count,height=40-(2*margin),command=lambda res=i: self.ButtonResult(res))
            x=margin+i*(300/count)
            c.place(x=x,y=80+margin)
            i+=1
        
        while self.result==-1:
            self.root.update()
        
        
        self.Close()
        return self.result
    def ButtonResult(self,i):
        self.result = i
    def IntermediateBarWindow(self,text,bar):
        for c in text:
            l = ctk.CTkLabel(self.root,text = c["text"],font=c["font"],width=300)
            l.place(x=0,y=c["position"])

        

        self.progress_bar = ctk.CTkProgressBar(self.root, width=bar["width"], height=bar["height"])
        self.progress_bar.place(x=bar["posx"],y=bar["posy"])
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
    def TextContentWindow(self,text):
        for c in text:
            l = ctk.CTkLabel(self.root,text = c["text"],font=c["font"],width=300,height=30)
            l.place(x=0,y=c["position"])
    def OnUserDestroy(event):
        if event.widget == root: 
            print("UserExit")
        
    def DataProgressHook(self, count, block, size):
        if(count == "downloadsuccessful"):
            print("Destroy")
            try:
                self.root.after(0, lambda: self.Close())
            except Exception as e:
                exit()
        else:
            if size > 0:
                
                percent = count*block/size
                self.root.after(0, lambda: self.progress_bar.set(percent))
                

            else:
                self.root.after(0, lambda: self.progress_bar.set(1.0))

                try:
                    self.root.after(0.1, lambda: self.Close())
                except Exception as e:
                    exit()
class NetworkManager():
    def ThreadDownloadZIP(self,url,d_path,e_path,processhook):
        t=threading.Thread(target=self.DownloadZIP,args=(url,d_path,e_path,processhook))
        t.start()
    def ThreadDownloadFile(self,url,d_path,f_path,f_name,processhook):
        t=threading.Thread(target=self.DownloadFile,args=(url,d_path,f_path,f_name,processhook))
        t.start()

    def __init__(self,m):
        self.master=m
        self.tempfolder = ""
    def DownloadZIP(self, url, d_path, e_path, processhook):
        logging.debug(f"NETWORK - downloading zip '{url}'")
        try:
            if os.path.exists(d_path):
                try:
                    os.remove(d_path)
                except Exception as e:
                    self.ErrorMessageBox(f"141: Error deleting existing zip: {e}",processhook)
            try:
                if(processhook != None):
                    urllib.request.urlretrieve(url, d_path,reporthook=processhook)
            except Exception as e:
                self.ErrorMessageBox(f"ERROR - download error: {e} {url}",processhook)
                
            try:
                with zipfile.ZipFile(d_path, 'r') as zip_ref:
                    zip_ref.extractall(e_path)
                try:
                    ending = ".exe"
                    if(self.master.system.systemname=="Linux"):
                        ending = ".x86_64"
                    fp = os.path.join(e_path,"Trihexangular Launcher"+ending)
                    st = os.stat(fp)
                    os.chmod(fp, st.st_mode | stat.S_IEXEC)

                except Exception as e:
                    print(f"TAG - Could not give executable tag to file - {e}")
                    #logging.log("TAG - Could not give executable tag to file")

            except zipfile.BadZipFile as e:
                self.ErrorMessageBox(f"ERROR - extraction failed due to bad zip file - {e}",processhook)
                
            except Exception as e:
                self.ErrorMessageBox(f"ERROR - extraction failed due to {e}",processhook)
                
            try:
                os.remove(d_path)
            except Exception as e:
                self.ErrorMessageBox(f"ERROR - failed to delete zip after use {e}",processhook)
            
            processhook("downloadsuccessful",0.1,0.1)
        except Exception as e:
            self.ErrorMessageBox(f"ERROR - an unexpected error occured {e}",processhook)
    def DownloadFile(self,url,d_path,f_path,filename,processhook=None):
        logging.debug(f"NETWORK - downloading file '{url}'")
        print("SAFE")
        try:

            os.makedirs(d_path, exist_ok=True)
            try:
                goodfp =os.path.join(d_path,filename)
                urllib.request.urlretrieve(url,goodfp,reporthook=processhook)
                shutil.move(goodfp,os.path.join(f_path,filename))
            except Exception as a:
                print(a)
                self.ErrorMessageBox(f"NETWORK - {a}",processhook)
            
            processhook("downloadsuccessful",0.1,0.1)
            
        except Exception as e:
            self.ErrorMessageBox(f"UNKNOWN - {e}",processhook)
        

    def ErrorMessageBox(self,string,process):
        process("downloadsuccessful",0.1,0.1)

        m = systemmessages.systemerror
        m["content"][1]["text"] = string

        self.master.currenterror = m
        logging.error(string)


class Manager():
    def __init__(self):
        self.nointernet=False
        self.currenterror = {}
       
        

        
        self.system = SystemManager(self)
        self.system.Configure()
        self.pacman = PackageManager(self,False)
        self.system.ApplyAwait()
        self.datman = PackageManager(self,True)
        self.network = NetworkManager(self)
        self.prompt = PromptManager(self)
        self.window = Window(self)

        self.window.Center()
        

        try:
            self.pacman.GetPackages()
            isInstalled = self.pacman.data["launcher"]["installed"]
        except Exception as e:
            isInstalled = False

        
        #isInstalled=False
        if(isInstalled): 
            self.system.DownloadData()
            self.datman.GetPackages()
            self.system.CompareVersion()
            self.system.Start()

        else: 
            self.system.SystemMessage(systemmessages.systemwelcome)
            #self.system.SystemMessage(systemmessages.systemos)
            self.system.SystemMessage(systemmessages.systemeula)
            self.system.SystemMessage(systemmessages.systemrepository)
            self.system.SystemMessage(systemmessages.systembranch)
            

            self.system.DownloadData()
            self.datman.GetPackages()
            
            self.system.Install()
            self.system.Start()

        self.pacman.Read()
        self.pacman.SetPackages()

m = Manager()