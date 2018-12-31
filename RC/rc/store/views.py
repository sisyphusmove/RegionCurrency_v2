from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, View
from django.http import JsonResponse, HttpResponse
from .models import Store, Category, Location, Photo
from .forms import StoreForm, PhotoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template import loader
import json

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
            queryset = Photo.objects.filter(store__name__icontains=search_query) # filter returns a list so you might consider skip except part
        else:
            queryset = Photo.objects.filter(location=loc)
        return queryset


def detailView (request, store_id=None):
    store = get_object_or_404(Store, pk=store_id)
    photo = get_object_or_404(Photo, store_id=store.pk)
    return render(request, 'store_list_detail.html', dict(store=store, photo=photo))
    
    # def store_list(request):
    #     photo_list = User.objects.all()
    #     print("##########################")
    #     page = request.GET.get('page', 1)
    #     paginator = Paginator(photo_list, 12)
    #     photos = paginator.page(1)

    #     try:
    #         photos = paginator.page(page)
    #     except PageNotAnInteger:
    #         photos = paginator.page(1)
    #     except EmptyPage:
    #         photos = paginator.page(paginator.num_pages)

    #     return render(request, "store/store_list.html",{'photos': photos})    
    

class StoreDPV(DetailView):
    model = Photo
    context_object_name = 'photo'


def store_edit(request, store_id=None):
    user = request.user.pk

    if store_id:
        store = get_object_or_404(Store, pk=store_id)
        photo = get_object_or_404(Photo, store=store)
    else:
        store = Store()
        photo = Photo()

    if request.method == "POST":
        form = StoreForm(request.POST, instance=store)
        photo_form = PhotoForm(request.POST, request.FILES)

        if form.is_valid():
            store = form.save(commit=False)
            store.store_id = store_id
            store.representative = User(user)
            store.status = "w"
            store.save()

            if photo_form.is_valid():
                photo = Photo(store=store, image=request.FILES['image'])
                photo.save()

        return redirect('profile:account_myInfo', request.user.pk)

    else:
        form = StoreForm(instance=store)
        photo_form = PhotoForm(instance=photo);
        category = Category.objects.all().order_by('id')
        location = Location.objects.all().order_by('id')
        return render(request, 'store/myStore_edit.html', dict(form=form, photo_form=photo_form, categorys=category, locations=location, store=store))


def store_remove(request, store_id=None):
    store = get_object_or_404(Store, pk=store_id)
    store.status = "d"
    store.save()
    return redirect('profile:account_myInfo', request.user.pk)


def get_myStore(request):
    u_id = request.GET.get('u_id', None)
    result = Store.objects.filter(Q(representative=u_id))
    
    data={}
    for store in result:
        try:
            photo = get_object_or_404(store_id=store.id)
        except:
            photo = ""
        print(photo)
        data = {
            'id'                : store.id,
            'name'              : store.name,
            'corporate_number'  : store.corporate_number,
            'category'          : get_object_or_404(Category, id=store.category_id).domain,
            'location'          : get_object_or_404(Location, id=store.location_id).loc,
            'address'           : store.address,
            'phone_number'      : store.phone_number,
            'url'               : store.url,
            'opening_time'      : store.opening_hour + " : " + store.opening_minute,
            'closing_time'      : store.closing_hour + " : " + store.closing_minute,
            'description'       : store.description,
            'registered_date'   : (store.registered_date).strftime('%Y-%m-%d'),
            'modified_date'     : (store.modified_date).strftime('%Y-%m-%d'),
            'status'            : store.status,
            'photo'             : photo
        }

    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type="application/json;charset=UTF-8")