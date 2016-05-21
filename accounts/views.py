# coding=utf-8
import random
from django.shortcuts import render, redirect
from django.core import signing
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils import timezone
from django.http import Http404
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ChangePasswordForm, UserResetPassForm
from .models import User, UserActivation
from accounts import mail_sending
from urllib.request import urlopen
from io import BytesIO
from django.core.files import File


@csrf_protect
def login_view(request):
    # if request.user.is_authenticated():
    #     return redirect('index_view')
    template = 'accounts/login.html'
    shortcut = lambda: render(request, template, {"form": form})
    form = UserLoginForm(request.POST or None)
    if form.is_valid:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=email, password=password)
        if user:
            if not user.banned and user.is_active:
                auth.login(request, user)
                return redirect('/')
            else:
                return shortcut()
        else:
            return shortcut()
    else:
        return shortcut()


def logout_view(request):
    auth.logout(request)
    return redirect('/')


def register_view(request):
    form = UserRegistrationForm(request.POST or None, request.FILES or None)
    if request.user.is_authenticated():
        return redirect('/')
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            activation_key = signing.dumps({'email': email})
            user = User.objects.get(email=email)
            UserActivation.objects.filter(user=user).delete()
            new_activation = UserActivation(user=user, activation_key=activation_key,
                                            request_time=timezone.now())
            new_activation.save()
            mail_sending.confirm_email(email, activation_key)
            user = auth.authenticate(username=email, password=password)
            auth.login(request, user)

            return redirect('/')
        else:
            messages.warning(request, "Здесь есть неверно заполненные поля!")
            return render(request, 'accounts/register.html', {'form': form})
    return render(request, 'accounts/register.html', {'form': form})


def register_confirm(request, activation_key):
    user_profile = UserActivation.objects.get(activation_key=activation_key)
    if not user_profile:
        raise Exception("Неверный код")
    else:
        user_profile.confirm_time = timezone.now()
        user_profile.save()
        user = user_profile.user
        user.is_active = True
        user.save()
        if not request.user.is_authenticated():
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
        return render(request, 'accounts/confirm_reg.html', {})
#
#
# def user_view(request, user_id):
#     try:
#         user = User.objects.get(id=user_id)
#     except ObjectDoesNotExist:
#         raise Http404("Такого пользователя не существует")
#     context = {'user': user}
#
#     if request.user.pk == user.pk:
#         context['current'] = True
#     return render(request, 'user.html', context)
#
#
# def users_view(request):
#     try:
#         query = request.GET.__getitem__('q')
#         users = User.objects.filter(first_name__icontains=query) | User.objects.filter(last_name__icontains=query) | User.objects.filter(phone__icontains=query)
#         context = {'users': users, 'query': query}
#     except KeyError:
#         context = {'users': User.objects.all().order_by('-last_login')}
#     return render(request, 'users.html', context)
#
#
# @login_required
# def user_update_view(request):
#     user = User.objects.get(email=request.user.email)
#     form = UserUpdateForm(request.POST or None, request.FILES or None, instance=user)
#
#     if 'code' in request.GET:
#         code = request.GET['code']
#         try:
#             access_token, user_id = vkontakte.auth_code(code, reverse('user_update_view'))
#         except vkontakte.AuthError as e:
#             messages.warning(request, u'Ошибка OAUTH авторизации {}'.format(e), extra_tags='integration')
#             return redirect('user_update_view')
#         try:
#             user = User.objects.get(vkuserid=user_id)
#             messages.warning(request, 'Этот аккаунт ВКонтакте уже связан с профилем', extra_tags='integration')
#             return redirect('user_update_view')
#         except User.DoesNotExist:
#             user = User.objects.get(email=request.user.email)
#             user.vkuserid = user_id
#             user.save()
#             messages.success(request, "Профиль ВКонтакте прикреплен", extra_tags='integration')
#             return redirect('user_update_view')
#
#     elif request.POST:
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Успешно сохранено!", extra_tags='info')
#             return redirect('user_update_view')
#         else:
#             messages.warning(request, "Некорректные данные", extra_tags='info')
#     return render(request, 'user_update.html', {'form': form, 'pass_form': ChangePasswordForm})
#
#
# @login_required
# def changepass(request):
#     user = User.objects.get(email=request.user.email)
#     pass_form = ChangePasswordForm(request.POST or None)
#     if request.method == 'POST':
#         if pass_form.is_valid():
#             password = pass_form.cleaned_data.get("password")
#             user.set_password(password)
#             user.save()
#             validation = auth.authenticate(username=user.email, password=password)
#             auth.login(request, validation)
#             messages.success(request, "Пароль изменен", extra_tags='changepass')
#         else:
#             messages.warning(request, "Введенные пароли некорректны!", extra_tags='changepass')
#     return redirect('user_update_view')
#
#
# @login_required
# def unsetvkid(request):
#     user = User.objects.get(email=request.user.email)
#     user.vkuserid = None
#     user.save()
#     messages.success(request, "Профиль ВКонтакте откреплен", extra_tags='integration')
#     return redirect('user_update_view')
#
#
# def resetpass(request):
#     form = UserResetPassForm(request.POST or None)
#     if request.method == 'POST':
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             new_pass = str(random.randint(100000, 999999))
#             user = User.objects.get(email=email)
#             user.set_password(new_pass)
#             user.save()
#             mailing.resetpass_email(email, new_pass)
#             messages.success(request, "Пароль изменен. Письмо отправлено на почту!")
#     return render(request, 'resetpass.html')