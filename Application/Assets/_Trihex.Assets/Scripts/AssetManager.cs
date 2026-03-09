using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.IO;
using System.IO.Compression;


public class AssetManager : MonoBehaviour {

    public ApplicationPath ap;
    public NetworkManager nm;

    // SETTING GAMES
    public Game GetGameFromName(string name){
        
        foreach(Game g in nm.dataObject.content.games){
            if(g.programmingname ==name){
                return g;
            }
        }
        Debug.LogError("[ASSET] Could not find game with name "+name);
        return null;
    }
    public void SetGameFromName(string name){
        
        Game g = GetGameFromName(name);
        ap.gm.currentGame=g;
        ap.lm.currentGame=g;
    }


    public Sprite GetImage(Game g, string image){
        
        string imagePath = Path.Combine(ap.GetPath(),"data","assets",g.programmingname,image);
        if (File.Exists(imagePath)){
            byte[] imageData = File.ReadAllBytes(imagePath);
            Texture2D texture = new Texture2D(2, 2);
            texture.LoadImage(imageData);
            return Sprite.Create(texture, new Rect(0, 0, texture.width, texture.height), new Vector2(0.5f, 0.5f));
        }
        else{
            Debug.LogWarning("[ASSET] Could not find "+imagePath);
        }
        return null;
    }
    public string GetVideo(Game g, string name){
        string vP = Path.Combine(ap.GetPath(),"data","assets",g.programmingname,name);
        if (File.Exists(vP)){
            return vP;
        }
        return null;
    }
}