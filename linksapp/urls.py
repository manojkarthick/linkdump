from django.conf.urls import url
from . import views

app_name = 'linksapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^all/$', views.AllView.as_view(), name='all'),
    url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^create/$', views.LinkCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/delete/$', views.LinkDelete.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/update/$', views.LinkUpdate.as_view(), name='update'),
    url(r'^(?P<link_id>\d+)/redirect/$', views.increment_hits, name='increment_hits'),
]
