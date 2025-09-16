import pandas as pd
import numpy as np
from datetime import datetime



def import_df(path):
    df = pd.read_csv(path, sep=';')
    return(df)


# function to make the conversion

def customerData_to_dailyData(orders_df, prod_settings):

    ''' beautifoul function that make all the preprocessing from customer data to day product sales data'''

    df = orders_df
    format_str = "%Y-%m-%d %H:%M:%S.%f"
    format_day = "%Y-%m-%d"

    # get dates
    date = [datetime.strptime(ts_str, format_str).date().strftime(format_day) for ts_str in df['ts']]
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    #get quantity by date and product
    cols = list(df.columns)
    last_col_id = cols.index('NOTE')
    prodcols = [cols[i] for i in range(last_col_id+1, df.shape[1])]

    df['date'] = date
    df_long = pd.melt(df, 
                    id_vars=['date'],
                    value_vars=prodcols,
                    var_name='prod',
                    value_name='quantity')

    df_agg = df_long.groupby(['prod', 'date'])['quantity'].sum().reset_index()

    #get time values
    date_obj = [datetime.strptime(date_str, format_day) for date_str in df_agg['date']]
    df_agg['day'] = [weekdays[date_o.weekday()] for date_o in date_obj]
    df_agg['year'] = [date_o.year for date_o in date_obj]
    df_agg['month'] = [date_o.month for date_o in date_obj]

    #get price
    dizio = dict(zip(prod_settings['prodotto'], prod_settings['prezzo']))
    df_agg['price'] = [dizio[o] for o in df_agg['prod']]

    #get n_day_sells
    date_quantity = df_agg.groupby(['date'])['quantity'].sum().reset_index()
    dizio = dict(zip(date_quantity['date'], date_quantity['quantity']))
    df_agg['n_day_sells'] = [dizio[o] for o in df_agg['date']]

    #get n_day_orders
    unici = np.unique(df['date'], return_counts=True)
    dizio = dict(zip(unici[0], unici[1]))
    df_agg['n_day_orders'] = [dizio[o] for o in df_agg['date']]

    #ordering columns
    df = df_agg[['quantity', 'price', 'prod', 'n_day_sells', 'n_day_orders', 'day', 'month', 'year']]

    return(df_agg)

