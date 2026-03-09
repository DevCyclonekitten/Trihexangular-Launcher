using UnityEngine;
using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine.UI;
#if UNITY_EDITOR
using UnityEditor;
#endif

public class LogHandler : ILogHandler
{
    private ILogHandler m_DefaultHandler = Debug.unityLogger.logHandler;
    private LoggingManager lm;

    void Awake(){
        lm=GameObject.Find("LoggingManager").GetComponent<LoggingManager>();
    }
    public void LogFormat(LogType logType, UnityEngine.Object context, string format, params object[] args){
        string message = string.Format(format, args);
        int errorType = GetErrorType(logType);

        TryDisplayMessage(message, errorType);
        m_DefaultHandler.LogFormat(logType, context, "[Launcher] " + format, args);
    }

    private int GetErrorType(LogType type){
        return type switch{
            LogType.Error or LogType.Exception or LogType.Assert => 2,
            LogType.Warning => 1,
            _ => 0
        };
    }


    void TryDisplayMessage(string message, int type){
        
        if(lm==null){
            lm=GameObject.Find("LoggingManager").GetComponent<LoggingManager>();
        }
        if(lm.disabled) return;

#if UNITY_EDITOR
        if (EditorApplication.isPlaying){
            try{lm.DisplayMessage(message,type);}
            catch (System.Exception e){
                lm.loggedMessages.Add(e.Message);
            }
        }
        
#else
        try{lm.DisplayMessage(message,type);}
            catch (System.Exception e){
                lm.loggedMessages.Add(e.Message);
            }
        
#endif


    }
    public void LogException(Exception exception, UnityEngine.Object context){
        m_DefaultHandler.LogException(exception, context);
    }
}


public class LoggingManager : MonoBehaviour {
    public bool disabled;
    public List<string> loggedMessages = new List<string>();
    public List<GameObject> loggedObjects = new List<GameObject>();
    public Transform messageOutput;
    public GameObject messagePrefab;
    public ApplicationPath ap;

    [Header("Scroll Viewing: ")]
    public ScrollRect scrollView;
    public RectTransform scrollViewport;
    public RectTransform content;

    // MonoBehaviour Stuff ////////////////////////
    void Start(){
        ClearLogs();
    }
    void Update(){
        if(Input.GetKeyDown("n")){
            WriteListToFile(loggedMessages,Path.Combine(ap.GetPath(),"log.txt"));
        }
    }
    // LOGS MANAGEMENT //////////////////////////
    public void WriteListToFile(List<string> lines, string fileName){
        string path = Path.Combine(ap.GetPath(), fileName);
        try{
            File.WriteAllLines(path, lines);
            Debug.Log("[LOG] Successfully wrote to file");
        }
        catch (IOException e){
            Debug.LogError("[LOG] Failed to write to file");
        }
    }

    // MESSAGE MANAGEMENT /////////////////////
    public void BroadcastMessage(string message){
        UnityEngine.Debug.Log(message);
    }
    
    public void ClearLogs(){

        loggedMessages.Clear();
        foreach(GameObject g in loggedObjects){
            Destroy(g);
        }
        loggedObjects.Clear();
        UnityEngine.Debug.Log("[LOG] Cleared log");
    }

    // UI MANAGEMENT //////////
    public void DisplayMessage(string msg, int type){
        loggedMessages.Add(msg+" - Debug Type - "+type);

        GameObject msgO = Instantiate(messagePrefab,messageOutput);
        LogHolder l = msgO.GetComponent<LogHolder>();
        l.errorType = type;
        l.content=msg;

        loggedObjects.Add(msgO);
        ScrollToElement(msgO.GetComponent<RectTransform>());
    }
    public void ScrollToElement(RectTransform target){
        Canvas.ForceUpdateCanvases();

        Vector2 targetPosition = (Vector2)scrollView.transform.InverseTransformPoint(target.position);
        Vector2 viewportPosition = (Vector2)scrollView.transform.InverseTransformPoint(scrollViewport.position);
        
        Vector2 diff = viewportPosition - targetPosition;
        
        Vector2 newPosition = content.anchoredPosition + diff - new Vector2(0f,250f);
        newPosition.x = content.anchoredPosition.x;

        content.anchoredPosition = newPosition;
    }
    
}