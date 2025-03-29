# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df2=pd.read_excel('/content/drive/MyDrive/maszynoweBilansOnlyV2.xlsx', index_col=False)
df2['wzrost'] = np.where(df2['symbol'].shift(-1) == df2['symbol'], (df2['kapitalizacja'].shift(-1)-df2['kapitalizacja'])/df2['kapitalizacja'].shift(-1), 9999)
df2['wzrost2'] = np.where(df2['wzrost'] > 0.05,1,0)
df2['wzrost3'] = np.where(df2['wzrost'] < -0.10,1,0)
df2['wzrost'] = np.where(df2['wzrost'] > 0.19,1,0)


print(df2.columns)

df=df2.drop(columns=['okres','symbol','Unnamed: 0','kapitalizacja','wzrost2','wzrost3','Kurs','cena akt'])
for col in df.columns:

  #print(x[col].value_counts())
  df=pd.get_dummies(df, columns=[col],drop_first=True)
print(df.shape)



x= df.drop(columns=['wzrost_1'])
#x=x.loc[~(x==0).all(axis=1)]
#print(x)

y= df['wzrost_1']

from keras.models import load_model

model = load_model('/content/drive/MyDrive/Bilans_spadek_03_02_2025.keras')

model.summary()

wagilist=model.get_weights()

print(wagilist[0])

# dfWagi=pd.DataFrame(wagilist[0])
# dfWagi.to_excel('/content/drive/MyDrive/wagi.xlsx')

# lll=dfAKT.drop(columns=['wzrost_1'])
# lll=lll.columns
# lll=pd.DataFrame(lll)
# lll.to_excel('/content/drive/MyDrive/kolumny.xlsx')
# print(lll)


prediction = model.predict(df.drop(columns=['wzrost_1']))
#prediction = model.predict(df.drop(columns=['wzrost_1']))
#prediction = model.predict(x_test)

symbolList=df2['symbol'].to_list()
okresList=df2['okres'].to_list()
listaIDX=df2.index.to_list()
listaIDX=df2.index.to_list()
c=0
ilosc_prawd=0
ilosc_prawd_5_proc=0
minus_10_procc=0
www=0
ggg=0

### raport ###

DFraport=pd.DataFrame(df2['symbol'].unique() )
DFraport=DFraport.set_index(0)

for x in prediction:
  symbol=df2.loc[listaIDX[c],'symbol']
  if df2.loc[listaIDX[c],'okres'].find('wrz24') !=-1 or df2.loc[listaIDX[c],'okres'].find('paź24') !=-1:

      DFraport.loc[symbol,'symbol']=df2.loc[listaIDX[c],'symbol']
      DFraport.loc[symbol,'okresPoprzedni']= df2.loc[listaIDX[c],'okres']
      DFraport.loc[symbol,'poprzedniKwartalSpadek_bilans']=  round(x[0],2)
  if df2.loc[listaIDX[c],'okres'].find('gru24') !=-1 or df2.loc[listaIDX[c],'okres'].find('sty25') !=-1:
      DFraport.loc[symbol,'symbol']=df2.loc[listaIDX[c],'symbol']
      DFraport.loc[symbol,'okresAktualny']= df2.loc[listaIDX[c],'okres']
      DFraport.loc[symbol,'AktualnyKwartalSpadek_bilans']=  round(x[0],2)
  if df2.loc[listaIDX[c],'okres'].find('AKT') !=-1:
      DFraport.loc[symbol,'symbol']=df2.loc[listaIDX[c],'symbol']
      DFraport.loc[symbol,'okresAktualny_spadek_CENA_Bilans']= df2.loc[listaIDX[c],'okres']
      DFraport.loc[symbol,'AktualnyKwartal_Spadek_CENA_Bilans']=  round(x[0],2)
      DFraport.loc[symbol,'Kurs']=   df2.loc[listaIDX[c],'Kurs']
      DFraport.loc[symbol,'cena akt']=  df2.loc[listaIDX[c],'cena akt']

      # DFraport.loc[symbol,'średnia ważona']=   df2.loc[listaIDX[c],'średnia ważona']
      # #DFraport.loc[symbol,'STOCH_RSI']=  df2.loc[listaIDX[c],'STOCH_RSI']
      # DFraport.loc[symbol,'CFD']=  df2.loc[listaIDX[c],'CFD']
  #if str(round(x[0],2)) == '0.12':
  if x[0] > 0.3:
    www=www+1
    if str(df2.loc[listaIDX[c],'wzrost']) == '1':
      ilosc_prawd=ilosc_prawd+1
    if str(df2.loc[listaIDX[c],'wzrost2']) == '1':
      ilosc_prawd_5_proc=ilosc_prawd_5_proc+1
    if str(df2.loc[listaIDX[c],'wzrost3']) == '1':
      minus_10_procc=minus_10_procc+1
  if str(df2.loc[listaIDX[c],'wzrost']) == '1':
    ggg=ggg+1
  c=c+1





print(DFraport)
DFraport.to_excel('/content/drive/MyDrive/raportSpadekBilans.xlsx')
print(ilosc_prawd)
print(www)
print('procent + 20%')
print((ilosc_prawd/www)*100)
print('procent + 5%')
print((ilosc_prawd_5_proc/www)*100)
print('procent <> -10%')
print((minus_10_procc/www)*100)
print('procent + 20% w test')
print((ilosc_prawd/ggg)*100)

from keras.models import load_model

model = load_model('/content/drive/MyDrive/Bilans_wzrost_03_02_2025.keras')

model.summary()

wagilist=model.get_weights()

print(wagilist[0])

dfWagi=pd.DataFrame(wagilist[0])
dfWagi['srednia']=dfWagi.mean(axis=1)
dfWagi=dfWagi.sort_values(by='srednia',ascending=False)
#dfWagi.to_excel('/content/drive/MyDrive/wagiMAKRO_EKO.xlsx')

lll=df.drop(columns=['wzrost_1'])
lll=lll.columns
lll=pd.DataFrame(lll)
#lll.to_excel('/content/drive/MyDrive/kolumnyMAKRO_EKO.xlsx')
print(lll)

dfWagi['kolumny']=lll
dfWagi=dfWagi[['kolumny','srednia']]
# dfWagi.to_excel('/content/drive/MyDrive/wagiMAKRO_EKO.xlsx')

#

# dfWagi=pd.DataFrame(wagilist[0])
# dfWagi.to_excel('/content/drive/MyDrive/wagi.xlsx')

# lll=dfAKT.drop(columns=['wzrost_1'])
# lll=lll.columns
# lll=pd.DataFrame(lll)
# lll.to_excel('/content/drive/MyDrive/kolumny.xlsx')
# print(lll)

#prediction = model.predict(dfAKT.drop(columns=['wzrost_1']))
prediction = model.predict(df.drop(columns=['wzrost_1']))
#prediction = model.predict(x_test)

symbolList=df2['symbol'].to_list()
okresList=df2['okres'].to_list()
listaIDX=df2.index.to_list()
listaIDX=df2.index.to_list()
c=0
ilosc_prawd=0
ilosc_prawd_5_proc=0
minus_10_procc=0
www=0
ggg=0

### raport ###


for x in prediction:
  symbol=df2.loc[listaIDX[c],'symbol']
  if df2.loc[listaIDX[c],'okres'].find('wrz24') !=-1 or df2.loc[listaIDX[c],'okres'].find('paź24') !=-1:

      DFraport.loc[symbol,'symbol']=df2.loc[listaIDX[c],'symbol']
      DFraport.loc[symbol,'okresPoprzedniBilans']= df2.loc[listaIDX[c],'okres']
      DFraport.loc[symbol,'poprzedniKwartalWzrostBilans']=  round(x[0],2)
  if df2.loc[listaIDX[c],'okres'].find('gru24') !=-1 or df2.loc[listaIDX[c],'okres'].find('sty25') !=-1:
      DFraport.loc[symbol,'symbol']=df2.loc[listaIDX[c],'symbol']
      DFraport.loc[symbol,'okresAktualnyBilans']= df2.loc[listaIDX[c],'okres']
      DFraport.loc[symbol,'AktualnyKwartalWzrostBilans']=  round(x[0],2)

  if df2.loc[listaIDX[c],'okres'].find('AKT') !=-1:
      DFraport.loc[symbol,'symbol']=df2.loc[listaIDX[c],'symbol']
      DFraport.loc[symbol,'okresAktualnyCENA_Bilans']= df2.loc[listaIDX[c],'okres']
      DFraport.loc[symbol,'AktualnyKwartalWzrostCENA_Bilans']=  round(x[0],2)
  #if str(round(x[0],2)) == '0.12':
  if x[0] > 0.4:
    if df2.loc[listaIDX[c],'okres'].find('wrz24') !=-1 or df2.loc[listaIDX[c],'okres'].find('paź24') !=-1:
      print(df2.loc[listaIDX[c],'symbol'])
      print(df2.loc[listaIDX[c],'okres'])
      print(round(x[0],2))
    www=www+1
    if str(df2.loc[listaIDX[c],'wzrost']) == '1':
      ilosc_prawd=ilosc_prawd+1
    if str(df2.loc[listaIDX[c],'wzrost2']) == '1':
      ilosc_prawd_5_proc=ilosc_prawd_5_proc+1
    if str(df2.loc[listaIDX[c],'wzrost3']) == '1':
      minus_10_procc=minus_10_procc+1
  if str(df2.loc[listaIDX[c],'wzrost']) == '1':
    ggg=ggg+1
  c=c+1





print(DFraport)
DFraport.to_excel('/content/drive/MyDrive/raportSpadekBilans.xlsx')
print(ilosc_prawd)
print(www)
print('procent + 20%')
print((ilosc_prawd/www)*100)
print('procent + 5%')
print((ilosc_prawd_5_proc/www)*100)
print('procent <> -10%')
print((minus_10_procc/www)*100)
print('procent + 20% w test')
print((ilosc_prawd/ggg)*100)

import pandas as pd
dfFinal=pd.read_excel('/content/drive/MyDrive/raportSpadekBilans.xlsx')
dfFinal22=pd.read_excel('/content/drive/MyDrive/raportSpadek.xlsx')
dfFFbilans=dfFinal[['symbol','okresPoprzedni','poprzedniKwartalSpadek_bilans','poprzedniKwartalWzrostBilans','okresAktualny','AktualnyKwartalSpadek_bilans','AktualnyKwartalWzrostBilans','okresAktualnyCENA_Bilans','AktualnyKwartal_Spadek_CENA_Bilans','AktualnyKwartalWzrostCENA_Bilans','Kurs','cena akt']]
print(dfFinal22.columns)
dfFF=dfFinal22[['symbol','okresPoprzedni','poprzedniKwartalSpadek','poprzedniKwartalWzrost','okresAktualny','AktualnyKwartalSpadek','AktualnyKwartalWzrost','okresAktualnyCENA','AktualnyKwartalSpadekCENA','AktualnyKwartalWzrostCENA']]

dfFFbilans=dfFFbilans.set_index('symbol',drop=False)

dfFF=dfFF.set_index('symbol',drop=False)
dfFFbilans['roznicaBilans']=dfFFbilans['AktualnyKwartalWzrostBilans']-dfFFbilans['AktualnyKwartalSpadek_bilans']
dfFF['roznica']=dfFF['AktualnyKwartalWzrost']-dfFF['AktualnyKwartalSpadek']
ingotwanie_symbol=['OEX','REM','LHD','PGG','SES','OVO']
#ingotwanie_symbol=[]
dfFFbilans['roznica']=dfFFbilans.apply(lambda x: dfFF.loc[x['symbol'],'roznica'] if x['symbol'] not in ingotwanie_symbol  else x,axis=1)
#dfFFbilans['srednia']=(dfFFbilans['roznicaBilans']+dfFFbilans['roznica'])/2
print(dfFFbilans)


dfFFbilans.to_excel('/content/drive/MyDrive/raportSpadekBilans_FINAL.xlsx')
dfFF.to_excel('/content/drive/MyDrive/raportSpadek.xlsx')