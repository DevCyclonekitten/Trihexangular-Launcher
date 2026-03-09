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
    public Game currentGame;

    [Header("Content Creator: ")]
    public Transform collectionsContent;
    public Transform gameContent;
    public GameObject collectionPrefab;
    public GameObject gamePrefab;

    [Header("Store View Page: ")]
    public GameObject browsePanel;
    public GameObject gamePanel;
    public Image gameIcon;
    public Image videoImageFallback;
    public VideoPlayer videoPlayer;
    public TextMeshProUGUI gameTitle;
    public TextMeshProUGUI gameDescription;
    public TextMeshProUGUI gameAuthor;
    public TextMeshProUGUI windowsOSType;
    public TextMeshProUGUI linuxOSType;
    
    
    public GameObject storeImagePrefab;
    public Transform storeImageContent;
    public ScrollRect scrollView;
    public ScrollRect scrollView2;

    [Header("APP: ")]
    public GameObject[] windows;

    [Header("Filtering: ")]
    public List<GameHolder> gameHolders;
    public List<CollectionHolder> collectionHolders;
    public TMP_InputField gameFilter;

    // MONOBEHAVIOUR STUFF ////////////
    void Start(){Invoke("DelayedStart",0.02f);} void DelayedStart(){
        gamePanel.SetActive(false);
        browsePanel.SetActive(true);
        LoadStoreCollections();
        LoadStoreGames();
    }

    // LOADING CONTENT ///////////
    public void LoadStoreShowContentGame(Game g){
        
        if(g==null){return;}
        if(g.id==""){return;}
        scrollView2.verticalNormalizedPosition = 1f;
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
        
        windowsOSType.color = new Color(1f,1f,1f);
        if(ap.sm.GetGameExeTypeFilteredOS(g,OS.Windows)==".exe"){
            windowsOSType.SetText("Windows 64 bit");
        }
        else{
            windowsOSType.SetText("Windows Unavailiable");
            windowsOSType.color = new Color(0.5f,0.5f,0.5f);
        }
        linuxOSType.color = new Color(1f,1f,1f);
        UnityEngine.Debug.Log("[STORE] Linux os detected "+ap.sm.GetGameExeTypeFilteredOS(g,OS.Linux));
        if(ap.sm.GetGameExeTypeFilteredOS(g,OS.Linux)==".exe"&&ap.dm.settingsData.linuxUseWine){
            linuxOSType.SetText("Linux through wine");
            linuxOSType.color = new Color(1f,1f,1f);
        }
        else if(ap.sm.GetGameExeTypeFilteredOS(g,OS.Linux)==".x86_64"){
            linuxOSType.SetText("Linux 64 bit");
            
        }
        else{
            linuxOSType.SetText("Linux Unavaliable");
            linuxOSType.color = new Color(0.5f,0.5f,0.5f);
        }
        

    }
    public void LoadStoreGames(){
        Game[] games = nm.dataObject.content.games;
        foreach(Game gm in games){
            if(!gm.invisible){
                GameObject go = Instantiate(gamePrefab,gameContent);
                GameHolder gh = go.GetComponent<GameHolder>();

                gh.UpdateSprite(gm);
                gameHolders.Add(gh);
            }
            

        }
    }
    public void FilterWord(string w){
        foreach(GameHolder gh in gameHolders){
            bool val = gh.game.programmingname.Replace(" ", "").StartsWith(w.Replace(" ", ""), System.StringComparison.OrdinalIgnoreCase);
            gh.gameObject.SetActive(val);
        }
        foreach(CollectionHolder ch in collectionHolders){
            bool val2 = ch.name.Replace(" ", "").StartsWith(w.Replace(" ", ""), System.StringComparison.OrdinalIgnoreCase);
            ch.gameObject.SetActive(val2);
        }
    }
    public void LoadStoreCollections(){
        Container[] collections = nm.dataObject.content.collections;

        foreach(Container c in collections){
            GameObject g = Instantiate(collectionPrefab,collectionsContent);
            CollectionHolder ch = g.GetComponent<CollectionHolder>();
            ch.UpdateSprite(c);
            collectionHolders.Add(ch);
        }
    }
    public void LoadStoresBundles(){} // EMPTY

    // ADDING CONTENT //////////////////
    public void GetCurrentGame(){
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
    public void GetGameFromString(string s){
        Game cg = ap.am.GetGameFromName(s);
        if(cg.name!=null){
            currentGame=cg;
            GetCurrentGame();
        }
        else{
            Debug.LogWarning("[STORE] Game doesn't exist");
        }
        
    }

    // MENU CONTENT ///////////////////
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
