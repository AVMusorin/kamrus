# coding: utf-8

from django import forms


SORT = (
    ('priceDown', u'Цена по возрастанию'),
    ('priceUp', u'Цена по убыванию'),
    ('last', u'Последние поступления'),
)          

class SortForm(forms.Form):
    ''' With this form user can choose
        how to sort goods '''


    sort = forms.ChoiceField(required = False, widget = forms.Select, choices = SORT, label='Сортировать')    

        
