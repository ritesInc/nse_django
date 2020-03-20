from django.shortcuts import render
from django.http import HttpResponse
from django.utils.html import format_html
from simple_app.forms import SymbolData
import pandas as pd

# Create your views here.

def symbol_data_request(request):

    symbol_data_request_status = False
    if(request.method == "POST"):
        form = SymbolData(request.POST)

        #checking if form is valid or Not
        if(form.is_valid()):
            symbol_data_request_status = True
            symbol = request.POST['symbol']
            #now reading csv file related to specific symbol
            csv_file = "simple_app/csv_30/"+symbol+".csv"
            try:
                df = pd.read_csv(csv_file)
                symbol_table = df.to_html(index=False)
            except Exception as e:
                symbol_table = "No Data Found Regarding Selected Option "+e
            return render(request, "index.html", {"symbol_table":format_html(symbol_table), "request_success":symbol_data_request_status, "form":form})


    else:
        form = SymbolData()
    return render(request, "index.html", {"form": form})
