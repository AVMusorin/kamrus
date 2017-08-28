from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import ExtendedUser, ActivationUser
from .views import generation_activation_key
from django.core import mail
import datetime

class AuthorizationTestCase(TestCase):

    def setUp(self):
        self.name = "test"
        self.email = "test@example.ru"
        self.password = "Qq143005"
        self.password2 = "Qq143005"
        self.phone_number = "89099994455"


    def test_user_login(self):
        client = Client()
        user = User.objects.create_user(self.name, self.email, self.password)
        if not user.is_active:
            user.is_active = True
            user.save()
        response = client.post('/account/login/', {"username": self.name, "password": self.password})
        self.assertEqual(response.content.decode('utf-8'), "Вы авторизировались успешно!")


    def test_registration(self):
        client = Client()
        response = client.post('/account/registration/', {"username":self.name,
                                                         "email":self.email,
                                                         "password":self.password,
                                                         "password2":self.password2,
                                                         "phone_number":self.phone_number})
        user = User.objects.get(username=self.name)
        extended_user = ExtendedUser.objects.get(user=user)
        activation_user = ActivationUser.objects.get(user = user)
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.email, self.email)
        self.assertEqual(extended_user.phone_number, self.phone_number)
        self.assertNotEqual(activation_user.activation_key, None)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Регистрация прошла успешно", response.content.decode('utf-8'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Подтверждение регистрации")


    def test_generation_activation_key(self):
        self.assertEqual(40, len(generation_activation_key(self.email)))


    def _create_user(self, is_active=False):
        user = User.objects.create_user(
            username=self.name, email=self.email, password=self.password)
        user.is_active = is_active
        user.save()
        return user


    def _create_activation_user(self, user):
        activation_key = "2da8306c94fe3a74b67c62e97c46ae403701277d"
        activation_user = ActivationUser.objects.create(user=user, 
                                                        activation_key = activation_key,
                                                        key_expires=datetime.datetime.now() + datetime.timedelta(1))
        activation_user.save()
        return activation_user


    def _create_extended_user(self, user):
        extended_user = ExtendedUser.objects.create(user=user, phone_number=self.phone_number)
        extended_user.save()
        return extended_user


    def test_registration_confirm(self):
        user = self._create_user()
        activation_user = self._create_activation_user(user)
        activation_key = activation_user.activation_key
        client = Client()
        response = client.get('/account/confirm/{}/'.format(activation_key))
        self.assertRedirects(response, '/account/login/')
        self.assertEqual(User.objects.get(username=self.name).is_active, True)


    def test_reset_password(self):
        new_password = 'Ww143005'
        client = Client()
        user = self._create_user(is_active=True)
        self._create_activation_user(user)
        self._create_extended_user(user)
        response = client.post("/account/reset_password/", {'email':self.email})
        extended_user = ExtendedUser.objects.get(user=user)
        self.assertNotEqual(extended_user.new_password, None)
        self.assertIn("Для активации нового пароля перейдите поссылке,", response.content.decode('utf-8'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Обновление пароля")


    def test_confirm_newpassword(self):
        new_password = 'Ww143005'
        user = self._create_user(is_active=True)
        activation_user = self._create_activation_user(user)
        extended_user = self._create_extended_user(user)
        extended_user.new_password = new_password
        extended_user.save()
        client = Client()
        response = client.get("/account/confirm_newpassword/{}/".format(activation_user.activation_key))
        self.assertEqual(User.objects.get(username=self.name).check_password(new_password), True)
        self.assertRedirects(response, '/account/login/')
