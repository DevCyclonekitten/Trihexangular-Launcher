systemerror = {
    "name":"Error",
    "content":[
        {"text":"An error occured","position":0,"font":("Helvetica",15)},
        {"text":"whatevertextyouneedtoreplaceputhere",'position':25,"font":("Helvetica",10)},
    ],
    "icon":"cancel",
    "flags":{
        "exit-after":0,
        "persistent":0,
        "invisible":0,
        "priority":1
    },
    "interactions":{
        "buttons":[
            {"text":"exit","interactor":[{"type":"dismiss"}]}
        ]
    }
}


systembranch = {
    "name":"Select branch",
    "content":[
        {"text":"Launcher branch","position":0,"font":("Helvetica",15)},
        {"text":"Do you want to take part in beta branch.",'position':25,"font":("Helvetica",10)},
        {"text":"Updates may break, reversable at any time.","position":50,"font":("Helvetica",10)}
    ],
    "icon":"question",
    "flags":{
        "exit-after":0,
        "persistent":0,
        "invisible":0,
        "priority":1
    },
    "interactions":{
        "buttons":[
            {"text":"Main","interactor":[
                {"type":"json","content":{
                    "branch":"main"
                }}
            ]},
             {"text":"Beta","interactor":[
                {"type":"json","content":{
                    "branch":"beta"
                }}
            ]}
        ]
    }
}

systemrepository = {
    "name":"Select Repository",
    "content":[
        {"text":"Do you want to use default repository","position":0,"font":("Helvetica",15)},
        {"text":"Default: 'https://github.com/DevCycloneki...","position":25,"font":("Helvetica",10)},
        {"text":"...tten/Trihexangular-Launcher'","position":50,"font":("Helvetica",10)}
    
    ],
    "icon":"cancel",
    "flags":{
        "exit-after":0,
        "persistent":0,
        "invisible":0,
        "priority":1
    },
    "interactions":{
        "buttons":[
            {"text":"Yes","interactor":[
                {"type":"json","content":{
                    "repository":"https://github.com/DevCyclonekitten/Trihexangular-Launcher"
                }}
            ]},
            {"text":"Custom","interactor":[
                {"type":"inputfield","content":{
                    "fieldname":"repository",
                    "returnbutton":True,
                    "name":"Enter repository"
                }}
            ]}
        ]
    }
}

systemwelcome = {
    "name":"Welcome",
    "content":[
        {"text":"Welcome","position":0,"font":("Helvetica",15)},
        {"text":"Do you want to install trihexangular launcher","position":25,"font":("Helvetica",10)}
    ],
    "icon":"cancel",
    "flags":{
        "exit-after":0,
        "persistent":0,
        "invisible":0,
        "priority":1
    },
    "interactions":{
        "buttons":[
            {"text":"Yes","interactor":[
                {"type":"dismiss"}
            ]},
            {"text":"Exit","interactor":[
                {"type":"exit"}
            ]}
        ]
    }
}

systemos = {
    "name":"Select OS",
    "content":[
        {"text":"Select Operating System","position":0,"font":("Helvetica",15)}
    ],
    "icon":"cancel",
    "flags":{
        "exit-after":0,
        "persistent":0,
        "invisible":0,
        "priority":1
    },
    "interactions":{
        "buttons":[
            {"text":"Windows","interactor":[
                {"type":"json","content":{
                    "os":"windows"
                }}
            ]},
            {"text":"Linux","interactor":[
                {"type":"json","content":{
                    "os":"linux"
                }}
            ]}
        ]
    }
}


systemeula = {"name":"EULA",
    "content":[
        {"text":"End user licence agreement","position":0,"font":("Helvetica",15)},
        {"text":"Have you read and do you agree to the eula?","position":25,"font":("Helvetica",10)}
    ],
    "icon":"cancel",
    "flags":{
        "exit-after":1,
        "persistent":1,
        "invisible":1,
        "priority":1
    },
    "interactions":{
        "json":{
            "eula":False
        },
        "buttons":[
            {"text":"Accept","interactor":[
                {"type":"dismiss"},
                {"type":"json","content":{
                    "eula":True
                    }
                }
                ]
            },
            {"text":"View","interactor":[
                {"type":"url","content":{"target":r"https://devcyclonekitten.github.io/Trihexangular-Launcher/eula.html"}},
                {"type":"messagelink","content":{"target":"repeat"}}
            ]},
            {"text":"Deny","interactor":[
                {"type":"messagelink","content":{"target":"DENYEULA"}},
                {"type":"messagebuilder","content":{
                        "name":"Denied Eula",
                        "content":[
                            {"text":"Cannot install launcher","position":0,"font":("Helvetica",15)},
                            {"text":"Cannot proceed with installation without agreeing to EULA.","position":25,"font":("Helvetica",10)}
    
                        ],
                        "icon":"cancel",
                        "flags":{

                        },
                        "interactions":{
                            "json":{},
                            "buttons":[
                                {"text":"Quit","interactor":[{"type":"exit"}]}
                            ]
                        }
                    }
                }
            ]}
        ]
    }
}