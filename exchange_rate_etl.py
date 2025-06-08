import requests
import pandas as pd
import psycopg2
from datetime import datetime

base_currency = 'USD'
target_currencies = ['INR', 'EUR', 'GBP', 'JPY', 'INR']

db_url = os.getenv('db_url')

def fetch_exchange_rates():
    url = f'https://open.er-api.com/v6/latest/{base_currency}'
    response = requests.get(url)
    data = response.json()

    rate = data['rates']
    date = data['time_last_update_utc']

    dateime_object = datetime.strptime(date, "%a, %d %b %Y %H:%M:%S %z")
    extracted_date = datetime_object.date()

    df = pd.DataFrame([{
        'base_currency': base_currency,
        'target_currency': tc,
        'exchange_rate': rate[tc],
        'date': extracted_date
    } for tc in target_currencies])
    return df

def insert_into_pgres(df):
    conn = psycopg2.connect(db_url)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            base_currency TEXT,
            target_currency TEXT,
            exchange_rate NUMERIC,
            date DATE,
            PRIMARY KEY (base_currency, target_currency, date)
        )
    """)
    conn.commit()

    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO exchange_rates VALUES (%s, %s, %s %s)
            ON CONFLICT (base_currency, target_currency, date) DO NOTHING
        """), (row['base_currency'], row['target_currency'], row['exchange_rate'], row['date'])
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Data inserted into Postgres!")

if __name__ == '__main__':
    df = fetch_exchange_rates()
    insert_into_pgres(df)
