from django.contrib import admin
from .models import ExtendedUser, ActivationUser
# Register your models here.

class ProfileUserAdmin(admin.ModelAdmin):
    search_fields = ['name', ]
    list_display = ['user', 'email','phone_number' ]
admin.site.register(ExtendedUser)
admin.site.register(ActivationUser)