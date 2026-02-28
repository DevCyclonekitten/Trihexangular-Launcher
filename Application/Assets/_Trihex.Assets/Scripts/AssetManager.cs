using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using System.IO;
using System.IO.Compression;


public class AssetManager : MonoBehaviour {

    public ApplicationPath ap;
    public NetworkManager nm;

    public Game GetGameFromName(string name){
        
        foreach(Game g in nm.dataObject.content.games){
            if(g.name ==name){
                return g;
            }
        }
        Debug.LogError("Could not find game with name "+name);
        return null;
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
            Debug.Log("Could not find :"+imagePath);
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