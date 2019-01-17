from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse, HttpResponse
from .models import Store, Category, Location, Photo
from .forms import StoreForm, PhotoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template import loader
import json, datetime

# Create your views here.

class StoreDV(DetailView):
    model = Store
    context_object_name = 'store'
    template_name = 'store/myStore_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StoreDV, self).get_context_data(**kwargs)
        return context
        

class StorePV(ListView):
    model=Photo
    paginate_by = 12
    context_object_name = 'photos'
    template_name = 'store_list.html'

    def get_context_data(self, **kwargs):
        context = super(StorePV, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)
        
        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

    def get_queryset(self, **kwargs):
        queryset = Photo.objects.filter(Q(store__status='a')) # filter returns a list so you might consider skip except part
        return queryset


class filteredStoresPV(ListView):
    model=Photo
    paginate_by = 12
    context_object_name = 'photos'
    template_name = 'store_list.html'

    def get_context_data(self, **kwargs):
        context = super(filteredStoresPV, self).get_context_data(**kwargs)
        paginator = context['paginator']
        page_numbers_range = 5  # Display only 5 page numbers
        max_index = len(paginator.page_range)

        page = self.request.GET.get('page')
        current_page = int(page) if page else 1

        start_index = int((current_page - 1) / page_numbers_range) * page_numbers_range
        end_index = start_index + page_numbers_range
        if end_index >= max_index:
            end_index = max_index

        page_range = paginator.page_range[start_index:end_index]
        context['page_range'] = page_range
        return context

    def get_queryset(self, **kwargs):
        loc = self.kwargs.get('loc',None)
        if loc == 4:
            search_query = self.request.GET.get('search_box', None)
            queryset = Photo.objects.filter(Q(store__name__icontains=search_query) & Q(store__status='a') ) # filter returns a list so you might consider skip except part
        else:
            queryset = Photo.objects.filter(Q(store__status='a') & Q(store__location=loc))
        return queryset


def detailView (request, store_id=None):
    store = get_object_or_404(Store, pk=store_id)
    photo = get_object_or_404(Photo, store_id=store.pk)
    return render(request, 'store_list_detail.html', dict(store=store, photo=photo))


class StoreDPV(DetailView):
    model = Photo
    context_object_name = 'photo'


def store_edit(request):
    user = request.user.pk
    store_id = request.POST.get("store_id", None)
    op = request.POST.get("op", None)

    if store_id != None and store_id != "None":
        store = get_object_or_404(Store, pk=store_id)
        photo = get_object_or_404(Photo, store=store)
    else:
        store = Store()
        photo = Photo()

    if request.method == "POST" and op != "template":
        form = StoreForm(request.POST, instance=store)
        photo_form = PhotoForm(request.POST, request.FILES, instance=photo)

        if form.is_valid():
            store = form.save(commit=False)
            store.store_id = store_id
            store.representative = User(user)
            store.status = "w"
            store.save()

            if photo_form.is_valid():
                photo = ""
                try:
                    photo = get_object_or_404(Photo, store_id=store.id)
                    photo.image = request.FILES['image']
                except:
                    photo = Photo(store=store, image=request.FILES['image'])
                photo.save()
                
        return redirect('profile:account_myInfo', request.user.pk)

    else:
        category = Category.objects.all().order_by('id')
        category_list = []
        for domain in category:
            temp = {
                'id' : domain.id,
                'domain' : domain.domain
            }
            category_list.append(temp)
        categorys = {
            'categoty_list' : category_list
        }
        json_category = json.dumps(category_list)
        
        location = Location.objects.all().order_by('id')
        location_list = []
        for loc in location:
            temp = {
                'id' : loc.id,
                'loc' : loc.loc
            }
            location_list.append(temp)
        locations = {
            'location_list' : location_list
        }
        json_location = json.dumps(location_list)
        return render(request, 'store/myStore_edit.html', dict(categorys=json_category, locations=json_location, store=store, photo=photo))


def store_remove(request):
    store_id = request.POST.get("del_id")
    store = get_object_or_404(Store, pk=store_id)
    store.status = "d"
    store.save()
    return redirect('profile:account_myInfo', request.user.pk)


def get_myStore(request):
    u_id = request.GET.get('u_id', None)
    store = Store.objects.filter(Q(representative=u_id) & ~Q(status='d'))
    photo = None

    data = {}
    if len(store) != 0:
        photo = Photo.objects.filter(Q(store_id=store[0].id))
        data = {
            'u_id'              : u_id,
            'id'                : store[0].id,
            'name'              : store[0].name,
            'corporate_number'  : store[0].corporate_number,
            'category'          : get_object_or_404(Category, id=store[0].category_id).domain,
            'location'          : get_object_or_404(Location, id=store[0].location_id).loc,
            'address'           : store[0].address,
            'phone_number'      : store[0].phone_number,
            'url'               : store[0].url,
            'opening_time'      : store[0].opening_hour + " : " + store[0].opening_minute,
            'closing_time'      : store[0].closing_hour + " : " + store[0].closing_minute,
            'registered_date'   : (store[0].registered_date).strftime('%Y-%m-%d %H:%M:%S'),
            'modified_date'     : (store[0].modified_date).strftime('%Y-%m-%d %H:%M:%S'),
            'status'            : store[0].status,
            'photo'             : photo[0].image.thumb_url
        }

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json;charset=UTF-8")

def get_QRcode(request):
    s_id = request.POST.get('s_id')
    store = get_object_or_404(Store, pk=s_id)
    return render(request, 'store/myStoreQRcode.html', dict(s_id=store.id, s_rid=store.representative_id, s_name=store.name))