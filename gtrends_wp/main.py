import os
import time


def history_reset():    #for run once sometimes
    file1 = open("history.txt","r+")
    d = file1.read()
    file1.close()
    d = d.split("\n")
    l = len(d)
    if l > 60:
        l = l-20
        i=0
        dd=""
        while i < 20:
            dd += d[l]+"\n"
            i=i+1
            l=l+1
        file2 = open("history.txt","w+")
        file2.write(dd)
        file2.close()



while True:
    history_reset()
    os.system("gtrends_wp.py")
    time.sleep(2)


