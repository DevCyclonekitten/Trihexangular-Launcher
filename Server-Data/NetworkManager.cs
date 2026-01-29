using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
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


    void Start(){
        if(control_downloadData){
            GetLauncherData();
        }
        else{
            if(control_loadData){
                LoadJsonData(Path.Combine(ap.GetPath(), "data","launcher_data.json"));
            }
        }
    }

    void DisplayText(string text){
        if(ui_loadingDescription != null){
            ui_loadingDescription.SetText(text);
        }
    }
    public void GetLauncherData(){
        string url = ap.repository+"/raw/main/Server/data/launcher_data.json";
        string pth = Path.Combine(ap.GetPath(),"data");
        string fn = "launcher_data.json";


        DisplayText("Downloading launcher_data.json");
        StartCoroutine(DownloadFile(url,pth,fn,true));

        
    }
    public void LoadLibrary(){
        DisplayText("Loading library");
        UnityEngine.SceneManagement.SceneManager.LoadSceneAsync("Library");
    }
    void Quit(){
        Application.Quit();
    }

    
    void LoadJsonData(string path)
    {
        DisplayText("Loading launcher data");
        if (File.Exists(path)){
            dataObject=JsonUtility.FromJson<JSONDataObject>(File.ReadAllText(path));
            if(control_loadLibrary){
                LoadLibrary();
            }
        }   
        else{
            DisplayText("Cannot load launcher data, exiting launcher");
            Invoke("Quit",3f);
        }

    }


    [Header("Enumerator Ecc")]
    public bool ecc_yield_result;

    private IEnumerator DownloadFile(string url,string f_path,string filename,bool loaddataflag){

        using (UnityWebRequest www = UnityWebRequest.Get(url))
        {
            yield return www.SendWebRequest();

            if (www.result != UnityWebRequest.Result.Success){
                ecc_yield_result = false;
                UnityEngine.Debug.Log(www.result);
                yield break;
            }

            try{

                File.WriteAllBytes(Path.Combine(f_path,filename), www.downloadHandler.data);
                ecc_yield_result = true;
                
                if(control_loadData&&loaddataflag){
                    LoadJsonData(Path.Combine(ap.GetPath(),"data","launcher_data.json"));
                }
                yield break;
            }
            catch (System.Exception e){
                ecc_yield_result = false;
                UnityEngine.Debug.Log(e);
                yield break;
            }
        }




    }


    public Game GetGameFromID(string i){
        foreach(Game g in dataObject.content.games){
            if(g.id==i){
                return g;
            }
        }
        return null;
    }
    
    
    public IEnumerator DownloadZIP(string url, string d_path,string f_path, string filename){
        UnityEngine.Debug.Log("Downloading: "+url);
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
            if (request.result != UnityWebRequest.Result.Success){UnityEngine.Debug.Log("Download Error: " + request.error);yield break;}
            if (request.downloadHandler.data == null || request.downloadHandler.data.Length == 0){UnityEngine.Debug.Log("Downloaded data is empty or null.");yield break;}

            //Write Downloaded
            try{
                File.WriteAllBytes(d_zip, request.downloadHandler.data);
            }
            catch (System.Exception e){UnityEngine.Debug.Log("Error saving the file: " + e.Message);yield break;}

            //Extract
            try{
                ZipFile.ExtractToDirectory(d_zip, f_file);
            }
            catch (System.Exception){UnityEngine.Debug.Log("Extraction failed: ");yield break;}
            //Delete
            try{
                File.Delete(d_zip);
            }
            catch (System.Exception e){UnityEngine.Debug.Log("Error deleting zip after extraction: " + e.Message);}
            UnityEngine.Debug.Log("Downloaded: "+url);
        }
    }

    [System.Serializable]
    public class JSONDataObject{
        public double manifest;
        public Launcher launcher;
        public Content content;
            
    }

   

}





[System.Serializable]
public class Launcher {
    public double version;
}

[System.Serializable]
public class Content {
    //public Messages[] messages;
    
    public Game[] games;
    public Bundle[] bundles;
    public Container[] collections;
}

///////////////////////////// GAME /////////////////////////

[System.Serializable]
public class Game {
    public string name;
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
    public string type;
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

}


////////// PACKAGE MANAGER


