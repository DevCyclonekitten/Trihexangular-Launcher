using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.Video;
using System.IO;
using System.IO.Compression;
using System.Diagnostics;
using UnityEngine.UI;
using TMPro;
public class GameManager : MonoBehaviour
{
    public ApplicationPath ap;
    public AssetManager am;
    public Game currentGame;


    public Image playButtonImage;
    public TextMeshProUGUI playButtonText;
    public bool downloading;
    public bool invalidOS;
    public GameObject settingsObject;
    void Start(){Invoke("DelayedStart",0.01f);installButtonVersionSelect.SetActive(false);} void DelayedStart(){
        //InstallGame("0.1");
        
    }
    void Update(){
        UpdateGameButton();
    }
    public void CheckGameValid(){
        if(ap.operatingSystem == OS.Linux){
            if(currentGame.builds.linux.Length == 0){
                invalidOS= true;
            }
            else{
                if(currentGame.builds.linux[0]==""){
                    invalidOS=true;
                }
                else{
                    invalidOS= false;
                }

            }
        }
        if(ap.operatingSystem == OS.Windows){
            if(currentGame.builds.windows.Length == 0){
                invalidOS= true;
            }
            else{
                if(currentGame.builds.windows[0]==""){
                    invalidOS=true;
                }
                else{
                    invalidOS= false;
                }

            }
        }
    }
    public void DeleteGame(){
        string path = Path.GetDirectoryName(GetGamesPath());
        try{
            Directory.Delete(path, true);
        }
        catch (System.Exception e){
            UnityEngine.Debug.Log("Error: "+e);
        }
        
    }
    public void ViewGameFiles()
    {   
        string path = Path.GetDirectoryName(GetGamesPath());

        Process.Start("xdg-open", path);
    }
    public string GetGamesPath(){
        string gamesPath = "";
        if(ap.operatingSystem==OS.Linux){
            gamesPath = Path.Combine(ap.GetPath(), "bin","games",currentGame.programmingname,currentGame.name+GetGameExeType());
        }
        if(ap.operatingSystem==OS.Windows){
            gamesPath = Path.Combine(ap.GetPath(), "bin","games",currentGame.programmingname,currentGame.name+GetGameExeType());
        }


        return gamesPath;
    }
    public void UpdateGameButton(){
        CheckGameValid();
        currentGame = ap.lm.currentGame;

        if(downloading){
            settingsObject.SetActive(false);
            return;
        }
        if(invalidOS){
            playButtonImage.color = new Color(0.2f,0.2f,0.2f);
            playButtonText.SetText("NOT COMPATIBLE");
            settingsObject.SetActive(false);
            return;
        }
        if(File.Exists(GetGamesPath())){
            playButtonImage.color = new Color(0.25f,1f,1f);
            playButtonText.SetText("PLAY");
            settingsObject.SetActive(true);
        }
        else{
            playButtonImage.color = new Color(1f,0.5f,0.25f);
            playButtonText.SetText("INSTALL");
            settingsObject.SetActive(false);
        }
    }
    public GameObject installButtonVersionSelect;
    public TMP_Dropdown dropdownField;
    public void StartButton(){
        if(invalidOS){return;}
        if(downloading){return;}
        currentGame = ap.lm.currentGame;

        if(File.Exists(GetGamesPath())){
            StartExecutable(GetGamesPath());
        }
        else{
            PopulateVersionOptions();
            installButtonVersionSelect.SetActive(true);
        }
    }
    public void PopulateVersionOptions(){
        string[] array = GetVersionOptions();
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
    public string[] GetVersionOptions(){
        if(invalidOS==false){
            if(ap.operatingSystem == OS.Linux) return (string[])currentGame.builds.linux.Clone();
            if(ap.operatingSystem == OS.Windows) return (string[])currentGame.builds.windows.Clone();
        }
        return null;
    }
    public void InstallStartButton(){
        InstallGame(GetVersionOptions()[dropdownField.value]);
        
    }
    public string GetGameExeType(){
        if(ap.operatingSystem==OS.Linux){
            return ".x86_64";
        }
        if(ap.operatingSystem==OS.Windows){
            return ".exe";
        }
        return ".exe";
    }
    public void LinuxGiveGameExecutableTag(){
        if(ap.operatingSystem != OS.Linux) return;
        string attachpath = currentGame.name+GetGameExeType();
        string exePath = Path.Combine(currentGame.name, attachpath);
        if(System.IO.File.Exists(exePath)){
            System.Diagnostics.Process process = new System.Diagnostics.Process();
            process.StartInfo.FileName = "chmod";
            process.StartInfo.Arguments = "+x \"" + exePath + "\"";
            process.StartInfo.UseShellExecute = false;
            process.Start();
            process.WaitForExit();
        }
    }
    public void StartExecutable(string path)
    {   
        try
        {
            
            Process process = new Process();
            process.StartInfo.FileName = path;
            process.Start();
        }
        catch (System.Exception ex){
            UnityEngine.Debug.Log(ex);
        }
    }
    public void InstallGame(string version){
        bool validversion = false;
        string url = "";


        if(ap.operatingSystem == OS.Linux){
            foreach(string build in currentGame.builds.linux){
                if(build == version){
                    validversion=true;
                    url = "linux/"+version+".zip";
                }
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
        
        if(!validversion){
            return;
        }
        
        string downloadPath = ap.repository + "/raw/main/Server/games/" + currentGame.programmingname + "/bin/" + url;


        StartCoroutine(ap.nm.DownloadZIPWithHandler(downloadPath,Path.Combine(ap.persistentDataPath,".temp"),Path.Combine(ap.persistentDataPath,"bin","games"),currentGame.programmingname,this));
        
        
    }
}
