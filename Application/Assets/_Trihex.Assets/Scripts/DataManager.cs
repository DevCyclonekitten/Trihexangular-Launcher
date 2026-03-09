using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using TMPro;

[System.Serializable]
public class LibraryData {
    public SerializableDictionary<string, string[]> currentLibraryGames;
    public List<string> messageIDs = new List<string>();
    public double assetVersion;
}

[System.Serializable]
public class PackageData {
    public string repository;
    public string system;
    public string branch;
    public bool eula;
    
}
[System.Serializable]
public class SettingsData {
    public bool linuxUseWine;
    public bool showDebugLog;
    public bool dontUpdateLauncher;
    public string branch;
}

public class DataManager : MonoBehaviour
{
    [Header("Settings: ")]
    public bool justloaddata;
    public float delayedStartTime=0.03f;
    [Header("Data: ")]
    public ApplicationPath ap;
    private string packagepath;
    private string librarypath;
    private string settingspath;
    public PackageData packageData;
    public LibraryData libraryData;
    public SettingsData settingsData;

    [Header("Display Mesage: ")]
    public Message currentMessage;
    public TextMeshProUGUI messageTitle;
    public TextMeshProUGUI messageDescription;
    public GameObject messageWindow;
    public List<string> laterMessageIDs = new List<string>();
    

    //MonobehaviourStuff
    void Start() {
        if(!justloaddata){
            messageWindow.SetActive(false);
        }
        if(delayedStartTime==0f){
            DelayedStart();
            return;
        }
        Invoke("DelayedStart",delayedStartTime);
    } 
    void DelayedStart(){
        packagepath = Path.Combine(ap.GetPath(), "data","packages.json");
        librarypath = Path.Combine(ap.GetPath(), "data","library_data.json");
        settingspath = Path.Combine(ap.GetPath(),"data","settings.json");
        
        LoadPackage();
        LoadLibrary();
        LoadSettings();

        if(justloaddata) return;
        DisplayNextMessage();
    }

    //SETTINGS ///////////////////////////
    public void SaveSettings(){
        
        string fs = JsonUtility.ToJson(settingsData, true);
        File.WriteAllText(settingspath, fs);

    }
    public void LoadSettings(){
        if (File.Exists(settingspath)){
            string fs = File.ReadAllText(settingspath);
            settingsData = JsonUtility.FromJson<SettingsData>(fs);
        }
        else{SaveSettings();}
    }
    //PACKAGES /////////////////////////
    public void SavePackage(){
        
        string fs = JsonUtility.ToJson(packageData, true);
        File.WriteAllText(packagepath, fs);

    }
    public void LoadPackage(){
        if (File.Exists(packagepath)){
            string fs = File.ReadAllText(packagepath);
            packageData = JsonUtility.FromJson<PackageData>(fs);
        }
        else{SavePackage();}
    }

    //LIBRARY /////////////////////////
    public void SaveLibrary(){
        string fs = JsonUtility.ToJson(libraryData, true);
        File.WriteAllText(librarypath, fs);
    }

    public void LoadLibrary(){
        if (File.Exists(librarypath)){
            string fs = File.ReadAllText(librarypath);
            libraryData = JsonUtility.FromJson<LibraryData>(fs);
        }
        else{
            ResetLibrary();
        }
    }
    public void ResetLibrary(){
        if(File.Exists(librarypath)){
            File.Delete(librarypath);
        }
        libraryData = new LibraryData();
        libraryData.messageIDs = new List<string>();
            foreach(Message m in ap.nm.dataObject.content.messages){
                libraryData.messageIDs.Add(m.id);
            }
        SaveLibrary();
        UnityEngine.SceneManagement.SceneManager.LoadSceneAsync("Loading");
    }
    // MESSAGES ////////////////////////
    public void RemindLaterNextMessage(){
        laterMessageIDs.Add(currentMessage.id);
        DisplayNextMessage();
    }
    public void DismissNextMessage(){
        libraryData.messageIDs.Add(currentMessage.id);
        SaveLibrary();
        DisplayNextMessage();
    }
    public void DisplayNextMessage(){
        List<Message> applicableMessages = new List<Message>();

        foreach(Message mc in ap.nm.dataObject.content.messages){
            bool dismissed=false;
            foreach(string id in libraryData.messageIDs){
                if(mc.id==id){
                    dismissed=true;
                    
                }
            }
            foreach(string lid in laterMessageIDs){
                if(mc.id==lid){
                    dismissed=true;
                    
                }
            }
            if(!dismissed) applicableMessages.Add(mc);
        }

        if(applicableMessages.Count==0){
            messageWindow.SetActive(false);
            return;
        }
        messageWindow.SetActive(true);

        Message m =applicableMessages[0];
        currentMessage=m;
        messageTitle.SetText(m.name);
        messageDescription.SetText(m.content[0].content[0]);
    }


    
    
    
    
}