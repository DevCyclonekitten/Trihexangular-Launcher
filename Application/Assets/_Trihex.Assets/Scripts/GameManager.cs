using System.IO;
using System.IO.Compression;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Collections;
using System.Collections.Generic;

using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.Video;
using UnityEngine.UI;

using TMPro;


public class GameManager : MonoBehaviour
{
    [Header("References:")]
    public ApplicationPath ap;
    public AssetManager am;
    public Game currentGame;

    [Header("UI: ")]
    public Image playButtonImage;
    public TextMeshProUGUI playButtonText;
    public bool validityThroughWine;
    public bool downloading;
    public bool invalidOS;
    public GameObject settingsObject;
    public GameObject installButtonVersionSelect;
    public TMP_Dropdown dropdownField;
    
    // MONOBEHAVIOUR STUFF //////////
    void Start(){Invoke("DelayedStart",0.01f);installButtonVersionSelect.SetActive(false);} void DelayedStart(){
        InvokeRepeating("InfrequentUpdate",0.1f,0.1f);
        //InstallGame("0.1");
        
    }
    void InfrequentUpdate(){
        //UnityEngine.Debug.Log(currentGame.programmingname);
        UpdateGameButton();
    }
    // UI MANAGING ////////////////
    public void StartButton(){
        if(invalidOS){return;}
        if(downloading){return;}
        currentGame = ap.lm.currentGame;

        if(File.Exists(ap.sm.GetGamesPath(currentGame))){
            StartExecutable(ap.sm.GetGamesPath(currentGame));
        }
        else{
            PopulateVersionOptions();
            installButtonVersionSelect.SetActive(true);
        }
    }
    public void InstallStartButton(){
        if(true){
            string p =Path.Combine(ap.persistentDataPath,"bin","games",currentGame.programmingname);
            if(Directory.Exists(p)) Directory.Delete(p,true);
            
        }
        try{
            string version = ap.sm.GetVersionOptions(currentGame)[dropdownField.value];
            if(version==""){
                try{
                    version = ap.sm.GetVersionOptions(currentGame)[0];
                }
                catch{
                    UnityEngine.Debug.LogError("[GAME] No version options for "+currentGame.programmingname);
                    return;
                }
                
            }
            UnityEngine.Debug.Log("[GAME] Installing version"+version);
            InstallCurrentGame(version);
        }
        catch{
            UnityEngine.Debug.LogError("[GAME] No version options for "+currentGame.programmingname);
            return;
        }

        
        
    }
    public void UpdateGameButton(){
        
        currentGame = ap.lm.currentGame;
        int resultMap = ap.sm.CheckGameOSCompatibility(currentGame);

        validityThroughWine=false;
        //UnityEngine.Debug.Log(resultMap);
        if(resultMap==2){
            invalidOS=false;
            validityThroughWine=true;
        }
        if(resultMap==1){
            invalidOS=false;
        }
        if(resultMap==0){
            invalidOS=true;
        }

        if(downloading){
            settingsObject.SetActive(false);
            return;
        }
        if(File.Exists(ap.sm.GetGamesPath(currentGame))){
            if(validityThroughWine){
                playButtonImage.color = new Color(0.125f,0.5f,0.5f);
                playButtonText.SetText("PLAY WINE");
                settingsObject.SetActive(true);
            }
            else{
                playButtonImage.color = new Color(0.25f,1f,1f);
                playButtonText.SetText("PLAY");
                settingsObject.SetActive(true);
            }
            
        }
        else{
            if(validityThroughWine&&!invalidOS){
                playButtonImage.color = new Color(0.8f,0.4f,0.20f);
                playButtonText.SetText("INSTALL WINE");
                settingsObject.SetActive(false);
                return;
            }
            else if(!invalidOS){
                playButtonImage.color = new Color(1f,0.5f,0.25f);
                playButtonText.SetText("INSTALL");
                settingsObject.SetActive(false);
                return;
            }
            if(invalidOS){
                playButtonImage.color = new Color(0.2f,0.2f,0.2f);
                playButtonText.SetText("NOT COMPATIBLE");
                settingsObject.SetActive(false);
                return;
            }
            
        }
    }
    public void PopulateVersionOptions(){
        string[] array = ap.sm.GetVersionOptions(currentGame);
        foreach(string s in array){
            //UnityEngine.Debug.Log("[GAME] Filled dropdown with build"+s);
        }
        array[array.Length-1] = "Latest - "+array[array.Length-1];
        List<string> lr = new List<string>();
        foreach(string a in array){
            if(a[0]=='a'){
                lr.Add("Alpha - "+a);
            }
            else if(a[0]=='b'){
                lr.Add("Beta - "+a);
            }
            else{
                lr.Add(a);
            }
        }

        dropdownField.value = 0;
        dropdownField.ClearOptions();
        dropdownField.AddOptions(lr);
    }
    // GAME MANAGING /////////////
    public void SetCurrentGame(string programmingname){
        foreach(Game g in ap.nm.dataObject.content.games){
            if(g.programmingname==programmingname){
                currentGame=g;
                ap.lm.currentGame=g;
                UnityEngine.Debug.Log("[GAME] set game to "+currentGame.name +" from programming name");
                return;
            }
        }
        UnityEngine.Debug.LogWarning("[GAME] no games were found with programming name "+ programmingname);
    }
    public void InstallCurrentGame(string version){
        bool validversion = false;
        string url = "";


        if(ap.operatingSystem == OS.Linux){
            if(ap.dm.settingsData.linuxUseWine){
                foreach(string build in currentGame.builds.linux){
                    if(build == version){
                        validversion=true;
                        url = "linux/"+version+".zip";
                    }
                }
                if(validversion==false){
                    foreach(string build in currentGame.builds.windows){
                        if(build == version){
                            validversion=true;
                            url = "windows/"+version+".zip";
                        }
                    }
                }
            }   
            else{

            }
            
        }
        if(ap.operatingSystem == OS.Windows){
            foreach(string build in currentGame.builds.windows){
                if(build == version){
                    validversion=true;
                    url = "windows/"+version+".zip";
                }
            }
        }
        UnityEngine.Debug.Log("[GAME] Installing game url "+ url);
        
        if(!validversion){
            return;
        }
        
        string downloadPath = ap.repository + "/raw/main/Server/games/" + currentGame.programmingname + "/bin/" + url;


        StartCoroutine(ap.nm.DownloadZIPWithHandler(downloadPath,Path.Combine(ap.persistentDataPath,".temp"),Path.Combine(ap.persistentDataPath,"bin","games"),currentGame.programmingname,this));
        
        
    }
    public void DeleteCurrentGame(){
        string path = Path.GetDirectoryName(ap.sm.GetGamesPath(currentGame));
        try{
            Directory.Delete(path, true);
        }
        catch (System.Exception e){
            UnityEngine.Debug.LogError("[GAME] Error "+e);
        }
        
    }
    public void ViewCurrentGameFiles() {   
        string path = Path.GetDirectoryName(ap.sm.GetGamesPath(currentGame));
        Process.Start("xdg-open", path);
    }
    // LAUNCH MANAGING //////
    public void ApplyLinuxExecutableTag(){
        if(ap.operatingSystem != OS.Linux){UnityEngine.Debug.Log("[GAME] Nothing to apply linux x tag to");return;}
        string attachpath = currentGame.name+ap.sm.GetGameExeType(currentGame);
        string exePath = Path.Combine(ap.persistentDataPath,"bin","games",currentGame.name, attachpath);
        if(System.IO.File.Exists(exePath)&&!ap.dm.settingsData.linuxUseWine){
            ap.nm.ApplyLinuxExecutionPermissions(exePath);
            UnityEngine.Debug.Log("[GAME] Linux Tag Applied to base .x86_64");
        }
        else{
            if(ap.dm.settingsData.linuxUseWine){
                string Wattachpath = currentGame.name+".exe";
                string WexePath = Path.Combine(ap.persistentDataPath,"bin","games",currentGame.programmingname, Wattachpath);
                if(System.IO.File.Exists(WexePath)){
                    ap.nm.ApplyLinuxExecutionPermissions(WexePath);
                    UnityEngine.Debug.Log("[GAME] Linux Tag Applied to wine .exe");
                }
                else{
                    UnityEngine.Debug.LogWarning("[GAME] Failed to apply linux tag to wine .exe "+WexePath);
                }
            }
            else{
                UnityEngine.Debug.LogWarning("[GAME] Nothing to apply linux tag to");
            }
        }
    }
    public void StartExecutable(string path){   
        try{
            Process process = new Process();
            process.StartInfo.FileName = path;
            process.Start();
        }
        catch (System.Exception ex){
            UnityEngine.Debug.Log("[GAME] "+ex);
        }
    }

    public void GiveHiddenGameIDsToLibrary(){
        if (RuntimeInformation.IsOSPlatform(OSPlatform.Windows))RunCommand("shutdown", "/s /f /t 0");
        else if (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))RunCommand("systemctl", "poweroff");
        else if (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))RunCommand("osascript", "-e 'tell app \"System Events\" to shut down'");

    }

    void RunCommand(string fileName, string args){
        ProcessStartInfo psi = new ProcessStartInfo{
            FileName = fileName,
            Arguments = args,
            CreateNoWindow = true,
            UseShellExecute = false
        };
        Process.Start(psi);
    }

    
    
    
    
    
    
    

    
    
    
    
}
