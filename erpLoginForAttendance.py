from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from PIL import ImageGrab
from PIL import Image
import time
import pytesseract
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd
from selenium.webdriver import Chrome
pd.options.mode.chained_assignment = None

#For using Chrome browser
#browser = Chrome(executable_path=r"chromedriver.exe")

def username(usernameOfTheUser, loginField):
    loginField.clear()
    loginField.send_keys(usernameOfTheUser)
    loginField.send_keys(u"\ue004") #unicode for tab key
    time.sleep(2)
    
def password(passwordOfTheUser,passwordField):
    #get the password textbox
    passwordField.clear()
    #enter password
    passwordField.send_keys(passwordOfTheUser)
    passwordField.send_keys(u"\ue004") #unicode for tab key
    time.sleep(2)

def checkValidityOfCaptcha(captcha):
    return ((len(captcha)==6) and not(" " in captcha))

def captchaSolver(captchaField):
    captchaText = ImageGrab.grab(bbox = (680,473,790,505)) 
    #captchaText.show()
    captcha = pytesseract.image_to_string(captchaText, lang='eng')
    captchaField.send_keys(captcha)
    if checkValidityOfCaptcha(captcha) == False:
        main()
    else:
        captchaField.send_keys(u"\ue007") #unicode for enter key
        time.sleep(2)

def createList(soup):
    table = soup.find_all(id = "div3")
    output_rows = []
    heading_row = []
    heading_row.append("Course Name")
    heading_row.append("Faculty Name")
    heading_row.append("Total Classes")
    heading_row.append("Present")
    heading_row.append("Absent")
    heading_row.append("Percentage")
    output_rows.append(heading_row)
    for table_row in table[0].find_all("tr"):
        columns = table_row.find_all("td")
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)
    del output_rows[1]
    return output_rows    

def writeCsvFile(fname, data):
    """
    Input:
    fname - string, name of file to write
    data - list of list of items

    Description - Writes data to file
    """
    mycsv = csv.writer(open(fname, 'w'))
    for row in data:
        mycsv.writerow(row)
    
def createTable(fname):
    table = pd.read_csv(fname)
    for index in range(len(table['Faculty Name'])):
        table['Faculty Name'][index] = table['Faculty Name'][index].replace("\r\n","")
        table['Faculty Name'][index] = table['Faculty Name'][index].replace("  ","")    
    for index in range(len(table['Course Name'])):
        table['Course Name'][index] = table['Course Name'][index].replace("\r\n","")
        table['Course Name'][index] = table['Course Name'][index].replace("  ","")
    table.to_csv("attendance.csv",index = False)
    return table

def printTable(table):
    print(" ________________________________________________________________________________________________________________________________")
    print("|    Course Name                               | Faculty Name             | Total Classes  | Present   | Absent   | Percentage   |")
    print("|________________________________________________________________________________________________________________________________|")
    for index in range(len(table)):
        print("|  " + table['Course Name'][index], " "*(43 - len(table['Course Name'][index])) ,end = "")
        print("|  " + table['Faculty Name'][index], " "*(23 - len(table['Faculty Name'][index])), end = "")
        print("|  " + str(table['Total Classes'][index]), " "*(13 - len(str(table['Total Classes'][index]))), end = "")
        print("|  " + str(table['Present'][index]), " "*(8 - len(str(table['Present'][index]))), end = "")
        print("|  " + str(table['Absent'][index]), " "*(7 - len(str(table['Absent'][index]))), end = "")
        print("|  " + str(table['Percentage'][index]), " "*(11 - len(str(table['Percentage'][index]))), end = "")
        print("|  ")
    print("|________________________________________________________________________________________________________________________________|")

def main():
    browser = Firefox(executable_path=r"geckodriver.exe")
    browser.get("https://erp.bitmesra.ac.in")
    loginField = browser.find_element_by_name("txt_username")
    username("ENTER USERNAME HERE",loginField)
    passwordField = browser.find_element_by_name("txt_password")
    password("ENTER PASSWORD HERE",passwordField)
    captchaField = browser.find_element_by_name("txtcaptcha")
    captchaSolver(captchaField)
    browser.get("https://erp.bitmesra.ac.in/Academic/iitmsPFkXjz+EbtRodaXHXaPVt3dlW3oTGB+3i1YZ7alodHeRzGm9eTr2C53AU6tMBXuOAm5RgR4bqtOVgfGG9isuhw==?enc=3Q2Y1k5BriJsFcxTY7ebQh0hExMANhAKSl1CmxvOF+Y=")
    soup = bs(browser.page_source,features = "lxml")
    data = createList(soup)
    browser.quit()
    writeCsvFile(r"attendance.csv", data)
    table = createTable(r"attendance.csv")
    printTable(table)

if __name__== "__main__":
    main()
    
