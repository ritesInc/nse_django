from django import forms
import pandas as pd
from pandas.tseries.offsets import BDay
import datetime
PAST_DAYS = 30

# defining all function we need to get all choices for select box
def getWorkingDates(PAST_DAYS):
    date_range = []
    today = datetime.datetime.today()
    for day_no in range(PAST_DAYS):
        last_working_date = str((today - BDay(day_no)).strftime("%d %b %Y")).upper()
        date_range.append(last_working_date)

    return date_range

def URLGenerator(date):
    date_part = date.split(" ")
    url_value = "https://archives.nseindia.com/content/historical/EQUITIES/"+ date_part[2] +"/"+ date_part[1] +"/cm"+ date_part[0]+date_part[1]+date_part[2] +"bhav.csv.zip"
    return url_value

def getAllURLs(PAST_DAYS):
    date_range_list = getWorkingDates(PAST_DAYS)
    url_list = []
    for date in date_range_list:
        #print(URLGenerator(date))
        url_list.append(URLGenerator(date))

    return url_list

def getCSVData(url_list):
    nse_df_dict = {}
    for url in url_list:
        try:
            #print(url)
            nse_df_dict[url] = pd.read_csv(url, usecols=["SYMBOL","SERIES","OPEN","HIGH","LOW","CLOSE","LAST","PREVCLOSE","TOTTRDQTY","TIMESTAMP"])
            del nse_df_dict[url]['Unnamed: 13']
        except Exception as e:
            pass
            #print("Can't Access requested URL : {}".format(url))
            #print(e)

    return nse_df_dict

def generateSymbolDataKeys(nse_df_dict):
    symbol_data_keys = []
    for df in nse_df_dict.keys():
        for symbol in nse_df_dict[df]['SYMBOL']:
            symbol_data_keys.append(symbol)

    return symbol_data_keys
#calling all required methods to get all choices for select box

url_list = getAllURLs(PAST_DAYS)
nse_df_dict = getCSVData(url_list)
symbol_data = generateSymbolDataKeys(nse_df_dict)
CHOICES = []
for symbol in symbol_data:
    CHOICES.append((symbol, symbol))

class SymbolData(forms.Form):
    symbol = forms.ChoiceField(widget=forms.Select(attrs={
        'class': 'form-control',
        'name': 'symbol'
    }), choices=CHOICES)
