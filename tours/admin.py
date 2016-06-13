from django.contrib import admin
from .models import Tours, TourPlayer


# Register your models here.
class TourPlayerInline(admin.TabularInline):
    model = TourPlayer
    extra = 0
    raw_id_fields = ('team',)
    can_delete = False


class TourAdmin(admin.ModelAdmin):
    model = Tours
    inlines = [TourPlayerInline]

admin.site.register(Tours, TourAdmin)
admin.site.register(TourPlayer)