import requests
from bs4 import BeautifulSoup
import pandas as pd

from sqlalchemy import create_engine,text
from Preparing_data_for_neural_network_Indicators import Wskazniki_do_sieci_neur,srawdza_czy_wzrost
from Preparing_data_for_neural_network_Balance import Bilans_do_sieci_neur,srawdza_czy_wzrost

from datetime import datetime, timedelta
def pobieranie_danych_biznesradar_WSK(listaSymboliGPW):


    for hh in listaSymboliGPW:
        frames=[]
        symbol = []
        kapitalizacja=[]
        OkresList = []
        OkresList_wskazniki = []
        symbol_wskazniki = []
        kapitalizacja_wskazniki = []
        frames_wskazniki = []

        hh=hh.split(".")[0]
        url = "https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/" + hh +',Q'
        print(hh)
        request_response = requests.get(url)
        url = request_response.url
        if url.find(',Q') != -1:
            request_response = requests.get(url)

        else:
            request_response = requests.get(url + ',Q')

        request_data = request_response.text
        soup = BeautifulSoup(request_data, "lxml")

        ### kapitalizacja ###

        for i in soup.find_all("table", {"class": "profileSummary"}):
            for g in i.find_all("td"):

                if str(g).find('Akcjonariat') != -1:
                    kapit=int(g.text.replace(" ","").replace("\n",""))



        for book_items in soup.find_all("table", {"class": "report-table"}):
            #print(book_items)

            ### okres ###
            for i in book_items.find_all("th", {"class": "thq h"}, {"class": "thq h newest"}):
                thname = i.text.replace(" ", "")
                miesiac = i.find("span").text
                thname = thname.replace(" ", "").replace(miesiac, "").replace("\n", "")
                thname = thname.replace(" ", "").replace(miesiac, "").replace("\t", "")

                OkresList.append(thname)
                Swiezynka = soup.find("th", {"class": "thq h newest"}).text.replace(" ", "").replace(miesiac,"").replace("\t","")
                Swiezynka = Swiezynka.replace("\n", "")
                #print(Swiezynka)

                OkresList.append(Swiezynka)
                symbol.append(hh)
                kapitalizacja.append(kapit)
                OkresList = list(dict.fromkeys(OkresList))


            symbol.append(hh)
            liiiist = {'symbol': symbol}
            dff = pd.DataFrame(liiiist)
            frames.append(dff)

            liiiist = {'okres': OkresList}
            dff = pd.DataFrame(liiiist)
            dff=dff.sort_values(by=['okres'])
            dff = dff.reset_index(drop=True)

            frames.append(dff)

            kapitalizacja.append(kapit)
            liiiist = {'liczba akcji2': kapitalizacja}
            dff = pd.DataFrame(liiiist)
            frames.append(dff)


            for cc in book_items.find_all("tr"):
                Nagllowki_2=[]

                try:

                    naglName=cc.find("td", {"class": "f"}).text

                    for g in cc.find_all("span", {"class": "value"}):

                        if g.find("span", {"class": "pv"}) != None:
                            IncomeRevenues = g.find("span").text.replace(" ", "")
                            Nagllowki_2.append(IncomeRevenues)
                            #print(IncomeRevenues)
                        else:
                            Nagllowki_2.append("NULL")
                    liiiist = {naglName:Nagllowki_2}
                    dff=pd.DataFrame(liiiist)
                    frames.append(dff)



                except:
                    ""
        #### wskazniki ###
        url3 = "https://www.biznesradar.pl/wskazniki-plynnosci/" + hh

        request_response = requests.get(url3)
        url3 = request_response.url

        request_data = request_response.text
        soup3 = BeautifulSoup(request_data, "lxml")

        for i in soup3.find_all("th", {"class": "thq h"}, {"class": "thq h newest"}):
            thname = i.text.replace(" ", "")
            miesiac = i.find("span").text
            thname = thname.replace(" ", "").replace(miesiac, "").replace("\n", "")
            thname = thname.replace(" ", "").replace(miesiac, "").replace("\t", "")


            OkresList_wskazniki.append(thname)
            Swiezynka = soup.find("th", {"class": "thq h newest"}).text.replace(" ", "").replace(miesiac, "").replace(
                "\t", "")
            Swiezynka = Swiezynka.replace("\n", "")
            # print(Swiezynka)

            OkresList_wskazniki.append(Swiezynka)
            symbol_wskazniki.append(hh)

            OkresList_wskazniki = list(dict.fromkeys(OkresList_wskazniki))

        symbol_wskazniki.append(hh)
        liiiist = {'symbol': symbol_wskazniki}
        dff = pd.DataFrame(liiiist)
        frames_wskazniki.append(dff)

        liiiist = {'okres': OkresList_wskazniki}
        dff = pd.DataFrame(liiiist)
        dff = dff.sort_values(by=['okres'])
        dff = dff.reset_index(drop=True)

        frames_wskazniki.append(dff)



        for cc in soup3.find_all("tr"):
            Nagllowki_2 = []

            try:

                naglName = cc.find("td", {"class": "f"}).text

                for g in cc.find_all("span", {"class": "value"}):

                    if g.find("span", {"class": "pv"}) != None:
                        IncomeRevenues = g.find("span").text.replace(" ", "")
                        Nagllowki_2.append(IncomeRevenues)
                        # print(IncomeRevenues)
                    else:
                        Nagllowki_2.append("NULL")
                liiiist = {naglName: Nagllowki_2}

                dff = pd.DataFrame(liiiist)
                frames_wskazniki.append(dff)
            except:
                ""
        ### aktywnosci ###
        url3 = "https://www.biznesradar.pl/wskazniki-aktywnosci/" + hh

        request_response = requests.get(url3)
        url3 = request_response.url

        request_data = request_response.text
        soup3 = BeautifulSoup(request_data, "lxml")




        for cc in soup3.find_all("tr"):
            Nagllowki_2 = []

            try:

                naglName = cc.find("td", {"class": "f"}).text

                for g in cc.find_all("span", {"class": "value"}):

                    if g.find("span", {"class": "pv"}) != None:
                        IncomeRevenues = g.find("span").text.replace(" ", "")
                        Nagllowki_2.append(IncomeRevenues)
                        # print(IncomeRevenues)
                    else:
                        Nagllowki_2.append("NULL")
                liiiist = {naglName: Nagllowki_2}

                dff = pd.DataFrame(liiiist)
                frames_wskazniki.append(dff)
            except:
                ""

        ### zadluzenia ###
        url3 = "https://www.biznesradar.pl/wskazniki-zadluzenia/" + hh

        request_response = requests.get(url3)
        url3 = request_response.url

        request_data = request_response.text
        soup3 = BeautifulSoup(request_data, "lxml")




        for cc in soup3.find_all("tr"):
            Nagllowki_2 = []

            try:

                naglName = cc.find("td", {"class": "f"}).text

                for g in cc.find_all("span", {"class": "value"}):

                    if g.find("span", {"class": "pv"}) != None:
                        IncomeRevenues = g.find("span").text.replace(" ", "")
                        Nagllowki_2.append(IncomeRevenues)
                        # print(IncomeRevenues)
                    else:
                        Nagllowki_2.append("NULL")
                liiiist = {naglName: Nagllowki_2}

                dff = pd.DataFrame(liiiist)
                frames_wskazniki.append(dff)
            except:
                ""
        ### przelplyw ###
        url3 = "https://www.biznesradar.pl/wskazniki-przeplywow-pienieznych/" + hh

        request_response = requests.get(url3)
        url3 = request_response.url

        request_data = request_response.text
        soup3 = BeautifulSoup(request_data, "lxml")
        for cc in soup3.find_all("tr"):
            Nagllowki_2 = []

            try:

                naglName = cc.find("td", {"class": "f"}).text

                for g in cc.find_all("span", {"class": "value"}):

                    if g.find("span", {"class": "pv"}) != None:
                        IncomeRevenues = g.find("span").text.replace(" ", "")
                        Nagllowki_2.append(IncomeRevenues)
                        # print(IncomeRevenues)
                    else:
                        Nagllowki_2.append("NULL")
                liiiist = {naglName: Nagllowki_2}

                dff = pd.DataFrame(liiiist)
                frames_wskazniki.append(dff)
            except:
                ""

        ### wskazniki-rentownosci ###
        url3 = "https://www.biznesradar.pl/wskazniki-rentownosci/" + hh

        request_response = requests.get(url3)
        url3 = request_response.url

        request_data = request_response.text
        soup3 = BeautifulSoup(request_data, "lxml")
        for cc in soup3.find_all("tr"):
            Nagllowki_2 = []

            try:

                naglName = cc.find("td", {"class": "f"}).text

                for g in cc.find_all("span", {"class": "value"}):

                    if g.find("span", {"class": "pv"}) != None:
                        IncomeRevenues = g.find("span").text.replace(" ", "")
                        Nagllowki_2.append(IncomeRevenues)
                        # print(IncomeRevenues)
                    else:
                        Nagllowki_2.append("NULL")
                liiiist = {naglName: Nagllowki_2}

                dff = pd.DataFrame(liiiist)
                frames_wskazniki.append(dff)
            except:
                ""

        ### wskazniki-wartosci-rynkowej ###
        url3 = "https://www.biznesradar.pl/wskazniki-wartosci-rynkowej/" + hh

        request_response = requests.get(url3)
        url3 = request_response.url

        request_data = request_response.text
        soup3 = BeautifulSoup(request_data, "lxml")
        for cc in soup3.find_all("tr"):
            Nagllowki_2 = []

            try:

                naglName = cc.find("td", {"class": "f"}).text

                for g in cc.find_all("span", {"class": "value"}):

                    if g.find("span", {"class": "pv"}) != None:
                        IncomeRevenues = g.find("span").text.replace(" ", "")
                        Nagllowki_2.append(IncomeRevenues)
                        # print(IncomeRevenues)
                    else:
                        Nagllowki_2.append("NULL")
                liiiist = {naglName: Nagllowki_2}

                dff = pd.DataFrame(liiiist)
                frames_wskazniki.append(dff)
            except:
                ""





        if len(OkresList) > 0:
            result = pd.concat(frames,axis=1)


            ### dodawanie do tebeli
            engine = create_engine('sqlite:///GPW3.db', echo=True)
            sqlite_connection = engine.connect()
            try:
                result.to_sql('RaportyGPW_biznesradar_Bilans', sqlite_connection, if_exists='append',
                               index=False)
            except:
                result.to_sql('RaportyGPW_biznesradar_Bilans_Banki', sqlite_connection, if_exists='append',
                              index=False)


        if len(OkresList) > 0:
            result = pd.concat(frames_wskazniki,axis=1)

            ### dodawanie do tebeli
            engine = create_engine('sqlite:///GPW3.db', echo=True)
            sqlite_connection = engine.connect()
            try:
                result.to_sql('RaportyGPW_biznesradar_wskazniki', sqlite_connection, if_exists='append',
                               index=False)
            except:
                result.to_sql('RaportyGPW_biznesradar_wskazniki_Banki', sqlite_connection, if_exists='append',
                              index=False)




def pobieranie_danych_biznesradar(listaSymboliGPW):


    for hh in listaSymboliGPW:
        frames=[]
        symbol = []
        kapitalizacja=[]
        OkresList = []
        OkresList_wskazniki = []
        symbol_wskazniki = []
        kapitalizacja_wskazniki = []
        frames_wskazniki = []

        hh=hh.split(".")[0]
        url = "https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/" + hh +',Q'
        print(hh)
        request_response = requests.get(url)
        url = request_response.url
        if url.find(',Q') != -1:
            request_response = requests.get(url)

        else:
            request_response = requests.get(url + ',Q')

        request_data = request_response.text
        soup = BeautifulSoup(request_data, "lxml")

        ### kapitalizacja ###

        for i in soup.find_all("table", {"class": "profileSummary"}):
            for g in i.find_all("td"):

                if str(g).find('Akcjonariat') != -1:
                    kapit=int(g.text.replace(" ","").replace("\n",""))



        for book_items in soup.find_all("table", {"class": "report-table"}):
            #print(book_items)

            ### okres ###
            for i in book_items.find_all("th", {"class": "thq h"}, {"class": "thq h newest"}):
                thname = i.text.replace(" ", "")
                miesiac = i.find("span").text
                thname = thname.replace(" ", "").replace(miesiac, "").replace("\n", "")
                thname = thname.replace(" ", "").replace(miesiac, "").replace("\t", "")

                OkresList.append(thname)
                Swiezynka = soup.find("th", {"class": "thq h newest"}).text.replace(" ", "").replace(miesiac,"").replace("\t","")
                Swiezynka = Swiezynka.replace("\n", "")
                #print(Swiezynka)

                OkresList.append(Swiezynka)
                symbol.append(hh)
                kapitalizacja.append(kapit)
                OkresList = list(dict.fromkeys(OkresList))


            symbol.append(hh)
            liiiist = {'symbol': symbol}
            dff = pd.DataFrame(liiiist)
            frames.append(dff)

            liiiist = {'okres': OkresList}
            dff = pd.DataFrame(liiiist)
            dff=dff.sort_values(by=['okres'])
            dff = dff.reset_index(drop=True)

            frames.append(dff)

            kapitalizacja.append(kapit)
            liiiist = {'liczba akcji2': kapitalizacja}
            dff = pd.DataFrame(liiiist)
            frames.append(dff)


            for cc in book_items.find_all("tr"):
                Nagllowki_2=[]

                try:

                    naglName=cc.find("td", {"class": "f"}).text

                    for g in cc.find_all("span", {"class": "value"}):

                        if g.find("span", {"class": "pv"}) != None:
                            IncomeRevenues = g.find("span").text.replace(" ", "")
                            Nagllowki_2.append(IncomeRevenues)
                            #print(IncomeRevenues)
                        else:
                            Nagllowki_2.append("NULL")
                    liiiist = {naglName:Nagllowki_2}
                    dff=pd.DataFrame(liiiist)
                    frames.append(dff)



                except:
                    ""

        hh = hh.split(".")[0]
        url = "https://www.biznesradar.pl/raporty-finansowe-bilans/" + hh + ',Q'
        print(hh)
        request_response = requests.get(url)
        url = request_response.url
        if url.find(',Q') != -1:
            request_response = requests.get(url)

        else:
            request_response = requests.get(url + ',Q')

        request_data = request_response.text
        soup = BeautifulSoup(request_data, "lxml")
        for book_items in soup.find_all("table", {"class": "report-table"}):
            #print(book_items)



            for cc in book_items.find_all("tr"):
                Nagllowki_2=[]

                try:

                    naglName=cc.find("td", {"class": "f"}).text

                    for g in cc.find_all("span", {"class": "value"}):

                        if g.find("span", {"class": "pv"}) != None:
                            IncomeRevenues = g.find("span").text.replace(" ", "")
                            Nagllowki_2.append(IncomeRevenues)
                            #print(IncomeRevenues)
                        else:
                            Nagllowki_2.append("NULL")
                    liiiist = {naglName:Nagllowki_2}
                    dff=pd.DataFrame(liiiist)
                    frames.append(dff)



                except:
                    ""
        hh = hh.split(".")[0]
        url = "https://www.biznesradar.pl/raporty-finansowe-przeplywy-pieniezne/" + hh + ',Q'
        print(hh)
        request_response = requests.get(url)
        url = request_response.url
        if url.find(',Q') != -1:
            request_response = requests.get(url)

        else:
            request_response = requests.get(url + ',Q')

        request_data = request_response.text
        soup = BeautifulSoup(request_data, "lxml")
        for book_items in soup.find_all("table", {"class": "report-table"}):
            # print(book_items)

            for cc in book_items.find_all("tr"):
                Nagllowki_2 = []

                try:

                    naglName = cc.find("td", {"class": "f"}).text

                    for g in cc.find_all("span", {"class": "value"}):

                        if g.find("span", {"class": "pv"}) != None:
                            IncomeRevenues = g.find("span").text.replace(" ", "")
                            Nagllowki_2.append(IncomeRevenues)
                            # print(IncomeRevenues)
                        else:
                            Nagllowki_2.append("NULL")
                    liiiist = {naglName: Nagllowki_2}
                    dff = pd.DataFrame(liiiist)
                    frames.append(dff)



                except:
                    ""




        if len(OkresList) > 0:
            result = pd.concat(frames,axis=1)
            cols_to_keep = []
            cols_to_drop = []
            for i, col in enumerate(result.columns):
                if col not in cols_to_keep:
                    cols_to_keep.append(col)
                else:
                    cols_to_drop.append(col)

            # Usuń duplikaty kolumn
            result = result.drop(columns=cols_to_drop, errors='ignore')
            ### dodawanie do tebeli
            engine = create_engine('sqlite:///GPW3.db', echo=True)
            sqlite_connection = engine.connect()
            print(result.columns)
            try:
                result.to_sql('RaportyGPW_biznesradar_Bilans_only4', sqlite_connection, if_exists='append',
                               index=False)
            except:
                result.to_sql('RaportyGPW_biznesradar_Bilans_Banki_only4', sqlite_connection, if_exists='append',
                              index=False)

            print(result)


def pobieraniecen():
    symbollist = []
    cenalist = []

    url = 'https://www.biznesradar.pl/gielda/akcje_gpw'

    request_response = requests.get(url)
    url = request_response.url

    request_data = request_response.text
    soup = BeautifulSoup(request_data, "lxml")

    for i in soup.find_all("td"):

        for cc in i.find_all("a"):
            symbollist.append(cc.text[0:3])
        for ww in i.find_all("span", {"data-push-type": "QuoteClose"}):
            cenalist.append(ww.text.replace(',', '.'))

    url = 'https://www.biznesradar.pl/gielda/newconnect'

    request_response = requests.get(url)
    url = request_response.url

    request_data = request_response.text
    soup = BeautifulSoup(request_data, "lxml")

    for i in soup.find_all("td"):

        for cc in i.find_all("a"):
            symbollist.append(cc.text[0:3])
        for ww in i.find_all("span", {"data-push-type": "QuoteClose"}):
            cenalist.append(ww.text.replace(',', '.'))

    cccc = {'symbol': symbollist, 'cena akt': cenalist}
    dff = pd.DataFrame(cccc)
    dff.to_excel('cenyakt.xlsx')
    engine = create_engine('sqlite:///GPW3.db', echo=True)
    sqlite_connection = engine.connect()
    dff.to_sql('RaportyGPW_Cenyy', sqlite_connection, if_exists='replace',
                               index=False)


def bilansonly():
    try:
        engine = create_engine('sqlite:///GPW3.db', echo=True)
        sqlite_connection = engine.connect()
        dfSQL = pd.read_sql_query(
            "SELECT * FROM RaportyGPW_biznesradar_Bilans_only4",sqlite_connection)
        print(dfSQL.columns)
        dfSQL['symb_okres']=dfSQL['symbol'] + dfSQL['okres'].str[0:7]
        listaNaj_raport=dfSQL['symb_okres'].to_list()

        s1=pd.read_html('https://www.biznesradar.pl/spolki-raporty-finansowe-rachunek-zyskow-i-strat/akcje_gpw')[0]
        s2=pd.read_html('https://www.biznesradar.pl/spolki-raporty-finansowe-rachunek-zyskow-i-strat/newconnect')[0]
        df=pd.concat([s1, s2])
        df['Profil']=df['Profil'].apply(lambda x: str(x)[0:3])
        df['symb_okres']=df['Profil'] + df['Raport']
        print(df)


        df['czy_jest_raport']=df['symb_okres'].apply(lambda x: 1 if x in listaNaj_raport else 0)
        print(df[df['czy_jest_raport']==0])
        df=df[df['czy_jest_raport']==0]
    except:
        ### brak tabeli ###
        s1 = pd.read_html('https://www.biznesradar.pl/spolki-raporty-finansowe-rachunek-zyskow-i-strat/akcje_gpw')[0]
        s2 = pd.read_html('https://www.biznesradar.pl/spolki-raporty-finansowe-rachunek-zyskow-i-strat/newconnect')[0]
        df = pd.concat([s1, s2])
        df['Profil'] = df['Profil'].apply(lambda x: str(x)[0:3])

    ListaSymboliGPW=df['Profil'].to_list()
    pobieranie_danych_biznesradar(ListaSymboliGPW)

def bilansonly_WSK():
    try:
        engine = create_engine('sqlite:///GPW3.db', echo=True)
        sqlite_connection = engine.connect()
        dfSQL = pd.read_sql_query(
            "SELECT * FROM RaportyGPW_biznesradar_wskazniki",sqlite_connection)
        print(dfSQL.columns)
        dfSQL['symb_okres']=dfSQL['symbol'] + dfSQL['okres'].str[0:7]
        listaNaj_raport=dfSQL['symb_okres'].to_list()

        s1=pd.read_html('https://www.biznesradar.pl/spolki-raporty-finansowe-rachunek-zyskow-i-strat/akcje_gpw')[0]
        s2=pd.read_html('https://www.biznesradar.pl/spolki-raporty-finansowe-rachunek-zyskow-i-strat/newconnect')[0]
        df=pd.concat([s1, s2])
        df['Profil']=df['Profil'].apply(lambda x: str(x)[0:3])
        df['symb_okres']=df['Profil'] + df['Raport']
        print(df)


        df['czy_jest_raport']=df['symb_okres'].apply(lambda x: 1 if x in listaNaj_raport else 0)
        print(df[df['czy_jest_raport']==0])
        df=df[df['czy_jest_raport']==0]
    except:
        ## brak tabeli ##
        s1 = pd.read_html('https://www.biznesradar.pl/spolki-raporty-finansowe-rachunek-zyskow-i-strat/akcje_gpw')[0]
        s2 = pd.read_html('https://www.biznesradar.pl/spolki-raporty-finansowe-rachunek-zyskow-i-strat/newconnect')[0]
        df = pd.concat([s1, s2])
        df['Profil'] = df['Profil'].apply(lambda x: str(x)[0:3])

    ListaSymboliGPW=df['Profil'].to_list()
    pobieranie_danych_biznesradar_WSK(ListaSymboliGPW)

bilansonly()
bilansonly_WSK()
pobieraniecen()
Wskazniki_do_sieci_neur()
Bilans_do_sieci_neur()