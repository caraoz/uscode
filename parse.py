from bs4 import BeautifulSoup


#this is for parsing each html page as a way to store to the USC to a db,
#among other things
def code():
    os.chdir('html/')
#    conn = sqlite3.connect('../usc.db')
#    c = conn.cursor()
    htm = glob.glob("*")
    for title in htm:
        f = open(title,'r',encoding='utf-8')
        soup = BeautifulSoup(f)
        for x in soup.findAll(class_="section-head"):
            print(x.text)
            soup.findAll(class_="statutory-body")







if __name__ == "__main__":
    code()