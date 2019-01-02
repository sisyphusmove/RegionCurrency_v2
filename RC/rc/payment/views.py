from django.shortcuts import render, get_object_or_404, redirect
import random
from django.contrib.auth.models import User
import json, requests
from datetime import date
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from store.models import Store
# Create your views here.

host = "http://210.107.78.166:8000/"

def withdraw(request,account_id=None):
    template_name = "payment/withdraw.html"
    user = get_object_or_404(User, pk=account_id)
    url = host +"get_account/" + user.username
    response = requests.get(url)
    res = json.loads(response.text)
    data = {       
         "balance" : res['value']
    }
    return render(request, template_name, data)

def transfer(request):
    fromId = request.POST.get("from")
    toId = request.POST.get("target") 
    amount = (request.POST.get("point")).replace(',', '')
    today = str(date.today())
    url = host + "transfer/" + fromId +"/"+toId+"/"+amount+"/5/"+today
    response = requests.get(url)
    return redirect ('profile:account_myInfo', account_id = request.user.pk)

def get_history(request):
    fro = request.GET.get('fro',None)
    this_page_num = request.GET.get('this_page',None)
    query_type = request.GET.get('type', 1)
    url = host + "get_txList/" + fro
    response = requests.get(url)
    res = json.loads(response.text)
    fullLength = len(res)
    result = res.reverse()

    filtered_list = []
    # 송금 (txType:5,6,7,8)
    if query_type == '2' :
        for x in res :
            if x["txType"] == '5' or x["txType"] == '6' or x["txType"] == '7' or x["txType"] == '8':
                filtered_list.append(x)
    # 결제 (txType:1,2,3,4)
    elif query_type == '3':
        for x in res :
            if x["txType"] =='1' or x["txType"] =='2' or x["txType"] =='3' or x["txType"] =='4':
                filtered_list.append(x)
    # 발행 (txType:0)
    elif query_type == '1':
        for x in res :
            if x["txType"] =='0':
                filtered_list.append(x)
    elif query_type == '0':
        filtered_list = res

    history_list = []
    page_size = 5
    p = Paginator(filtered_list, page_size)

    for history in p.page(this_page_num):
        temp = {
            'balance':history["balance"],
            'trader':history["trader"],
            'amount':history["amount"],
            'txType':history["txType"],
            'date':history["date"]
        }
        history_list.append(temp)

    start_seq = p.count - (page_size * (int(this_page_num) - 1))
    data = {
        'start_seq' : start_seq,
        'history_list' : history_list,
        'current_page_num' : this_page_num,
        'max_page_num' : p.num_pages,
        'fullLength' : start_seq
    }
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json;charset=UTF-8")

def payment(request):
    s_id = request.GET.get('s_id')
    s_name = request.GET.get('s_name')
    u_name = request.user.username
    try:
        store = get_object_or_404(Store, pk=s_id)
        if s_name == store.name:
            print("결제")
    except:
        print("에러")

    return render (request, 'payment/templates/payment/payment.html', dict(s_id=s_id, s_name=s_name, u_name=u_name))
