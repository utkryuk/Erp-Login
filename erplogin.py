
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
#opts = Options()
#opts.set_headless()

#assert opts.headless
#browser = Firefox(executable_path=r"C:\Users\Ezone\Downloads\geckodriver.exe", options=opts)

browser = Firefox(executable_path=r"C:\Users\Ezone\Downloads\geckodriver.exe")

#For using Chrome browser
#browser = Chrome(executable_path=r"C:\Users\Ezone\Downloads\chromedriver.exe")


browser.get("https://erp.bitmesra.ac.in")

login_field = browser.find_element_by_name("txt_username")
login_field.clear()
login_field.send_keys("ENTER YOUR USERNAME HERE")

login_field.send_keys(u"\ue004") #unicode for tab key
time.sleep(2)


#get the password textbox
password_field = browser.find_element_by_name("txt_password")
password_field.clear()

#enter password
password_field.send_keys("ENTER YOUR PASSWORD HERE")
password_field.send_keys(u"\ue004") #unicode for tab key
time.sleep(2)




captcha_field = browser.find_element_by_name("txtcaptcha")

captchaText = ImageGrab.grab(bbox = (680,473,790,505)) 

#captchaText.show()


options = pytesseract.image_to_string(captchaText, lang='eng')

captcha_field.send_keys(options)
captcha_field.send_keys(u"\ue007") #unicode for enter key
time.sleep(2)


browser.get("https://erp.bitmesra.ac.in/Academic/iitmsPFkXjz+EbtRodaXHXaPVt3dlW3oTGB+3i1YZ7alodHeRzGm9eTr2C53AU6tMBXuOAm5RgR4bqtOVgfGG9isuhw==?enc=3Q2Y1k5BriJsFcxTY7ebQh0hExMANhAKSl1CmxvOF+Y=")


soup = bs(browser.page_source,features = "lxml")
#soup = bs(source, "html.parser")

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


writeCsvFile(r"data1.csv", output_rows)

t = pd.read_csv(r"data1.csv")


for index in range(len(t['Faculty Name'])):
    t['Faculty Name'][index] = t['Faculty Name'][index].replace("\r\n","")
    t['Faculty Name'][index] = t['Faculty Name'][index].replace("  ","")
    
for index in range(len(t['Course Name'])):
    t['Course Name'][index] = t['Course Name'][index].replace("\r\n","")
    t['Course Name'][index] = t['Course Name'][index].replace("  ","")



t.to_csv("attendance.csv",index = False)

browser.quit()