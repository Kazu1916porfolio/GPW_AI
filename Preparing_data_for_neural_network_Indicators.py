from sqlalchemy import create_engine
import pandas as pd
import numpy as np


def srawdza_czy_wzrost(symb, df, listDFF,listAKT):
    dftemp = df[df['symbol'] == symb]

    # dftemp = dftemp.drop(columns=['symbol', 'okres'])

    ### kopiowanie ostatniego wiersza ###
    #print(dftemp)
    Aktualnyokres_wiersz=dftemp['Unnamed: 0'].max()+1
    Poprzedniokres_wiersz = dftemp['Unnamed: 0'].max()
    dftemp.loc[Aktualnyokres_wiersz] = dftemp.loc[Poprzedniokres_wiersz].copy()
    #print(dftemp)

    dfFinal = pd.DataFrame()
    dfFinalAKT=pd.DataFrame()
    lista_column = dftemp.columns
    print(symb)
    colselect=['Wartość księgowa na akcję','Wartość księgowa Grahama na akcję','Przychody ze sprzedaży na akcję','Zysk na akcję','Zysk operacyjny na akcję','Enterprise Value na akcję','ROE','ROA'
               ,'Udział zysku netto w przepływach operacyjnych','Zadłużenie ogólne','Płynność podwyższona','Płynność bieżąca']
    for col in lista_column:

        if col == 'okres' or col == 'symbol' or col == 'kapitalizacja':
            # print(dftemp[col])
            dfFinal[col] = dftemp[col]
        if col in colselect:
            if col.find('na akcję') != -1:
                try:

                    dfFinal[col] = dftemp[col]/dftemp['Kurs']
                except:
                    # print(dftemp[col])
                    # print(dftemp['Kurs'])
                    dfFinal[col] = dftemp[col].fillna(0)
                    dfFinal[col] = dftemp[col] / dftemp['Kurs']
            else:
                dfFinal[col] = dftemp[col]
            dfFinal[col + 'proc'] = round(((dftemp[col] - dftemp[col].shift(1)) / dftemp[col]), 4)
            dfFinal[col + 'procROK'] = round(((dftemp[col] - dftemp[col].shift(4)) / dftemp[col]), 4)
            dfFinal[col + 'procROK2'] = round(((dftemp[col] - dftemp[col].shift(8)) / dftemp[col]), 4)

    ### aktualna cena ####
    for col in lista_column:

        if col == 'okres':
            # print(dftemp[col])
            dfFinal.loc[Aktualnyokres_wiersz,'okres'] = 'AKT'
        if col == 'symbol':
            # print(dftemp[col])
            dfFinal.loc[Aktualnyokres_wiersz,'symbol'] = dfFinal.loc[Poprzedniokres_wiersz,'symbol']
        if col == 'kapitalizacja':
            # print(dftemp[col])
            dfFinal.loc[Aktualnyokres_wiersz,'kapitalizacja'] = dftemp.loc[Poprzedniokres_wiersz,'Liczba akcji']*dftemp.loc[Poprzedniokres_wiersz,'cena akt']

        if col in colselect:
            if col.find('na akcję') != -1:
                dfFinal.loc[Aktualnyokres_wiersz,col] = dftemp.loc[Poprzedniokres_wiersz,col]/dftemp.loc[Poprzedniokres_wiersz,'cena akt']

            else:
                dfFinal.loc[Aktualnyokres_wiersz,col] = dftemp.loc[Poprzedniokres_wiersz,col]
            try:
                dfFinal.loc[Aktualnyokres_wiersz, col + 'proc']=round(((dftemp.loc[Poprzedniokres_wiersz,col] - dftemp.loc[Poprzedniokres_wiersz-1,col]) / dftemp.loc[Poprzedniokres_wiersz,col]), 4)
            except:
                dfFinal.loc[Aktualnyokres_wiersz, col + 'proc']=0
            try:
                dfFinal.loc[Aktualnyokres_wiersz, col + 'procROK'] =round(((dftemp.loc[Poprzedniokres_wiersz,col] - dftemp.loc[Poprzedniokres_wiersz-4,col]) / dftemp.loc[Poprzedniokres_wiersz,col]), 4)
            except:
                dfFinal.loc[Aktualnyokres_wiersz, col + 'procROK'] =0
            try:
                dfFinal.loc[Aktualnyokres_wiersz, col + 'procROK2'] = round(((dftemp.loc[Poprzedniokres_wiersz, col] -dftemp.loc[Poprzedniokres_wiersz - 8, col]) /dftemp.loc[Poprzedniokres_wiersz, col]), 4)
            except:
                dfFinal.loc[Aktualnyokres_wiersz, col + 'procROK2'] = 0
            #dfFinal[col + 'proc'] = round(((dftemp[col] - dftemp[col].shift(1)) / dftemp[col]), 4)
            #dfFinal[col + 'procROK'] = round(((dftemp[col] - dftemp[col].shift(4)) / dftemp[col]), 4)
            #dfFinal[col + 'procROK2'] = round(((dftemp[col] - dftemp[col].shift(8)) / dftemp[col]), 4)

    # dfFinal['wzrost'] = dfFinal['kapitalizacja'].apply(lambda x: 1 if x > 0 else 0)


    dfFinal['wzrost'] = np.where(dftemp['kapitalizacja'].shift(-1) > dftemp['kapitalizacja'], 1, 0)
    #print(dfFinal)

    # dfFinal = dfFinal.drop(columns=['Liczba akcji','Kurs'])
    listDFF.append(dfFinal)


    #### aktualny kurs
    for col in lista_column:
        try:
            if col == 'okres' or col == 'symbol' or col == 'kapitalizacja':
                # print(dftemp[col])
                dfFinalAKT[col] = dftemp[col]
            if col in colselect:
                if col.find('na akcję') != -1:
                    dfFinalAKT[col] = dftemp[col] / dftemp['cena akt']

                else:
                    dfFinalAKT[col] = dftemp[col]
                dfFinalAKT[col + 'proc'] = round(((dftemp[col] - dftemp[col].shift(1)) / dftemp[col]), 4)
                dfFinalAKT[col + 'procROK'] = round(((dftemp[col] - dftemp[col].shift(4)) / dftemp[col]), 4)
                dfFinalAKT[col + 'procROK2'] = round(((dftemp[col] - dftemp[col].shift(8)) / dftemp[col]), 4)
        except:
            ""
    # dfFinal['wzrost'] = dfFinal['kapitalizacja'].apply(lambda x: 1 if x > 0 else 0)

    dfFinalAKT['wzrost'] = np.where(dftemp['kapitalizacja'].shift(-1) > dftemp['kapitalizacja'], 1, 0)

    # dfFinal = dfFinal.drop(columns=['Liczba akcji','Kurs'])
    listAKT.append(dfFinalAKT)

    return listDFF,listAKT





def Wskazniki_do_sieci_neur():
    listDFF = []
    listAKT=[]
    dfFinalFull = pd.DataFrame()
    engine = create_engine('sqlite:///GPW3.db', echo=True)
    sqlite_connection = engine.connect()
    df1 = pd.read_sql_query(
        "SELECT * FROM RaportyGPW_biznesradar_Bilans as a left join RaportyGPW_biznesradar_wskazniki as c on a.symbol=c.symbol and a.okres=c.okres left join RaportyGPW_Cenyy as d on a.symbol=d.symbol",
        sqlite_connection)
    #df1=pd.read_csv('GPW2.csv')
    df1 = df1.drop_duplicates(['symbol', 'okres'])

    print(df1['liczba akcji2'])
    print(df1['Liczba akcji'])
    print(df1.columns)
    df1=df1.dropna(subset=['Liczba akcji'])

    df1 = df1.loc[:, ~df1.columns.duplicated()].copy()
    df1 = df1.drop(columns=['liczba akcji2', 'Data publikacji'])
    df1 = df1.apply(pd.to_numeric, downcast='integer', errors='ignore')


    colselect=['Wartość księgowa na akcję','Wartość księgowa Grahama na akcję','Przychody ze sprzedaży na akcję','Zysk na akcję','Zysk operacyjny na akcję','Enterprise Value na akcję','ROE','ROA'
                   ,'Udział zysku netto w przepływach operacyjnych','Zadłużenie ogólne','Płynność podwyższona','Płynność bieżąca']

    for col in colselect:
        print(col)
        df1[col] = df1[col].apply(lambda x: None if x is None else float(str(x).replace(',','.').replace('%', '')))

    df1['Kurs']=df1['Kurs'].apply(lambda x: float(str(x).replace(",",".")))
    df1['cena akt']=df1['cena akt'].apply(lambda x:  None if x is None else   float(str(x).replace(",",".").replace(" ",'')))
    df1=df1[df1['Kurs'] != 0]
    df1['kapitalizacja'] = df1.apply(lambda x: x['Liczba akcji'] * float(str(x['Kurs']).replace(",",".")), axis=1)

    df_unikalne = df1.drop_duplicates(subset=['symbol'], keep='last')
    df_unikalne['Unnamed: 0']=df_unikalne.index
    df1['Unnamed: 0']=df1.index
    df_unikalne['wzrost'] = df_unikalne.apply(lambda x: srawdza_czy_wzrost(x['symbol'], df1, listDFF,listAKT), axis=1)

    result = pd.concat(listDFF)
    result = result.drop_duplicates()

    resultAKT = pd.concat(listAKT)
    resultAKT = resultAKT.drop_duplicates()


    colselect=['Wartość księgowa na akcję','Wartość księgowa Grahama na akcję','Przychody ze sprzedaży na akcję','Zysk na akcję','Zysk operacyjny na akcję','Enterprise Value na akcję','ROE','ROA'
                   ,'Udział zysku netto w przepływach operacyjnych','Zadłużenie ogólne','Płynność podwyższona','Płynność bieżąca']

    result=result.fillna(0)
    listaCol=result.columns

    resultAKT=resultAKT.fillna(0)
    listaCol=resultAKT.columns
    result.replace([np.inf, -np.inf], np.nan, inplace=True)
    for col in listaCol:
        if col in colselect or col.find('proc') != -1:
            print(result[col])
            try:
                result[col] = pd.qcut(result[col], q=10, duplicates='drop')

                print(result[col])
            except:
                result.drop(columns=[col])
    # result.to_csv('maszynowe16.csv')
    result.to_excel('maszynowe16.xlsx')

    print(result)
