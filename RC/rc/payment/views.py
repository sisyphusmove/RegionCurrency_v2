from django.shortcuts import render,redirect,get_object_or_404
import random
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json, requests
from django.http import JsonResponse, HttpResponse
# Create your views here.

host = 'http://210.107.78.166:8000/'

def getContext(user_id):
    user = get_object_or_404(User, pk=user_id)
    context = {
        "username" : user.username,
        "email" : user.email,
        "image" : user.profile.image,
        "gender" : user.profile.gender,
        'birth_year': user.profile.birth_year,
        'birth_month': user.profile.birth_month,
        'birth_date': user.profile.birth_date,
        "type" : user.profile.type,
        "status" : user.profile.status
    }
    return context

def withdraw(request, account_id=None):
    template_name = "payment/withdraw.html"
    context = getContext(account_id)
    url = host +"get_account/" + str(account_id)
    response = requests.get(url)
    res = json.loads(response.text)
    data = {
        "context" : context,
        "balance" : res['value']
    }
    return render(request, template_name, data)

def transfer(request, account_id=None):
    template_name = "payment/withdraw.html"
    context = getContext(account_id)
    url = host +"transfer/" + str(from_id) + "/" + str(to_id) + "/" + str(amount) + "/" + str(type) + "/" + str(current)
    response = requests.get(url)
    print(response)


def history(request):
    account_id = request.GET.get("account_id")
    url = host +"get_txList/" + str(account_id)
    response = requests.get(url)
    res = json.loads(response.text)
    data = {
        "tx" : res['value']
    }
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json;charset=UTF-8")

    # page = request.GET.get('page', 1)
    # paginator = Paginator(withdraw_list, 10)
    # withdraws = paginator.page(1)

    # try:
    #     withdraws = paginator.page(page)
    # except PageNotAnInteger:
    #     withdraws = paginator.page(1)
    # except EmptyPage:
    #     withdraws = paginator.page(paginator.num_pages)

    # return render(request, "payment/history.html",{'withdraws': withdraws})