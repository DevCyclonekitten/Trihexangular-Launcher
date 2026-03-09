
using UnityEngine;
using TMPro;
using System;
using System.IO;
using System.Linq;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;
public class MethodExpander : MonoBehaviour {

    public MonoBehaviour expandedManager;
    public TextMeshProUGUI expandedName;
    public TMP_Dropdown expandedDropdown;
    public TMP_InputField[] expandedInputs;
    private ApplicationPath ap;

    
    void Start(){
        ap=GameObject.Find("ApplicationPath").GetComponent<ApplicationPath>();

        expandedDropdown.ClearOptions();
        expandedDropdown.AddOptions(GetMethodNames(expandedManager));
        InvokeRepeating("InfrequentUpdate",0.01f,0.2f);
        expandedName.SetText(expandedManager.GetType().ToString());
    }
    public void InfrequentUpdate(){
        UpdateArrayMethod(expandedDropdown.options[expandedDropdown.value].text);
    }

    public List<string> GetMethodNames(MonoBehaviour target){
        MethodInfo[] methods = target.GetType().GetMethods(BindingFlags.Instance | BindingFlags.Public | BindingFlags.DeclaredOnly);
        var result = methods.Where(m => !m.IsSpecialName).Select(m => m.Name).ToList();
        //Debug.Log("Starting: "+target.GetType().ToString());
        foreach(string v in result){
            //Debug.Log("Loaded: "+v);
        }
        return result;
    } 

    public void UpdateArrayMethod(string methodName){
        MethodInfo method = expandedManager.GetType().GetMethod(methodName);
        if(method==null) {
            UnityEngine.Debug.LogWarning("[EXPANDER] Could not run method "+methodName);
            return;
        }
        ParameterInfo[] parameters = method.GetParameters();

        for(int i=0; i <  parameters.Length;i++){
            expandedInputs[i].gameObject.transform.parent.gameObject.SetActive(true);
        }
        for(int i=parameters.Length; i <  expandedInputs.Length;i++){
            expandedInputs[i].gameObject.transform.parent.gameObject.SetActive(false);
        }

    }


    public void RunMethod(string methodName){
        MethodInfo method = expandedManager.GetType().GetMethod(methodName);
        if(method==null) {
            UnityEngine.Debug.LogWarning("[EXPANDER] Could not run method "+methodName);
            return;
        }
        ParameterInfo[] parameters = method.GetParameters();

        if (parameters.Length == 0){
            UnityEngine.Debug.Log("[EXPANDER] Running method "+ methodName +" from "+ expandedManager.GetType().ToString() +" with no parameters");
            method.Invoke(expandedManager, null);
            
        }
        else{
            List<object> paramsA = new List<object>();

            for(int i=0; i<parameters.Length;i++){
                paramsA.Add(ConvertToType(expandedInputs[i].text, parameters[i].ParameterType));
                UnityEngine.Debug.Log("[EXPANDER] Adding method parameter " +expandedInputs[i].text);
            }
            UnityEngine.Debug.Log("[EXPANDER] Running method "+ methodName +" from "+ expandedManager.GetType().ToString());
            method.Invoke(expandedManager, paramsA.ToArray());
            
        }
    }

    private object ConvertToType(string input, Type targetType){
        if (targetType == typeof(int)) return int.Parse(input);
        if (targetType == typeof(float)) return float.Parse(input);
        if (targetType == typeof(bool)) return bool.Parse(input.ToLower());
        if (targetType == typeof(string)) return input;
        if(targetType == typeof(Game)){
            foreach(Game g in ap.nm.dataObject.content.games){
                if(g.programmingname==input){
                    return g;
                }
            }
            return null;
        }

        return null;
    }

    public void GetCurrentUserMethod(){
        RunMethod(expandedDropdown.options[expandedDropdown.value].text);
    }



}





    

    