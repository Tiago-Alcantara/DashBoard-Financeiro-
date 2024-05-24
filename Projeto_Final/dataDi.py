import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time 
import datetime
import plotly.graph_objects as go
from selenium.common.exceptions import NoSuchElementException



def webScrapingDi():

    today = datetime.datetime.now()
    oneYearAgo = today - datetime.timedelta(days=365)
    threeYearAgo = today - datetime.timedelta(days=365 * 3)
    fiveYearAgo = today - datetime.timedelta(days=365 * 5)
    tenYearAgo = today - datetime.timedelta(days=365 * 10)

    listDates = [today,oneYearAgo,threeYearAgo,fiveYearAgo,tenYearAgo]

    listNames = ["Today","One year ago","Three year ago","Five year ago","Ten year ago"]

    subtitle = pd.Series(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                        index = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z'])
    
    listDataFrames = []

    for n,date in enumerate(listDates):

        options = Options()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        dateNow = date

        for i in range(0,5):

            dateTest = dateNow.strftime("%d/%m/%Y")

            url = f'''https://www2.bmf.com.br/pages/portal/bmfbovespa/boletim1/SistemaPregao1.asp?
                        pagetype=pop&caminho=Resumo%20Estat%EDstico%20-%20Sistema%20Preg%E3o&Data={dateTest}
                        &Mercadoria=DI1'''

            try:
                table,index = getDataDi(url,driver)
                break
            except NoSuchElementException:
                dateNow = dateNow - datetime.timedelta(days= 1)
        driver.quit()

        dataDi = processingDataDi(table,index,subtitle)

        dataDi = dataDi.reset_index()
        dataDi.colluns= ["Due date","Price"]
        dataDi["Price Date"] = listNames[n]

        listDataFrames.append(dataDi)
    dataDi = pd.concat(listDataFrames, ignore_index=True)
    
    # Salva os dados que chegaram em um csv
    dataDi.to_csv("dados_di.csv", index = False)

    return dataDi


def getDataDi(url, driver):
        
        isConnection = True
        
        while isConnection:
            try:
                driver.get(url)
                isConnection = False
            except:
                pass
                
        time.sleep(3)

        localTable = '''

        /html/body/form[1]/table[3]/tbody/tr[3]/td[3]/table
        '''

        localIndex = '''
        /html/body/form[1]/table[3]/tbody/tr[3]/td[1]
        '''

        element = driver.find_element("xpath", localTable)

        elementIndex = driver.find_element("xpath", localIndex)

        htmlTable = element.get_attribute('outerHTML')
        htmlIndex = elementIndex.get_attribute('outerHTML')

        

        table = pd.read_html(htmlTable)[0]
        index = pd.read_html(htmlIndex)[0]

        return table, index

def processingDataDi(dfData, index, subtitle):
        
    dfData.columns = dfData.loc[0]

    dfData = dfData['ÚLT. PREÇO']

    dfData = dfData.drop(0, axis = 0)

    index.columns = index.loc[0]

    index = index.drop(0, axis = 0)
    
    dfData.index = index['VENCTO']
    
    dfData = dfData.astype(int)

    dfData = dfData[dfData != 0]

    df = dfData/1000

    listDates = []

    for index in df.index:

        character = index[0]
        year = index[1:3]

        month = subtitle[character]

        data = f"{month}-{year}"

        data = datetime.datetime.strptime(data, "%b-%y")

        listDates.append(data)
        
    df.index = listDates  

    df = df/100
        
    return df 

    
if __name__ == "__main__":

    dataDi = webScrapingDi()
    print(dataDi)
