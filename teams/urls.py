from django.conf.urls import url
from teams import views


urlpatterns = [
    url(r'^$', views.games_view, name="team_view"),
    # url(r'^create/$',post_create),
    # url(r'^(?P<slug>[\w-]+)/$',post_detail, name='detail'),
    # url(r'^(?P<slug>[\w-]+)/edit/$', post_update, name="update"),
    # url(r'^(?P<slug>[\w-]+)/delete/$', post_delete),
]