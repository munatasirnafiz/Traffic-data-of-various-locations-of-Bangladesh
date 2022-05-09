from datetime import datetime
import datetime
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time
import xlsxwriter
from tqdm import tqdm
import csv
import pandas as pd
from multiprocessing import Pool
import itertools
import numpy as np
from selenium.common.exceptions import NoSuchElementException 
import threading  
"""      
driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
driver.set_window_size(1024, 768)

driver.get("https://www.google.com.bd/maps/dir/22.796877,91.9109344/22.8351612,91.9127128/@22.8161413,91.8945145,14z/data=!3m1!4b1!4m6!4m5!2m3!6e0!7e2!8j1643734800!3e0?hl=en")
time.sleep(2)

cdt="/data=!4m6!4m5!2m3!6e0!7e2!8j1420131600!3e0?hl=en"
# cc=input("press ENTER to PROCEED.")
# cc=input("press ENTER Again.")
def check_exists_by_css_selector(csss):
    try:
        driver.find_element_by_css_selector(csss)
    except NoSuchElementException:
        return False
    return True


if check_exists_by_css_selector('[aria-label="Agree to the use of cookies and other data for the purposes described"]'):
    driver.find_element_by_css_selector('[aria-label="Agree to the use of cookies and other data for the purposes described"]').click()

# year=input("Write month and year of data: (example-January 2012) : ")

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'sENrwf-YPqjbf')))
driver.find_element_by_class_name('sENrwf-YPqjbf').click()

WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[6]/table/thead/tr/td[1]/button')))

while True:
    driver.find_element_by_xpath('/html/body/div[6]/table/thead/tr/td[1]/button').click()
    datea = driver.find_element_by_class_name('goog-date-picker-monthyear').text
    time.sleep(0.05)
    if year in datea:
        break

cdt1=input("Set the departure time and date in the browser window and Press Enter!")
cdt1=driver.current_url
cdt=cdt1[cdt1.index("/data"):]
date_time_str = input("Write the date of the link in 01/01/12(dd/mm/yy) format for indexing(important): ")
enddate=input("Write the Last date of the link in 01/02/12(dd/mm/yy) format: ")
date_time_end =datetime.datetime.strptime(enddate, '%d/%m/%y')
csvv= input("Output csv name: ")

"""
cdt1="https://www.google.com.bd/maps/dir/22.796877,91.9109344/22.8351612,91.9127128/@22.8161017,91.8945146,14z/data=!3m1!4b1!4m6!4m5!2m3!6e0!7e2!8j1293901200!3e0?hl=en" #2011
cdt=cdt1[cdt1.index("/data"):]
date_time_str = "01/01/11"
enddate="31/12/11"
date_time_end =datetime.datetime.strptime(enddate, '%d/%m/%y')
csvv="2011full"


file2_location=r"adm3_locations_dd.xls"
# uzf = pd.read_excel(file2_location,sheet_name='adm3_locations', usecols="A")
# Uzfname=uzf.values.tolist()
lks = pd.read_excel(file2_location,sheet_name='adm3_locations', usecols="G")
link=lks.values.tolist()
sdll=[]
lln=[]
for i in link:
    ss=str(i)
    ss1=ss[:ss.index("/data")].replace("['","")
    sdll.append(ss1+cdt)
    ltl=ss.replace(ss[:ss.index("dir/")+4],"")
    ltl=ltl[:ltl.index("/@")].replace("/","    ")
    lln.append(ltl)

print("Found " + str(len(sdll))+ " Map Routes")


# driver.close()
sdll1=sdll[0:150]
sdll2=sdll[150:300]
sdll3=sdll[300:450]
sdll4=sdll[450:len(sdll)]

# sdll1=sdll[0:15]
# sdll2=sdll[15:30]
# sdll3=sdll[30:45]
# sdll4=sdll[45:60]

clc=0
value=5.0
##############
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]
##############

def scrapey(sdll_, clc, sdll, lln, date_time_str, csvv): 
    errors=[]
    uk=1
    csvn=csvv+".csv"
    csvoutput= open(csvn, 'w',newline='') 
    writer = csv.writer(csvoutput)
    writer.writerow(["lat lon"]+["link"]+["date"]+["duration"]+["distance"])

    driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
    driver.set_window_size(1024, 768)
    print("Intiating scrapper...")
    for ii in tqdm(range(len(sdll_)),desc=csvv+" "):
      date_time_obj =datetime.datetime.strptime(date_time_str, '%d/%m/%y')
      day_delta = datetime.timedelta(days=1)

      start_date = date_time_obj

      
      try:
        driver.get(sdll_[ii])
      except:
        driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
        driver.set_window_size(1024, 768)
        driver.get(sdll_[ii])
        uk=1
        
      if uk==1:
        try:
          WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Agree to the use of cookies and other data for the purposes described"]')))
          driver.find_element_by_css_selector('[aria-label="Agree to the use of cookies and other data for the purposes described"]').click()
        except:
          print("\n")
        uk=0
        
      lastdate = int(start_date.strftime("%d%m"))
      yyy=int(start_date.strftime("%Y"))
      datereached=0
      while datereached==0:
          donee=0
          tryy=7
          while donee==0 and tryy>0:
              tryy-=1
              if tryy<6:
                print("\nTrial: "+str(tryy)+"\n")
                
              if tryy==5:
                try:
                  WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Agree to the use of cookies and other data for the purposes described"]')))
                  driver.find_element_by_css_selector('[aria-label="Agree to the use of cookies and other data for the purposes described"]').click()
                except:
                  pass



              if tryy<5 and tryy>2:
                try:    
                    driver.get(lastlink)
                    try:
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]')))
                        driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]').click()
                        time.sleep(2)
                    except:
                        try:
                          WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Agree to the use of cookies and other data for the purposes described"]')))
                          driver.find_element_by_css_selector('[aria-label="Agree to the use of cookies and other data for the purposes described"]').click()
                          WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]')))
                          driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]').click()
                        except:
                          pass
                except:
                    print("\n ye dukh kahe khatam nahi hota hai be! :'( \n")
                    
                
              if tryy==2:
                print("CPR for last hope!")
                try:
                    driver.close()
                except:
                    pass
                try:
                    driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
                    driver.set_window_size(1024, 768)
                except:
                    print("\nCan't restart driver!\n")
                
                try:    
                    driver.get(lastlink)
                    try:
                      WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Agree to the use of cookies and other data for the purposes described"]')))
                      driver.find_element_by_css_selector('[aria-label="Agree to the use of cookies and other data for the purposes described"]').click()
                    except:
                      pass
                    try:  
                        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]')))
                        driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]').click()
                        print("Revived!")
                        time.sleep(2)
                    except:
                      pass
                
                except:
                    pass    
                




              if tryy==1:
                try:
                  writer.writerow([lln[sdll.index(sdll_[ii])]] + [driver.current_url] + ["ERROR"] + ["ERROR"] + ["ERROR"] )
                  print("\n"+str([lln[sdll.index(sdll_[ii])]]) +" , "+ str(driver.current_url)+" , " + "ERROR"+" , " + "ERROR" +" , "+ "ERROR"+ "\n")
                  errors.append("\n"+"Error Scraping: "+str(driver.current_url)+"\n")
                  try:
                    driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]').click()

                  except:
                    print(
                        "\nCannot navigate to next date for particular location.Moving to next location!\n"
                    )
                except:
                    writer.writerow([lln[sdll.index(sdll_[ii])]] + [sdll_[ii]] + ["ERROR"] + ["ERROR"] + ["ERROR"] )
                    print("\n"+str([lln[sdll.index(sdll_[ii])]]) +" , "+ str(sdll_[ii]) +" , "+ "ERROR" +" , "+ "ERROR" +" , "+ "ERROR"+ "\n")
                    errors.append("\n"+"Error Scraping: "+str(sdll_[ii])+"\n")
                donee=1
                datereached=1

              try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'xB1mrd-T3iPGc-iSfDt-ij8cu')))
                time.sleep(.3)
                dat_1 = driver.find_element_by_class_name('sENrwf-YPqjbf').text
                dat_1=dat_1[dat_1.index(",")+1:].strip()
                if lastdate==3112:
                    yyy+=1
                fulldat=dat_1+" "+str(yyy)
                try:
                  date_time_obj11 = datetime.datetime.strptime(fulldat, '%d %b %Y')
                except:
                  date_time_obj11 = datetime.datetime.strptime(fulldat, '%b %d %Y')

                time_1 = driver.find_elements_by_class_name('xB1mrd-T3iPGc-iSfDt-n5AaSd')
                tmtt=[]
                dstt=[]
                
                for i in time_1:
                  txt=i.text.replace('\n', ', ')
                  tmtt.append(txt[txt.index("typically")+9:txt.index(",")])
                  dstt.append(float(txt[txt.rindex(",")+1:txt.index("km")]))

                aa=find_nearest(dstt, value)
                ixx=dstt.index(aa)

                date_time = date_time_obj11.strftime("%d/%m/%y")
                lastdate = int(date_time_obj11.strftime("%d%m"))
                
                writer.writerow([lln[sdll.index(sdll_[ii])]] + [driver.current_url] + [date_time] + [tmtt[ixx]] + [dstt[ixx]])
                # print([lln[sdll.index(sdll_[ii])]] + [driver.current_url] + [date_time] + [tmtt[ixx]] + [dstt[ixx]])
                lastlink=driver.current_url
                donee=1

                if date_time_obj11 == date_time_end or date_time_obj11 > date_time_end:
                  datereached=1

                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]')))
                driver.find_element_by_xpath('//*[@id="pane"]/div/div[1]/div/div/div[2]/div[1]/span[2]/span[2]/button[2]').click()
                time.sleep(.2)

                
              
              except:
                print("\n ---x-x-x-x-x-x-x-x-x-x-x-x-x-x--- \n")
                
      
      

    csvoutput.close()
    print(*errors,sep="\n")
    
   

# scrapey(sdll1, clc, sdll, lln, date_time_str, csvv=csvv+"1")

a_thread = threading.Thread(target=scrapey, args=[sdll1, clc, sdll, lln, date_time_str, csvv+"_1"])
b_thread = threading.Thread(target=scrapey, args=[sdll2, clc, sdll, lln, date_time_str, csvv+"_2"])
c_thread = threading.Thread(target=scrapey, args=[sdll3, clc, sdll, lln, date_time_str, csvv+"_3"])
d_thread = threading.Thread(target=scrapey, args=[sdll4, clc, sdll, lln, date_time_str, csvv+"_4"]) 

#a_thread.start()
#b_thread.start()
c_thread.start()
d_thread.start()



# 
