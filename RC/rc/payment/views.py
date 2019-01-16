from django.shortcuts import render, get_object_or_404, redirect
import random
from django.contrib.auth.models import User
import json, requests, datetime
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from store.models import Store
from payment.models import Cancellation

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
    today = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
    url = host + "transfer/" + fromId +"/"+toId+"/"+amount+"/5/"+today
    response = requests.post(url)
    print(response)
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
    page_size = 10
    p = Paginator(filtered_list, page_size)

    for history in p.page(this_page_num):
        s_name = history['trader']
        if history['txType'] == '1':
            user = get_object_or_404(User, username=history['trader'])
            store = Store.objects.filter(Q(representative=user.id) & ~Q(status='d'))
            s_name = store[0].name
        temp = {
            'balance':history["balance"],
            'trader':s_name,
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


def get_receipt(request):
    u_id = request.GET.get('u_id', None)
    this_page_num = request.GET.get('this_page', None)
    data = {}
    
    user = get_object_or_404(User, pk=u_id)
    store = Store.objects.filter(Q(representative_id=u_id) & ~Q(status='d'))
    if store:
        registered_date = (store[0].registered_date).strftime('%Y-%m-%d %H:%M:%S')    
        url = host + 'get_txList/' + user.username
        response = requests.get(url)
        res = json.loads(response.text)
        res.reverse()

        filtered_list = []
        for receipt in res:
            if (receipt['date'] >= registered_date) and (receipt['txType'] == '2' or receipt['txType'] == '3'):
                filtered_list.append(receipt)

        page_size = 10
        p = Paginator(filtered_list, page_size)

        history_list = []
        for receipt in p.page(this_page_num):
            canceled = Cancellation.objects.filter(Q(txHash=receipt['tx_id'])).exists()

            temp = {
                'txHash' : str(receipt['tx_id']),
                'trader' : receipt['trader'],
                'amount' : receipt['amount'],
                'txType' : receipt['txType'],
                'date'  : receipt['date'],
                'canceled' : canceled
            }
            history_list.append(temp)

        start_seq = p.count - (page_size * (int(this_page_num) - 1))
        data = {
            'start_seq' : start_seq,
            'receipt_list' : history_list,
            'current_page_num' : this_page_num,
            'max_page_num' : p.num_pages,
        }

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json;charset=UTF-8")


def progress(request):
    s_id = request.GET.get('s_id')
    s_name = request.GET.get('s_name')
    u_id = request.user.pk
    u_name = request.user.username

    try:
        store = get_object_or_404(Store, pk=s_id)
        if s_name == store.name:
            print("결제")
    except:
        print("에러")

    return render (request, 'payment/payment.html', dict(s_id=s_id, s_name=s_name, u_id=u_id, u_name=u_name))
########################################CSRF############################
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
########################################################################
def payment(request):
    u_id = request.POST.get("u_id", None)
    s_id = request.POST.get("s_id", None)
    amount = request.POST.get("amount", 0)
    
    store = get_object_or_404(Store, pk=s_id)
    from_user = get_object_or_404(User, pk=u_id)
    to_user = get_object_or_404(User, pk=int(store.representative_id))
    today = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
            
    url = host + "transfer/" + from_user.username + "/" + to_user.username + "/" + amount + "/1/" + today
    response = requests.post(url)
    res = json.loads(response.text)
    data = {
        "result" : res
    }
    ###################차트 데이터####################
    user = get_object_or_404(User, id=u_id)

    age = int(datetime.datetime.now().year) - int(user.profile.birth_year) 
    gender = user.profile.gender
    location = store.location
    category = store.category
    print(user," : ",age," : ",gender,':',location,":",category)
    
    from operate.models import ChartStat
    chart = ChartStat()
    chart.age = age
    chart.gender = gender
    chart.store = store
    chart.amount = amount
    chart.location = location
    chart.category = category

    chart.save()
############################################################################################################

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json;charset=UTF-8")


def cancel_payment(request):
    to = request.POST.get('to', None)
    amount = request.POST.get('amount', None)
    tx = request.POST.get('tx', None)
    me = get_object_or_404(User, username=request.user.username)
    store = Store.objects.filter(Q(representative=me) & ~Q(status='d'))
    return render(request, 'payment/cancel_payment.html', dict(trader=to, store=store[0].name, username=me.username, amount=amount, tx=tx))


def add_canceled_payment(request):
    to = request.POST.get('trader', None)
    key = request.POST.get('username', None)
    amount = request.POST.get('amount', None)
    tx = request.POST.get('tx', None)
    today = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')

    url = host +'transfer/' + key + '/' + to + '/' + amount + '/3/' + today
    response = requests.post(url)
    res = json.loads(response.text)

    if res['result'] == 'success':
        canceled = Cancellation()
        canceled.s_id = Store.objects.filter(Q(representative=request.user.pk))[0]
        canceled.txHash = tx
        canceled.save()

    return redirect('profile:account_myInfo', request.user.pk)

