from flask import Flask, render_template, request
import re
from datetime import datetime

app = Flask(__name__)

deadline = []
# intinya baca line pertama, terus iterasi deadline semua di deadline.txt
f = open("../test/deadline.txt",'r')
cnt = int(f.readline())
if cnt > 0:
    for i in range(cnt - 1):
        deadline.append(f.readline()[:-1])
    deadline.append(f.readline())
    f.close()
print(deadline)
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

def findTipeTugas(myString): #return string tipe tugas, depends on isi kata_penting
    for elements in kata_penting:
        tugas = re.search(elements,myString)
        if (type(tugas) is not type(None)): #if found then break
            break
    return tugas
def findTopikTugas(myString,kodeKuliah):#returns topik tugas, must be in between "kode kuliah" and "pada"
    topik = re.search("(?<="+kodeKuliah+" )(.*)(?=pada)",myString)
    return topik

def findTanggal(myString): #returns string tanggal, always after "pada"
    tanggal = re.search("(?<=pada )(.*)[0-9]",myString) #makes it stop at [0-9] (detects end of year)
    return tanggal

def findTanggalNoPada(myString): #returns string tanggal, always after "pada"
    tanggal = re.search("(\d)+-(\d)+-(\d)+",myString) or re.search("(\d)+/(\d)+/(\d)+",myString) #makes it stop at [0-9] (detects end of year)
    if (type(tanggal) is type(None)):
        for i in range(len(Bulan)):
            tanggal = re.search("(\d)+ " + Bulan[i] + " (\d)+", myString)
            if (type(tanggal) is not type(None)):
                break
    return tanggal

def stringContainsBulanName(myString): #returns true if a string contains nama bulan in the Bulan array
    for elements in Bulan:
        nameExist = re.search(elements,myString)
        if (type(nameExist) is not type(None)): #if found then break
            break
    if (type(nameExist) is not type(None)): #if found
        return True
    else:
        return False

print(stringContainsBulanName("Desember"))

def convertBulanToMonth(tanggalString):
    #oh boy this is a long one
    #basically reformat the name of month in a string from indonesian to english
    if "januari" in tanggalString or "Januari" in tanggalString: 
        return re.sub("[jJ]anuari","January",tanggalString)
    elif "februari" in tanggalString or "Februari" in tanggalString:
        return re.sub("[fF]ebruari","February",tanggalString)
    elif "maret" in tanggalString or "Maret" in tanggalString:
        return re.sub("[mM]aret","March",tanggalString)
    elif "april" in tanggalString:
        return re.sub("april","April",tanggalString)
    elif "mei" in tanggalString or "Mei" in tanggalString:
        return re.sub("[mM]ei","May",tanggalString)
    elif "juni" in tanggalString or "Juni" in tanggalString:
        return re.sub("[jJ]uni","June",tanggalString)
    elif "juli" in tanggalString or "Juli" in tanggalString:
        return re.sub("[jJ]uli","July",tanggalString)
    elif "agustus" in tanggalString or "Agustus" in tanggalString:
        return re.sub("[aA]gustus","August",tanggalString)
    elif "oktober" in tanggalString or "Oktober" in tanggalString:
        return re.sub("[oO]ktober","October",tanggalString)
    elif "desember" in tanggalString or "Desember" in tanggalString:
        return re.sub("[dD]esember","December",tanggalString)
    else:
        return tanggalString
    
def convertStringToDate(myString): #returns datetime object
    if "-" in myString and len(myString)== 10: #case xx-xx-XXXX
        return datetime.strptime(myString, '%d-%m-%Y')
    elif "/" in myString and len(myString)==10: #case xx/xx/XXXX
        return datetime.strptime(myString, '%d/%m/%Y')
    elif "-" in myString and len(myString)==8: #case xx-xx-xx
        return datetime.strptime(myString, '%d-%m-%y')
    elif "/" in myString and len(myString)==8: #case xx/xx/xx
        return datetime.strptime(myString, '%d/%m/%y')
    elif (stringContainsBulanName(myString) and " " in myString[-3]): #case xx bulan xx
        formatted = convertBulanToMonth(myString)
        return datetime.strptime(formatted, '%d %B %y')
    else: #case xx bulan XXXX
        formatted = convertBulanToMonth(myString)
        return datetime.strptime(formatted, '%d %B %Y')
    


#rendering the template
@app.route("/")
def index():
    return render_template("index.html")

#get endpoint
@app.route("/get")
def get_bot_response():    
    # asumsi id sebuah task itu nomor index + 1 a.k.a. elemen ke-berapa dari array deadline
    userText = request.args.get('msg') #INI YG BAKAL DIPROSES
    # uwu finder
    uwu = re.search("[Uu][Ww][Uu]",userText)
    #case1: add deadlines
    case1 = re.search("[Aa]dd|[TNtn]ambah",userText)
    # case 2: undur atau majuin deadline
    case2 = re.search("[Uu]ndur|[Mm]aju|[Gg]anti",userText)
    # case 3: task selesai
    case3 = re.search("[Ss]elesai|[Dd]one",userText)
    # case 6: help
    case6 = re.search("[hH]elp|[bB]antu",userText)
    # case 4 : seluruh task
    case4 = re.search("[Aa]pa|[Ss]aja|[Dd]eadline|[Ss]ejauh",userText)
    # case 5 : seluruh task antar tanggal
    case5 = re.search("[Aa]pa|[Ss]aja|[Dd]eadline|[Ss]ampai|[Aa]ntara|dan",userText)
    # case 7 : task tertentu antar tanggal
    case7 = re.search("[\d*]|[Mm]inggu|[Hh]ari|[Bb]ulan|[Tt]u[gb][ae]s|[Kk]uis|[Aa]pa saja",userText)
    # case 8 : deadline suatu task tertentu
    case8 = re.search("[Dd]eadline|[Tt]u[bg][ea][s]|IF....",userText)

    returner = ""
    if (type(case1) is not type(None)): #handle case1
        try:
            kk = findKodeKuliah(userText)
            tugas = findTipeTugas(userText)
            topik = findTopikTugas(userText,kk[0])
            tanggal = findTanggal(userText)
            tanggal_formatted = convertStringToDate(tanggal[0])
            newDeadline = str(tanggal_formatted.day) +"/"+ str(tanggal_formatted.month) + "/" + str(tanggal_formatted.year) + "-" + kk[0] + "-" + tugas[0] + "-" +topik[0]
            #  14/04/2021 - IF2211 - Tubes - String matching
            deadline.append(newDeadline)
            returner += "Berhasil add <br/>" + "(ID: " + str(len(deadline)) +") "+ newDeadline
        except:
            returner += "Masukkan sesuai format. Ketik 'help' untuk bantuan"

    elif (type(case2) is not type(None)):
        id = re.search("\s\d+\s", userText) # cari bilangan yg berdiri sendiri
        tanggal = findTanggalNoPada(userText)
        if (type(id) is type(None)):
            returner += "Mohon tambahkan ID"
        elif (type(tanggal) is type(None)):
            returner += "Mohon tambahkan tanggal"
        else:
            realID = int(id[0][1 : (len(id[0]) - 1)])
            if (realID > len(deadline)):
                returner += "ID tidak ada"
            else:
                tanggal = convertStringToDate(tanggal[0])
                tanggal = str(tanggal.day)+"/"+str(tanggal.month)+"/"+str(tanggal.year)

                tobeUpdated = deadline[realID - 1]
                tanggalNow = findTanggalNoPada(tobeUpdated)[0]
                undurDeadline(realID, tanggalNow, tanggal)  

                returner += "Deadline " + str(realID) +" berhasil di" + str(case2[0][0].lower() + case2[0][1:])+ " menjadi "+tanggal

    elif (type(case3) is not type(None)):
        res = taskDone(userText)
        returner += res
    elif (type(case4) is not type(None)):
        res = showDeadlineAll()
        for r in res:
            returner += r
    elif (type(case5) is not type(None)):
        tanggal1 = re.search("(?<=antara )(.*)[0-9]",userText)
        tanggal2 = re.search("(?<=sampai )(.*)[0-9]",userText) or re.search("(?<=dan )(.*)[0-9]",userText)
        res = showDeadlineAllTanggal(tanggal1,tanggal2)
        for r in res:
            returner += r

    elif (type(case6) is not type(None)):
        returner+= "COMMAND 1. add Deadline<br/>Format: text must contain 'add'/'tambah', and 'pada {Tanggal}'<br/> e.g. 'add Tubes IF2211 String Matching pada 14 April 2021' <br/><br/>"
        returner+= "COMMAND 2. modify Deadline<br/> Format: text must contain 'undur'/'maju'/'ganti' + detail deadline (kode kelas, tanggal, dsb)</br> e.g. 'Deadline 1 diundur 24/02/2020' <br/><br/>"
        returner+= "COMMAND 3. selesaikan deadline<br/> Format: text must contain deadline ID and keyword 'selesai' or 'done' e.g. 'deadline 1 selesai uwu'<br/>"
        returner+= "COMMAND 4. show all deadline <br/> Format: text must contain 'apa' / 'saja' / 'deadline' / 'sejauh' <br/>"
        returner+= "COMMAND 5. deadline all task in between dates <br/> Format: text must contain 'antara' or 'dan' and 2 dates <br/>"
        returner+= "COMMAND 6. help <br/>Format: text must contain 'help'/'bantu'<br/>"
        returner+= "COMMAND 7. deadline tugas spesifik between dates <br/> Format: text must contain 'antara' or 'dan' and 2 dates and the keyword 'tugas' / 'tubes' <br/>"
        returner+= "COMMAND 8. deadline tugas per kode kelas <br/> Format: text must contain keyword 'tugas' / 'tubes' and kode kelas IF...."
    
    elif (type(case7) is not type(None)):
        tanggalNow = datetime.datetime.Now 
        n = int(re.search(r'\d*',userText))
        tipeN = re.search(r"[Mm]inggu",userText) or re.search(r"[Hh]ari",userText) or re.search(r"[Bb]ulan",userText)
        if (tipeN == "Hari" or tipeN == "hari"):
            d = datetime.timedelta(days=n)
            tanggal2 = tanggalNow + d
        elif (tipeN == "Minggu" or tipeN == "minggu"):
            d = datetime.timedelta(weeks=n)
            tanggal2 = tanggalNow + d
        elif (tipeN == "Bulan" or tipeN == "bulan"):
            d = datetime.timedelta(months=n)
            tanggal2 = tanggalNow + d
        task = re.search("[Kk]uis", userText) or re.search("[Tt]ugas", userText) or re.search("[Tt]ubes", userText)
        res = showDeadlinePeriodeTask(tanggal2, task)
        for r in res:
            returner += r

    elif (type(case8) is not type(None)):
        tugas = findKodeKuliah(userText)
        res = showDeadlineTertentu(tugas)
        returner += res
        
    else:
        returner += "Maaf, command tidak dikenali"
    if (type(uwu) is not type(None)):
        # uwu bot update, not used by default, kalo mau pake uncomment aja
        # # uwu bot 2.0
        # returner = returner.replace("l", "w").replace("r","w").replace("L", "W").replace("R","W")
        # # uwu bot 3.0 (broken, ntah kenapa ketemu </br> jadi ancur)
        # vowel = ["a","i","u","e","o"]
        # prec=""
        # j = 0
        # yes = True
        # for i in returner:
        #     if i in vowel and prec not in vowel and prec != "w" and yes:
        #         returner = returner[:j] + "w" + returner[j:]
        #         j+=1
        #     yes = not(yes)
        #     prec = i
        #     j+=1

        # uwu 1.0
        returner += " uwu"

    # intinya update deadline txt sama jadwal baru abis command
    f = open("deadline.txt",'w')
    f.write(str(len(deadline)) + '\n')
    for i in deadline[:-1]:
        f.write(i+'\n')
    if (len(deadline) > 0):
        f.write(deadline[-1])
    f.close()

    return returner

def undurDeadline(id, tanggalNow, tanggalNext):
    # dari main, udh dapet pesannya ada tulisan ubah
    # cari idnya sama tanggal
    # lalu update
    # print(realID)
    tobeUpdated = deadline[id - 1]
    
    newdeadline = tobeUpdated.replace(tanggalNow, tanggalNext)
    deadline[id - 1] = newdeadline

def taskDone(userText):
    id = re.search("\s\d+\s", userText) # cari bilangan yg berdiri sendiri
    if (type(id) is type(None)):
        return "Mohon tambahkan ID"
    else:
        realID = int(id[0][1 : (len(id[0]) - 1)])
        if (realID > len(deadline)):
            return "ID tidak ada"
        else:
            deadline.remove(deadline[realID - 1])
            return "Deadline " + str(realID) + " sudah selesai"

def showDeadlineAll():
    #sejauh ini
    listdeadline = []
    for dead in deadline:
        listdeadline.append(dead)
    return listdeadline

def showDeadlineAllTanggal(tanggal1, tanggal2):
    date1 = convertStringToDate(tanggal1)
    date2 = convertStringToDate(tanggal2)
    listdeadline = []
    for dead in deadline:
        deaddate = convertStringToDate(re.search(r'\d\d[-]\d\d[-]\d\d\d\d', dead).string)
        if (date1 <= deaddate and deaddate <= date2):
            listdeadline.append(dead)
    return listdeadline

def showDeadlineTertentu(tugas):
    for dead in deadline:
        if (re.search(tugas, dead) != None and re.search("[Tt]ugas", dead) != None):
            tanggal = re.search(r'\d\d[-]\d\d[-]\d\d\d\d')
            break
    return tanggal

def showDeadlinePeriodeTask(tanggal, task):
    listdeadline = []
    for dead in deadline:
        if (re.search("task", dead) != None):
            deaddate = convertStringToDate(re.search(r'\d\d[-]\d\d[-]\d\d\d\d', dead).string)
            if (deaddate <= tanggal):
                listdeadline.append(dead)
    return listdeadline

if __name__ == "__main__":
    app.run(debug = True)
 
