# coding: utf-8


from catalog.models import Good
from django.views.generic.base import ContextMixin
from django.shortcuts import render
from django.contrib.auth.models import User

class CategoryListMixin(ContextMixin):

    ''' input: request.get
        if True, html shows result of search 
        else html shows that it found nothing
        output: result (list) / None
    '''  

    def get_context_data(self, **kwargs):
        context = super(CategoryListMixin, self).get_context_data(**kwargs)
        context['current_url'] = self.request.path      
        return context
