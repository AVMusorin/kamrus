# coding: utf-8

from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Category, Good
from .forms import SortForm
from django.shortcuts import redirect
from mixins.general_mixins import CategoryListMixin
from django.contrib.auth.mixins import LoginRequiredMixin

class CategoryView(ListView):

    ''' Shows all categories'''

    model = Category
    template_name = 'catalog.html'
    goods = None


class CategoryDetailView(LoginRequiredMixin, ListView):

    ''' When category is chosen, this view shows 
        all good in this chosen category

        input date: category_id 
        output date: list of all goods with category_id '''

    login_url = '/account/login/'
    template_name = 'detail_catalog.html'
    category_id = None
    model = Good

    def get(self, request, *args, **kwargs):

        ''' returns goods depending of sort '''

        self.category_id = kwargs['id']
        # print (request.session.keys())
        # for i in request.session.keys():
        #     print (request.session[i])
        return super(CategoryDetailView,self).get(request, *args, **kwargs)

    def sort_goods(self, request):
        if 'sort' in request.GET:
            if request.GET['sort'] == 'priceUp':
                self.goods = Good.objects.filter(category = self.category_id).order_by('-price')
            elif request.GET['sort'] == 'priceDown':
                self.goods = Good.objects.filter(category = self.category_id).order_by('price')
            elif request.GET['sort'] == 'last':
                self.goods = Good.objects.filter(category = self.category_id).order_by('-createDate')
            else:
                self.goods = Good.objects.filter(category = self.category_id)
        else:
            self.goods = Good.objects.filter(category = self.category_id)
        return self.goods    

    def search_goods(self, request):
        result = False
        if 'search' in request.GET:
            search = request.GET['search']
            result = Good.objects.filter(name__icontains=request.GET['search'])
            if len(result) == False:        
                result = u'По запросу "%s"  ничего не найдено' %search     
        return result       
            

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['goods'] = self.sort_goods(self.request)
        context['sort'] = SortForm() 
        context['search'] = self.search_goods(self.request)
        return context    

