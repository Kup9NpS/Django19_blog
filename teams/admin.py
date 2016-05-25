from django.contrib import admin
from .models import Teams, TeamPlayer


# Register your models here.
class TeamPlayerInline(admin.TabularInline):
    model = TeamPlayer
    extra = 0
    raw_id_fields = ('user',)
    can_delete = False


class TeamAdmin(admin.ModelAdmin):
    model = Teams
    inlines = [TeamPlayerInline]

admin.site.register(Teams, TeamAdmin)
admin.site.register(TeamPlayer)
