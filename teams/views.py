from django.shortcuts import render
from .models import TeamPlayer, Teams


def games_view(request):
    teams = Teams.objects.all().first()
    players = TeamPlayer.objects.filter(team=teams)
    teams.add_captain_in_team()
    context = {
        'teams':teams,
        'players':players
    }

    return render(request, 'teams/team_view.html', context)
