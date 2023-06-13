# -*- coding: utf-8 -*-
# pip install webdriver-manager, pip install selenium
import os
import time
import selenium 
import warnings
import Correo
import pyperclip as clipboard
import sqlite3
import os.path
from datetime import date
from decimal import Decimal
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


#baseDir = u'G:\Otros ordenadores\Mi PC\Plan De Backend\Atenea'
#datosDll = r'C:\Users\O002141\Documents\ATENEA\datos.dll'
datosDll = r'datos.dll'

def ejecucion():
        today = date.today()
        hora_ini = datetime.now().time()
        date_ini= str(today)+' '+str(hora_ini)
        status='IN PROGRESS'
        loadStatusExecution(date_ini, '', status)
        
        try:
            
            print("  -      Run Selenium IDE")
            warnings.simplefilter("ignore")
            options = webdriver.ChromeOptions()
            options.add_argument('log-level=0') #INFO = 0, WARNING = 1, LOG_ERROR = 2, LOG_FATAL = 3.
            options.add_experimental_option('excludeSwitches', ['enable-automation','enable-logging'])
            options.add_argument("--disable-blink-features=AutomationControlled")        
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--remote-debugging-port=9222')
            #options.add_argument('--remote-debugging-port=5900')
            prefs = {"profile.default_content_setting_values.notifications" : 2}    
            options.add_experimental_option("prefs",prefs)
        

            #options.add_argument("--start-maximized")
            options.add_argument("--window-size=1382,744")
            
            errordriver=False
            try:
                #driver = webdriver.Chrome("C:\chromedriver.exe", options=options)    
                driver = webdriver.Remote('http://127.0.0.1:4444/wd/hub',options=options) 
                print("Abrir conexión")    
            except WebDriverException as e:
                errordriver=True
                print("Error al ejecutar el controlador de Chrome: {}".format(str(e)))
            
            if errordriver: 
                driver = webdriver.Chrome(ChromeDriverManager().install())
                driver.get('chrome://version')
                version_element = driver.find_element_by_xpath('/html/body')
                version_text = version_element.text
                version = version_text.split('\n')[0].split(' ')[2]
                print('Versión de Google Chrome:', version)
                
            #driver.delete_all_cookies()
            datos = leerArchivoDll()
                    
            intento=True
            print("- Login Correo")
            contador=0
            while intento:
                            try:
                                driver.implicitly_wait(50)     
                                driver.get("https://globaldevtools.bbva.com/jira/")
                                time.sleep(10)
                                driver.get("https://globaldevtools.bbva.com/jira/")
                                time.sleep(5)
                                #myInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
                                WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH,  '//*[@id="identifierId"]'))).click()
                                print("button clicked")
                                intento = False
                            except:
                                print("\r        - Sleep Charging, retry", end=' ', flush=True)
                                driver.get("https://globaldevtools.bbva.com/jira/")
                                contador=contador+1
                                print("Intento de carga numero:",contador)
                                if contador == 10:
                                    intento = False
                                    print("Pagina No cargada")
                                time.sleep(5)

            print("- Pagina Cargada")
            myInput = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="identifierId"]')))
            myInput.click()
            
            myInput.send_keys(str(datos[2]).replace("\n",""))
            driver.find_element(By.XPATH, '//*[@id="identifierNext"]/div/button').click()
            time.sleep(5)

            print("- Login BBVA")
            f = open ('holamundo.txt','w')
            f.write(driver.page_source)
            f.close()  
            myInputname = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
            myInputname.send_keys(str(datos[0]).replace("\n",""))

            myInputps = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'password')))
            myInputps.click()
            myInputps.clear()
            myInputps.send_keys(str(datos[1]).replace("\n",""))
            time.sleep(2)
            print("- Data user completed")
            time.sleep(5)
            
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="loginForm"]/div[2]/button[1]'))).click()
            time.sleep(5)
            
            if ("Está intentando acceder a los sistemas de BBVA" in driver.page_source or
                "You are trying to access BBVA systems" in driver.page_source):
                    print("- Validacion de Cuenta")
                    # Click para seleccionar correo
                    mySelect = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'presentMail')))
                    mySelect.click()
                    # Click para enviar clave
                    mybtnEnviar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, '_eventId_proceed')))
                    #print(type(mybtnEnviar))
                    mybtnEnviar.click()
                    print("- Click en recibir clave de correo")
                    # Click para colocar clave
                    textClave = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'otp_mail')))
                    textClave.click()
                    time.sleep(10) #agregar llamado de la clase correo y colocar texto
                    codigoVerificacion = Correo.consultarCorreo(datos[2],datos[3])
                    print("- CodigoVerificacion : "+codigoVerificacion)
                    print("- Click para colocar codigo de verificacion")
                    # Click para colocar clave
                    btnValidar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'otp_mail')))
                    btnValidar.send_keys(codigoVerificacion)
                    # Click para enviar clave
                    mybtnEnviar = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, '_eventId_proceed')))
                    mybtnEnviar.click()
                
                    #mybtn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'btn-important')))
                    #mybtn.click()
                    
                    print("- Click para confirmar cuenta")
                    mybtnconf = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')))
                    mybtnconf.click()
                    time.sleep(15)
                    print("- _oauth2_proxy")
                    cookie = driver.get_cookie("_oauth2_proxy")
                    print(cookie)
                    print("- Valor _oauth2_proxy")
                    print(cookie.get('value'))
                    value=cookie.get('value')
                    nameCookie='_oauth2_proxy'
                    time.sleep(20)
                    today = date.today()
                    hora_actual = datetime.now().time()
                    print("hora_actual:",hora_actual)
                    print(str(today))
                    loadCookieToSqlite(nameCookie, value, str(today)+ ' ' +str(hora_actual))
                    
                    
            else:
                print("Error se relanzara")
                hora_fin = datetime.now().time()
                date_fin= str(today)+' '+str(hora_fin)
                status='ERROR'
                loadStatusExecution(date_ini, date_fin, status)
                
            driver.close()
            driver.quit()
            
        except:
            hora_fin = datetime.now().time()
            date_fin= str(today)+' '+str(hora_fin)
            status='ERROR'
            loadStatusExecution(date_ini, date_fin, status)
        
        if status!='ERROR':
            hora_fin = datetime.now().time()
            date_fin= str(today)+' '+str(hora_fin)
            status='FINISHED'
            loadStatusExecution(date_ini, date_fin, status)


def loadCookieToSqlite(nameCookie, value, date):
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_dir = (BASE_DIR + '\\automation.db')
        #db_dir = ('\\\\tsclient\\G\\Otros ordenadores\\Mi PC\\Plan De Backend\\BD_Sqlite\\automation.db')
        sqliteConnection = sqlite3.connect(db_dir)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert = """INSERT INTO COOKIE
                            (NAME, VALUE, DATE)
                            VALUES (?, ?, ? );"""
        data_tuple = (nameCookie, value, date)
        cursor.execute(sqlite_insert, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into Cookie table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table: ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
  

def loadStatusExecution(date_ini, date_fin, status):
    try:
        db_dir = ('./automation.db')
        #db_dir = ('\\\\tsclient\\G\\Otros ordenadores\\Mi PC\\Plan De Backend\\BD_Sqlite\\automation.db')
        sqliteConnection = sqlite3.connect(db_dir)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        sqlite ='';
        data_tuple ='';
        
        if(date_fin == ""):
            sqlite = """INSERT INTO EXECUTIONS_JIRA
                                (DATE_INI, DATE_FIN, STATUS)
                                VALUES (?, ?, ? );"""
            data_tuple = (date_ini, date_fin, status)                                
        else:
            sqlite = """UPDATE EXECUTIONS_JIRA 
                                SET DATE_FIN= ?, STATUS=? 
                                WHERE DATE_INI=?  """
            data_tuple = (date_fin, status, date_ini)  
                                
        
        cursor.execute(sqlite, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into executions jira table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table: ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")

def leerArchivoDll():
    with open(datosDll) as archivoPlano:
        user = archivoPlano.readline()
        psswrd = archivoPlano.readline()
        correo = archivoPlano.readline()
        copssd = archivoPlano.readline()
        return user, psswrd, correo, copssd


def main():
    ejecucion()
    print("- Process end succesfully")
    time.sleep(10)


if __name__=="__main__":
    os.system('cls')
    print("")
    main()