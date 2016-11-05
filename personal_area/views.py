from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from login_logout.models import ExtendedUser
from django.contrib.auth.models import User
from login_logout.forms import UserForm, ExtendedUserForm

# Create your views here.

@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        extended_form = ExtendedUserForm(request.POST)
    else: 
        user_form = UserForm()
        extended_form = ExtendedUserForm()
    return render(request, 'profile.html', {'user_form' : user_form, 'extended_form' : extended_form})




