from django.contrib import admin
from .models import Mixes, MixPlayer


# Register your models here.
class TeamPlayerInline(admin.TabularInline):
    model = MixPlayer
    extra = 0
    raw_id_fields = ('user',)
    can_delete = False


class TeamAdmin(admin.ModelAdmin):
    model = Mixes
    inlines = [TeamPlayerInline]

admin.site.register(Mixes, TeamAdmin)
admin.site.register(MixPlayer)
