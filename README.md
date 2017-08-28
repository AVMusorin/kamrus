# login_logout

Система авторизации пользователей через электронную почту включает в себя:
* регистрация нового пользователя с подтверждением по email;
* вход пользователя в систему;
* выход пользователя из системы;
* восстановление пароля по email;

### Использование:
1. Добавить login_logout в INSTALLED_APPS
2. Для корректной работы шаблонов необходимо добавить файлы bootstrap в static https://github.com/twbs/bootstrap
3. Настроить почту для отправки сообщений [Django docs](https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-EMAIL_HOST)
