import glob

#s
files = glob.glob("Sources/*.html")
#
baseindex = open("Sources/base.html","r")
content = baseindex.read()
baseindex.close()
#

for file in files:
    print(f"\nConverting: {file}")
    if(file!="Sources/base.html"):
        fs = open(file)
        insertion = fs.read()
        fs.close()

        PATH = file.replace("Sources/","")
        fs2 = open(PATH,"w")
        fs2.write(content.replace("<p>{CONTENT_INSERTION}</p>",insertion))
        fs2.close()