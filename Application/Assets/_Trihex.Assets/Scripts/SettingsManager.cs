using UnityEngine;
using System.IO;
public class SettingsManager : MonoBehaviour{
    public ApplicationPath ap;

    void Start(){
        if(ap==null){
            ap=GameObject.Find("ApplicationPath").GetComponent<ApplicationPath>();
        }
    }
    public string[] GetVersionOptions(Game currentGame){
            if(ap.operatingSystem == OS.Linux){
                int r = CheckGameValid(currentGame);
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
    public int CheckGameValid(Game currentGame){
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
}
