from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserForm, ExtendedUserForm, ResetPasswordForm
from django.contrib import messages 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import ActivationUser, ExtendedUser
import datetime, hashlib, random
from django.contrib.auth.models import User
from django.core.mail import send_mail
import datetime
import pytz
from django.core.exceptions import ObjectDoesNotExist

def user_login(request):
    ''' Функция для входа в систему'''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Проверить сущетсвует ли такой пользователь в базе
        user = authenticate(username=username, password=password)
        if user:
            # если существует и активен
            if user.is_active:
                # Пропустить пользователя и дать ему сессию
                login(request, user)
                return HttpResponse('Вы авторизировались успешно!')
            else:
                return HttpResponse('Ваш аккаунт - неактивен')
        else:
            # Сформировать сообщение для пользователя
            messages.add_message(request, messages.ERROR, u'Введены неправильные имя пользователя и пароль')
            return render(request, 'login.html', {})
    else:
        return render(request, 'login.html', {})


def generation_activation_key(email):
    ''' produce activation key in format '2da8306c94fe3a74b67c62e97c46ae403701277d' '''
    salt = hashlib.sha1((str(random.random())).encode('utf-8')).hexdigest()[:5]
    activation_key = hashlib.sha1((salt+email).encode('utf-8')).hexdigest()
    return activation_key    


def generation_key_expires(days=1):
    ''' Создает дату крайнего срока активации аккаунта '''
    key_expires = datetime.datetime.now() + datetime.timedelta(days)
    return key_expires
  

def send_email_to_user(email, email_subject, email_body):
    send_mail(email_subject, email_body, 'kamrusshop@gmail.com',[email], fail_silently=False)


def registration(request):
    '''Регистрация нового пользователя
    
       Пользователь присылает форму с контактнымми данными, после чего они проверяются на валидность,
       сравниваются пароль и его подтверждение. Валидность email проверяется на клиенте с помощью 
       встроенной проверки bootstrap. После проверки хэшируется пароль и пользователь сохранятся в базу,
       генерируется код подтверждения и отправляется пользователю на почту.
    '''
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_user_form = ExtendedUserForm(request.POST)
        if user_form.is_valid() and profile_user_form.is_valid():
            if request.POST.get('password') == request.POST.get('password2'):
                user = user_form.save()
                # hasing password with set_password
                user.set_password(user.password)
                # resave user
                user.save() 
                phone_number = profile_user_form.cleaned_data['phone_number']
                username = user_form.cleaned_data['username']
                # save dates from form in the model 
                profile_form = ExtendedUser(user = user, phone_number = phone_number)  
                profile_form.save()
                email = user_form.cleaned_data['email']
                activation_key = generation_activation_key(email)
                key_expires = generation_key_expires()
                activation_form = ActivationUser(user = user, activation_key = activation_key, key_expires = key_expires)
                activation_form.save()
                email_subject = 'Подтверждение регистрации'
                # TODO: Брать домен из настроек 
                email_body = "Добро пожаловать, %s, спасибо, что зарегестрировались. Чтобы активировать аккаунт, перейдите по ссылке в течение 24 часов http://127.0.0.1:8000/account/confirm/%s" % (username, activation_key)
                send_email_to_user(email, email_subject, email_body)
                messages.add_message(request, messages.SUCCESS, u'Регистрация прошла успешно, Вам на почту отправлено письмо для подтверждения!')
            else:
                messages.add_message(request, messages.ERROR, u'Пароли не совпадают')      
        else:
            messages.add_message(request, messages.ERROR, u'Ошибка при вводе данных')
    else:
        user_form = UserForm()
        profile_user_form = ExtendedUserForm()
    return render(request, 'registration.html', {'user_form' : user_form, 
                                                 'profile_user_form' : profile_user_form})


def get_activation_key(request):
    ''' Вернет ключ активации из запроса '''
    return request.path.split('/')[-2]


def registration_confirm(request, **kwargs):
    ''' Подтверждение регистрации '''
    # if request.user.is_authenticated():
    #     return HttpResponseRedirect('/')  
    activation_key = get_activation_key(request)
    try:
        user_profile = ActivationUser.objects.get(activation_key = activation_key)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, 'Ключ активации отсутствует')
        return HttpResponseRedirect('/account/login/')
    if user_profile.key_expires > pytz.utc.localize(datetime.datetime.now()):
        user = user_profile.user
        user.is_active = True
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Регистрация успешно завершена!')
        return HttpResponseRedirect('/account/login/') 
    else:
        return HttpResponseRedirect('/account/registration/') 


@login_required(login_url='/account/login/')                
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')   


def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # generating new random password
            try:
                user = User.objects.get(email = email)
            except ObjectDoesNotExist:
                messages.add_message(request, messages.ERROR, u'Не найдено пользователя с таким email')
                return render(request, 'reset_password.html', {'form': ResetPasswordForm()})
            new_password = hashlib.sha1((str(random.random())).encode('utf-8')).hexdigest()[:8]
            extended_user = ExtendedUser.objects.get(user=user)
            extended_user.new_password = new_password
            extended_user.save()

            activation_key = generation_activation_key(email)
            key_expires = generation_key_expires()
            # change dates in the base 
            activation_user = ActivationUser.objects.get(user = user)
            activation_user.activation_key = activation_key
            activation_user.key_expires = key_expires
            activation_user.save()
            email_subject = 'Обновление пароля'
            email_body = "Hey %s, this is your new password %s. To activate it, click this link within \
            48hours http://127.0.0.1:8000/account/confirm/%s" % (user.username, new_password, activation_key)
            send_email_to_user(email, email_subject, email_body) 
            print (activation_key)
            messages.add_message(request, messages.SUCCESS, u'Письмо отправлено на почту!')
            return render(request, 'success.html')
    else:
        form = ResetPasswordForm()
        return render(request, 'reset_password.html', {'form':form})


def confirm_newpassword(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/catalog/')  
    activation_key = get_activation_key(request)
    try:
        user_profile = ActivationUser.objects.get(activation_key = activation_key)
    except ObjectDoesNotExist:
        messages.add_message(request, messages.ERROR, u'Ошибка системы, ключ активации отсутвует')
        return HttpResponseRedirect('/account/reset_password/')
    if user_profile.key_expires > pytz.utc.localize(datetime.datetime.now()):  # переводит в UTC timezone 
        user = user_profile.user
        new_password = ExtendedUser.objects.get(user=user).new_password
        user.set_password(new_password)
        user.save()
        messages.add_message(request, messages.SUCCESS, u'Пароль успешно изменен!')
        return HttpResponseRedirect('/account/login/') 
    else:
        return HttpResponseRedirect('/account/registration/') 


