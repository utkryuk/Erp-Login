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
    table = soup.find_all(id = "ctl00_ContentPlaceHolder1_grdExaMarDetl")
    output_rows = []
    heading_row = []
    heading_row.append("CCODE")
    heading_row.append("Course Name")
    heading_row.append("Internal")
    heading_row.append("Midsem")
    heading_row.append("Progressive Evaluation(PE)")
    heading_row.append("Endsemester Evaluation(ES)")
    heading_row.append("Viva")
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

def printTable(fname):
    table = pd.read_csv(fname)
    print(" _________________________________________________________________________________________________________________________________________________")
    print("|    CCODE       | Course Name                         | Internal  | Midsem   | Progressive Evaluation(PE) | Endsemester Evaluation(ES) | Viva    |")
    print("|_________________________________________________________________________________________________________________________________________________|")
    for index in range(len(table)):
        print("|  " + str(table['CCODE'][index]), " "*(13 - len(str(table['CCODE'][index]))) ,end = "")
        print("|  " + table['Course Name'][index], " "*(34 - len(table['Course Name'][index])), end = "")
        print("|  " + str(table['Internal'][index]), " "*(8 - len(str(table['Internal'][index]))), end = "")
        print("|  " + str(table['Midsem'][index]), " "*(7 - len(str(table['Midsem'][index]))), end = "")
        print("|  " + str(table['Progressive Evaluation(PE)'][index]), " "*(25 - len(str(table['Progressive Evaluation(PE)'][index]))), end = "")
        print("|  " + str(table['Endsemester Evaluation(ES)'][index]), " "*(25 - len(str(table['Endsemester Evaluation(ES)'][index]))), end = "")
        print("|  " + str(table['Viva'][index]), " "*(6 - len(str(table['Viva'][index]))), end = "")
        print("|  ")
    print("|_________________________________________________________________________________________________________________________________________________|")

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
    writeCsvFile(r"marks.csv", data)
    browser.quit()
    printTable(r"marks.csv")

if __name__== "__main__":
    main()
