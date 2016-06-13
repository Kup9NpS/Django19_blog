# coding=utf-8
from django.db import models
from teams.models import Teams


class Tours(models.Model):
    title = models.CharField(max_length=120, default='MixDefault', unique=True)
    type = models.CharField(max_length=120, default='CyberSport')
    data = models.DateField(default='2000-01-01')
    place = models.CharField(max_length=120, default='Club',)
    is_online = models.BooleanField('Тип турнира', default=False,
                                    help_text="Галочка если онлайн")
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta():
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'
        ordering = ['-timestamp']
        app_label = 'tours'

    def __str__(self):
        return 'Турнир по {} - {}'.format(self.type, self.title)


class TourPlayer(models.Model):
    tour = models.ForeignKey('Tours', verbose_name='Турнир')
    team = models.ForeignKey(Teams, verbose_name='Команда')
    is_banned = models.BooleanField('Бан на турнире', default=False,
                                    help_text="Бан на конкретном турнире")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta():
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        app_label = 'tours'

    def __str__(self):
        return 'Команда {}'.format(self.team.title)