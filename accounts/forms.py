# coding=utf-8
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from django.utils import timezone
from django.contrib.auth import authenticate, get_user_model

now = timezone.now()
User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=email, password=password)
        user_qs = User.objects.filter(email=email)
        if user_qs.count() == 1:
            user = user_qs.first()
        if email and password:
            if not user:
                raise forms.ValidationError('Неверное сочетание Email/Password')
            if not user.check_password(password):
                raise forms.ValidationError('Неверное сочетание Email/Password')
            if not user.is_active:
                raise forms.ValidationError('Акктаунт дeактивирован. Обратитесь к администрации.')
            if user.banned:
                raise forms.ValidationError('Акктаунт забанен. Обратитесь к администрации.')
        return self.cleaned_data


class UserResetPassForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=150)


class UserRegistrationForm(forms.ModelForm):
    # TODO: Override all error messages
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = User.REGISTRATION_FIELDS
        dateTimeOptions = {
            'format': 'dd.mm.yy',
            'autoclose': True,
            'showMeridian': True,

        }
        year = now.year
        #TODO: 'bdate': forms.SelectDateWidget(),
        widgets = {'password': forms.PasswordInput(render_value=False),
                   'email': forms.EmailInput(),
                   'bdate': forms.SelectDateWidget(years=range(year, year-101, -1)),
                   }

    def clean_bdate(self):
        bdate = self.cleaned_data.get("bdate")
        if timezone.now().date() - bdate < timezone.timedelta(days=3650):
            raise forms.ValidationError("Тебе меньше 10 лет, серьезно?")
        return bdate

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.is_active = False
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('avatar', 'first_name', 'last_name', 'nickname','bdate', 'sex', 'steam_name', 'battle_tag', 'lol_name')
        dateTimeOptions = {
            'format': 'dd.mm.yy',
            'autoclose': True,
            'showMeridian': True,
        }


    def clean_bdate(self):
        bdate = self.cleaned_data.get("bdate")
        if timezone.now().date() - bdate < timezone.timedelta(days=3650):
            raise forms.ValidationError("Тебе меньше 10 лет, серьезно?")
        return bdate

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ChangePasswordForm(forms.Form):
    password_old = forms.CharField(label='Старый Пароль', widget=forms.PasswordInput)
    password = forms.CharField(label='Новый пароль', widget=forms.PasswordInput())
    password1 = forms.CharField(label='Еще раз', widget=forms.PasswordInput())

    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password != password1:
            raise forms.ValidationError("Введенные пароли не совпадают", code='password_mismatch',)
        return password1
