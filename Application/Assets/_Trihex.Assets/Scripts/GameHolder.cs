using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class GameHolder : MonoBehaviour
{
    public Sprite sprite;
    public Game game;
    

    [Header("Content: ")]
    public Image icon;
    public TextMeshProUGUI title;
    public TextMeshProUGUI description;
    public int[] truncateLength;
    public int clickType;

    public void Clicked(){
        if(clickType==1){
            GameObject.Find("LibraryManager").GetComponent<LibraryManager>().DisplayCurrentGame(game);
        }
        if(clickType==2){
            GameObject.Find("StoreManager").GetComponent<StoreManager>().StoreShowContentGame(game);
        }
    }
    public void UpdateSprite(Game g){
        game = g;
        AssetManager am = GameObject.Find("AssetManager").GetComponent<AssetManager>();
        if(g.content.general.iconimages.Length > 0){
            sprite = am.GetImage(g,g.content.general.iconimages[0]);
            icon.sprite = sprite;
        }
        
        if(truncateLength.Length!=0){
            title.SetText(Truncate(g.name,truncateLength[0]));
            description.SetText(Truncate(g.content.store.storedescription[0].content[0],truncateLength[1]));
        }
        else{
            title.SetText(g.name);
            description.SetText(g.content.store.storedescription[0].content[0]);
        }
        



    }
    public string Truncate(string value, int maxChars) //Thanks stack overflow
    {
        return value.Length <= maxChars ? value : value.Substring(0, maxChars) + "...";
    }

    


}
