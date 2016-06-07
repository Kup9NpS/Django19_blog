from django.conf.urls import url
from teams import views


urlpatterns = [
    url(r'^(?P<user_id>\d+)/$', views.profile_team_view, name="team_view"),
    url(r'^(?P<user_id>\d+)/edit$', views.team_update_view, name="team_update_view"),
    url(r'^(?P<user_id>\d+)/create$', views.team_create_view, name="team_create_view"),
    url(r'^detail/(?P<team_id>\d+)/$', views.team_detail_view, name="team_detail_view"),
    url(r'^detail/(?P<user_id>\d+)/delete$', views.team_delete_view, name="team_delete_view"),
    url(r'^detail/(?P<user_id>\d+)/delete/user$', views.delete_user_from_team, name="user_delete_view"),
    url(r'^detail/(?P<team_id>\d+)/invite$', views.invite_user_in_team, name="invite_view"),
    url(r'^detail/(?P<team_id>\d+)/invite/add$', views.add_user_in_team, name="add_view"),
    url(r'^detail/(?P<team_id>\d+)/invite/reject$', views.reject_user_from_team, name="reject_view"),
    url(r'^list/$', views.team_list_view, name="list_view"),
    # url(r'^(?P<slug>[\w-]+)/$',post_detail, name='detail'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name="update"),
    # url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
]