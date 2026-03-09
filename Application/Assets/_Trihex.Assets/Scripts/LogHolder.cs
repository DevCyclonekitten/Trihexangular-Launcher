using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using TMPro;
using UnityEngine.UI;
public class LogHolder : MonoBehaviour {

    public string content;
    public int errorType;
    [Header("Colours: ")]
    public Color debugColour;
    public Color warningColour;
    public Color errorColour;

    [Header("References: ")]
    public TextMeshProUGUI errorText;
    public TextMeshProUGUI contentText;
    public Image backgroundColor;
    private float backgroundTimer=1f;


    void Start(){
        backgroundTimer=1f;
        errorText.SetText("Debug Type "+errorType);
        contentText.SetText(content);

        if(errorType==0){
            errorText.color = debugColour;
            contentText.color = debugColour;
        }
        else if(errorType==1){
            errorText.color = warningColour;
            contentText.color = warningColour;
        }
        else if(errorType==2){
            errorText.color = errorColour;
            contentText.color = errorColour;
        }
    }
    void Update(){
        backgroundTimer-=Time.deltaTime;
        if(backgroundTimer<=0f){
            //Destroy(backgroundColor.gameObject);
            Destroy(this);
            return;
        }
        backgroundColor.color = new Color(backgroundColor.color.r,backgroundColor.color.g,backgroundColor.color.b,backgroundTimer);
        
    }
}