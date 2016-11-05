# coding: utf-8

from django import forms
from django.contrib.auth.models import User  
from login_logout.models import ExtendedUserForm  
from django.core.exceptions import ObjectDoesNotExist

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def clean_username(self):
        raise form.ValidationError('RRRRRRRRRRRRRRRR')

    def clean_email(self):

        ''' Check unique of email '''

        email = self.cleaned_data['email']
        try:
            User.objects.get(email = email)
        except  ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Такой адрес электронной почты уже зарегистрирован') 


class ExtendedUserForm(forms.ModelForm):
    class Meta:
        model = ExtendedUser
        fields = ['phone_number']
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))



