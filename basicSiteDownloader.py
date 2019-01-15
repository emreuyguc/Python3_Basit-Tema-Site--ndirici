from tkinter import *
import os
import urllib.request
from html.parser import HTMLParser

pnc = Tk()

class myhtmlparser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.reset()
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []
    def handle_starttag(self, tag, attrs):
        self.NEWTAGS.append(tag)
        self.NEWATTRS.append(attrs)
    def handle_data(self, data):
        self.HTMLDATA.append(data)
    def clean(self):
        self.NEWTAGS = []
        self.NEWATTRS = []
        self.HTMLDATA = []


parser = myhtmlparser()


def cal():
    global anaKlasor
    global site
    anaKlasor = klasor.get()
    
    for root, dirs, files in os.walk(anaKlasor):
        for file in files:
            if file.endswith(".html"):
                fullurl = os.path.join(root, file)
                print(fullurl)
    
    site = ip.get()
    if not os.path.exists(anaKlasor):
        os.makedirs(anaKlasor)
    

    fp = urllib.request.urlopen(site)
    mybytes = fp.read()
    anasayfaVeri = mybytes.decode("utf8")
    fp.close()
    
    file = open(anaKlasor + "/index.html","w")
    file.write(anasayfaVeri)
    file.close()
    
    kodSuzgeci(anasayfaVeri)
    
    for root, dirs, files in os.walk(anaKlasor):
        for file in files:
            if file.endswith(".html") and file != 'index.html':
                fullurl = os.path.join(root, file)
                print('sayfa işleniyor ----> ' + file)
                veri = sayfaVeriCek(fullurl)
                kodSuzgeci(veri)
    print('İŞLEMLER TAMAMEN BİTTii')
def sayfaVeriCek(dosya):
    file = open(dosya,"r")
    ham = file.read()
    dosyaicerik = ham
    file.close()
    return(dosyaicerik)

def icerikCek(url):
    global site
    fp = urllib.request.urlopen(site + url)
    mybytes = fp.read()
    veri = mybytes
    fp.close()
    return(veri)

def sayfaKaydet(url):
    global anaKlasor
    global site
    fp = urllib.request.urlopen(site + "/" + url)
    mybytes = fp.read()
    sayfaVeri = mybytes.decode("utf8")
    fp.close()
    
    yol = url.split('/')
    if len(yol)>1:
        klasor = '/'.join(yol[:-1])
        if not os.path.exists(anaKlasor + "/" + klasor):
            os.makedirs(anaKlasor + "/" + klasor)
        
    file = open(anaKlasor + "/" + url,"w")
    file.write(sayfaVeri)
    file.close()
    
def icerikKaydet(dosya,veri):
    global anaKlasor
    yol = dosya.split('/')
    if len(yol)>1:
        klasor = '/'.join(yol[:-1])
        if not os.path.exists(anaKlasor + "/" + klasor):
            os.makedirs(anaKlasor + "/" + klasor)
        
    file = open(anaKlasor + "/" + dosya,"wb")
    file.write(veri)
    file.close()

def mevcutmu(url):
    global anaKlasor
    if os.path.isfile(anaKlasor + "/" + url):
        return(1)
    else:
        return(0)
        
def kodSuzgeci(veri):
    global anaKlasor
    parser.feed(veri)
    attrs = parser.NEWATTRS
    parser.clean()
    for r in attrs:
        try:
            if len(r)>0:
                if r[0][0] == 'rel':
                    if(r[1][0] == 'href'):
                        kontrol = mevcutmu(r[1][1])
                        if kontrol == 0:
                            print('işleniyor : ',r[1])
                            veri = icerikCek(r[1][1])
                            icerikKaydet(r[1][1],veri)
                        else:
                            print('dosya zaten mevcut pas geçildi',r[1][1])
                elif r[0][0] == 'type':
                    if r[1][0] == 'src':
                        kontrol = mevcutmu(r[1][1])
                        if kontrol == 0:
                            print('işleniyor : ',r[1])
                            veri = icerikCek(r[1][1])
                            icerikKaydet(r[1][1],veri)
                        else:
                            print('dosya zaten mevcut pas geçildi',r[1][1])
                    elif r[1][0] == 'rel':
                        if(r[2][0] == 'href'):
                            kontrol = mevcutmu(r[2][1])
                            if kontrol == 0:
                                print('işleniyor : ',r[2])
                                veri = icerikCek(r[2][1])
                                icerikKaydet(r[2][1],veri)
                            else:
                                print('dosya zaten mevcut pas geçildi',r[2][1])
                elif r[0][0] == 'src':
                    kontrol = mevcutmu(r[0][1])
                    if kontrol == 0:
                        print('işleniyor : ',r[0])
                        veri = icerikCek(r[0][1])
                        icerikKaydet(r[0][1],veri)
                    else:
                        print('dosya zaten mevcut pas geçildi',r[0][1])
                elif r[0][0] == 'href':
                    if r[0][1][-4:] == 'html':
                        print('işleniyor : ',r[0])
                        sayfaKaydet(r[0][1])
        except:
            continue
    print('işlem bitti')

y1 = Label(text="Klasör Adı :")
y1.grid(row=0,column=0)

klasor = Entry()
klasor.grid(row=0,column=1)

y2 = Label(text="Site Tam Url (http ile birlikte) :")
y2.grid(row=1,column=0)

ip = Entry()
ip.grid(row=1,column=1)

cal = Button(text="İndir",command=cal)
cal.grid(row=2,column=0)


pnc.mainloop()
