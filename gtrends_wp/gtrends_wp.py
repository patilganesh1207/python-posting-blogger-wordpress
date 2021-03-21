import os
import re
import time
import pickle
import random
#from codecs import open
from selenium import webdriver
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, EditPost
from wordpress_xmlrpc.methods.users import GetUserInfo

from oauth2client import client
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from goose3 import Goose
from urllib.request import urlopen
from bs4 import BeautifulSoup

import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


# Fetch the service account key JSON file contents
cred = credentials.Certificate('C:/server_main/cred/firebase_admin.json')
databaseURL = {'databaseURL': "https://get-any-service.firebaseio.com"}
# account, granting admin privileges
firebase_admin.initialize_app(cred, databaseURL)


print (time.asctime())
print ("----------------------Start-----------------------")

cont = ['', '', '', '', '', '', '', '', '']

def warning():
    os.system("C:/server_main/cred/alarm1.MP4")
    exit()

def history_save(d):
    hist = open("history.txt","a+")
    hist.write(str(d)+"\n")
    hist.close()


def read_file(file_n):
    f = open(file_n,"r+",encoding='latin1')
    d = f.read()
    f.close()
    return d



geo = read_file("countries.txt")
geo = geo.split("\n")




def start(geo):
    html = ""
    while (html == ""):
        driver = webdriver.Chrome(executable_path=r'C:/server_main/cred/chromedriver.exe')
        driver.minimize_window()
        driver.get("https://trends.google.com/trends/trendingsearches/daily/rss?geo="+geo)
        time.sleep(3)
        html = driver.page_source
        if "This site can’t be reached" in html or "No internet" in html:
            print ("Reloading")
            html = ""
        driver.quit()

    raw = html.split("\n")
    r=['0','0','0','0']
    data=""
    stop=0
    i=0
    while stop < 10:
        html = raw[i]
        i = i+1
        html=html.strip()
        if "<title>" in html:
            html = html.replace("<title>","")
            html = html.replace("</title>","")
            if "Daily Search Trends" not in html:
                history = read_file("history.txt")
                if r[0] in history:
                    print (r[0])
                else:
                    d = (",".join(r))
                    data += str(d)+"\n"
                r=['0','0','0','0']
                stop=stop+1
                r[0]=html
                
        elif "<ht:picture>" in html:
            html = html.replace("<ht:picture>","")
            html = html.replace("</ht:picture>","")
            r[1]=html
            
        elif "<ht:news_item_url>" in html:
            html = html.replace("<ht:news_item_url>","")
            html = html.replace("</ht:news_item_url>","")
            if r[2] == "0":
                r[2]=html
            else:
                r[3]=html

    data = data.replace("0,0,0,0\n","")
    print ("start done")
    return data

    

def get(url):
    if url == "0":
        return "00000000000000000"
    html = ""
    while (html == ""):
        driver = webdriver.Chrome(executable_path=r'C:/server_main/cred/chromedriver.exe')
        driver.minimize_window()
        driver.get(url)
        time.sleep(3)
        html = driver.page_source
        if "This site can’t be reached" in html or "No internet" in html:
            print ("Reloading")
            html = ""
        driver.quit()
            
    ds = ['', '', '', '', '', '', '', '', '']
    g = Goose()
    data = g.extract(raw_html=html)
    ds[1] = data.cleaned_text 
    ds[2] = data.title
    ds[3] = data.meta_description
    ds[4] = data.meta_keywords
    tag = data.tags
    ds[5] = tag
    i=0
    db=""
    for t in tag:
        i=i+1
        if i>5:   #tags count now 7
          print ("tags: "+str(i))
          ds[5]=db.split(",")
          break
        else:
            db+=(t+",")
    ds[6] = data.meta_favicon
    g.close()
    bs = BeautifulSoup(html, 'html.parser')
    images = bs.find_all('img', {'src':re.compile('.jpg')})
    for image in images: 
        print(image['src']+'\n')
        ds[7] = (image['src'])
        break
    print ("get done")
    return ds


def public_manipulate(ttitle,d):
    d = ['', '', '', '', '', '', '', '', '']
    d[1] = spin(d[1])
    d[2] = spin(ttitle+" | "+d[2])
    d[3] = spin(ttitle+" "+d[3])
    return d


def manipulate(cont1,cont2,ttitle,timage):
    cont = ['', '', '', '', '', '', '', '', '']
    try:
        d = cont1[1]+"\n  "+cont2[1]
    except Exception as ex:
        print(str(ex))
    cont[1] = spin(d)
    d = ttitle+" "+cont1[3]
    cont[3] = spin(d)
    d = ttitle+" | "+cont1[2]
    cont[2] = spin(d)
    cont[4] = cont1[4]
    cont[6] = cont1[6]
    
    if "http" in cont1[7] or "www." in cont1[7]:
        timage = cont1[7]
    elif "http" in cont2[7] or "www." in cont2[7]:
        timage = cont2[7]

    if timage == "0":
        print ("no image")
    else:
        cont[1] = "<a href=\"https://liv-india.blogspot.com/\"><img src=\""+timage+"\" /> </a> <br/> "+cont[1]

    if cont2 == "0":
        cont[5] = cont1[5]
    else:
        cont[5] = cont2[5]

    print ("manipulate done")
    return cont



def blogger(g,cont):
    udata = read_file("blog_id.txt")
    udata = udata.split("\n")
    ui=0
    while udata[ui] != "end":
        d = udata[ui]
        d = d.split(",")
        print (g+" : "+d[1])
        if g in d[1]:
            post_blogger(cont,d[0])
            print ("Blogger Posted: "+d[0])
        ui=ui+1
    print ("Blogger Done")


def wp(g,cont):
    udata = read_file("wp_users.txt")
    udata = udata.split("\n")
    ui=0
    while udata[ui] != "end":
        d = udata[ui].split("###")
        print (g+" : "+d[5])
        if g in d[5]:
            if "Google Trends" in str(d[6]):
                if 0 < int(d[7]):
                    if "Content Spinner" in str(d[8]):
                        cons = cont
                        cons[1] = spin(cont[1])
                        post_wp(cons,d[2],d[3],d[4])
                    else:
                        post_wp(cont,d[2],d[3],d[4])
                    print ("Wordpress Posted: "+d[1])
                else:
                    print ("0 Balance")
        ui=ui+1
    print ("WP Done")


def post_wp(d,usite,uname,upass):
    wp = Client(usite, uname, upass)
   # wp.call(GetPosts())
   # wp.call(GetUserInfo())
    post = WordPressPost()
    post.title = d[2]
    post.content = d[1]
    post.terms_names = {'post_tag': d[5],'category': d[4]}
    post.post_status = 'publish'
    try:
        wp.call(NewPost(post))
        print ("----------------------Wordpress-Post-Done-----------------------")
    except Exception as ex:
        print(str(ex))
        excw = open("exception.txt", "a+")
        excw.write(str(ex)+" : "+time.asctime()+"\n")
        excw.write("\n--------------------------------------------------------------------------------\n")
        excw.close()
    


SCOPES = ['https://www.googleapis.com/auth/blogger', 'https://www.googleapis.com/auth/drive.file']

def post_blogger(cont,BLOG_ID):
    drive_handler, blog_handler = get_blogger_service_obj()
   # get_blog_information(blog_handler)

    data = {
      "kind": "blogger#post",
      "blog": {
        "id": BLOG_ID
      },
      #"url": cont[2],
      "title": cont[2],
      "content": cont[1],
      "images": [
        {
          "url": ""
        }
      ],
      "customMetaData": cont[3],
      "author": {
        "displayName": "Admin",
        "url": "Admin",
        "image": {
          "url": cont[6]
        }
      },
      "labels": [cont[5]]
    }
        
    posts = blog_handler.posts()
    try:
        posts.insert(blogId=BLOG_ID, body=data, isDraft=False, fetchImages=True).execute()
        print ("----------------------Blogger-Post-Done-------------------------")
    except Exception as ex:
        print(str(ex))
        if "sorry, but one or more limits for the requested action have been exceeded." in ex:
            warning()
        excw = open("exception.txt", "a+")
        excw.write(str(ex)+" : "+time.asctime()+"\n")
        excw.write("\n--------------------------------------------------------------------------------\n")
        excw.close()



def get_blogger_service_obj():
    creds = None
    cred_path = "C:\server_main\cred\\"
    if os.path.exists(cred_path+'blogger_auth_token.pickle'):
        with open(cred_path+'blogger_auth_token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_path+'blogger_cred.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(cred_path+'blogger_auth_token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    blog_service = build('blogger', 'v3', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)

    return drive_service,blog_service


def get_blog_information(api_handler=None, blog_max_posts=1):
    try:
        if not api_handler:
            return None
        blogs = api_handler.blogs()
        resp = blogs.get(blogId=BLOG_ID, maxPosts=blog_max_posts, view='ADMIN').execute()
        for blog in resp['posts']['items']:
            print('The blog title : \'%s\'  and url : %s' % (blog['title'], blog['url']))
    except Exception as ex:
        print(str(ex))


            
def spin(d):
##    dd = read_file("data.zip")
##    d = d.lower()
##    dd = dd.lower()
##    d = d.split(" ")
##    dd = dd.split("\n")
##    length = len(d)
##    print ("spin words: "+str(length))
##    i = 0
##    di = 0
##    while (i < length):
##        try:
##            t = d[i]
##            if t in dd[di]:
##                l = dd[di].split(",")
##                d[i] = random.choice(l)
##                #print (d[i])
##                i = i + 1
##                di = 0
##            else:
##                di = di + 1
##        except Exception as ex:
##            #print(str(ex))
##            di = 0
##            i = i + 1  
##
##    do = (" ".join(d))
##    print ("spin done")
    return d



def embed(d,timage,img1,img2):
    if "http" in img1 or "www." in img1:
        timage = img1
    elif "http" in img2 or "www." in img2:
        timage = img2

    if timage == "0":
        print ("no image")
    else:
        d = "<a href=\"https://liv-india.blogspot.com/\"><img src=\""+timage+"\" /> </a> <br/> "+d
    return d




def firebase_check_wp_users():
    ref = db.reference("wp_regv/upd/")
    d = ref.get("s")
    e = json.dumps(d)
  #  print (e)
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



def control():
  #  firebase_check_wp_users()
    i=0
    while geo[i] != "end":
        dgeo = geo[i]
        dgeo = dgeo.split(",")
        wp_d = read_file("wp_users.txt")
        id_d = read_file("blog_id.txt")
        l=0
        data=""
        if dgeo[1] in wp_d or dgeo[1] in id_d:
            data = start(dgeo[0])
            data = data.split("\n")
            l = len(data)
            l=l-1
            print ("Data Packets: "+str(l)+", Geo :"+dgeo[1])
        else:
            l=-1
        di=0
        while di < l:
            subdata = data[di]
            subdata = subdata.split(",")
            ttitle = subdata[0]
            timage = subdata[1]
            cont1 = get(subdata[2])
            cont2 = get(subdata[3])
            cont = manipulate(cont1,cont2,ttitle,timage)
            
##            try:
##                cont1[1] = embed(cont1[1],timage,cont1[7],cont2[7])
##                cont2[1] = embed(cont2[1],timage,cont2[7],cont1[7])
##            except Exception as ex:
##                print(str(ex))
##                print (cont2[1]+timage+cont2[7]+cont1[7])
##
            
            
            blogger(dgeo[1],cont)
            
           # cont1 = public_manipulate(ttitle,cont1)
            wp(dgeo[1],cont)
          #  cont2 = public_manipulate(ttitle,cont2)
          #  wp(dgeo[1],cont2)
            
            history_save(subdata[0]+","+subdata[2]+","+subdata[3])
            
            di=di+1
            print ("data packet running: "+dgeo[1]+" "+str(di))
        i=i+1



while True:
    control()


