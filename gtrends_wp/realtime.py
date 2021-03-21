import os
import re
import time
import pickle
import random
import requests
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



def start_real(geo):
    data=""
    d=""
    while d == "":
        r = requests.get('https://trends.google.com/trends/api/realtimetrends?hl=en-GB&tz=-60&cat=h&fi=0&fs=0&geo='+geo+'&ri=300&rs=20&sort=0')
        e = json.loads(r.text[5:])
        d = json.dumps(e)
        d = d.split("newsUrl")
    i=0
    while i < len(d):
        dd = d[i].split("\"")
        di=0
        pl=0
        while di < len(dd):
            if "http" in dd[di]:
                if "google.com" not in dd[di]:
                    cc = read_file("history.txt")
                    if di < 3:
                        if dd[di] in cc:
                            di=len(dd)+5
                    else:
                        if pl < 4 and dd[di] not in cc and dd[di] not in data:
                            data += dd[di]+","
                            pl=pl+1
                            #print(dd[di])

            di=di+1
        if data != "":
            data += ",,remove"
            data = data.replace(",,,remove","")
            data += "\n"
        i=i+1
    data += "remove"
    data = data.replace("\nremove","")
    #print (data)
    print ("start done")
    return data

    

def get(url):
    print(url)
    if url == "0":
        return "00000000000000000"
    html = ""
    while (html == ""):
        driver = webdriver.Chrome(executable_path=r'C:/server_main/cred/chromedriver.exe')
        driver.minimize_window()
        try:
            driver.get(url)
        except Exception as ex:
            print(str(ex))
        #time.sleep(3)
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
    if "[]" not in ds[5]:
        i=0
        db=""
        for t in tag:
            i=i+1
            if i>7:   #tags count now 7
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
        #print(image['src']+'\n')
        ds[7] = (image['src'])
        break
    print ("get done")
    return ds


def public_spin(d):
    d[1] = spin(d[1])
    d[2] = spin(ttitle+" | "+d[2])
    d[3] = spin(ttitle+" "+d[3])
    return d


def mreal_manipulate(d):
    co = ['', '', '', '', '', '', '', '', '']
    i=0
    while i < len(d):
        dd = d[i].split("#_#")
        dd[1] = spin(dd[1])
        if "http" in dd[7] or "www." in dd[7]:
            dd[1] = "<a href=\"https://liv-india.blogspot.com/\"><img src=\""+dd[7]+"\" /> </a> <br/> "+dd[1]
        co[1] += dd[1]
        if i < 2:
            if "[]" not in co[5]:
                co[5] = dd[5]
            co[4] = dd[4]
            co[6] = dd[6]
        else:
            co[2] = dd[2]
            co[3] = spin(dd[3])
        i=i+1
    print ("mreal_manipulate done")
    return co


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
    except Exception as ex:
        print(str(ex))
        excw = open("exception.txt", "a+")
        excw.write(str(ex)+" : "+time.asctime()+"\n")
        excw.write("\n--------------------------------------------------------------------------------\n")
        excw.close()
    print ("----------------------Wordpress-Post-Done-----------------------")



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
    except Exception as ex:
        print(str(ex))
        excw = open("exception.txt", "a+")
        excw.write(str(ex)+" : "+time.asctime()+"\n")
        excw.write("\n--------------------------------------------------------------------------------\n")
        excw.close()
    print ("----------------------Blogger-Post-Done-------------------------")



def get_blogger_service_obj():
    creds = None
    cred_path = "C:/server_main/cred/"
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
##            t = ","+d[i]+","
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
    if "http://" in img1 or "https://" in img1:
        timage = img1
    elif "http://" in img2 or "https://" in img2:
        timage = img2

    if timage == "0":
        print ("no image")
    else:
        d = "<a href=\"https://liv-india.blogspot.com/\"><img src=\""+timage+"\" /> </a> <br/> "+d
    return d


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
                       # cons[1] = spin(cont[1])
                        post_wp(cons,d[2],d[3],d[4])
                    else:
                        post_wp(cont,d[2],d[3],d[4])
                    print ("Wordpress Posted: "+d[1])
                else:
                    print ("0 Balance")
        ui=ui+1
    print ("WP Done")




def control():
    i=0
    while geo[i] != "end":
        dgeo = geo[i]
        dgeo = dgeo.split(",")
        wp_d = read_file("wp_users.txt")
        id_d = read_file("blog_id.txt")
        l=0
        data=""
        if dgeo[1] in wp_d or dgeo[1] in id_d:
            data = start_real(dgeo[0])
            data = data.split("\n")
            l = len(data)
            print ("Data Packets: "+str(l)+", Geo :"+dgeo[1])
        else:
            l=-1
        di=0
        while di < l:
            subdata = data[di]
            subdata = subdata.split(",")
            bcont=""
            si=0
            while si < len(subdata):
                e = get(subdata[si])
                o = "#_#".join(map(str, e))
                bcont += o+"###"
                si=si+1
            bcont += "remove"
            bcont = bcont.replace("###remove","")
            bcont = bcont.split("###")
            
            mbcont = mreal_manipulate(bcont)
            blogger(dgeo[1],mbcont)
            wp(dgeo[1],mbcont)

            history_save(subdata)
            di=di+1
            print ("data packet running: "+dgeo[1]+" "+str(di))
        i=i+1





while True:
    control()
   # os.system("C:/server_main/yt/pages/yt_trend.py")
    




