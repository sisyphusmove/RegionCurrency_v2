from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, BaseUserManager
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from time import sleep
import json, docxpy, datetime, requests

from .models import Profile

# Create your views here.

host = 'http://210.107.78.166:3000/'

# 로그인
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)   
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            messages.error(request, '일치하는 회원정보가 없습니다.')
            return redirect('account:login')
    else:
        return render(request, 'account/login.html', {})

# 로그아웃
@login_required
def logout(request):
    auth_logout(request)
    return redirect('/logout/done/')

# 아이디 찾기
def forget_id(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        user_queryset = User.objects.filter(email=email)
        if not user_queryset:
            messages.error(request, '일치하는 회원정보가 없습니다.')
        else:
            for user in user_queryset:
                messages.info(request, user.username)
        return redirect('account:forget_id')
    else:
        return render(request, 'account/forget_id.html', {})

# 비밀번호 초기화
def forget_pwd(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        user = User.objects.filter(username=username, email=email)
        if user:
            # char_set = 'abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
            # new_pwd = BaseUserManager().make_random_password(length=10, allowed_chars=char_set)
            # user[0].set_password(new_pwd)
            # user[0].save()
            # send_mail(
            #     '[RC: 발신전용] 비밀번호 안내 메일',
            #     '비밀번호가 [ ' + new_pwd + ' ]로 초기화 되었습니다.',
            #     'doradora46@naver.com',
            #     [user[0].email],
            #     fail_silently=False,
            # )
            messages.info(request, '임시 비밀번호를 전송했습니다.')
        else:
            messages.error(request, '일치하는 회원정보가 없습니다.')
        return redirect('account:forget_pwd')
    else:
        return render(request, 'account/forget_pwd.html', {})

# 회원가입 동의서
def agreement(request):
    f = None
    context = {}
    
    try:
        doc = docxpy.process('static/doc/개인정보 수집·이용 동의.docx')
    except FileNotFoundError:
        context['agreement1'] = '개인정보 수집·이용 약관을 불러오는데 실패했습니다.'
    else:
        context['agreement1'] = doc
    finally:
        if not (f is None):
            f.close()

    try:
        doc = docxpy.process('static/doc/개인정보 처리 동침 동의.docx')
    except FileNotFoundError:
        context['agreement2'] = '개인정보 처리 동침 동의 약관을 불러오는데 실패했습니다.'
    else:
        context['agreement2'] = doc
    finally:
        if not (f is None):
            f.close()

    return render(request, 'account/agreement.html', context)

# 아이디 중복 검사
def chk_username(request):
    username = request.GET.get('username', None)
    res = User.objects.filter(username=username).exists()
    data = {
        'exist' : res
    }
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json;charset=UTF-8")

# 비밀번호 일치 확인
@login_required
def chk_password(request):
    data = {}
    if request.method == 'POST':
        username = request.user.username
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            data['exist'] = True
        else:
            data['exist'] = False
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json;charset=UTF-8")

# 회원가입
@csrf_exempt
def signup(request):
    success = 1
    if request.method == 'POST':
        key = request.POST.get('username', None)
        if key:
            # 계좌 생성
            today = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
            headers = {'Content-Type': 'application/json; charset=utf-8'}
            url = host + 'init_wallet'
            data = {
                'user_id' : key,
                'from_id' : 'admin',
                'date' : today
            }
            param_data = { 'param_data' : json.dumps(data) }
            response = requests.post(url, params=param_data, headers=headers)
            msg = response.json()
            if msg['result'] == 'fail':
                success = 3
            else:
                try:
                    get_object_or_404(User, email=request.POST.get('email', None))
                except:
                    sleep(3)
                    # 3000 rc 발행
                    today = (datetime.datetime.now()).strftime('%Y-%m-%d %H:%M:%S')
                    headers = {'Content-Type': 'application/json; charset=utf-8'}
                    url = host + 'publish'
                    data = {
                        'user_id'   : key, 
                        'from_id'   : 'admin',
                        'amount'    : '3000',
                        'date'      : today
                    }
                    param_data = { 'param_data' : json.dumps(data) }
                    response = requests.post(url, params=param_data, headers=headers)
                    msg = response.json()
                    if msg['result'] == 'success':
                        success = 2

                user = User()
                user.username = request.POST.get('username', None)
                user.set_password(request.POST.get('password1', None))
                user.email = request.POST.get('email', None)
                user.gender = request.POST.get('gender', None)
                user.birth_year = request.POST.get('birth_year', None)
                user.birth_month = request.POST.get('birth_month', None)
                user.birth_date = request.POST.get('birth_date', None)
                user.type = 2
                user.status = 1
                user.save()
        return redirect('/signup'+str(success)+'/done/')
    else:
        return render(request, 'account/signup.html', {})

# 계정정보 획득
@login_required
def get_myinfo(request):
    utype = ['가맹점회원', '일반회원', '관리자계정']
    gender = ['남자', '여자']
    return render(request, 'account/myinfo.html', {'utype': utype[request.user.profile.type - 1], 'gender': gender[request.user.profile.gender - 1]})

# 본인인증
@login_required
def identity(request, op=None, s_id=None):
    if request.method == 'POST':
        username = request.user.username
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if op == 'u_edit':
                return redirect('account:edit')
            elif op == 's_edit':
                return redirect('store:edit')
            elif op == 's_del':
                s_id = request.POST.get('s_id', None)
                return redirect('/store/'+s_id+'/delete')
        else:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
        
    data = {}
    if op == 'u_edit':
        data['title'] = '계정관리'
        data['url'] = 'account:info'
    elif op == 's_edit':
        data['title'] = '가맹점 관리'
        data['url'] = 'store:info'
    elif op == 's_del':
        data['title'] = '가맹점 관리'
        data['s_id'] = s_id
        data['url'] = 'store:info'
    data['op'] = op
    return render(request, 'account/identity.html', dict(data=data))
    
# 정보수정
@login_required
def account_edit(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.pk)
        profile = get_object_or_404(Profile, user_id=request.user.pk)
        user.email = request.POST.get('email', None)
        profile.gender = request.POST.get('gender', None)
        profile.birth_year = request.POST.get('birth_year', None)
        profile.birth_month = request.POST.get('birth_month', None)
        profile.birth_date = request.POST.get('birth_date', None)
        user.save()
        profile.save()
        return redirect('account:info')
    return render(request, 'account/account_edit.html', {})

# 비밀번호 변경
@login_required
def change_pwd(request):
    if request.method == 'POST':
        user = get_object_or_404(User, pk=request.user.pk)
        old_pwd = request.POST.get('password', None)
        validated_pwd = authenticate(username=user.username, password=old_pwd)
        if validated_pwd is not None:
            new_pwd = request.POST.get('password1', None)
            user.set_password(new_pwd)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('account:info')
        else:
            messages.error(request, '현재 비밀번호가 일치하지 않습니다.')
            return redirect('account:chg_pwd')
    return render(request, 'account/password_edit.html', {})