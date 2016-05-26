# coding=utf-8
from django.db import models

class Teams(models.Model):
    title = models.CharField(max_length=120, default='TeamDefault', unique=True)
    logo = models.ImageField(upload_to='logos',
                              blank=True, null=True,
                              verbose_name='Логотип')
    is_verified = models.BooleanField('Проверена', default=False,
                                      help_text="Допущена ли к регестрации")
    captain_user = models.ForeignKey('accounts.User',
                                      related_name='team_captain',
                                      limit_choices_to={'is_captain':True},
                                      verbose_name='Капитан команды')
    wins = models.IntegerField(default=0)
    looses = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)

    class Meta():
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ['-timestamp']
        app_label = 'teams'

    def __str__(self):
        return 'Команда №{} - {}'.format(self.id, self.title)

    def add_captain_in_team(self):
        try:
            TeamPlayer.objects.get(user=self.captain_user)
        except TeamPlayer.DoesNotExist:
            TeamPlayer.objects.create(team=self, user=self.captain_user, role='captain', action=INTEAM)

    def add_player(self, current_user, role):
        if not current_user.is_inteam:
            TeamPlayer.objects.create(team=self, user=current_user, role=role, action=INTEAM)
        else:
            pass

    def all_team(self):
        teammates = TeamPlayer.objects.filter(team=self).filter(action=TeamPlayer.INTEAM)
        users = list()
        for mate in teammates:
            users.append(mate.user)
        return users


INVITED = 1
INTEAM = 2
LEAVED = 3


ACTIONS = (
          (INTEAM, 'Вступил в команду'),
          (LEAVED, 'Вышел из команды'),
          (INVITED, 'Приглашен в команду'),
    )


class TeamPlayer(models.Model):
    team = models.ForeignKey('Teams', verbose_name='Команда')
    user = models.ForeignKey('accounts.User', verbose_name='Игрок')
    role = models.CharField(max_length=120)
    action = models.PositiveSmallIntegerField(verbose_name='Действие', choices=ACTIONS)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    class Meta():
        verbose_name = 'Игрок'
        verbose_name_plural = 'Игроки'
        app_label = 'teams'
        unique_together = ("team", "user")

    def __str__(self):
        return 'Игрок {} - {}'.format(self.user.nickname, self.team.title)