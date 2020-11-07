import re
import random
import names
import linecache

from faker import Faker
fake = Faker()

#generates a valid US zipcode
def genZpCode():
    print(linecache.getline("zipcodes2.txt", random.randint(1, 38500)))
    

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


def genEmail(fn, ln):
    emlStr = ""
    emlStr += fn.lower()
    emlStr += ln.lower()
    emlStr += str(random.randint(100, 999))
    emlStr += "@gmail.com"
    return emlStr

# print(genEmail(names.get_first_name(), names.get_last_name()))

# print(fake.address())
# myAddr = fake.address()
# strAddr = myAddr.splitlines()
# print(myAddr)
# print(strAddr[0])

#generates a CA Drivers license
def genDLic():
    dLStr = "Z"
    for i in range(7):
        dLStr += str(random.randint(0, 9))
    return dLStr

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

def genAcctNum():
    acctNum = ""
    acctNum += str(random.randint(1, 9))
    for i in range(random.randint(8, 10)):
        acctNum += str(random.randint(0, 9))
    return acctNum


Faker.seed(random.randint(1, 1000))
