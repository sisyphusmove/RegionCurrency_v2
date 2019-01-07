from django.shortcuts import render, get_object_or_404, redirect
import random
from django.contrib.auth.models import User
import json, requests, datetime
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

host = "http://210.107.78.166:8000/"

def publish(request):
    template_name = "publish/publish.html"
    return render(request,"publish/publish.html")

def doPublish(request):
    toId = request.POST.get("userid") 
    amount = request.POST.get("amount")
    print(amount)
    today = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    url = host + "publish/" + toId + "/admin/" + amount + "/" + today
    print(url)
    response = requests.get(url)
    data = {
        'res' : response.text
    }
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json;charset=UTF-8")