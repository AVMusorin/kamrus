# coding: utf-8

from django.db import models
from datetime import datetime

class Category(models.Model):
    name = models.CharField(max_length=30, unique = True, verbose_name='Название категории')
    createDate = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    description = models.TextField(blank= True, null = True, verbose_name='Описание категории', help_text='Необязательное поле')
    relative = models.ForeignKey('self', blank = True, null = True, on_delete = models.SET_NULL, 
                                 verbose_name='Категории', help_text='Необязательное поле')
    class Meta:
        ordering = ['createDate']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Good(models.Model):
    name = models.CharField(max_length=30, unique = True, verbose_name = 'Название товара')
    createDate = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')     
    description = models.TextField(blank= True, null = True, verbose_name='Описание товара')
    in_stock = models.BooleanField(default = True, verbose_name= 'В наличии')
    price = models.FloatField(verbose_name = 'Цена')
    category = models.ForeignKey(Category, verbose_name='Категория')
    complited = models.BooleanField(default = False, verbose_name = 'Выполнено')
    class Meta:
        ordering = ['createDate']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        display_string = self.name + ' '
        if self.in_stock:
            display_string += 'в наличии' + ' '
        else:
            display_string += 'нет в наличии' + ' '
        if self.complited:
            display_string += 'ВЫПОЛНЕНО'
        else:
            display_string += 'НЕ ВЫПОЛНЕНО'    
        return display_string        




