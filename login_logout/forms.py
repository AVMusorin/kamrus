# coding: utf-8

from django import forms
from django.contrib.auth.models import User  
from .models import ExtendedUser  
from django.core.exceptions import ObjectDoesNotExist

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
    username = forms.CharField(error_messages={'required': 'Введите ваше имя'}, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(error_messages={'required': 'Введите почту'}, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(error_messages={'required': 'Введите пароль'}, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


    def clean_email(self):

        ''' Check unique of email '''

        email = self.cleaned_data['email']
        try:
            User.objects.get(email = email)
        except  ObjectDoesNotExist:
            return email
        raise forms.ValidationError('Такой адрес электронной почты уже зарегистрирован')  


    def save(self, commit = True):

        ''' Make user isn't active before he opens activation key '''

        user = super(UserForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False
            user.save()
        return user

class ExtendedUserForm(forms.ModelForm):
    class Meta:
        model = ExtendedUser
        fields = ['phone_number']
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))



class ResetPasswordForm(forms.Form):
    email = forms.CharField(error_messages={'required': 'Введите почту'}, required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))