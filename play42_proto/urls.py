from django.conf.urls import url
from . import views


urlpatterns = [
    url('bet_double/', views.bet_double, name='bet_double'),
    url('bet_double_result/(?P<pk>[0-9]+)/$', views.bet_double_result, name='bet_double_result'),

    url('bet_triple/', views.bet_triple, name='bet_triple'),
    url('bet_triple_result/(?P<pk>[0-9]+)/$', views.bet_triple_result, name='bet_triple_result'),

    url('bet_n/', views.bet_n, name='bet_n'),
    url('bet_n_result/(?P<pk>[0-9]+)/$', views.bet_n_result, name='bet_n_result'),

    url(r'^$', views.functions_list, name='functions_list'),
]

