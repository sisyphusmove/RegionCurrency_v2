from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.models import User

# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': "test",
    }
    return HttpResponse(template.render(context, request))

def intro(request):
    template = loader.get_template('intro.html')
    context = {
        'latest_question_list': "test",
    }
    return HttpResponse(template.render(context, request))


def map(request):
    template = loader.get_template('map.html')
    context = {
        'latest_question_list': "test",
    }
    return HttpResponse(template.render(context, request))

# check logged user
class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class UserCreateView(CreateView):
    template_name = "registration/register.html"
    

    # def form_valid(self, form):
    #     user = User.objects.create_user(
    #         self.form.username,
    #         self.form.password1,
    #         self.form.email,
    #         self.form.age,
    #         'U',
    #         'Y'
    #         )
    #     user.save()


class UserCreateDone(TemplateView):
    template_name = "registration/register_done.html"