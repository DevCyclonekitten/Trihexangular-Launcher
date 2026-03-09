using UnityEngine;
using System.IO;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using System.Collections.Generic;
public class SettingsManager : MonoBehaviour{
    public ApplicationPath ap;

    [Header("Settings: ")]
    public Toggle t_linuxUseWine;
    public Toggle t_showDebugLog;
    public Toggle t_dontUpdateLauncher;
    public TMP_Dropdown d_launcherBranch;
    public GameObject showDebugLog_gameObject;


    // MONOBEHAVIOUR STUFF
    void Start(){
        if(ap==null){
            ap=GameObject.Find("ApplicationPath").GetComponent<ApplicationPath>();
        }
        Invoke("DelayedStart",0.2f);
    }
    void DelayedStart(){
        LoadUIFromData();
    }
    // GET GAME OS COMPATIBILITY
    public int CheckGameOSCompatibility(Game currentGame){
        if(ap.operatingSystem == OS.Linux){
            if(currentGame.builds.linux.Length == 0){
                if(!ap.dm.settingsData.linuxUseWine){
                    return 0;
                }
                else{
                    //Debug.Log("Return Wine");
                    return 2;
                }
            }
            else{
                if(currentGame.builds.linux[0]==""){
                    if(!ap.dm.settingsData.linuxUseWine){
                        return 0;
                    }
                    else{
                        return 2;
                    }
                }
                else{
                    return 1;
                }

            }
        }
        if(ap.operatingSystem == OS.Windows){
            if(currentGame.builds.windows.Length == 0){
                return 0;
            }
            else{
                if(currentGame.builds.windows[0]==""){
                    return 0;
                }
                else{
                    return 1;
                }

            }
        }
        return 0;
    }
    public string GetGamesPath(Game currentGame){
        string gamesPath = "";
        string dlp = Path.Combine(ap.GetPath(), "bin","games",currentGame.programmingname,currentGame.name+".x86_64");
        string dwp = Path.Combine(ap.GetPath(), "bin","games",currentGame.programmingname,currentGame.name+".exe");
        if(ap.operatingSystem==OS.Linux){

            if(File.Exists(dlp)){
                return dlp;
            }
            else{
                if(File.Exists(dwp)&&ap.dm.settingsData.linuxUseWine){
                    //Debug.Log("FOUND WINDOWS PATH");
                    return dwp;
                }
                else{
                    return dlp;
                }
            }
        }
        if(ap.operatingSystem==OS.Windows){
            return dwp;
        }


        return "";
    }
    public string GetGameExeTypeFilteredOS(Game currentGame,OS operatingSystem){
        if(currentGame==null){
            return "";
        }
        if(operatingSystem==OS.Windows){
            if(currentGame.builds.windows.Length>0){
                if(currentGame.builds.windows[0]!=""){
                    return ".exe";
                }
                else{
                    return "";
                }
            }
            else{
                return "";
            }

        }
        if(operatingSystem==OS.Linux){
            if(currentGame.builds.linux.Length>0){
                if(currentGame.builds.linux[0]!=""){
                    return ".x86_64";
                }
                else{
                    return ".exe";
                }
            }
            else{
                return ".exe";
            }
            
            
            
        }
        return "";
    }
    public string GetGameExeType(Game currentGame){
        if(currentGame==null){
            return ".exe";
        }
        if(ap.operatingSystem==OS.Windows){
            return ".exe";
        }
        if(ap.operatingSystem==OS.Linux){
            string[] opt = GetVersionOptions(currentGame);
            if(opt!=null){
                if(opt.Length==0){
                    if(ap.dm.settingsData.linuxUseWine){
                        return ".exe";
                    }
                    else{
                        return "";
                    }
                }
                return ".x86_64";
            }
            
            
            
        }
        return ".exe";
    }
    public string[] GetVersionOptions(Game currentGame){
            if(ap.operatingSystem == OS.Linux){
                int r = CheckGameOSCompatibility(currentGame);
                //Debug.Log("CheckGameValidity: "+r.ToString());
                if(r==1){
                    return (string[])currentGame.builds.linux.Clone();
                }
                if(r==2){
                    //Debug.Log("ValidityReturned: "+currentGame.builds.windows[0]);
                    return (string[])currentGame.builds.windows.Clone();
                }
            }
            
            if(ap.operatingSystem == OS.Windows){
                return (string[])currentGame.builds.windows.Clone();
            }
            return null;
    }

    // SETINGS MANAGEMENT ////////////
    public void SaveDataFromUI(){
        SettingsData d = ap.dm.settingsData;

        d.linuxUseWine = t_linuxUseWine.isOn;
        d.showDebugLog = t_showDebugLog.isOn;
        d.dontUpdateLauncher = t_dontUpdateLauncher.isOn;

        d.branch = ReadDropdown(d_launcherBranch);

        ap.dm.settingsData = d;
        ap.dm.SaveSettings();
        LoadUIFromData();
    }
    public void LoadUIFromData(){
        SettingsData d = ap.dm.settingsData;
        t_linuxUseWine.isOn = d.linuxUseWine;
        t_showDebugLog.isOn = d.showDebugLog;
        t_dontUpdateLauncher.isOn = d.dontUpdateLauncher;
        showDebugLog_gameObject.SetActive(t_showDebugLog.isOn);
        FillDropdown(d_launcherBranch,new List<string> {"main","beta"}, d.branch);
        
    }
    public void FillDropdown(TMP_Dropdown dropdown, List<string> options,string selected){
        int sV = 0;
        for(int i=0; i<options.Count;i++){
            if(options[i]==selected){
                sV=i;
            }
        }
        dropdown.ClearOptions();
        dropdown.AddOptions(options);
        dropdown.RefreshShownValue();
        dropdown.value = sV;
    }
    public string ReadDropdown(TMP_Dropdown dropdown){
        return dropdown.options[dropdown.value].text;
    }
    
}
