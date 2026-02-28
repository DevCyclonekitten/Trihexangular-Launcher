using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Linq;
public class LibraryManager : MonoBehaviour
{
    public ApplicationPath ap;
    public AssetManager am;
    public NetworkManager nm;
    public Game currentGame;

    [Header("Content: ")]
    public List<Game> libraryGames;
    public GameObject contentWindow;
    public TextMeshProUGUI gameTitle;
    public TextMeshProUGUI gameDescription;
    public Image gameBanner;
    public Image gameIcon;
    
    [Header("Sidebar Content: ")]
    public GameObject sidebarPrefab;
    public Transform sidebarContent;

    
    void Start(){contentWindow.SetActive(true);Invoke("DelayedStart",0.03f);} void DelayedStart(){
        UpdateLibrary();
    }
    public void GetGameDatabase(){
        var db = ap.dm.libraryData.currentLibraryGames.Keys;
        libraryGames.Clear();
        foreach(Game g in ap.nm.dataObject.content.games){
            foreach (string game in db){
                if(g.id==game){
                    libraryGames.Add(g);
                }

            }
        }
    }
    public void DisplayCurrentGame(Game g){
        currentGame=g;
        if(currentGame==null){
            contentWindow.SetActive(true);
        }
        contentWindow.SetActive(false);
        gameTitle.SetText(g.name);

        gameBanner.sprite = ap.am.GetImage(g,"banner.png");
        gameIcon.sprite = ap.am.GetImage(g,"icon.png");
        //gameDescription.SetText(gameDescription);


    }
    public void UpdateLibrary(){
        GetGameDatabase();
        CreateGameSidebar();
        if(currentGame.id == ""){
            if(libraryGames.Count >0){
                DisplayCurrentGame(libraryGames[0]);
            }
            else{
                contentWindow.SetActive(true);
            }

        }
    }
    public void CreateGameSidebar(){
        foreach(Transform c in sidebarContent){
            Destroy(c.gameObject);
        }
        foreach(Game g in libraryGames){
            
            GameObject go = Instantiate(sidebarPrefab,sidebarContent);
            GameHolder gh = go.GetComponent<GameHolder>();
            gh.UpdateSprite(g);
        }
    }
}
