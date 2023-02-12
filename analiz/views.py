from django.shortcuts import render, redirect
from .forms import *
from .models import *
import numpy as np
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def upload_csv(request):
    data = []
    if request.method == "POST":
        file = request.FILES.get("csv-file")
        if not file or not file.name.endswith(".csv"):
            return render(request, "index.html", {"error": "Please select a valid CSV file"})
        df = pd.read_csv(file)
        if request.POST.get("submit") == "Upload":
            data = df.to_dict(orient="records")
        elif request.POST.get("submit") == "Percentage":
            rows = request.POST.get("rows")
            if rows is None:
                rows = df.shape[0]
            else:
                rows = int(rows)
            df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
            base_value = df.iloc[rows-1, 1:].sum()
            df.iloc[:rows, 1:] = df.iloc[:rows, 1:].div(base_value)
            df.iloc[:, 1:] = df.iloc[:, 1:].mul(100)
            df.iloc[:, 1:] = df.iloc[:, 1:].applymap(lambda x: "{:.0f}%".format(x))
            data = df.to_dict(orient="records")
            columns = df.columns.tolist()
        elif request.POST.get("submit") == "Describe":
            data = df.describe().to_dict(orient="records")
    return render(request, "analiz/index.html", {"data": data})
