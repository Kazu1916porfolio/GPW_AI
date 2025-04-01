from sqlalchemy import create_engine
import pandas as pd
import numpy as np


def srawdza_czy_wzrost(symb, df, listDFF,listAKT):
    dftemp = df[df['symbol'] == symb]

    Aktualnyokres_wiersz = dftemp['Unnamed: 0'].max() + 1
    Poprzedniokres_wiersz = dftemp['Unnamed: 0'].max()
    dftemp.loc[Aktualnyokres_wiersz] = dftemp.loc[Poprzedniokres_wiersz].copy()

    dftemp.loc[Aktualnyokres_wiersz,'okres'] = 'AKT'
    dftemp.loc[Aktualnyokres_wiersz,'symbol'] = dftemp.loc[Poprzedniokres_wiersz,'symbol']

    dftemp.loc[Aktualnyokres_wiersz,'kapitalizacja'] = dftemp.loc[Poprzedniokres_wiersz,'Liczba akcji']*dftemp.loc[Poprzedniokres_wiersz,'cena akt']

    # dftemp = dftemp.drop(columns=['symbol', 'okres'])
    # print(dftemp)
    dfFinal = pd.DataFrame()
    dfFinalAKT=pd.DataFrame()
    lista_column = dftemp.columns
    print(symb)

    colselect = ['Przychody ze sprzedaży',
                 'Zysk ze sprzedaży','Zysk operacyjny (EBIT)','Zysk z działalności gospodarczej','Zysk przed opodatkowaniem','Zysk netto'
                 ,'Zysk netto akcjonariuszy jednostki dominującej','Aktywa trwałe','Aktywa obrotowe','Aktywa razem','Kapitał własny akcjonariuszy jednostki dominującej',
                 'Zobowiązania długoterminowe','Zobowiązania krótkoterminowe','Pasywa razem','Przepływy pieniężne z działalności operacyjnej','Przepływy pieniężne z działalności inwestycyjnej','Przepływy pieniężne z działalności finansowej',
                 'Przepływy pieniężne razem']
    for col in lista_column:
        try:
            if col == 'okres' or col == 'symbol' or col == 'kapitalizacja' or col == 'Kurs' or col == 'cena akt' or col == 'średnia ważona' or col == 'CFD' or col == 'STOCH_RSI':
                # print(dftemp[col])
                dfFinal[col] = dftemp[col]
            if col in colselect:
                if col.find('na akcję') != -1:
                    dfFinal[col] = (dftemp[col]*1000)/dftemp['kapitalizacja']

                else:
                    dfFinal[col] = (dftemp[col]*1000)/dftemp['kapitalizacja']
                    dfFinal[col + 'proc'] = round(((dftemp[col] - dftemp[col].shift(1)) / dftemp[col]), 4)
                    dfFinal[col + 'procROK'] = round(((dftemp[col] - dftemp[col].shift(4)) / dftemp[col]), 4)
                    dfFinal[col + 'procROK2'] = round(((dftemp[col] - dftemp[col].shift(8)) / dftemp[col]), 4)
        except:
            ""
    dfFinal['wzrost'] = np.where(dftemp['kapitalizacja'].shift(-1) > dftemp['kapitalizacja'], 1, 0)


    # dfFinal = dfFinal.drop(columns=['Liczba akcji','Kurs'])
    listDFF.append(dfFinal)


    #### aktualny kurs
    for col in lista_column:

        if col == 'okres' or col == 'symbol' or col == 'kapitalizacja':
            # print(dftemp[col])
            dfFinalAKT[col] = dftemp[col]
        if col in colselect:
            if col.find('na akcję') != -1:
                dfFinalAKT[col] = (dftemp[col]*1000)/dftemp['kapitalizacja']

            else:
                dfFinalAKT[col] = (dftemp[col]*1000)/dftemp['kapitalizacja']
                dfFinalAKT[col + 'proc'] = round(((dftemp[col] - dftemp[col].shift(1)) / dftemp[col]), 4)
                dfFinalAKT[col + 'procROK'] = round(((dftemp[col] - dftemp[col].shift(4)) / dftemp[col]), 4)
                dfFinalAKT[col + 'procROK2'] = round(((dftemp[col] - dftemp[col].shift(8)) / dftemp[col]), 4)

    # dfFinal['wzrost'] = dfFinal['kapitalizacja'].apply(lambda x: 1 if x > 0 else 0)

    dfFinalAKT['wzrost'] = np.where(dftemp['kapitalizacja'].shift(-1) > dftemp['kapitalizacja'], 1, 0)

    # dfFinal = dfFinal.drop(columns=['Liczba akcji','Kurs'])
    listAKT.append(dfFinalAKT)

    return listDFF,listAKT





def Bilans_do_sieci_neur():
    listDFF = []
    listAKT=[]
    dfFinalFull = pd.DataFrame()
    engine = create_engine('sqlite:///GPW3.db', echo=True)
    sqlite_connection = engine.connect()
    # df33=pd.read_csv('GPW2.csv')
    # df33.to_sql('RaportyGPW_biznesradar_WSK', sqlite_connection, if_exists='replace',
    #                                index=False)
    df1 = pd.read_sql_query(
        "SELECT a.*,c.'Liczba akcji',c.kurs,d.'cena akt' FROM RaportyGPW_biznesradar_Bilans_only4 as a left join RaportyGPW_biznesradar_wskazniki as c on a.symbol=c.symbol and a.okres=c.okres left join RaportyGPW_Cenyy as d on a.symbol=d.symbol",
        sqlite_connection)
    print(df1)
    df1.to_csv('gpwtemp.csv')
    df1=pd.read_csv('gpwtemp.csv')

    df1 = df1.drop_duplicates(['symbol', 'okres'])
    print(df1)

    print(df1.columns)


    df1 = df1.loc[:, ~df1.columns.duplicated()].copy()
    df1 = df1.drop(columns=['liczba akcji2'])
    df1 = df1.apply(pd.to_numeric, downcast='integer', errors='ignore')

    df1=df1.dropna(subset=['Liczba akcji'])


    df1['Kurs']=df1['Kurs'].apply(lambda x: float(str(x).replace(",",".")))
    df1['cena akt']=df1['cena akt'].apply(lambda x: None if x is None else  float(str(x).replace(",",".").replace(" ",'')))
    df1=df1[df1['Kurs'] != 0]
    df1['kapitalizacja'] = df1.apply(lambda x: x['Liczba akcji'] * float(str(x['Kurs']).replace(",",".")), axis=1)

    df_unikalne = df1.drop_duplicates(subset=['symbol'], keep='last')
    df_unikalne['wzrost'] = df_unikalne.apply(lambda x: srawdza_czy_wzrost(x['symbol'], df1, listDFF,listAKT), axis=1)

    result = pd.concat(listDFF)
    result = result.drop_duplicates()

    resultAKT = pd.concat(listAKT)
    resultAKT = resultAKT.drop_duplicates()


    colselect=['Przychody ze sprzedaży',
           'Techniczny koszt wytworzenia produkcji sprzedanej', 'Koszty sprzedaży',
           'Koszty ogólnego zarządu', 'Zysk ze sprzedaży',
           'Pozostałe przychody operacyjne', 'Pozostałe koszty operacyjne',
           'Zysk operacyjny (EBIT)', 'Przychody finansowe', 'Koszty finansowe',
           'Pozostałe przychody (koszty)', 'Zysk z działalności gospodarczej',
            'Zysk przed opodatkowaniem',
           'Zysk (strata) netto z działalności zaniechanej', 'Zysk netto',
           'Zysk netto akcjonariuszy jednostki dominującej',
           'Aktywa trwałe', 'Wartości niematerialne i prawne',
           'Rzeczowe składniki majątku trwałego',
            'Należności długoterminowe',
           'Inwestycje długoterminowe', 'Pozostałe aktywa trwałe',
           'Aktywa obrotowe', 'Zapasy', 'Należności krótkoterminowe',
           'Inwestycje krótkoterminowe',
           'Środki pieniężne i inne aktywa pieniężne',
           'Aktywa trwałe przeznaczone do sprzedaży', 'Aktywa razem',
           'Kapitał własny akcjonariuszy jednostki dominującej',
           'Kapitał (fundusz) podstawowy',
           'Kapitał (fundusz) zapasowy', 'Udziały niekontrolujące',
           'Zobowiązania długoterminowe', 'Z tytułu dostaw i usług',
           'Kredyty i pożyczki', 'Z tytułu emisji dłużnych papierów wartościowych',

           'Inne zobowiązania długoterminowe', 'Zobowiązania krótkoterminowe',
           'Inne zobowiązania krótkoterminowe', 'Rozliczenia międzyokresowe',
           'Pasywa razem', 'Przepływy pieniężne z działalności operacyjnej',
           'Amortyzacja', 'Przepływy pieniężne z działalności inwestycyjnej',

           'Przepływy pieniężne z działalności finansowej',

           'Przepływy pieniężne razem']
    colselect = ['Przychody ze sprzedaży',
                     'Zysk ze sprzedaży','Zysk operacyjny (EBIT)','Zysk z działalności gospodarczej','Zysk przed opodatkowaniem','Zysk netto'
                     ,'Zysk netto akcjonariuszy jednostki dominującej','Aktywa trwałe','Aktywa obrotowe','Aktywa razem','Kapitał własny akcjonariuszy jednostki dominującej',
                     'Zobowiązania długoterminowe','Zobowiązania krótkoterminowe','Pasywa razem','Przepływy pieniężne z działalności operacyjnej','Przepływy pieniężne z działalności inwestycyjnej','Przepływy pieniężne z działalności finansowej',
                     'Przepływy pieniężne razem']
    result=result.fillna(0)
    listaCol=result.columns

    resultAKT=resultAKT.fillna(0)
    listaCol=resultAKT.columns
    result.replace([np.inf, -np.inf], np.nan, inplace=True)
    for col in listaCol:
        if col in colselect or col.find('proc') != -1:
            #print(result[col])
            try:
                result[col] = pd.qcut(result[col], q=10, duplicates='drop')

                #print(result[col])
            except:
                result.drop(columns=[col])
    # result.to_csv('maszynoweBilansOnlyV2.csv')
    result.to_excel('maszynoweBilansOnlyV2.xlsx')
    print(result)

