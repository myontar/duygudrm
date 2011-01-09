import os 
PROJECT_DIR = os.path.dirname(__file__) 
LOCALE_DIR = "locale"
STATIC_DIR = "statics/js/"
folder = os.path.join(PROJECT_DIR, LOCALE_DIR)
for i in os.listdir(folder):
    jsname = i
    try:
        file =  os.path.join(folder, i, "LC_MESSAGES","djangojs.po")
        print file
        f = open(file,"r")
        data = f.read()
        text = ""
        for ix in data.split("#:"):
            r = ix.split("\n")
            if r[1][:5] == "msgid":
                if r[2][5:].replace('r ""',"").strip() != "":
                    print r[2][5:].replace('"',"").strip()
                    text += "catalog["+r[1][5:].strip() + "] = " + r[2][5:].replace("r ","") + "\n"
        
        print text
        folder_save = os.path.join(PROJECT_DIR, STATIC_DIR,jsname+"-lang.js")
        os.remove(folder_save)
        ff = open(folder_save,"a+")
        ff.write(text)
        ff.close()
    except Exception as e:
        print e

raw_input("")


       
