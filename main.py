import time
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

import os
############################## pip install webdriver-manager descarga la ultima vercion del driver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))

##########################################
#DRIVER_PATH = 'C:\driver\chromedriver'
#driver = webdriver.Chrome(executable_path=DRIVER_PATH)
# driver.get('https://google.com/')
driver.get('https://portal.channelsight.com/')

email = driver.find_element(By.ID, "i0116")
email.send_keys("cs_pm_operador5@salamancasolutions.com")
time.sleep(5)
email.send_keys(Keys.ENTER)

passwd = driver.find_element(By.ID, "i0118")
passwd.send_keys("#CS2022viva")  # CS2022viva
passwd.send_keys(Keys.ENTER)
time.sleep(5)

signIn = driver.find_element(By.ID, "idSIButton9").click()  #################
time.sleep(5)

###########################################################
driver.execute_script("window.open('');")
time.sleep(2)
driver.switch_to.window(driver.window_handles[1])
driver.get("https://portal.channelsight.com/Administration/SKUCorrectionLog")
time.sleep(2)
btn_burger = driver.find_element(By.XPATH, '//*[@id="minimalizeLinkNavbarId"]/i').click()
###########################################################
selectionuser = driver.find_element(By.XPATH, '//*[@id="userSelector_chosen"]')
selectionuser.click()
user = driver.find_element(By.XPATH, '//*[@id="userSelector_chosen"]/ul/li/input')
user.send_keys('Operator 4')
user.send_keys(Keys.ENTER)
time.sleep(2)

select_manufactured = driver.find_element(By.XPATH, '//*[@id="manufacturerSelector_chosen"]')
select_manufactured.click()
manufactured = driver.find_element(By.XPATH, '//*[@id="manufacturerSelector_chosen"]/div/div/input')
manufactured.send_keys('All')
manufactured.send_keys(Keys.ENTER)
time.sleep(2)

Select_retailer = driver.find_element(By.XPATH, '//*[@id="retailerSelector_chosen"]')
Select_retailer.click()
retailer = driver.find_element(By.XPATH, '//*[@id="retailerSelector_chosen"]/div/div/input')
retailer.send_keys('All')
retailer.send_keys(Keys.ENTER)
time.sleep(2)

'''datee = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[2]/div/div/div/div[1]/div/div[2]/div[5]/div')
datee.click
dateee = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/div[2]/div/div/div/div[1]/div/div[2]/div[5]/div/span/span')
dateee.send_keys('10/10/22')
dateee.send_keys(Keys.ENTER)
time.sleep(20)
#########################################################  
# time.sleep(20)'''
flag = False
print("configura o introduce los parametros en panel CS, los campos que puedes configurar son las siguientes:")
print("Users, Manufacturer, Brand, Retailer, From date, To date")
while not flag:
    option = input("Introduce \"yes\" o \"y\" para continuiar o \"q\" para salir: ")
    if (option == "yes" or option == "y"):
        flag = True
    elif (option == "s"):
        driver.quit()
        exit()

###########################################################
aggregationMode_chosen = driver.find_element(By.ID, 'aggregationMode_chosen')
aggregationMode_chosen.click()
chosen_nothing = driver.find_element(By.XPATH, '//*[@id="aggregationMode_chosen"]/div/div/input')
chosen_nothing.send_keys('Nothing')
chosen_nothing.send_keys(Keys.ENTER)

limit = 250  # 20,50,100,250
logLimit_chosen = driver.find_element(By.ID, 'logLimit_chosen')
logLimit_chosen.click()
logLimit = driver.find_element(By.XPATH, '//*[@id="logLimit_chosen"]/div/div/input')
logLimit.send_keys(limit)
logLimit.send_keys(Keys.ENTER)

searchLogs = driver.find_element(By.ID, 'searchLogs')
searchLogs.click()
time.sleep(15)  # 15
###########################################################
itemsFrom = driver.find_element(By.ID, 'itemsFrom')
itemsFrom = itemsFrom.text
itemsTo = driver.find_element(By.ID, 'itemsTo')
itemsTo = itemsTo.text
itemsOutOf = driver.find_element(By.ID, 'itemsOutOf')
itemsOutOf = itemsOutOf.text
print(itemsFrom)
print(itemsTo)
print(itemsOutOf)

if (itemsTo == "-" or itemsOutOf == "-"):
    print(" no hay operaciones a mostrar")
    driver.quit()
    exit()

items_partial = int(itemsTo)
items_total = int(itemsOutOf)
list_products = list()
print('--------------start----------------')
while (items_partial <= items_total):
    products = driver.find_elements(By.CLASS_NAME, 'product-container')
    for product in products:
        list_products.append(product.text)
        # print(list_products.text)
    print(items_partial, "cargado")

    next_button = driver.find_element(By.ID, 'btnNextItems').click()
    time.sleep(15)  # 15
    if (items_partial == items_total):
        print(items_partial, "finalizado")
        break
    items_partial = int(driver.find_element(By.ID, 'itemsTo').text)

# for list_product in list_products:
# print(list_products)
print("numero total de items cargados", len(list_products))
driver.quit()
##########################################
titles = list()
manufactures = list()
retailers = list()
matches = list()
links = list()
ops = list()
date_ops = list()
for list_product in list_products:
    list_product = str(list_product).split('\n')
    # print(list_product) # imprime la lista
    # print(len(list_product))
    if len(list_product) == 6:  # caso no match
        list_product.insert(3, 'no-code')
    if len(list_product) == 5:  # caso search cat.
        list_product.insert(3, 'no-link')
        list_product.insert(2, 'no-retailers')

    titles.append(list_product[0])
    manufactures.append(list_product[1])
    retailers.append(list_product[2])
    matches.append(list_product[3])
    links.append(list_product[4])
    ops.append(list_product[5])
    date_ops.append(list_product[6])
#####################################################
driver.quit()

df = pd.DataFrame({'title': titles, 'manufacturer':manufactures, 'retailer':retailers, 'code':matches, 'link':links, 'operation':ops, 'date_ops': date_ops } )
print(df)
now = datetime.now().strftime('%d_%m_%Y')
#namecsv=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
df.to_csv(now + '.csv')
'''
##############################################
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
name2drive = namecsv + ".csv"
upload_file_list = [name2drive]
for upload_file in upload_file_list:
    gfile = drive.CreateFile({'parents': [{'id': '1hHpAo_ozmmrwbPA4H1tPUYeuVcEQwXgm'}]})
    # Read file and set it as the content of this instance.
    gfile.SetContentFile(upload_file)
    gfile.Upload()  # Upload the file

file_list = drive.ListFile(
    {'q': "'{}' in parents and trashed=false".format('1hHpAo_ozmmrwbPA4H1tPUYeuVcEQwXgm')}).GetList()
for file in file_list:
    fileID = file['id']
    print('title: %s, id: %s, %s' % (
    file['title'], file['id'], "https://drive.google.com/file/d/" + fileID + "/view?usp=sharing"))
###########################################################
try:
    os.remove(name2drive)
    print("csv removido")
except OSError as e:
    print(f"Error:{e.strerror}")'''
