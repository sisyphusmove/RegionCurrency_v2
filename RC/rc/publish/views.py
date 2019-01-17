from django.shortcuts import render, get_object_or_404, redirect
import random
from django.contrib.auth.models import User
import json, requests, datetime
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

host = "http://210.107.78.166:3000/"

def publish(request):
    template_name = "publish/publish.html"
    return render(request,"publish/publish.html")

@csrf_exempt
def doPublish(request):
    toId = request.POST.get("userid") 
    amount = request.POST.get("amount")
    today = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    # url = host + "publish/" + toId + "/admin/" + amount + "/" + today
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    url = host + "publish"
    data = {
        'user_id'   : toId, 
        'from_id'   : 'admin',
        'amount'    : amount,
        'date'      : today
    }
    data_json = json.dumps(data)
    param_data = { 'param_data' : data_json }
    response = requests.post(url, params=param_data, headers=headers)
    data = {
        'res' : response.status_code
    }
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json;charset=UTF-8")