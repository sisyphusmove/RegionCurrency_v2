from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User

import json,requests

from board.models import Board, Comment, BoardLiker
from django.db.models import Q

from board.forms import BoardForm

import datetime
from datetime import datetime as dt
from datetime import timedelta

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class BoardLV(ListView):
    # model = Board
    # context_object_name = 'boards'
    paginate_by = 10

    def __init__(self):
        self.user_type = 1

    def get_queryset(self):
        if self.request.user.username == '':
            queryset = Board.objects.filter(category=1)
        else:
            user = get_object_or_404(User, username=self.request.user.username)

            self.user_type = user.profile.type
            queryset = Board.objects.filter(category=self.user_type)
        return queryset

class BoardDV(DetailView):
    model = Board

    def get_context_data(self, **kwargs):
        context = super(BoardDV, self).get_context_data(**kwargs)

        added = self.object.count + 1
        board = get_object_or_404(Board, id=self.object.id)
        board.count = added
        board.save()

        comment_cnt = 0

        try:
            comment = get_object_or_404(Comment, board_id=self.object.id)
            comment_cnt = len(comment)
        except:
            comment_cnt = 0

        context['object'] = self.object
        context['comment_cnt'] = comment_cnt
        return context

def board_edit(request, board_id=None):

    user = request.user.pk

    if board_id:
        board = get_object_or_404(Board, pk=board_id)
    else:
        board = Board()

    if request.method == "POST":
        # POST 된 request 데이터를 가지고 Form 생성
        form = BoardForm(request.POST, instance=board)
        if form.is_valid():
            board = form.save(commit=False)
            board.board_id = Board(board_id)
            board.writer = User(user)
            board.save()
            # request 없이 페이지 이동만 한다.
        return redirect('board:list')
    else:
        # book instance에서 Form 생성
        form = BoardForm(instance=board)
        # 사용자의 request를 가지고 이동한다.
        return render(request, 'board/board_edit.html', dict(form=form, board=board))

def board_delete(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    board.delete()
    return redirect('board:list')

def get_comment(request):
    now = dt.now()
    board_id = request.GET.get('board_id', )

    comments = Comment.objects.filter(board_id=board_id)
    time_diff = ''

    # print(now.timetuple().tm_year)
    print(now.utctimetuple())

    # print(now.date() - comments[0].modify_date.date())
    data_list = []
    for li in comments:
        
        print(li.modify_date.utctimetuple().tm_year)
        print(li.modify_date.utctimetuple().tm_mon)
        print(li.modify_date.utctimetuple().tm_mday)
        print(li.modify_date.utctimetuple().tm_hour)
        print(li.modify_date.utctimetuple().tm_min)
        temp = {}
        temp['board_id'] = li.board_id.id
        temp['writer'] = str(li.writer.profile.user)
        temp['content'] = li.content
        if(now.timetuple().tm_year != li.modify_date.timetuple().tm_year):
            temp['time_diff'] = "{} 년 전 ".format(now.timetuple().tm_year - li.modify_date.timetuple().tm_year)
        elif(now.timetuple().tm_mon != li.modify_date.timetuple().tm_mon):
            temp['time_diff'] = "{} 달 전 ".format(now.timetuple().tm_mon - li.modify_date.timetuple().tm_mon)
        elif(now.timetuple().tm_mday != li.modify_date.timetuple().tm_mday):
            temp['time_diff'] = "{} 일 전 ".format(now.timetuple().tm_mday - li.modify_date.timetuple().tm_mday)
        elif (now.timetuple().tm_hour != li.modify_date.timetuple().tm_hour):
            temp['time_diff'] = "{} 시간 전 ".format(now.timetuple().tm_hour - li.modify_date.timetuple().tm_hour)
        elif (now.timetuple().tm_min != li.modify_date.timetuple().tm_min):
            temp['time_diff'] = "{} 분 전 ".format(now.timetuple().tm_min - li.modify_date.timetuple().tm_min)
        print(temp['time_diff'])
        temp['modify_date'] = str(li.modify_date)
        temp['status'] = li.status
        data_list.append(temp)
    json_format = json.dumps(data_list)

    return HttpResponse(json_format, content_type="application/json:charset=UTF-8")

def chg_board(request):

    board_type = request.GET.get('board_type', )
    input_page = request.GET.get('page', )
    category = request.GET.get('category')
    keyword = request.GET.get('keyword')

    contents_per_page = 10

    if input_page == None:
        input_page = 1

    if keyword:
        if category == "":
            board = Board.objects.filter(
                Q(writer__profile__type=board_type) & Q(title__icontains=keyword) | Q(writer__profile__user__username=keyword) | Q(content__icontains=keyword)).distinct()
        elif category == "title":
            board = Board.objects.filter(
                Q(writer__profile__type=board_type) & Q(title__icontains=keyword)).distinct()
        elif category == "writer":
            board = Board.objects.filter(
                Q(writer__profile__type=board_type) & Q(writer__profile__user__username=keyword)).distinct()
        elif category == "content":
            board = Board.objects.filter(
                Q(writer__profile__type=board_type) & Q(content__icontains=keyword)).distinct()
    else:
        board = Board.objects.filter(writer__profile__type=board_type)

    paginator = Paginator(board, contents_per_page)
    this_page = paginator.page(input_page)
    # boards = this_page.object_list

    object = {}
    board_list = []
    for li in list(this_page):
        temp = {}
        temp['id'] = li.id
        temp['title'] = li.title
        temp['content'] = li.content
        temp['count'] = li.count
        temp['recommend'] = li.recommend
        temp['writer'] = str(li.writer)
        temp['create_date'] = str(li.create_date)[0:10]
        temp['modify_date'] = str(li.modify_date)[0:10]
        temp['category'] = li.category
        temp['get_absolute_url'] = li.get_absolute_url()
        board_list.append(temp)

    object['object'] = board_list
    object['current_page'] = input_page
    object['max_page'] = contents_per_page
    object['num_pages'] = paginator.num_pages
    object['has_prev'] = this_page.has_previous()
    object['has_next'] = this_page.has_next()
    object['start_index'] = this_page.start_index()

    if object['has_prev']:
        object['prev_page'] = this_page.previous_page_number()
    if object['has_next']:
        object['next_page'] = this_page.next_page_number()

    json_format = json.dumps(object)

    return HttpResponse(json_format, content_type="application/json:charset=UTF-8")

def write_comment(request):
    board_id = request.GET.get('board_id', )
    input_comment = request.GET.get('comment', )
    user = request.user.pk

    comment = Comment()

    comment.board_id = Board(board_id)
    comment.writer = User(user)
    comment.content = input_comment
    comment.status = 'y'

    try:
        comment.save()

        result = json.dumps([
            {'result': 'seccess'}
        ])

    except Exception as e:
        print(e)
        result = json.dumps([
            {'result':'fail'}
        ])

    return HttpResponse(result, content_type="application/json:charset=UTF-8")

def add_like(request):
    board_id = request.GET.get('board_id', )
    user_type = request.user.profile.type
    liker = request.user.pk

    board = get_object_or_404(Board, pk=board_id)
    like = BoardLiker()

    if_liked = BoardLiker.objects.filter(liker=liker, board=board_id)

    if user_type != 1 and user_type != 2:
        result = json.dumps([
            {'likes': 'notLogin'}
        ])
        return HttpResponse(result, content_type="application/json:charset=UTF-8")
    elif if_liked:
        result = json.dumps([
            {'likes': 'already'}
        ])
        return HttpResponse(result, content_type="application/json:charset=UTF-8")
    else:
        like.liker = User(liker)
        like.board = board
        like.save()

        added = board.recommend + 1
        board.recommend = added
        board.save()
        result = json.dumps([
            {'likes' : added }
        ])
        return HttpResponse(result, content_type="application/json:charset=UTF-8")

def test(request):
    return render(request, "board/test.html", ({}))



def board_search(request):
    userid = request.GET.get('userid', )
    board = Board.objects.filter(Q(writer_id=userid) & Q(status='Y')).order_by('-id')
    this_page_num = request.GET.get('this_page',1)
    board_list = []
    page_size = 5
    p = Paginator(board, page_size)
    # for li in list(board):
    for li in p.page(this_page_num):
        temp = {}
        temp['id'] = li.id
        if len(li.title) > 30 : temp['title'] = str(li.title)[0:30]+"..."
        else : temp['title'] = li.title
        temp['content'] = li.content
        temp['recommend'] = li.recommend
        temp['create_date'] = str(li.create_date)[0:10]
        temp['category'] = li.category
        temp['count'] = li.count
        board_list.append(temp)

    start_seq = p.count - (page_size * (int(this_page_num) - 1))
    res = {
        'start_seq' : start_seq,
        'a': board_list,
        'current_page_num' : this_page_num,
        'max_page_num' : p.num_pages
    }
    json_format = json.dumps(res)
    return HttpResponse(json_format, content_type="application/json:charset=UTF-8")
        
    