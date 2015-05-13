## -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
A significant rewrite of the original author's USC tool
"""

import requests
import os
import sys
import zipfile
import tempfile
from bs4 import BeautifulSoup
import glob
import sqlite3


#ONLY download the large zip file that contains EVERY title
def bulkdl(path):
    r = requests.get('http://uscode.house.gov/download/download.shtml')
    soup = BeautifulSoup(r.text)
    pl = soup.find(class_="releasepointinformation").text
    pl = pl.split(' ')[2]
    #current congress #
    cc = pl.split('-')[0]
    #current version
    cv = pl.split('-')[1]
    base = "http://uscode.house.gov/download/releasepoints/us/pl/"
    suffixHTM = "htm_uscAll@" + cc + "-" + cv + ".zip"
    suffix = cc + "/" + cv + "/" + suffixHTM
    url = base + suffix
    print(url)
    os.chdir("./tmp/")
    r = requests.get(url)
    with open(suffixHTM, "wb") as USC:
        USC.write(r.content)
                    ##START EXTRACTING
        zipnames = glob.glob("*")
        for fn in zipnames:
            zip_ref = zipfile.ZipFile(fn, 'r')
            zip_ref.extractall('../html/')
            zip_ref.close()
    os.remove(newzip)
    print(newzip + " DONE")


#download every title separated
def difftitles():
    r = requests.get('http://uscode.house.gov/download/download.shtml')
    soup = BeautifulSoup(r.text)
    pl = soup.find(class_="releasepointinformation").text
    pl = pl.split(' ')[2]
    #current congress #
    cc = pl.split('-')[0]
    #current version
    cv = pl.split('-')[1]
    base = "http://uscode.house.gov/download/releasepoints/us/pl/" + cc + "/" + cv + "/htm_usc"
    suffix = "@" + cc + "-" + cv + ".zip"

    title_names = []
    for i in range(1,55):
        if i == 5:
            title_names.append("05")
            title_names.append("05a")
        elif i == 11:
            title_names.append("11")
            title_names.append("11a")
        elif i == 18:
            title_names.append("18")
            title_names.append("18a")
        elif i == 28:
            title_names.append("28")
            title_names.append("28a")
        elif i == 34:
            pass
        elif i == 50:
            title_names.append("50")
            title_names.append("50a")
        elif i == 53:
            pass
        else:
            i = '%02d' % i
            title_names.append(i)


##inefficient: create another list
    tname = []
    for element in title_names:
        url = base + element + suffix
        tname.append(url)

    print(tname)
    os.chdir("./tmp/")
##extract to tmp, move to html, delete zip file
    for url in tname:
        r = requests.get(url)
        newzip = url.split('/')[-1]
        with open(newzip, "wb") as USC:
            USC.write(r.content)
            ##START EXTRACTING
            zipnames = glob.glob("*")
            for fn in zipnames:
                zip_ref = zipfile.ZipFile(fn, 'r')
                zip_ref.extractall('../html/')
                zip_ref.close()
        os.remove(newzip)
        print(newzip + " DONE")

def extract():
    os.chdir("tmp/")
    zipnames = glob.glob("*")
    for fn in zipnames:
        zip_ref = zipfile.ZipFile(fn, 'r')
        zip_ref.extractall('../html/')
        zip_ref.close()
        print(fn + " DONE")

def rename():
    os.chdir('html/')
    htm = glob.glob("*")
    for fn in htm:
        new = fn.split('PRELIMusc')[1]
        os.rename(fn,new)






if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: retrive_code <dest_path>")
        sys.exit(1)
    os.makedirs("tmp", exist_ok=True)
    os.makedirs("html", exist_ok=True)
    os.makedirs("code", exist_ok=True)
#    bulkdl(sys.argv[1])
    difftitles()
    rename()
#