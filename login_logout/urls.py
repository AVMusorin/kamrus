from django.conf.urls import url
from .views import *

urlpatterns = [
  url(r'^login/', user_login, name='login'),
  url(r'^registration/', registration, name='registration'),
  url(r'^logout/', user_logout, name='logout'),
  url(r'^confirm/\w+/', registration_confirm, name = 'registration_confirm'),
  url(r'^reset_password/', reset_password, name = 'resetpassword'),
  url(r'^confirm_newpassword/\w+/', confirm_newpassword, name = 'confirmnewpassword'),
]