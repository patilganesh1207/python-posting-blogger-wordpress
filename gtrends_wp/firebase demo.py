import time
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import facebook
# Fetch the service account key JSON file contents
cred = credentials.Certificate('C:/server_main/cred/firebase_admin.json')
databaseURL = {'databaseURL': "https://get-any-service.firebaseio.com"}
# account, granting admin privileges
firebase_admin.initialize_app(cred, databaseURL)




def firebase_check_wp_users():
    ref = db.reference("wp_regv/upd/")
    d = ref.get("s")
    e = json.dumps(d)
    print (e)
    if "\"1\"}" in e:
        print ("firebase wp-users data changed")
        ref = db.reference("wp_reg")
        d = ref.get()
        dd = json.dumps(d)
##        ffw = open("uss1.txt","w+")
##        ffw.write(str(dd))
##        ffw.close()
        dd = dd.replace("[null, \"","")
        dd = dd.replace("\": {\"","###")
        dd = dd.replace("{\"","")
        dd = dd.replace("\": \"","###")
        dd = dd.replace("\", \"","###")
        dd = dd.replace("\"}, \"","\n")
        dd = dd.replace("\"]}","\nend")
        dd = dd.replace("\": ","###")
        dd = dd.replace(", \"","###")

        ff = open("wp_users.txt","w+")
        ff.write(dd)
        ff.close()
        ref = db.reference("wp_regv/upd/s")
        ref.set("0")
    print ("firebase wp-users checked")


firebase_check_wp_users()
exit()
