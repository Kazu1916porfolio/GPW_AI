from flask import Flask, render_template, request, send_file, flash, redirect, url_for
import pandas as pd
import pandas_gbq
import pydata_google_auth
import re
import io
import os  # Dodaj import os
import numpy as np
from sqlalchemy import create_engine
from flask import jsonify
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = 'tajny_klucz'
username = os.getlogin()



@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')

@app.route('/Analiza_spolki')

def Analiza_spolki():
    engine = create_engine('sqlite:///GPW3.db', echo=True)
    sqlite_connection = engine.connect()
    dfSQL = pd.read_sql_query(
        "SELECT * FROM RaportyGPW_biznesradar_wskazniki", sqlite_connection)
    dfSQL = dfSQL.drop_duplicates(['symbol', 'okres'])
    try:
        dfSQL=dfSQL.drop(columns=['Unnamed: 0'])
    except:
        ""
    dfSQL = dfSQL[['symbol', 'okres', 'Wartość księgowa na akcję', 'Wartość księgowa Grahama na akcję',
                   'Przychody ze sprzedaży na akcję', 'Zysk na akcję', 'Zysk operacyjny na akcję',
                   'Enterprise Value na akcję', 'ROE', 'ROA'
        , 'Udział zysku netto w przepływach operacyjnych', 'Zadłużenie ogólne', 'Płynność podwyższona',
                   'Płynność bieżąca']]
    last_rows = dfSQL.groupby('symbol').last().reset_index()

    print(last_rows.columns)
    print(last_rows)
    return render_template("Analiza_spolki.html", dane=last_rows)



@app.route('/get_chart_data')
def get_chart_data():
    symbol = request.args.get('symbol')
    column = request.args.get('column')

    engine = create_engine('sqlite:///GPW3.db', echo=True)
    sqlite_connection = engine.connect()

    # Pobierz wszystkie rekordy dla danego symbolu i kolumny
    query = f"""
    SELECT symbol, okres, `{column}` as value 
    FROM RaportyGPW_biznesradar_wskazniki 
    WHERE symbol = '{symbol.upper()}' 
    ORDER BY okres
    """
    df = pd.read_sql_query(query, sqlite_connection)

    # Przygotuj dane do wykresu
    data = []
    for _, row in df.iterrows():
        data.append({
            'symbol': row['symbol'],
            'okres': row['okres'],
            'value': str(row['value']),
            'column': column
        })

    return jsonify(data)


@app.route('/szczegoly_spolki')
def szczegoly_spolki():
    symbol = request.args.get('symbol')

    engine = create_engine('sqlite:///GPW3.db', echo=True)
    sqlite_connection = engine.connect()

    # Pobierz wszystkie rekordy dla danego symbolu
    query = f"SELECT * FROM RaportyGPW_biznesradar_wskazniki WHERE symbol = '{symbol}' ORDER BY okres"
    df = pd.read_sql_query(query, sqlite_connection)

    return render_template("szczegoly_spolki.html", dane=df, symbol=symbol)



if __name__ == '__main__':
    app.run(debug=True)
