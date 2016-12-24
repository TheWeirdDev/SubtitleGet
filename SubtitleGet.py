#!/usr/bin/python

###########################
#                         #
# Created by @Alireza6677 #
#                         #
###########################

import os , sys , requests
try:
    import bs4
    import urllib
except:
    print("You need beautifulsoup4 & urllib to run this script")
    print("Install them using 'pip install beautifulsoup4 urllib'")
    exit(1)

#from random import randint

def usage():
    print("SubtitleGet.py version 1.0 by @Alireza6677 (Using sub.salamdl.ir).")
    print("Usage : ./SubtitleGet.py 'Movie/Serial Name'\n")
    exit(1)

def getPageContent(url):
    page = ""
    try:
        page = requests.get(url)
        return page.content
    except:
        print("Connection error !\nCheck your internet connection and try again.")
        exit(1)

def downloadFile(url, path):
    resp = ""
    try:
        resp = urllib.request.urlopen(url).read()
    except:
        print("Error downloading the file.\nCheck your internet connection and try agian")
        exit(1)
    try:
        output =  open(path , "wb")
        output.write(resp)
        output.close()
    except:
        print("Error saving the file.\nCheck your disk space or this path:\n"+path)
        exit(1)

def main():
    movie = ""
    if len(sys.argv) > 1:
        i = 1
        while i < len(sys.argv):
            movie += " " + sys.argv[i]
            i += 1
    else:
        usage()

    page = getPageContent("http://sub.salamdl.ir/subtitles/title?q=" + movie)
    bs = bs4.BeautifulSoup(page , "html.parser")
    
    items = bs.find_all("div" , {"class" : "title"})
    names = []
    links = []

    for item in items:
        names.append(item.a.decode_contents(formatter="html"))
        links.append(item.a['href'])
    
    if len(names) == 0:
        print("Error : Movie not found !")
        exit(1)

    i = len(names) - 1
    while i >= 0:
        #item = "[%d] " % i+1
        print(" ["+str(i+1)+"] " + names[i])
        i -= 1
    inp = input("\nChoose one of the movies above (1 - %d): " % len(names)).strip()
    
    try:
        inp = int(inp)
    except:
        print("Error : Wrong input")
        exit(1)

    if inp < 1 or inp > len(names):
        print("Error : Input out of range")
        exit(1)
    for i in range(3):
        print("\n")

    link = "http://sub.salamdl.ir" + links[inp - 1] + "/farsi_persian"
    bs2 = bs4.BeautifulSoup(getPageContent(link)  , "html.parser")
    h = bs2.find_all("span" , {"class" : "positive-icon"})
    for i in h:
        i.decompose()
    
    h = bs2.find_all("span" , {"class" : "neutral-icon"})
    for i in h:
        i.decompose()
    
    subs = bs2.find_all("td" , {"class" : "a1"})
    subtitles = []
    sublinks = []
    for i in subs:
        subtitles.append(i.a.span.decode_contents(formatter="html").strip())
        sublinks.append(i.a['href'])

    if len(subtitles) < 1:
        print("No persian subtitles found :(")
        exit()

    i = len(subtitles) - 1 
    while i >= 0:
        print(" ["+str(i+1)+"] " + subtitles[i])
        i -= 1

    inp2 = input("\nChoose one of subtitles above (1 - %d): " % len(subtitles)).strip()
    
    try:
        inp2 = int(inp2)
    except:
        print("Error : Wrong input")
        exit(1)

    if inp2 < 1 or inp2 > len(subtitles):
        print("Error : Input out of range")
        exit(1)

    print("Downloading...")

    link2 = "http://sub.salamdl.ir"  + sublinks[inp2 - 1]
    name2 = subtitles[inp2 - 1]

    bs3 = bs4.BeautifulSoup(getPageContent(link2) , "html.parser")
    downloadLink = "http://sub.salamdl.ir" +  bs3.find("a" , {"id":"downloadButton"})['href']
    path = os.path.expanduser("~")+"/Downloads/" + name2 + ".zip" 
    
    downloadFile(downloadLink , path)
    print("\n\nAll Done.\n saved to :" + path)


if __name__ == "__main__":
    main()
