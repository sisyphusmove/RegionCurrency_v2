from django.shortcuts import render, get_object_or_404
import random
from django.contrib.auth.models import User
import json, requests
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

# def history(request):
#     print("#############################")
#     withdraw_list = []
#     item_list = ["짜장면", "오징어", "호박엿"]
#     name_list = ["영선","재호","종석","민근","광민"]
#     type_list = ["pagado","pendiente","cancelado"]
#     price_list = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000]
#     date_list = ["18.10.11","18.9.11","18.8.11","18.7.11","18.6.11","18.5.11","18.4.11"]
#     for s in range(70):
#         number = 70-s
#         dic = {}
#         dic['no'] = number
#         dic['name'] = random.choice(name_list)
#         dic['item'] = random.choice(item_list)
#         dic['type'] = random.choice(type_list)
#         if dic['type'] == "pagado":
#             kortype = "송금"
#         elif dic['type'] == "pendiente":
#             kortype = "결제"
#         elif dic['type'] == "cancelado":
#             kortype = "발행"
#         dic['typekor'] = kortype
#         dic['price'] = random.choice(price_list)
#         # 70~60 = 1 / 50번대 = 2 / 40번대 = 3 / 30번대 = 4 / 20번대 = 5 / 10번대 = 6
#         if dic['no'] >= 60:
#             dic['date'] = date_list[1]
#         elif dic['no'] >= 50:
#             dic['date'] = date_list[2]
#         elif dic['no'] >= 40:
#             dic['date'] = date_list[3]
#         elif dic['no'] >= 30:
#             dic['date'] = date_list[4]
#         elif dic['no'] >= 20:
#             dic['date'] = date_list[5]
#         elif dic['no'] >= 10:
#             dic['date'] = date_list[6]
#         elif dic['no'] >= 0:
#             dic['date'] = date_list[6]

#         withdraw_list.append(dic)
#     # withdraw_list = User.objects.all()
#     print(withdraw_list)
#     page = request.GET.get('page', 1)
#     paginator = Paginator(withdraw_list, 10)
#     withdraws = paginator.page(1)

#     try:
#         withdraws = paginator.page(page)
#     except PageNotAnInteger:
#         withdraws = paginator.page(1)
#     except EmptyPage:
#         withdraws = paginator.page(paginator.num_pages)

#     return render(request, "payment/history.html",{'withdraws': withdraws})