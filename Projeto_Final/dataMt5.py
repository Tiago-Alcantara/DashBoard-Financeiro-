import pandas as pd
import MetaTrader5 as mt5
import pandas as pd
import datetime
import pytz


def getAllTickers():

    mt5.initialize()

    symbols = mt5.symbols_get()

    tickers = [symbol.name for symbol in symbols]

    tickers = sorted(tickers, reverse=True)

    acoes = []

    for ticker in tickers:
    
        try:
            int(ticker[3]) #a quarta letra tem que ser uma string, não um número
        except:
            
            endTicker = ticker[4:]

            if len(endTicker) == 2:

                if endTicker == "11":

                    if (ticker[0:4] + "3") in acoes or (ticker[0:4] + "4") in acoes:

                        acoes.append(ticker)

            if len(endTicker) == 1:  

                if endTicker == "3" or endTicker == "4":

                    acoes.append(ticker)

    return acoes    


def generateMainList():

    '''
    O vencimento do contrato de dólar acontece no primeiro dia útil de todo mês.
    Já o vencimento do contrato de índice acontece a cada dois meses (somente nos meses pares).
    '''
     
    subtitleIndex = pd.Series([2, 4, 6, 8, 10, 12],
                        index = ['G', 'J', 'M', 'Q', 'V', 'Z'])
    
    subtitleDolar = pd.Series(list(range(1, 13)),
                        index = ['F', 'G', 'H', 'J', 'K', 'M', 'N', 'Q', 'U', 'V', 'X', 'Z'])
    
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month

    if month == 12:

        indexLetter = 'G'
        dolarLetter = 'F'
        indexCode = 'WIN' + indexLetter + str(year + 1)[2:]
        dolarCode = 'WDO' + dolarLetter + str(year + 1)[2:]
    
    else:
         
        indexLetter = (indexLetter[indexLetter > month]).index[0]
        dolarLetter = (dolarLetter[dolarLetter > month]).index[0]

        indexCode = 'WIN' + indexLetter + str(year)[2:]
        dolarCode = 'WDO' + dolarLetter + str(year)[2:]

    tickersFees = ['DI1F' + str(ano_escolhido)[2:] for ano_escolhido in range(year + 1, year + 6)] 

    tickers_mercado = [indexCode, dolarCode, 'SMAL11', 'IVVB11'] + tickersFees

    return tickers_mercado


def selectingTickers():

    acoes = getAllTickers()

    tickersMarket = generateMainList()
    
    tickersTotals = acoes + tickersMarket

    for ticker in tickersTotals:

           mt5.symbol_select(ticker)



def pullingQuotes(tickersSelect, main = False):

    dfQuotes = pd.DataFrame(columns=['Ticker', 'Preço', 'Retorno'], index=list(range(0, len(tickersSelect))))
    # print(mt5.symbol_info(WEGE3).price_change)
    print(mt5.symbol_info('WEGE3').last)

    for i, ticker in enumerate(tickersSelect):
        print(mt5.symbol_info(ticker).session_deals)
        if main == False:

            if mt5.symbol_info(ticker).session_deals > 10:

                retorno = mt5.symbol_info(ticker).price_change
                fechamento = mt5.symbol_info(ticker).last
                print(retorno)
                print(fechamento)
                dfQuotes.loc[i, :] = [ticker, fechamento, retorno]

        else:
             
            retorno = mt5.symbol_info(ticker).price_change
            fechamento = mt5.symbol_info(ticker).last
            print(retorno)
            print(fechamento)
            dfQuotes.loc[i, :] = [ticker, fechamento, retorno]


    print(dfQuotes)
    return dfQuotes


def biggestHighs(tickers_ibov): 
        
        acoes = getAllTickers()

        df = pullingQuotes(acoes)

        df = df[df['Ticker'].isin(tickers_ibov)]

        df = df.sort_values("Retorno", ascending = False)
        df = df.head(3)
        df = df.reset_index(drop = True)

        return df

def lowHighs(tickers_ibov):

        acoes = getAllTickers()

        df = pullingQuotes(acoes)
        
        df = df[df['Ticker'].isin(tickers_ibov)]

        df = df.sort_values("Retorno", ascending = True)
        df = df.head(3)
        df = df.reset_index(drop = True)

        return df


def historicalConstructionQuotes():
    
    acoes = getAllTickers()
    listDataframeQuotes = []
    timezone = pytz.timezone("Brazil/West")
    startDate = (datetime.datetime.now(tz = timezone) - datetime.timedelta(days= 1095))
    endDate = datetime.datetime.now(tz = timezone)

    for acao in acoes:

        try:

            quotes = mt5.copy_rates_range(acao, mt5.TIMEFRAME_D1, startDate, endDate)

            quotes = pd.DataFrame(quotes)
            
            quotes = quotes[['time', 'open', 'high', 'low', 'close']]
            quotes['time']= pd.to_datetime(quotes['time'], unit='s')
            quotes['ticker'] = acao

        except:
             
             print(acao)

        listDataframeQuotes.append(quotes)

    finalQuotes = pd.concat(listDataframeQuotes)

    companies = finalQuotes['ticker'].unique()

    dataframeCompanies = pd.DataFrame({'tickers': companies})

    dataframeCompanies.to_csv('tickers.csv', index = False)
    finalQuotes.to_parquet("cotacoes.parquet", index = False) 



if __name__ == "__main__":

    historicalConstructionQuotes()

























