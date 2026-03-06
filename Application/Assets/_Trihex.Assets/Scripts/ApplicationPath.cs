using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System;
using TMPro;
using System.IO;
using UnityEngine.UI;
public class ApplicationPath : MonoBehaviour
{
    public string persistentDataPath;
    public string repository = "https://github.com/DevCyclonekitten/Trihexangular-Launcher";


    [Header("Operating Systems: ")]
    public OS operatingSystem;

    [Header("Managers: ")]
    public NetworkManager nm;
    public DataManager dm;
    public AssetManager am;
    public LibraryManager lm;
    public GameManager gm;
    public SettingsManager sm;
    
    void Start(){
        
        UnityEngine.Debug.unityLogger.logHandler = new LogHandler();
        ConfigurePaths();
        if(PlayerPrefs.GetInt("ViewOS")==0){
            PlayerPrefs.SetInt("ViewOS",1);
            operatingSystem= OS.Null;
        }

        ConfigurePaths();
        
    }
    
    public string GetPath(){
        if(persistentDataPath==""){
            ConfigurePaths();
        }
        return persistentDataPath;
    }
    void ConfigurePaths(){
        if(operatingSystem==OS.Null){
            if(Application.platform.ToString()=="LinuxEditor" || Application.platform.ToString()=="LinuxPlayer"){
                operatingSystem = OS.Linux;
            }
            else if(Application.platform.ToString() == "WindowsEditor" || Application.platform.ToString()=="WindowsPlayer"){
                operatingSystem = OS.Windows;
            }
            else{
            }
        }
        if(operatingSystem == OS.Linux){
            persistentDataPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile),".trihexangular-launcher");
        }
        if(operatingSystem == OS.Windows){
            persistentDataPath = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),"trihexangular-launcher");
        }

    }




}

public enum OS{
    Null,
    Windows,
    Mac,
    Linux
}