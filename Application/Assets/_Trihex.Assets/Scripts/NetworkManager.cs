using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.Linq;
using System.IO;
using System.IO.Compression;
using System.Diagnostics;
using UnityEngine.UI;
using TMPro;
using Newtonsoft.Json;
public class NetworkManager : MonoBehaviour
{   
    public ApplicationPath ap;
    
    [Header("JSON")]
    public JSONDataObject dataObject;
    
    [Header("UI: ")]
    public TextMeshProUGUI ui_loadingDescription;
    [Header("Controls: ")]
    public bool control_downloadData;
    public bool control_loadData;
    public bool control_loadLibrary;
    public bool control_downloadAssets;
    public bool control_forceDownloadAssets;
    [Header("Enumerator Ecc")]
    public bool ecc_yield_result;

    // MONOBEHAVIOUR STUFF ///////////
    void Start(){Invoke("DelayedStart",0.01f);}void DelayedStart(){
        if(control_downloadData){
            GetLauncherData();
        }
        else{
            if(control_loadData){
                LoadLauncherData(Path.Combine(ap.GetPath(), "data","launcher_data.json"));
            }
        }
    }
    // GETTING /////////
    public void GetAssets(){
        if(Directory.Exists(Path.Combine(ap.GetPath(),"data","assets"))){
            double cv = dataObject.launcher.assetversion;
            double installed = ap.dm.libraryData.assetVersion;
            UnityEngine.Debug.Log("[NETWORK] Current asset version "+installed.ToString() +" -> "+cv.ToString());
            if(cv<=installed){
                UnityEngine.Debug.Log("[NETWORK] Skipping getting assets");
                LoadLibrary();return;
            }
            //continue and get
            
        }
        string url = ap.repository+ "/raw/main/Server/data/Assets.zip";
        UnityEngine.Debug.Log("[NETWORK] Downloading Assets: "+url);
        string tpth = Path.Combine(ap.GetPath(),".temp");
        string pth = Path.Combine(ap.GetPath(),"data");
        string fn = "assets";

        DisplayLoadingText("Downloading assets");
        StartCoroutine(DownloadZIP(url,tpth,pth,fn,true));
    }
    public Game GetGameFromID(string i){
        foreach(Game g in dataObject.content.games){
            if(g.id==i){
                return g;
            }
        }
        return null;
    }
    public void GetLauncherData(){
        string branch = ap.dm.packageData.branch;
        string url = ap.repository+"/raw/main/Server/data/"+branch+"_launcher_data.json";
        UnityEngine.Debug.Log("[NETWORK] Downloading Data "+url);
        string pth = Path.Combine(ap.GetPath(),"data");
        string fn = "launcher_data.json";


        DisplayLoadingText("Downloading launcher_data.json");
        StartCoroutine(DownloadFile(url,pth,fn,true));

        
    }
    void LoadLauncherData(string path){
        UnityEngine.Debug.Log("[NETWORK] Loading launcher data");
        DisplayLoadingText("Loading launcher data");
        if (File.Exists(path)){
            dataObject=JsonUtility.FromJson<JSONDataObject>(File.ReadAllText(path));
            dataObject.SortGamesByID();
            
            if(control_loadLibrary&&!control_downloadAssets){
                LoadLibrary();
            }
            else if(control_downloadAssets){
                GetAssets();
            }
        }   
        else{
            DisplayLoadingText("Cannot load launcher data, exiting launcher");
            Invoke("Quit",3f);
        }

    }

    // Managing ///////////////////////////
    

    public void DisplayLoadingText(string text){
        if(ui_loadingDescription != null){
            ui_loadingDescription.SetText(text);
        }
    }

    public void LoadLibrary(){
        DisplayLoadingText("Loading library");
        UnityEngine.SceneManagement.SceneManager.LoadSceneAsync("Library");
    }
    

    

    // DOWNLOAD HANDLERS/////////////
    public void DownloadFileHandler(bool loaddataflag,bool success){
        if(control_loadData&&loaddataflag){
            LoadLauncherData(Path.Combine(ap.GetPath(),"data","launcher_data.json"));
        }
    }
    public void DownloadAssetFileHandler(bool loaddataflag,bool success){
        if(loaddataflag&&success){
            UnityEngine.Debug.Log("[NETWORK] Loading Assets");
            double cv = dataObject.launcher.assetversion;
            ap.dm.libraryData.assetVersion=cv;
            ap.dm.SaveLibrary();
            UnityEngine.Debug.Log("[NETWORK] Loaded Asset version "+ap.dm.libraryData.assetVersion);
            LoadLibrary();
        }
    }
    public void DownloadZIPHandler(){
        if(control_loadLibrary){
            //LoadLibrary();
        }
    }
    
    // DOWNLOADING
    public IEnumerator DownloadFile(string url,string f_path,string filename,bool loaddataflag){

        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success){
                ecc_yield_result = false;
                UnityEngine.Debug.LogError("[NETWORK] Download file error "+www.result);
                DownloadFileHandler(loaddataflag,false);
                DisplayLoadingText("Failed to download file");
                yield break;
            }

            try{
                DisplayLoadingText("Writing file");
                File.WriteAllBytes(Path.Combine(f_path,filename), www.downloadHandler.data);
                ecc_yield_result = true;
                DisplayLoadingText("Loading file");
                
                DownloadFileHandler(loaddataflag,true);
                yield break;
            }
            catch (System.Exception e){
                ecc_yield_result = false;
                UnityEngine.Debug.Log("[NETWORK] Download file error "+e);
                //DisplayLoadingText("Failed to get assets");
                DownloadFileHandler(loaddataflag,false);
                yield break;
            }
        }




    }
    public IEnumerator DownloadZIP(string url, string d_path,string f_path, string filename,bool loaddataflag){
        UnityEngine.Debug.Log("[NETWORK] Downloading "+url);
        string d_zip = Path.Combine(d_path,filename);
        string f_file = Path.Combine(f_path,filename);

        //Generate Dirs in case
        if (!Directory.Exists(d_path)){Directory.CreateDirectory(d_path);}
        if (!Directory.Exists(f_path)){Directory.CreateDirectory(f_path);}

        if (File.Exists(d_zip)){
            try{File.Delete(d_zip);}
            catch (System.Exception e){ ecc_yield_result = false; yield break;}
        }

        using (UnityWebRequest request = UnityWebRequest.Get(url))
        {
            yield return request.SendWebRequest();


            //Download ecc
            if (request.result != UnityWebRequest.Result.Success){UnityEngine.Debug.LogError("[NETWORK] Download zip error " + request.error);DownloadZIPHandler();DownloadAssetFileHandler(loaddataflag,false);yield break;}
            if (request.downloadHandler.data == null || request.downloadHandler.data.Length == 0){UnityEngine.Debug.LogError("[NETWORK] Downloaded data is empty or null");DownloadZIPHandler();DownloadAssetFileHandler(loaddataflag,false);yield break;}

            //Write Downloaded
            try{
                File.WriteAllBytes(d_zip, request.downloadHandler.data);
            }
            catch (System.Exception e){UnityEngine.Debug.LogError("[NETWORK] Error saving the file " + e.Message);DownloadZIPHandler();DownloadAssetFileHandler(loaddataflag,false);yield break;}

            //Extract
            try{
                ZipFile.ExtractToDirectory(d_zip, f_file,true);
            }
            catch (System.Exception e){
                UnityEngine.Debug.LogError("[NETWORK] Extraction failed "+e.Message);DownloadZIPHandler();DownloadAssetFileHandler(loaddataflag,false);yield break;
            }
            //Delete
            try{
                File.Delete(d_zip);
            }
            catch (System.Exception e){UnityEngine.Debug.LogError("[NETWORK] Error deleting zip after extraction" + e.Message);DownloadAssetFileHandler(loaddataflag,false);}
            UnityEngine.Debug.Log("[NETWORK] Downloaded "+url);
            
            DownloadAssetFileHandler(loaddataflag,true);
        }
    }
    public IEnumerator DownloadZIPWithHandler(string url, string d_path,string f_path, string filename,GameManager gm){
        UnityEngine.Debug.Log("[NETWORK] Downloading "+url);
        string d_zip = Path.Combine(d_path,filename);
        string f_file = Path.Combine(f_path,filename);

        //Generate Dirs in case
        if (!Directory.Exists(d_path)){Directory.CreateDirectory(d_path);}
        if (!Directory.Exists(f_path)){Directory.CreateDirectory(f_path);}

        if (File.Exists(d_zip)){
            try{File.Delete(d_zip);}
            catch (System.Exception e){ ecc_yield_result = false; UnityEngine.Debug.LogError("[NETWORK] File delete error"+e); yield break;}
        }
        if (Directory.Exists(Path.Combine(f_path,filename))){
            try{Directory.Delete(Path.Combine(f_path,filename),true);}
            catch (System.Exception e){ ecc_yield_result = false; UnityEngine.Debug.LogError("[NETWORK] Directory delete error"+e); yield break;}
        }
        gm.downloading = true;
        gm.playButtonImage.color = new Color(0.4f,0f,0.4f);
        gm.playButtonText.SetText("DOWNLOADING");

        using (UnityWebRequest request = UnityWebRequest.Get(url))
        {
            yield return request.SendWebRequest();


            //Download ecc
            if (request.result != UnityWebRequest.Result.Success){UnityEngine.Debug.LogError("[NETWORK] Download Error " + request.error);yield break;}
            if (request.downloadHandler.data == null || request.downloadHandler.data.Length == 0){UnityEngine.Debug.LogError("[NETWORK] Downloaded data is empty or null.");yield break;}

            //Write Downloaded
            try{
                File.WriteAllBytes(d_zip, request.downloadHandler.data);
            }
            catch (System.Exception e){UnityEngine.Debug.LogError("[NETWORK]  Error saving the file " + e.Message);yield break;}

            //Extract
            try{
                //SET BUTTON TO EXTRACTING
                gm.playButtonImage.color = new Color(0.65f,0f,1f);
                gm.playButtonText.SetText("EXTRACTING");


                //EXTRACT
                ZipFile.ExtractToDirectory(d_zip, f_file);
                string attachpath = gm.currentGame.name+ap.sm.GetGameExeType(gm.currentGame);
                string exePath = Path.Combine(f_file, attachpath);
                if(System.IO.File.Exists(exePath) && ap.operatingSystem==OS.Linux){
                    ApplyLinuxExecutionPermissions(exePath);
                }

                // SET BUTTON TO PREPARING
                gm.playButtonImage.color = new Color(0.4f,0f,0.4f);
                gm.playButtonText.SetText("PREPARING");
                gm.downloading=false;
            }
            catch (System.Exception e){UnityEngine.Debug.LogError("[NETWORK]  Extraction failed " + e.Message);yield break;}
            //Delete
            try{File.Delete(d_zip);}
            catch (System.Exception e){UnityEngine.Debug.LogError("[NETWORK]  Error deleting zip after extraction " + e.Message);}

            

            if(ap.operatingSystem==OS.Linux&&ap.sm.CheckGameOSCompatibility(gm.currentGame)==2){//ap.sm.CheckGameValid(currentGame)==2){
                string p1 = Path.Combine(f_path,filename);
                string[] dir = Directory.GetDirectories(p1);
                FixWinePrefixDirectoryStructure(dir[0]);

                string attachpath = gm.currentGame.name+"."+"exe"; //ap.sm.GetGameExeType(gm.currentGame);
                string exePath = Path.Combine(f_file, attachpath);

                ApplyLinuxExecutionPermissions(exePath);
            }
            else{
                UnityEngine.Debug.Log(" [NETWORK] Skipping windows to linux wine zip compatibility directory extraction");
            }

            UnityEngine.Debug.Log("[NETWORK] Downloaded "+url);
        }
    }


    // LINUX COMPATIBILITY ////////
    public void ApplyLinuxExecutionPermissions(string exePath){
        UnityEngine.Debug.Log("[NETWORK] Attaching x tag to "+exePath);
        var process = new System.Diagnostics.Process();
        process.StartInfo.FileName = "chmod";
        process.StartInfo.Arguments = "+x \"" + exePath + "\"";
        process.StartInfo.UseShellExecute = false;
        process.Start();
        process.WaitForExit();

    }
    public void FixWinePrefixDirectoryStructure(string p2){

        string p = Directory.GetParent(p2).FullName;


        string[] files = Directory.GetFiles(p2);
        foreach (string file in files)
        {
            string fileName = Path.GetFileName(file);
            string destPath = Path.Combine(p, fileName);

            File.Move(file, destPath);
        }

        string[] dirs = Directory.GetDirectories(p2);
        foreach (string dir in dirs)
        {
            string dirName = new DirectoryInfo(dir).Name;
            string destPath = Path.Combine(p, dirName);
            
            Directory.Move(dir, destPath);
        }
    }

    // MANAGING
    void QuitLauncher(){
        Application.Quit();
    }

    // SERIALIZABLE
    [System.Serializable]
    public class JSONDataObject{
        public double manifest;
        public Launcher launcher;
        public Content content;

        public void SortGamesByID(){
            this.content.games = this.content.games.OrderBy(game => int.Parse(game.id)).ToArray();
        }
            
    }
    
    [System.Serializable]
    public class JSONPackageObject{
        public string system;
        public string repository;
        public string eula;
    }
   

}





[System.Serializable]
public class Launcher {
    public double version;
    public double assetversion;
}

[System.Serializable]
public class Content {
    //public Messages[] messages;
    
    public Game[] games;
    public Bundle[] bundles;
    public Container[] collections;
    public Message[] messages;
}

///////////////////////////// GAME /////////////////////////

[System.Serializable]
public class Game {
    public string name;
    public bool invisible;
    public string id;
    public string programmingname;
    public string[] author;

    public GameContent content;
    public GamePurchasing purchasing;
    public GameBuilds builds;
}

[System.Serializable]
public class GameContent {
    public GameContentGeneral general;
    public GameContentStore store;
}

[System.Serializable]
public class GameContentGeneral {
    public string[] iconimages;
    public string[] displayimages;
    public string[] displayvideo;
}

[System.Serializable]
public class GameContentStore {
    public UltraText[] storefaq;
    public UltraText[] storecontent;
    public UltraText[] storedescription;
}

[System.Serializable]
public class UltraText {
    public string type; //text, content=[line, position,font]
    public string[] content;

}

[System.Serializable]
public class GamePurchasing {
    public double price;
}

[System.Serializable]
public class GameBuilds {
    public string[] windows;
    public string[] mac;
    public string[] linux;
    
}


/////////////////////// OTHER ////////////////////////



[System.Serializable]
public class Bundle{
    public string name;
    public string id;
    public string description;
    public string[] games;
    public double price;
    public string[] images;
}

[System.Serializable]
public class Container{
    public string name;
    public string id;
    public string description;
    public string[] games;
    public string sortby;
}




[System.Serializable]
public class Message{
    public string id;
    public string name;
    public UltraText[] content;
    public string icon;
    public string images;
    public Flag flags;
    public MessageInteractions interactions;
}
[System.Serializable]
public class Flag{
    public int exit_after;
    public int persistent;
    public int invisible;
    public int priority;
}
[System.Serializable]
public class MessageInteractions{
    public UltraText[] buttons;
}


////////// PACKAGE MANAGER


