from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, View,TemplateView

import requests

from info.models import Notice
from board.models import Comment, BoardLiker
from store.models import Photo, Store
from operate.models import ChartStat
from django.db.models import Q, Sum

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from info.forms import NoticeForm

from rest_framework.views import APIView
from rest_framework.response import Response

import json

Userchart = get_user_model()
#--------------------------------------로그인-----------------------------------------------#

def login_required(fn):
    def wrapper(*args, **kwargs):
        request = args[0]
        request_url = request.resolver_match.url_name
        key = 'admin_name'
        context = {}
        if key in request.session:
            if bool(request.session['admin_name'] == 'admin_server') & bool(request_url != 'network') & bool(request_url != 'dashboard'):
                return redirect('operate:dashboard')
            elif bool(request.session['admin_name'] == 'admin') & bool(request_url == 'network') & bool(request_url != 'dashboard'):
                return redirect('operate:dashboard')
            else:
                return fn(request)
        elif request.method == "POST":
            admin_name = request.POST.get('username', '')
            admin_pass = request.POST.get('password', '')
            user = authenticate(request, username=admin_name, password=admin_pass)
            if user is not None:
                request.session['admin_name'] = admin_name
                request.session.modified = True
                if bool(admin_name == 'admin_server') & bool(request_url != 'network') & bool(request_url != 'dashboard'):
                    return redirect('operate:dashboard')
                elif bool(admin_name == 'admin') & bool(request_url == 'network') & bool(request_url != 'dashboard'):
                    return redirect('operate:dashboard')
                else:
                    return fn(request)    
        else:
            context['main'] = 'main'
            return render(request, 'operate/manage_main.html', {'main': 'main'})
    return wrapper

def admin_logout(request, *args):
    request.session['admin_name'] = {}
    request.session.modified = True 
    logout(request)
    return redirect('operate:main')

#--------------------------------------메인-----------------------------------------------#

def main(request):
    key = 'admin_name'
    context = {}
    context['main'] = "main"
    if key in request.session:
        return redirect('operate:dashboard')
    else:
        if request.method == 'POST': # POST
            admin_name = request.POST.get('username', '')
            admin_pass = request.POST.get('password', '')
            user = authenticate(request, username=admin_name, password=admin_pass)
            if user is not None:
                request.session['admin_name'] = admin_name
                request.session.modified = True
                if admin_name != "":
                    return redirect('operate:dashboard')
                else:
                    return render(request, 'operate/manage_main.html', (context))
            else: 
                return render(request, 'operate/manage_main.html', (context))
        else: # GET
            return render(request, 'operate/manage_main.html', (context))

#--------------------------------------대시보드-----------------------------------------------#

@login_required
def dashboard(request):
    context = {}
    context['tx_cnt']              = get_tx_cnt()
    context['store_cnt']           = get_store_cnt()
    context['account_cnt']         = get_account_cnt()
    context['publish']             = get_publish_amount()
    context['west_stats']          = 0 if get_total_location_tx(2) == None else get_total_location_tx(2)
    context['north_stats']         = 0 if get_total_location_tx(3) == None else get_total_location_tx(3)
    context['wooleung_stats']      = 0 if get_total_location_tx(1) == None else get_total_location_tx(1)
    context['store_waiting_list']  = get_waiting_store()
    context['notice_list']         = get_notices()
    return render(request, 'operate/manage_dashboard.html', (context))

#--------------------------------------사용자관리-----------------------------------------------#
@login_required
def manageUser(request):
    context = {}
    username = request.GET.get('keyword', '')
    context['users'] = User.objects.filter(Q(username__icontains=username) & ~Q(profile__type=0)).order_by('id')

    return render(request, 'operate/manage_users.html', (context))

def get_like(request):
    user_id = request.GET.get('user_id', '')
    like = BoardLiker.objects.filter(liker = user_id)
    board = BoardLiker.objects.filter(board = user_id)
       
    context = {}
    context['like_cnt'] = len(like)
    context['board_cnt'] = len(board)
    json_format = json.dumps(context)
    return HttpResponse(json_format, content_type="application/json:charset=UTF-8") 
#-------------------------------------------------------------------------------------------#

#--------------------------------------가맹점승인관리-----------------------------------------------#
@login_required
def manage_store_approval(request):
    context = {}
    context['photos'] = Photo.objects.filter(store__status='w')
    return render(request, 'operate/manage_approval.html', (context))

def get_approval(request):
    store_id = request.GET.get('store_id', '')
    store = get_object_or_404(Store, id=store_id)
    userid = store.representative
    user = get_object_or_404(User, profile__user=userid)
    context = {}
    if store.status == 'w':
        store.status = 'a'
        store.save()
        user.profile.type = 1
        user.save()
        context['result'] = 'y'
    else:
        context['result'] = 'n'

    json_format = json.dumps(context)
    return HttpResponse(json_format, content_type="application/json:charset=UTF-8") 
#-------------------------------------------------------------------------------------------#

#--------------------------------------공지사항관리-----------------------------------------------#
@login_required
def manage_notice(request):
    context = {}
    context['notice_list'] = Notice.objects.all()
    return render(request, 'operate/manage_notice.html', (context))

def notice_edit(request, notice_id=None):
    if notice_id:
        notice = get_object_or_404(Notice, pk=notice_id)
    else:
        notice = Notice()
    
    if request.method == 'POST': # POST
        form = NoticeForm(request.POST, instance=notice) 
        if form.is_valid():
            notice = form.save(commit=False)
            notice.save()
        return redirect('operate:notice')

    else: # GET 
        form = NoticeForm(instance=notice) 
        return render(request, 'operate/manage_notice_edit.html', dict(form=form, notice=notice))

def notice_activate(request):
    change_list = []
    change_list = request.GET.getlist('change_list[]', )
    
    context = {}
    try:
        for change_id in change_list:
            notice = get_object_or_404(Notice, id=change_id)
            if notice.status == "Y":
                notice.status = "N"
                notice.save()
            elif notice.status == "N":
                notice.status = "Y"
                notice.save()
            context['result'] = "success"
    except Exception as e:
        print(e)
        context['result'] = "fail"
            
    json_format = json.dumps(context)
    return HttpResponse(json_format, content_type="application/json:charset=UTF-8") 

#--------------------------------------발행이력관리-----------------------------------------------#
@login_required
def publish(request):
    context = {}
    publish_list = []
    publish_list = list(get_publish_amount()['publish_list'])
    context['publish_list'] = publish_list
    return render(request, 'operate/manage_publish.html', (context))

#--------------------------------------네트워크 관리-----------------------------------------------#
@login_required
def network(request):
    return render(request, 'operate/manage_network.html', ({}))

##----------------------차트관리------------------------------------------------#

@login_required
def manage_stats(request):
    return render(request, 'operate/manage_stats.html', ({}))

##################북면#########################################
@login_required
def north_stats(request):
    return render(request, 'operate/manage_stats_north.html', {})
    
#################서면############################################
@login_required
def west_stats(request):
    return render(request, 'operate/manage_stats_west.html', {})

##################울릉읍#########################################
@login_required


def wooleung_stats(request):
    return render(request, 'operate/manage_stats_wooleung.html', {})

class ChartData(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, format=None):

        location = self.request.GET.get("location")
        
        ################울릉도 전체#####################
        all_labels = ['2015','2016','2017','2018','2019']
        # data_list = ChartStat.objects.values_list('time', flat=True)
        default = {}
        for label in all_labels:
            default[label] = 0
            value = ChartStat.objects.filter(time__icontains=label).aggregate(Sum('amount'))['amount__sum']
            if value != None:
                default[label] = value
       
        ###############polar###########################
        labels = ['남자','여자']
        data_list1 = ChartStat.objects.values_list('gender', flat=True).filter(store__location=location)
        default_items = [0, 0]
        for data in data_list1:
            if data == '남':
                default_items[0] += 1
            else : default_items[1] += 1

        ###############bar###########################
        labels_second = ['10대미만','10대', '20대','30대','40대','50대','60대 이상',]
        data_list2 = ChartStat.objects.values_list('age', flat=True).filter(store__location=location)
        default1_items = [0, 0, 0, 0, 0, 0, 0]
        for data in data_list2:
            if int(data) >= 60:
                default1_items[6] += 1
            elif int(data) >= 50:
                default1_items[5] += 1
            elif int(data) >= 40:
                default1_items[4] += 1
            elif int(data) >= 30:
                default1_items[3] += 1
            elif int(data) >= 20:
                default1_items[2] += 1
            elif int(data) >= 10:
                default1_items[1] += 1
            else:
                default1_items[0] += 1

        ###############line###########################
        labels_thard = ['요식업','숙박업','레저','쇼핑']
       
        
        default2_items = [0,0,0,0]

        
        for li in range(4):
            
            object_money = (ChartStat.objects.filter(Q(store__location=location) & Q(store__category = li+1)).aggregate(Sum('amount')))['amount__sum']
            if object_money != None:
                default2_items[li] = object_money
            


        data = {

                "all_labels" : all_labels,
                "all_default" : default.values(),
               
                "labels": labels,
                "default": default_items,

                "labels_second" : labels_second,
                "default1": default1_items,

                "labels_thard" : labels_thard,
                "default2": default2_items,
                
        }
        return Response(data)

#-----------------------------------------------------------------#

## utils
def check_length(string, max_len):
    result = ""
    if len(string) > max_len:
        result = str(string)[0:max_len] + "..."
    else:
        result = str(string)
    return result

host = "http://210.107.78.166:3000/"

## query
def get_notices():
    notice = Notice.objects.order_by('-id')
    notice_list = []
    for li in list(notice)[0:4]:
        temp = {}
        temp['id'] = li.id
        temp['title'] = check_length(str(li.title), 5)
        temp['writer'] = check_length(str(li.writer), 5)
        temp['status'] = li.status
        temp['create_date'] = str(li.create_date)[0:10]
        temp['modify_date'] = str(li.modify_date)[0:10]
        notice_list.append(temp)
    return notice_list

def get_publish_amount():
    get_publish_url = host + "get_total_publish"
    publish_data = {}
    publish_amount = 0

    try:
        response = requests.get(get_publish_url)
        json_format = json.loads(response.text)
        data_list = []
        for datas in json_format:
            data = {}
            publish_amount = datas['balance']
            data['tx_id'] = str(datas['tx_id'])
            data['amount'] = datas['amount']
            data['person'] = datas['trader']
            data['date'] = datas['date']
            data_list.append(data)
            
        publish_data['total_publish'] = publish_amount
        publish_data['publish_list'] = data_list
    except Exception as e:
        print(e)
        publish_data['publish_list'] = ""
    return publish_data

def get_account_cnt():
    users = User.objects.all()
    user_cnt = len(users)
    return user_cnt

def get_tx_cnt():
    tx_height = 0
    get_block_url = host + "get_tx_cnt"
    try:
        response = requests.get(get_block_url)
        json_format = json.loads(response.text)
        tx_height = json_format['block_height']
    except Exception as e:
        print(e)
    return tx_height

def get_store_cnt():
    store = Store.objects.all()
    store_cnt = len(store)
    return store_cnt

def get_waiting_store():
    store = Store.objects.filter(status='w').order_by('-modified_date')[0:4]
    store_list = []
    for li in store:
        stores = {}
        stores['name'] = li.name
        stores['modified_date'] = li.modified_date
        stores['corporate_number'] = li.corporate_number
        if str(li.category).strip() == "쇼핑":
            stores['category'] = 1
        if str(li.category).strip() == "레저":
            stores['category'] = 2
        if str(li.category).strip() == "숙박업":
            stores['category'] = 3
        if str(li.category).strip() == "요식업":
            stores['category'] = 4
        store_list.append(stores)
    return store_list

def get_total_location_tx(location):
    return ChartStat.objects.filter(Q(store__location=location)).aggregate(Sum('amount'))['amount__sum']
