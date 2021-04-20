import re
from app import findTanggalNoPada, Bulan, convertStringToDate

# myString = "Aku suka 24 April 2009"
# tanggal = re.search("(\d)+-(\d)+-(\d)+",myString) or re.search("(\d)+/(\d)+/(\d)+",myString) #makes it stop at [0-9] (detects end of year)
# if (type(tanggal) is type(None)):
#     for i in Bulan:
#         tanggal = re.search("(\d)+ " + i + " (\d)+", myString)
#         if (type(tanggal) is not type(None)):
#             break
# print(tanggal)
deadline = ["14/04/2021 - IF2211 - Tubes - String matching"]
ipt = "Deadline 3 ganti 28-04-2022"
id = re.search("\s\d+\s", ipt) # cari bilangan yg berdiri sendiri
realID = int(id[0][1 : (len(id[0]) - 1)])
# print(realID)
if (realID > len(deadline)):
    print("ID tidak ada")
else:
    tobeUpdated = deadline[realID - 1]
    tanggalNow = findTanggalNoPada(tobeUpdated)[0]
    print(tanggalNow)

    tanggal = findTanggalNoPada(ipt)
    tanggal = convertStringToDate(tanggal[0])
    tanggal = str(tanggal.day)+"/"+str(tanggal.month)+"/"+str(tanggal.year)
    print(tanggal)
    # print(tobeUpdated)
    newdeadline = tobeUpdated.replace(tanggalNow, tanggal)
    deadline[realID - 1] = newdeadline
    print(deadline[realID - 1])