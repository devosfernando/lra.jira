# -*- coding: utf-8 -*-
# pip install webdriver-manager, pip install selenium
import os
import time
import selenium 
import warnings
import Correo
import os.path
import mysql.connector
from datetime import date
from datetime import datetime
from selenium.webdriver.support.wait import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from dotenv import load_dotenv

#baseDir = u'G:\Otros ordenadores\Mi PC\Plan De Backend\Atenea'
#datosDll = r'C:\Users\O002141\Documents\ATENEA\datos.dll'
datosDll = r'datos.dll'

# Cargar las variables de entorno del archivo .env
load_dotenv()

def ejecucion():
        today = date.today()
        hora_ini = datetime.now().time()
        #date_ini= str(today)+' '+str(hora_ini)
        date_ini = time.strftime('%Y-%m-%d %H:%M:%S')
        status = 'IN PROGRESS'
        loadStatusExecution(str(date_ini), '', status)
        
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
            print("Conexión a el driver de chrome") 
            try:
                #driver = webdriver.Chrome("C:\chromedriver.exe", options=options)    
                driver = webdriver.Remote('http://localhost:4444/wd/hub',options=options) 
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
                
                    print("- Click para confirmar cuenta")
                    mybtnconf = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')))
                    mybtnconf.click()
                    time.sleep(20)
                    print("-Obtener Cookie _oauth2_proxy")
                    cookie = driver.get_cookie("_oauth2_proxy")
                    print(cookie)
                    print("- Valor _oauth2_proxy")
                    print(cookie.get('value'))
                    value=cookie.get('value')
                    nameCookie='_oauth2_proxy'
                    #time.sleep(20)
                    today = date.today()
                    hora_actual = datetime.now().time()
                    fecha_actual = time.strftime('%Y-%m-%d %H:%M:%S')
                    print("fecha_actual:",fecha_actual)
                    loadCookieToSqlite(nameCookie, value,str(fecha_actual))
                    
            else:
                print("Error se relanzara no cargo correctamente la pagina")
                status='ERROR PAGINA'
                
            driver.close()
            driver.quit()
            status='FINISHED'
            print("Finaliza Correctamente")
            
        except Exception as e:
            status='ERROR GENERAL'
            print("Se produjo un error:", e)
            print("Error generico")
        finally:
            #hora_fin = datetime.now().time()
            #date_fin= str(today)+' '+str(hora_fin)
            date_fin = time.strftime('%Y-%m-%d %H:%M:%S')
            loadStatusExecution(date_ini, date_fin, status)
            print("Update Status Executions")

def conexion():
    print ("---Conection Database---")
    db = mysql.connector.connect(host=os.getenv("host_mysql"),
                                    port=os.getenv("port_mysql"),
                                    user=os.getenv("user_mysql"), 
                                    password=os.getenv("pass_mysql"), 
                                    database=os.getenv("bd_mysql"),
                                    auth_plugin=os.getenv("ath_mysql"))
    return db  

def loadCookieToSqlite(nameCookie, value, date):
    try:
        conn = conexion()
        cursor = conn.cursor()       
        print("Connected to BD")

        sqlite_insert = ("INSERT INTO automation.cookie"
                          "  (NAME, VALUE, DATE_CREATE)"
                           " VALUES (%s, %s, %s ) ")
        data_tuple = (nameCookie, value, date)
        cursor.execute(sqlite_insert, data_tuple)
        conn.commit()
        #sqliteConnection.commit()
        print(cursor.rowcount, "record inserted into Cookie table")
        #print("Python Variables inserted successfully into Cookie table")
    except mysql.connector.Error as err: 
        print(" ERROR: INSERT COOKIE: {}".format(err)) 
        conn.rollback()
    finally:
        cursor.close() 
        conn.close()
  

def loadStatusExecution(date_ini, date_fin, status):
    try:
        conn = conexion()
        cursor = conn.cursor()       
        print("Connected to BD")

        sqlite ='';
        data_tuple ='';
        print(str(date_ini))
        
        if(date_fin == ""):
            sqlite = ("INSERT INTO automation.executions_jira "
                            " (DATE_INI, DATE_FIN, STATUS) "
                             "   VALUES (%s,null,%s) ")
            data_tuple = (str(date_ini), status)                                
        else:
            sqlite = ("UPDATE automation.executions_jira "
                             "   SET DATE_FIN= %s, STATUS= %s "
                              "  WHERE DATE_INI= %s  ")
            data_tuple = (str(date_fin), status, str(date_ini))  
                                
        cursor.execute(sqlite, data_tuple)
        conn.commit()
        print("Python Variables inserted successfully into executions jira table")
    except mysql.connector.Error as err:
        print("Failed to INSERT/UPDATE: {}".format(err))
        conn.rollback()
    finally:
        cursor.close()
        if conn:
            conn.close()
            print("The SQL connection is closed")

def leerArchivoDll():
    
    """ with open(datosDll) as archivoPlano:
        user = archivoPlano.readline()
        psswrd = archivoPlano.readline()
        correo = archivoPlano.readline()
        copssd = archivoPlano.readline()"""
    user = os.getenv("usuario")
    psswrd = os.getenv("usuario_ps")
    correo = os.getenv("correo")
    copssd = os.getenv("imap")
    return user, psswrd, correo, copssd


def main():
    ejecucion()
    print("- Process end succesfully")
    time.sleep(10)


if __name__=="__main__":
    os.system('cls')
    print("")
    main()