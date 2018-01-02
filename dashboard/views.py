import json

from django.shortcuts import render, get_object_or_404
import pandas as pd
from pandas import *
from pymongo import MongoClient
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        client = MongoClient()
        db = client.testdb
        pd.options.display.max_colwidth = 1000
        df = pd.DataFrame(list(db.test.aggregate([{'$group': {'_id': {'EventID': "$EventID"}, "count": {'$sum': 1}}},
                                                  {'$project': {"_id": 0, "EventID": "$_id.EventID", "count": "$count"}}])))
        for_table = pd.DataFrame(list(db.test.aggregate(
            [{'$group': {'_id': {'Hostname': "$Hostname", 'EventID': "$EventID"}, "count": {'$sum': 1}}}, {
                '$project': {"_id": 0, "Hostname": "$_id.Hostname", "EventID": "$_id.EventID",
                             "count": "$count"}}])))
        chart_events_json = df.to_json(orient='records')
        html_table = for_table.to_html()
        context = {'chart_events_json': chart_events_json, 'table_events': html_table}
        return render(request, "dashboard/dashboard.html", context)
    else:
        return redirect("/login")

def filter_tables(request):
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    client = MongoClient()
    db = client.testdb
    pd.options.display.max_colwidth = 1000
    df = pd.DataFrame(list(db.test.aggregate([{'$group': {'_id': {'EventID': "$EventID"}, "count": {'$sum': 1}}},
                                              {'$project': {"_id": 0, "EventID": "$_id.EventID", "count": "$count"}}])))
    for_table = pd.DataFrame(list(db.test.aggregate(
        [{'$group': {'_id': {'Hostname': "$Hostname", 'EventID': "$EventID"}, "count": {'$sum': 1}}}, {
            '$project': {"_id": 0, "Hostname": "$_id.Hostname", "EventID": "$_id.EventID",
                         "count": "$count"}}])))
    chart_events_json = df.to_json(orient='records')
    html_table = for_table.to_html()
    context = {'chart_events_json': chart_events_json, 'table_events': html_table}
    return render(request, "dashboard/dashboard.html", context)