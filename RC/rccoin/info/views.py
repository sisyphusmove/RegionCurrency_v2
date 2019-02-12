from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import ListView

from info.models import Notice
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import json
# from django.contrib.auth.decorators import login_required

# Create your views here.

# def notice_view(request):
class NoticeLV(ListView):
    template_name = 'notice/notice_list.html'
    model = Notice
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        input_page = self.request.GET.get('page', )
        if input_page == None:
            input_page = 1
        print(input_page)
        context = {}
        notices = Notice.objects.filter(status='Y').order_by('-modify_date')
        contents_per_page = 11

        paginator = Paginator(notices, contents_per_page)
        this_page = paginator.page(input_page)
        print(this_page)
        # boards = this_page.object_list

        context = {}
        notice_list = []
        for li in list(this_page):
            temp = {}
            temp['id'] = li.id
            temp['title'] = li.title
            temp['content'] = li.content
            temp['status'] = li.status
            temp['modify_date'] = str(li.modify_date)[0:10]
            notice_list.append(temp)

        context['notice_list'] = notice_list
        temp_list = []
        context['remain_of_page'] = [ remain for remain in range(contents_per_page - len(this_page)) ]
        context['current_page'] = input_page
        context['max_page'] = contents_per_page
        context['num_pages'] = [ num + 1 for num in range(paginator.num_pages) ]
        context['has_prev'] = this_page.has_previous()
        context['has_next'] = this_page.has_next()
        context['start_index'] = this_page.start_index()

        if context['has_prev']:
            context['prev_page'] = this_page.previous_page_number()
        if context['has_next']:
            context['next_page'] = this_page.next_page_number()
        print(context)
        return context