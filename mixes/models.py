# coding=utf-8
from django.db import models


class Mixes(models.Model):
    title = models.CharField(max_length=120, default='MixDefault', unique=True)
    type = models.CharField(max_length=120, default='CyberSport')
    data = models.DateField(default='2000-01-01')
    place = models.CharField(max_length=120, default='Club',)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta():
        verbose_name = 'Микс'
        verbose_name_plural = 'Миксы'
        ordering = ['-timestamp']
        app_label = 'mixes'

    def __str__(self):
        return 'Микс по {} - {}'.format(self.type, self.title)


class MixPlayer(models.Model):
    mix = models.ForeignKey('Mixes', verbose_name='Микс')
    user = models.ForeignKey('accounts.User', verbose_name='Игрок')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta():
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        app_label = 'mixes'

    def __str__(self):
        return 'Игрок {}'.format(self.user.nickname)