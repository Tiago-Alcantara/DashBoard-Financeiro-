import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from datetime import date
import zipfile
import os


def sectorsMarket(pathDownload):

    options = Options()
    options.headless = False

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = 'https://www.b3.com.br/data/files/57/E6/AA/A1/68C7781064456178AC094EA8/ClassifSetorial.zip'

    driver.get(url)


    time.sleep(5)

    driver.quit()

    arquivo_zip = zipfile.ZipFile(pathDownload + r"\ClassifSetorial.zip")

    for sheet in arquivo_zip.namelist():

        sectors = pd.read_excel(arquivo_zip.open(sheet), skiprows=6)

    arquivo_zip.close()

    sectors['SUBSETOR'] = sectors['SUBSETOR'].ffill()

    sectors = sectors.dropna(subset = ['SEGMENTO'])

    sectors = sectors[['SUBSETOR', 'SEGMENTO', 'LISTAGEM']]

    sectors = sectors.dropna()

    sectors.columns = ['SETOR', 'NOME', 'TICKER']

    os.remove(pathDownload + r"\ClassifSetorial.zip")
    print(sectors)
    sectors.to_csv("setores.csv", index = False) 


def compositionIbov(pathDownload):

    options = Options()
    options.headless = False

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    url = 'https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/indice-ibovespa-ibovespa-composicao-da-carteira.htm'

    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.frame_to_be_available_and_switch_to_it((By.ID, "bvmf_iframe")))
    
    time.sleep(3)

    sheet = driver.find_element("xpath", '//*[@id="divContainerIframeB3"]/div/div[1]/form/div[2]/div/div[2]/div/div/div[1]/div[2]/p/a')

    driver.execute_script("arguments[0].click();", sheet)

    time.sleep(5)

    driver.quit()

    day = date.today().day
    month = date.today().month
    year = date.today().year

    if day < 10:
        
        day = "0" + str(day)

    if month < 10:
        
        month = "0" + str(month)
        
    year = str(year)[2:]

    ibovespa_comp = pd.read_csv(pathDownload + fr"\IBOVDia_{day}-{month}-{year}.csv", sep = ";", 
                            skipfooter = 2, encoding = 'ISO-8859-1', engine = 'python', decimal = ',',
                           thousands = ".", header = 1, index_col = False)
    
    
    os.remove(pathDownload + fr"\IBOVDia_{day}-{month}-{year}.csv")

    ibovespa_comp.columns = ['codigos', 'nome', 'classe', 'qtd', 'part']
    
    ibovespa_comp.to_csv("comp_ibov.csv", index = False)


if __name__ == "__main__":
    pathDownload = r'C:\Users\Tiago\Downloads'
    sectorsMarket(pathDownload)

    compositionIbov(pathDownload)























