from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MixPlayer, Mixes


def mix_list_view(request):
    queryset = Mixes.objects.all()
    context = {
        "object_list": queryset,

    }
    return render(request, 'mixes/mix_list.html', context)


def mix_detail_view(request, mix_id=None):
    mix= get_object_or_404(Mixes, id=mix_id)
    players = MixPlayer.objects.filter(mix=mix)
    try:
        MixPlayer.objects.get(mix=mix, user=request.user)
        in_that_mix = True
    except MixPlayer.DoesNotExist:
        in_that_mix = False
    context = {
            'mix': mix,
            'players': players,
            'in_that_mix': in_that_mix
        }
    return render(request, 'mixes/mix_view.html', context)


@login_required
def add_user_in_mix(request, mix_id=None):
    mix = get_object_or_404(Mixes, id=mix_id)
    try:
        MixPlayer.objects.get(mix=mix, user=request.user)
        return redirect('mixes:mix_view', mix.id)
    except MixPlayer.DoesNotExist:
        MixPlayer.objects.create(mix=mix, user=request.user)
    return redirect("mixes:mix_view", mix.id)


@login_required
def leave_user_from_mix(request, mix_id=None):
    mix = get_object_or_404(Mixes, id=mix_id)
    player = MixPlayer.objects.get(mix=mix, user=request.user)
    player.delete()
    return redirect("mixes:mix_view", mix.id)