# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

df2=pd.read_excel('/content/drive/MyDrive/maszynowe16.xlsx', index_col=False)
df2=df2[df2['kapitalizacja'] != 0]
df2['wzrost'] = np.where(df2['symbol'].shift(-1) == df2['symbol'], (df2['kapitalizacja'].shift(-1)-df2['kapitalizacja'])/df2['kapitalizacja'].shift(-1), 0)
df2['wzrost2'] = np.where(df2['wzrost'] > 0.05,1,0)
df2['wzrost3'] = np.where(df2['wzrost'] < -0.10,1,0)
df2['wzrost'] = np.where(df2['wzrost'] > 0.19,1,0)
print(df2)

df=df2.drop(columns=['okres','symbol','Unnamed: 0','kapitalizacja','wzrost2','wzrost3'])
for col in df.columns:

  #print(x[col].value_counts())
  df=pd.get_dummies(df, columns=[col],drop_first=True)
print(df.shape)



x= df.drop(columns=['wzrost_1'])
x=x.loc[~(x==0).all(axis=1)]
#print(x)

from keras.models import load_model

model = load_model('/content/drive/MyDrive/moj_najlepszy_model_WK_spadek_03_02_2025.keras')

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
      DFraport.loc[symbol,'poprzedniKwartalSpadek']=  round(x[0],2)
  if df2.loc[listaIDX[c],'okres'].find('gru24') !=-1 or df2.loc[listaIDX[c],'okres'].find('sty25') !=-1:
      DFraport.loc[symbol,'symbol']=df2.loc[listaIDX[c],'symbol']
      DFraport.loc[symbol,'okresAktualny']= df2.loc[listaIDX[c],'okres']
      DFraport.loc[symbol,'AktualnyKwartalSpadek']=  round(x[0],2)
  if df2.loc[listaIDX[c],'okres'].find('AKT') !=-1:
      DFraport.loc[symbol,'symbol']=df2.loc[listaIDX[c],'symbol']
      DFraport.loc[symbol,'okresAktualnyCENA']= df2.loc[listaIDX[c],'okres']
      DFraport.loc[symbol,'AktualnyKwartalSpadekCENA']=  round(x[0],2)
  #if str(round(x[0],2)) == '0.12':
  if x[0] > 0.4:
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
DFraport.to_excel('/content/drive/MyDrive/raportSpadek.xlsx')
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

model = load_model('/content/drive/MyDrive/moj_najlepszy_model_wzrost_WK_03_02_2025.keras')

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
#dfWagi.to_excel('/content/drive/MyDrive/wagiMAKRO_EKO.xlsx')
lll=df.drop(columns=['wzrost_1'])
lll=lll.columns
lll=pd.DataFrame(lll)
#lll.to_excel('/content/drive/MyDrive/kolumnyMAKRO_EKO.xlsx')
print(lll)

dfWagi['kolumny']=lll
dfWagi=dfWagi[['kolumny','srednia']]
dfWagi.to_excel('/content/drive/MyDrive/wagiMAKRO_EKO.xlsx')


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


for x in prediction:
  symbol=df2.loc[listaIDX[c],'symbol']
  if df2.loc[listaIDX[c],'okres'].find('wrz24') !=-1 or df2.loc[listaIDX[c],'okres'].find('paź24') !=-1:

      DFraport.loc[symbol,'symbol']=df2.loc[listaIDX[c],'symbol']
      DFraport.loc[symbol,'okresPoprzedni']= df2.loc[listaIDX[c],'okres']
      DFraport.loc[symbol,'poprzedniKwartalWzrost']=  round(x[0],2)
  if df2.loc[listaIDX[c],'okres'].find('gru24') !=-1 or df2.loc[listaIDX[c],'okres'].find('sty25') !=-1:
      DFraport.loc[symbol,'symbol']=df2.loc[listaIDX[c],'symbol']
      DFraport.loc[symbol,'okresAktualny']= df2.loc[listaIDX[c],'okres']
      DFraport.loc[symbol,'AktualnyKwartalWzrost']=  round(x[0],2)

  if df2.loc[listaIDX[c],'okres'].find('AKT') !=-1:
      DFraport.loc[symbol,'symbol']=df2.loc[listaIDX[c],'symbol']
      DFraport.loc[symbol,'okresAktualnyCENA']= df2.loc[listaIDX[c],'okres']
      DFraport.loc[symbol,'AktualnyKwartalWzrostCENA']=  round(x[0],2)
  #if str(round(x[0],2)) == '0.12':
  if x[0] > 0.4:
    if (df2.loc[listaIDX[c],'okres'].find('wrz24') !=-1 or df2.loc[listaIDX[c],'okres'].find('paź24') !=-1):
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
DFraport.to_excel('/content/drive/MyDrive/raportSpadek.xlsx')
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
