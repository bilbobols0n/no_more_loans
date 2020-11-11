import random
import re
import names
import time
import linecache

from RandomWordGenerator import RandomWord

def smallWait():
    return time.sleep(random.uniform(0.1, 0.4))

#generates a birthday like mmddyyyy
def genBday():
    bDayStr = ""
    mm = str(random.randint(1, 12))
    if re.match("\d{1}$", mm):
        zrM = "0"
        zrM += mm
        mm = zrM
    dd = str(random.randint(1, 29))
    if re.match("\d{1}$", dd):
        zrM = "0"
        zrM += dd
        dd = zrM
    yyyy = str(random.randint(1950, 1996))
    bDayStr += mm
    bDayStr += dd
    bDayStr += yyyy
    return bDayStr

def routingNum():
    zpLst = []
    handl = open("routing_numbers.txt", "r")
    for line in handl:
        zpRange = re.findall("\d{9}", line)
        zpLst.append(zpRange)
    zpI = random.randint(0, 42)
    handl.close()
    return str(random.randint(int(zpLst[zpI][0]), int(zpLst[zpI][1])))

#generates a valid US zipcode
def genZpCode():
    return linecache.getline("zipcodes2.txt", random.randint(1, 35415))


#generates a valid-looking us phone number
def genPhonNum():
    #instantiate list of area codes
    handl = open("areacodes.txt")
    rawFileTxt = handl.read()
    areaCodes = re.findall("\d{3}", rawFileTxt)
    handl.close()
    #done with area codes

    emStr = ""
    #Add NPA
    indxr = random.randrange(0, 341, 1)
    emStr += areaCodes[indxr]
    #Add NXX
    emStr += str(random.randrange(2, 9, 1))
    emStr += str(random.randrange(1, 9, 1))
    emStr += str(random.randrange(2, 9, 1))
    #Add xxxx
    for i in range(4):
        emStr += str(random.randrange(0, 9, 1))
    return emStr

def genEmail(fn, ln):
    emlStr = ""
    emlStr += fn.lower()
    emlStr += ln.lower()
    emlStr += str(random.randint(100, 999))
    emlStr += "@gmail.com"
    return emlStr

def genDLic():
    dLStr = "Z"
    for i in range(7):
        dLStr += str(random.randint(0, 9))
    return dLStr

def genJobTitle():
    wrdCount = random.randint(1, 2)
    wrdSize = random.randint(8, 10)
    title = ""
    iteRatr = 0
    for i in range(wrdCount):
        title += RandomWord(max_word_size=wrdSize).generate()
        if iteRatr == 0 and wrdCount == 2:
            title += " "
        iteRatr = 1
    return title

#Generates a routing number from a major US bank
def genRoutingNum():
    rtngMegaLst = []
    handl = open("routing_numbers.txt", "r")
    for line in handl:
        rtngLst = re.findall("\d{9}", line)
        if len(rtngLst) > 0:
            rtngMegaLst.append(rtngLst[0])
    rgI = random.randint(0, 200)
    handl.close()
    return rtngMegaLst[rgI]

#Generates a 10-12 digit number not starting with zero. Not a real acct number
def genAcctNum():
    acctNum = ""
    acctNum += str(random.randint(1, 9))
    for i in range(random.randint(8, 10)):
        acctNum += str(random.randint(0, 9))
    return acctNum


# def pageLoadedChckr(elementStr):
#     while True:
#         try:
#             target = driver.find_element_by_name(elementStr)
#             print("found target, proceeding")
#             break
#             smallWait()
#         except:
#             smallWait()
#             print("target ", elementStr, " not yet found, trying again")
#             continue
        