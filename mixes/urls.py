from django.conf.urls import url

from mixes import views

urlpatterns = [
    url(r'^$', views.mix_list_view, name='mix_list_view'),
    url(r'^(?P<mix_id>\d+)/$', views.mix_detail_view, name="mix_view"),
    url(r'^(?P<mix_id>\d+)/add$', views.add_user_in_mix, name="add_view"),
    url(r'^(?P<mix_id>\d+)/leave$', views.leave_user_from_mix, name="leave_view"),
]
