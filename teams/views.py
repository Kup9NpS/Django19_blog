# coding=utf-8
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from .models import TeamPlayer, Teams
from .forms import TeamUpdateForm
from django.http import Http404
from django.db.models import  Q


def team_list_view(request):
    queryset_list = Teams.objects.all()
    query = request.GET.get("q")
    if query:
        queryset_list = queryset_list.filter(
                    Q(title__icontains=query)|
                    Q(teamplayer__user__nickname__icontains=query)
                    ).distinct()
    paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
    page_request_var = "page"
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)
    context = {
        "object_list": queryset,
        "page_request_var": page_request_var,
    }
    return render(request, 'teams/team_list.html', context)


def team_detail_view(request, team_id=None):
    current = False
    teams = get_object_or_404(Teams, id=team_id)
    players = TeamPlayer.objects.filter(team__title=teams.title, user__is_inteam=True, action=2)
    context = {
            'team':teams,
            'players':players,
            'current':current
        }
    return render(request, 'teams/team_view.html', context)


def profile_team_view(request, user_id=None):
    current = False
    if request.user.is_authenticated():
        player = get_object_or_404(TeamPlayer, user__id=user_id)
        team = get_object_or_404(Teams, title=player.team.title)
        players = TeamPlayer.objects.filter(team__title=team.title, user__is_inteam=True, action=2)
        if request.user.pk == player.user.id:
            current = True
        context = {
            'team':team,
            'player':player,
            'players':players,
            'current':current
        }
        return render(request, 'teams/team_view.html', context)
    else:
        raise Http404


def team_update_view(request, user_id=None):
    player = get_object_or_404(TeamPlayer, user__id=user_id)
    form = TeamUpdateForm(request.POST or None, request.FILES or None, instance=player.team)
    if form.is_valid():
        form.save()
        return redirect('teams:team_view', player.user.id)
    else:
        messages.warning(request, "Некорректные данные", extra_tags='info')
    return render(request, 'teams/team_edit.html', {'user': player, 'form': form, })

@login_required
def invite_user_in_team(request, team_id=None):
    teams = get_object_or_404(Teams, id=team_id)
    new_player = Teams.invite_player(current_user=request.user)
    return redirect('/')



def add_user_in_team(request):

    pass

