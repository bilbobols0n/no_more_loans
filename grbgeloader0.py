from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from generators import genBday, genAcctNum, genRoutingNum, genJobTitle, genDLic, genEmail, genZpCode, genPhonNum 
from joblib import Parallel, delayed
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from faker import Faker
from RandomWordGenerator import RandomWord

fake = Faker()

import time
import random
import re
import names
import linecache

# waits more than 1 second, but not too long
def bigWait():
    return time.sleep(random.uniform(1, 2.5))

# waits less than 1 sec
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
    return linecache.getline("zipcodes2.txt", random.randint(1, 38500))

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


def loadSizeLarge(url):
    while True:
        Faker.seed(random.randint(1, 1000))

        driver = webdriver.Chrome("/home/jpartridge36/chromedriver")
        driver.get(url)
        smallWait()
        print("got to webdriver")

        #Confirm page load
        def pageIsLoaded():
            return driver.find_element_by_tag_name("body") != None

        i = 0
        while i < 1:
            if not pageIsLoaded:
                smallWait()
            else:
                i = 1
                continue

        #Loan Amount
        lnAmntField = driver.find_element_by_name("requestedAmount")
        lnAmntStr = str(random.randint(1000, 10000))
        lnAmntField.send_keys(lnAmntStr)
        smallWait()

        #Purpose of Loan
        dDList = driver.find_elements_by_class_name('css-1wa3eu0-placeholder')

        dDList[0].click()
        smallWait()
        prpsStr = "react-select-2-option-"
        prpsStr += str(random.randint(0, 15))
        driver.find_element_by_id(prpsStr).click()
        smallWait()

        #Your Credit Score
        dDList[1].click()
        smallWait()
        crdtStr = "react-select-3-option-"
        crdtStr += str(random.randint(0, 4))
        driver.find_element_by_id(crdtStr).click()
        smallWait()

        #Zip Code
        zpCdField = driver.find_element_by_name("zip")
        zpCdField.send_keys(genZpCode())
        smallWait()

        #Legal First Name
        lFrstNm = driver.find_element_by_name("firstName")
        storedFN = names.get_first_name()
        lFrstNm.send_keys(storedFN)
        smallWait()

        #Legal Last Name
        lLastNm = driver.find_element_by_name("lastName")
        storedLN = names.get_last_name()
        lLastNm.send_keys(storedLN)
        smallWait()

        #Birthday
        bDay = driver.find_element_by_name("birthDate")
        bDay.send_keys(genBday())
        smallWait()

        #Phone Number
        phonNumField = driver.find_element_by_name("homePhone")
        phonNumField.send_keys(genPhonNum())
        smallWait()

        #Email Address
        emlField = driver.find_element_by_name("email")
        emlField.send_keys(genEmail(storedFN, storedLN))
        smallWait()

        #Last 4 Digits of SSN
        ssnField = driver.find_element_by_name("ssn4")
        ssnField.send_keys(str(random.randint(1000, 9999)))
        smallWait()

        #SMS Consent Checkbox
        smsCB = driver.find_element_by_class_name("Checkbox--content--1iy0t")
        smsCB.click()
        smallWait()

        #Continue Button
        contBtn = driver.find_elements_by_class_name("start--submitButton--3m9Gk")
        contBtn[0].click()

        #Second Page (further personal information)

        #confirm page 2 loaded

        while len(driver.find_elements_by_css_selector('.SecondaryButton--secondary--1qGfL.GlobalButton--button--1pVQi.Button--button--1oMyq.Button--large--3I4Em')) < 1:
            smallWait()
            print("waiting for page 2 to load")
            continue

        #Street Address
        stAddrField = driver.find_element_by_name("address")
        stAddrField.send_keys()
        myAddr = fake.address()
        stAddr = myAddr.splitlines()
        stAddrField.send_keys(stAddr[0])
        smallWait()

        #Length at Address
        dDList = driver.find_elements_by_class_name('css-1wa3eu0-placeholder')
        dDList[0].click()
        smallWait()
        lAAStr = "react-select-6-option-"
        lAAStr += str(random.randint(0, 12))
        driver.find_element_by_id(lAAStr).click()
        smallWait

        #Home Ownership
        dDList[1].click()
        smallWait()
        hmStr = "react-select-7-option-"
        hmStr += str(random.randint(0, 1))
        driver.find_element_by_id(hmStr).click()
        smallWait()

        #Car Ownership
        dDList[2].click()
        smallWait()
        carStr = "react-select-8-option-"
        carStr += str(random.randint(0, 1))
        driver.find_element_by_id(carStr).click()
        smallWait()

        #Driver's License
        dLicField = driver.find_element_by_name("driverLicenseNumber")
        dLicField.send_keys(genDLic())
        smallWait()

        #License State
        dDList[3].click()
        smallWait()
        LicStStr = "react-select-9-option-"
        LicStStr += str(random.randint(0, 55))
        driver.find_element_by_id(LicStStr).click()
        smallWait()

        #Best Contact Time
        dDList[4].click()
        smallWait()
        bCTStr = "react-select-10-option-"
        bCTStr += str(random.randint(0, 3))
        driver.find_element_by_id(bCTStr).click()
        smallWait()

        #Continue Button
        contBtn = driver.find_elements_by_class_name("start--submitButton--3m9Gk")
        contBtn[0].click()

        #Third Page (job and pay)

        #confirm page 3 loaded
        while len(driver.find_elements_by_class_name('react-datepicker__input-container')) < 1:
            smallWait()
            print("waiting for page 3 to load")
            continue


        #Work Phone
        wrkPhon = driver.find_element_by_name("workPhone")
        wrkPhon.send_keys(genPhonNum())
        smallWait()

        #Income Source
        dDList = driver.find_elements_by_class_name('css-1wa3eu0-placeholder')
        dDList[0].click()
        smallWait()
        incStr = "react-select-16-option-"
        incStr += str(random.randint(0, 6))
        driver.find_element_by_id(incStr).click()
        smallWait()

        #Job Title
        jbTitl = driver.find_element_by_name("jobTitle")
        jbTitl.send_keys(fake.job())

        #Employer Name
        emplrNm = driver.find_element_by_name("employer")
        emplrNm.send_keys(fake.company())

        #Time Employed
        dDList[1].click()
        smallWait()
        tmEmpld = "react-select-17-option-"
        tmEmpld += str(random.randint(0, 12))
        driver.find_element_by_id(tmEmpld).click()
        smallWait()

        #Pay Frequency
        dDList[2].click()
        smallWait()
        tmEmpld = "react-select-18-option-"
        tmEmpld += str(random.randint(0, 3))
        driver.find_element_by_id(tmEmpld).click()
        smallWait()

        #Next Pay Date
        nxtPayDt = driver.find_element_by_name("payDate1")
        nxtPayDt.click()
        smallWait()
        advncMnthLst = driver.find_elements_by_class_name("react-datepicker__navigation--next")
        advncMnthLst[0].click()
        #create list of only available-day web element buttons
        avbleDays = driver.find_elements_by_css_selector("div.react-datepicker__day:not(.react-datepicker__day--disabled)")
        print(len(avbleDays))
        chsnDay = random.randint(0, (len(avbleDays)-1))
        avbleDays[chsnDay].click()
        smallWait()

        #Active Military
        dDList[3].click()
        smallWait()
        actMltr = "react-select-19-option-"
        actMltr += str(random.randint(0, 1))
        driver.find_element_by_id(actMltr).click()
        smallWait()

        #Continue Button
        contBtn = driver.find_elements_by_class_name("start--submitButton--3m9Gk")
        contBtn[0].click()
        smallWait()

        #confirm page 4 loaded
        while len(driver.find_elements_by_css_selector('.start--finalConsent--1OkSe.start--isNotSigned--3fi6Q')) < 1:
            smallWait()
            print("waiting for page 4 to load")
            continue

        #Monthly Net Income
        dDList = driver.find_elements_by_class_name('css-1wa3eu0-placeholder')
        dDList[0].click()
        smallWait()
        mNtInc = "react-select-24-option-"
        mNtInc += str(random.randint(0, 11))
        driver.find_element_by_id(mNtInc).click()
        smallWait()

        #Direct Deposit
        dDList[1].click()
        smallWait()
        dDepst = "react-select-25-option-"
        dDepst += str(random.randint(0, 1))
        driver.find_element_by_id(dDepst).click()
        smallWait()

        #Routing Number
        rtngNumField = driver.find_element_by_name("bankAba")
        rtngNumField.send_keys(genRoutingNum())
        smallWait()

        #Account Number
        bnkAcct = driver.find_element_by_name("bankAccountNumber")
        bnkAcct.send_keys(genAcctNum())
        smallWait()

        #Account Type
        dDList[2].click()
        smallWait()
        acctTyp = "react-select-26-option-"
        acctTyp += str(random.randint(0, 1))
        driver.find_element_by_id(acctTyp).click()
        smallWait()

        #Months at Bank
        dDList[3].click()
        smallWait()
        mAtBnk = "react-select-27-option-"
        mAtBnk += str(random.randint(0, 12))
        driver.find_element_by_id(mAtBnk).click()
        smallWait()

        #Social Security Number
        socialSN = driver.find_element_by_name("ssn")
        socialSN.send_keys(fake.ssn())
        smallWait()

        #Submit Button
        sbtBtn = driver.find_elements_by_class_name("PrimaryButton--primary--1GBE0")
        sbtBtn[0].click()
        smallWait()

        #Confirm Page 5 loaded
        waitingInt = 0
        confrmtns = 0
        while len(driver.find_elements_by_css_selector(".processing--noButton--16eNa.SecondaryButton--secondary--1qGfL.GlobalButton--button--1pVQi.Button--button--1oMyq.Button--large--3I4Em")) < 1:
            time.sleep(1)
            waitingInt += 1
            print("waiting for page 5 to load")
            if waitingInt > 60:
                break
            else:
                continue
        try:
            #Attempt to Connect to Lender
            yesBtnLst = driver.find_elements_by_class_name("PrimaryButton--primary--1GBE0")
            yesBtnLst[0].click()
            smallWait()
            time.sleep(60)
            confrmtns += 1
            #Start script over from beginning
            driver.close()
            #logging
            handl = open("loaderLog.txt", "w")
            logStr = "Submitted "
            logStr += str(confrmtns)
            logStr += " forms successfully before page 5."
            handl.write(logStr)
            handl.close()
            continue
            #log links here later for other python scripts to use

        except:
            #Start script over from beginning
            driver.close()
            #logging
            handl = open("loaderLog.txt", "w")
            logStr = "Submitted "
            logStr += str(confrmtns)
            logStr += " forms successfully before page 5."
            handl.write(logStr)
            handl.close()
            continue

urls = [
    "https://fundsrelief.co/start/", 
    "https://lendyoudollars.com/start/",
    "https://octoberfunds.com/start/",
    "https://autumnfunds.com/start/",
    ]
print(urls)
Parallel(n_jobs=-1)(delayed(loadSizeLarge)(url) for url in urls)

# #logging
# handl = open("loaderLog.txt", "w")
# logStr = "Submitted "
# logStr += str(confrmtns)
# logStr += " forms successfully before page 5."
# handl.write(logStr)
# handl.close()

# driver.close()