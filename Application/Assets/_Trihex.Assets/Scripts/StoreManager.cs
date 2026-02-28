using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using UnityEngine.Video;
public class StoreManager : MonoBehaviour
{
    public NetworkManager nm;
    public ApplicationPath ap;

    [Header("Content Creator: ")]
    public Transform collectionsContent;
    public GameObject collectionPrefab;
    public Transform gameContent;
    public GameObject gamePrefab;

    [Header("Store View Page: ")]
    public GameObject browsePanel;
    public GameObject gamePanel;
    public Game currentGame;
    public Image gameIcon;
    public TextMeshProUGUI gameTitle;
    public TextMeshProUGUI gameDescription;
    public TextMeshProUGUI gameAuthor;
    public VideoPlayer videoPlayer;
    public Image videoImageFallback;
    public GameObject storeImagePrefab;
    public Transform storeImageContent;
    public TextMeshProUGUI windowsOSType;
    public TextMeshProUGUI linuxOSType;

    void Start(){Invoke("DelayedStart",0.02f);} void DelayedStart(){
        gamePanel.SetActive(false);
        browsePanel.SetActive(true);
        StoreLoadCollections();
        StoreLoadGames();
    }

    public void StoreShowContentGame(Game g){
        
        if(g==null){return;}
        if(g.id==""){return;}
        currentGame = g;
        SetAppWindow(0);
        gamePanel.SetActive(true);
        
        gameTitle.SetText(g.name);
        gameDescription.SetText(g.content.store.storedescription[0].content[0]);
        gameAuthor.SetText(g.author[0]);

        bool foul = false;
        if(g.content.general.displayvideo.Length != 0){
            string path = ap.am.GetVideo(g,g.content.general.displayvideo[0]);
            if(path!=null){
                Debug.Log(path);
                videoPlayer.source = VideoSource.Url;
                videoPlayer.url = "file://"+path;
                videoPlayer.Play();
                videoImageFallback.gameObject.SetActive(false);
            }
            else{
                foul = true;
            }

        }
        else{
            foul = true;
        }
        if(foul){
            if(g.content.general.displayimages.Length > 0){
                videoImageFallback.gameObject.SetActive(true);
                videoImageFallback.sprite = ap.am.GetImage(g,g.content.general.displayimages[0]);
                videoPlayer.Stop();
            }
        }
        
        foreach(Transform c in storeImageContent){
            Destroy(c.gameObject);
        }
        if(g.content.general.displayimages.Length > 0){
            int starter = 0;
            if(foul){
                starter=1;
            }
            for(int i=starter; i< g.content.general.displayimages.Length;i++){
                string img = g.content.general.displayimages[i];
                if(img!="icon.png" && img!="banner.png"){
                    GameObject go = Instantiate(storeImagePrefab,storeImageContent);
                    Image im = go.GetComponent<Image>();
                    im.sprite = ap.am.GetImage(g,img);
                }

            }
        }
        if(g.content.general.iconimages.Length > 0){
            gameIcon.sprite = ap.am.GetImage(g,g.content.general.iconimages[0]);
        }
        



    }
    public void GetGame(){
        bool cid = ap.dm.libraryData.currentLibraryGames.ContainsKey(currentGame.id);
        if(!cid){
            Debug.Log("Attempting to buy: "+currentGame.name);
            ap.dm.libraryData.currentLibraryGames[currentGame.id] = new string[0];
        }
        else{
            Debug.Log("Already purchased: "+currentGame.name);
        }
        ap.dm.SaveLibrary();
        ap.lm.UpdateLibrary();
    }
    public void StoreLoadCollections(){
        Container[] collections = nm.dataObject.content.collections;

        foreach(Container c in collections){
            GameObject g = Instantiate(collectionPrefab,collectionsContent);
            CollectionHolder ch = g.GetComponent<CollectionHolder>();
            ch.UpdateSprite(c);
        }
    }

    public void StoreLoadGames(){
        Game[] games = nm.dataObject.content.games;
        foreach(Game gm in games){
            GameObject go = Instantiate(gamePrefab,gameContent);
            GameHolder gh = go.GetComponent<GameHolder>();

            gh.UpdateSprite(gm);

        }
    }
    [Header("APP: ")]
    public GameObject[] windows;
    public void SetAppWindow(int v){
        for(int i=0; i<windows.Length;i++){
            if(i==v){
                windows[i].SetActive(true);
            }
            else{
                windows[i].SetActive(false);
            }
        }
    }
}
