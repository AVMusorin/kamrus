# coding: utf-8

from django.contrib import admin
from .models import Category, Good

def update_complited(modeladmin, reguest, queryset):

    ''' Change uncomplited to complited '''
    
    queryset.update(complited = True)
update_complited.short_description = "Отметить выбранные как ВЫПОЛНЕНО"    

class CategoryAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'relative')
    search_fields = ['name']

class GoodAdmin(admin.ModelAdmin):
    actions = [update_complited]
    search_fields = ['name']
    list_filter = ['complited']
    list_display = ['name', 'price','complited' ]


admin.site.register(Good, GoodAdmin)
admin.site.register(Category, CategoryAdmin)