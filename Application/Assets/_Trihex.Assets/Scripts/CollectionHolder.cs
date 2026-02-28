using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using TMPro;

public class CollectionHolder : MonoBehaviour
{
    public NetworkManager nm;

    public string name;
    public string description;
    public string[] gameids;

    public TextMeshProUGUI titletmp;
    public TextMeshProUGUI descriptiontmp;
    public TextMeshProUGUI counter;

    public GameObject gamePrefab;
    public Transform content;
    

    public void UpdateSprite(Container c){
        nm = GameObject.Find("NetworkManager").GetComponent<NetworkManager>();

        name = c.name;
        description = c.description;
        gameids = c.games;

        titletmp.SetText(name);
        descriptiontmp.SetText(description);
        
        counter.SetText(gameids.Length +" games");
        if(gameids.Length<=1){
            counter.SetText("1 game");
        }


        foreach(string s in gameids){
            GameObject g = Instantiate(gamePrefab,content);

            GameHolder gh = g.GetComponent<GameHolder>();
            Game gm = nm.GetGameFromID(s);
            if(gm !=null){
                gh.UpdateSprite(gm);
            }
        }


        
    }
}
