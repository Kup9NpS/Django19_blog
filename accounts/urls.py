from django.conf.urls import url

from accounts import views

urlpatterns = [
    url(r'^login$', views.login_view, name='login_view'),
    url(r'^logout$', views.logout_view, name='logout_view'),
    url(r'^register$', views.register_view, name='reg_view'),
    url(r'^confirm/(?P<activation_key>.*.{5,100})$', views.register_confirm, name='confirm'),
    url(r'^(?P<user_id>\d+)/edit$', views.user_update_view, name="user_edit_view"),
    url(r'^changepass$', views.changepass, name="changepass"),
    url(r'^resetpass$', views.resetpass, name="resetpass"),
    url(r'^(?P<user_id>\d+)$', views.user_view, name='user_view'),
    url(r'^list$', views.users_view, name='users_view'),
]
