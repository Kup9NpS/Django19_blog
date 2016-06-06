# coding=utf-8
import datetime
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, password, is_superuser=False, is_active=False, **extra_fields):
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')

        is_staff = is_superuser
        is_admin = extra_fields.pop("is_admin", False)
        first_name = extra_fields.pop("first_name", '')
        last_name = extra_fields.pop("last_name", '')

        user = self.model(
            email=self.normalize_email(email),
            is_active=is_active,
            is_admin=is_admin,
            is_staff=is_staff,
            is_superuser=is_superuser,
            first_name=first_name,
            last_name=last_name,
            last_login=now,
            date_joined=now,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(email, password, is_superuser=True, is_active=True, **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('Email', max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(u'Активность', default=False,
                                    help_text="Вместо удаления аккаунта, сделайте его неактивным")
    is_admin = models.BooleanField('Админ', default=False,
                                   help_text="Админ сайта")
    is_staff = models.BooleanField('Админ', default=False,
                                   help_text="Админ сайта, доступ в админку")
    banned = models.BooleanField('Забанен', default=False,
                                 help_text="Забанить игрока на сайте")
    is_captain = models.BooleanField('Капитан', default=False,
                                     help_text="Является ли капитаном команды")
    is_inteam = models.BooleanField('В команде', default=False,
                                    help_text="Состоит ли в команде")
    nickname = models.CharField('Никнейм', max_length=20, default="nameless")
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name='Аватар')
    date_joined = models.DateTimeField('Дата регистрации', default=timezone.now)
    bdate = models.DateField('Дата рождения', auto_now_add=False, blank=True, null=True)
    first_name = models.CharField('Имя', max_length=120)
    last_name = models.CharField('Фамилия', max_length=120)
    sex = models.CharField(max_length=1, choices=(('m', 'мужской'), ('f', 'женский')), verbose_name='Пол')
    steam_name = models.CharField(max_length=50, default=' ', blank=True, null=True)
    battle_tag = models.CharField(max_length=50, default=' ', blank=True, null=True)
    lol_name = models.CharField(max_length=50, default=' ', blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    REGISTRATION_FIELDS = ['first_name', 'last_name'] + ['nickname'] + ['sex'] + ['bdate'] + [USERNAME_FIELD]

    class Meta:
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        db_table = 'auth_user'
        abstract = True

    def get_full_name(self):
        return u'{} {}'.format(self.first_name, self.last_name)

    def get_short_name(self):
        return self.last_name

    @property
    def age(self):
        today = datetime.date.today()
        return today.year - self.bdate.year - ((today.month, today.day) < (self.bdate.month, self.bdate.day))

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_absolute_url(self):
        return "/users/%i" % self.id

    def __str__(self):
        return u'{} {}'.format(self.first_name, self.last_name)


class User(AbstractUser):
    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'

    def get_absolute_url(self):
        return "/user/%i" % self.id


class UserActivation(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=100, blank=True)
    request_time = models.DateTimeField(default=timezone.now)
    confirm_time = models.DateTimeField('Дата активации', blank=True, null=True)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name_plural = u'Активации'
