from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from time import sleep
import requests, json, datetime
from store.models import Store
from wallet.models import Cancellation
from operate.models import ChartStat

# Create your views here.

host = 'http://210.107.78.166:3000/'

# wallet 정보 획득
@login_required
def read_wallet(request):
    url = host + 'get_account'
    params = {'user_id' : request.user.username}
    response = requests.get(url, params=params)
    res = response.json()
    data = {
        'balance' : '{:,}'.format(int(res['value']))
    }
    return render(request, 'wallet/read_wallet.html', data)

# RC코인 발행
@csrf_exempt
@login_required
def publish(request):
    if request.method == 'POST':
        toId = request.POST.get('userid') 
        amount = request.POST.get('amount')
        today = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = host + 'publish'
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
        return HttpResponse(json_data, content_type='application/json;charset=UTF-8')
    return render(request,'wallet/publish.html')

# 송금
@csrf_exempt
@login_required
def remittance(request):
    if request.method == 'POST':
        # 송금로직
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        fromId = request.user.username
        toId = request.POST.get("target") 
        amount = (request.POST.get("point")).replace(',', '')
        today = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = host + 'transfer'
        data = {
            'from_id'   : fromId, 
            'to_id'     : toId,
            'amount'    : amount,
            'type'      : '5',
            'date'      : today
        }
        param_data = { 'param_data' : json.dumps(data) }
        response = requests.post(url, params=param_data, headers=headers)
        res = response.json()
        
        if res['result'] == 'success':
            return redirect('/remittance1/done/')
        else:
            return redirect('/remittance2/done/')
    
    # 송금위한 잔액 전송
    user = get_object_or_404(User, pk=request.user.pk)
    url = host + 'get_account'
    params = {'user_id' : user.username}
    response = requests.get(url, params=params)
    res = response.json()
    data = {
        'balance' : '{:,}'.format(int(res['value']))
    }
    return render(request, 'wallet/remittance.html', data)

# 결제
@csrf_exempt
@login_required
def payment(request):
    if request.method == 'POST':
        amount = request.POST.get("amount", 0).replace(',', '')
        s_id = request.POST.get('s_id', 0)
        store = get_object_or_404(Store, pk=s_id)
        to_user = get_object_or_404(User, pk=int(store.representative_id))
        today = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
        if to_user.pk == request.user.pk:
            return redirect('/payment2/done/')
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = host + "transfer"
        data = {
            'from_id'   : request.user.username, 
            'to_id'     : to_user.username,
            'amount'    : amount,
            'type'      : '1',
            'date'      : today
        }
        data_json = json.dumps(data)
        param_data = { 'param_data' : data_json }
        response = requests.post(url, params=param_data, headers=headers)
        msg = response.json()
        # 결제 결과 처리
        if msg['result'] == 'success':
            
            ###################차트 데이터####################
            user = get_object_or_404(User, id=request.user.pk)

            age = int(datetime.datetime.now().year) - int(user.profile.birth_year) 
            gender = user.profile.gender
            location = store.location
            category = store.category
            tx_id = msg['tx_id']

            chart = ChartStat()
            chart.age = age
            chart.gender = gender
            chart.store = store
            chart.amount = amount
            chart.location = location
            chart.category = category
            chart.tx_id = tx_id['_transaction_id']

            chart.save()
            ##################################################
            return redirect('/payment1/done/')
        else:
            return redirect('/payment2/done/')
    try:
        
        s_id = request.GET.get('s_id', 0)
        store = get_object_or_404(Store, id=s_id)
    except:
        return redirect('/payment2/done/')
    
    url = host + 'get_account'
    params = {'user_id' : request.user.username}
    response = requests.get(url, params=params)
    res = response.json()
    data = {
        'store' : store,
        'balance' : '{:,}'.format(int(res['value']))
    }
    return render(request, 'wallet/payment.html', data)

# 결제 히스토리
@login_required
def get_history(request):
    fro = request.GET.get('fro',None)
    this_page_num = request.GET.get('this_page',None)
    query_type = request.GET.get('type', 1)
    url = host + "get_txList"
    params = {'user_id' : fro}
    response = requests.get(url, params=params)
    res = response.json()
    res.reverse()

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
        if history['txType'] == '1' or history['txType'] == '4':
            user = get_object_or_404(User, username=history['trader'])
            store = Store.objects.filter(Q(representative=user.id) & ~Q(status=3))
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


# 삭제된 거래 내역인지 검사
def chk_canceled(_txHash):
    res = False
    res = Cancellation.objects.filter(txHash=_txHash).exists()
    return res

# 가맹점 거래 히스토리
@login_required
def get_receipt(request):
    this_page_num = request.GET.get('this_page', None)
    option = request.GET.get('option', None)
    data = {}
    user = get_object_or_404(User, pk=request.user.pk)
    store = Store.objects.filter(Q(representative=user) & ~Q(status=3))
    if store:
        registered_date = (store[0].registered_date).strftime('%Y-%m-%d %H:%M:%S')    
        url = host + 'get_txList'
        params = {'user_id' : user.username}
        response = requests.get(url, params=params)
        res = response.json()
        res.reverse()

        filtered_list = []
        for receipt in res:
            if option == '0':
                if (receipt['date'] >= registered_date) and (receipt['txType'] == '2' or receipt['txType'] == '3'):
                    filtered_list.append(receipt)
            elif option == '1':
                if (~chk_canceled(receipt['tx_id']) and receipt['date'] >= registered_date) and (receipt['txType'] == '2'):
                    filtered_list.append(receipt)
            elif option == '2':
                if (~chk_canceled(receipt['tx_id']) and receipt['date'] >= registered_date) and (receipt['txType'] == '3'):
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


# 거래 취소 확인 페이지
@csrf_exempt
@login_required
def cancel_payment(request):
    to = request.POST.get('to', None)
    amount = request.POST.get('amount', None)
    tx = request.POST.get('tx', None)
    me = get_object_or_404(User, username=request.user.username)
    store = Store.objects.filter(Q(representative=me) & ~Q(status=3))
    return render(request, 'wallet/cancel_payment.html', dict(trader=to, store=store[0].name, username=me.username, amount=amount, tx=tx))


# 거래 취소
@csrf_exempt
@login_required
def cancel(request):
    if request.method == 'POST':
        to = request.POST.get('trader', None)
        key = request.POST.get('username', None)
        amount = request.POST.get('amount', None)
        tx = request.POST.get('tx', None)
        comment = request.POST.get('comment', None)
        today = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')

        headers = {'Content-Type': 'application/json; charset=utf-8'}
        url = host + "transfer"
        data = {
            'from_id'   : key, 
            'to_id'     : to,
            'amount'    : amount,
            'type'      : '3',
            'date'      : today
        }
        data_json = json.dumps(data)
        param_data = { 'param_data' : data_json }
        response = requests.post(url, params=param_data, headers=headers)
        msg = response.json()
        if msg['result'] == 'success':
            canceled = Cancellation()
            canceled.s_id = Store.objects.filter(Q(representative=request.user.pk))[0]
            canceled.txHash = tx
            canceled.amount = amount
            canceled.comment = comment
            canceled.removed_date = today
            canceled.save()

            chart = ChartStat.objects.get(tx_id = tx)
            chart.delete()
            return redirect('/cancel1/done/')

        return redirect('/cancel2/done/')
