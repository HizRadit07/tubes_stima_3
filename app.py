from flask import Flask, render_template, request
import re
import datetime

app = Flask(__name__)

deadline = []
Bulan = ["[Jj]anuari","[Ff]ebruari","[Mm]aret","[Aa]pril","[Mm]ei","[jJ]uni","[Jj]uli","[aA]gustus","[sS]eptember","[oO]ktober","[Nn]ovember","[Dd]esember"]
Kode_kuliah = ["IF2121","IF2110","IF2120","IF2124","IF2123","IF2130","IF2210","IF2211","IF2220","IF2230","IF2240","IF2250"]
kata_penting = ["[kK]uis","[uU]jian","[tT]ucil","[tT]ubes","[pP]raktikum"]

def convertArrToString(array):
    s = ""
    for elements in array:
        s += elements+"<br/>"; #newline buat html pake <br/>
    return s

#myString = convertArrToString(deadline)
#print(myString)

def findKodeKuliah(myString):#find kode kuliah in a string
    for elements in Kode_kuliah:
        kk = re.search(elements,myString)
        if (type(kk) is not type(None)): #if found then break
            break
    return kk

def findTipeTugas(myString):
    for elements in kata_penting:
        tugas = re.search(elements,myString)
        if (type(tugas) is not type(None)): #if found then break
            break
    return tugas
def findTopikTugas(myString,kodeKuliah):
    topik = re.search("(?<="+kodeKuliah+")(.*)(?=pada)",myString)
    return topik
def findTanggal(myString):
    tanggal = re.search("(?<=pada)(.*)",myString)
    return tanggal


#rendering the template
@app.route("/")
def index():
    return render_template("index.html")

#get endpoint
@app.route("/get")
def get_bot_response():    
    userText = request.args.get('msg') #INI YG BAKAL DIPROSES
    #case1: add deadlines
    case1 = re.search("[Aa]dd",userText) or re.search("[TNtn]ambah",userText)

    if (type(case1) is not type(None)): #handle case1
        kk = findKodeKuliah(userText)
        tugas = findTipeTugas(userText)
        topik = findTopikTugas(userText,kk[0])
        tanggal = findTanggal(userText)
        newDeadline = tanggal[0] + "-" + kk[0] + "-" + tugas[0] + "-" +topik[0]
        deadline.append(newDeadline)
        return "Berhasil add <br/>" + newDeadline
    else:
        return "Maaf, command tidak dikenali"




if __name__ == "__main__":
    app.run(debug = True)
