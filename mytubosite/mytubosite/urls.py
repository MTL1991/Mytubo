from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from ppal.views import *

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^$', index, name='index'),
    url(r'^tuber/profile/(\d+)/$', tuber_view, name='profile_tuber'),
    url(r'^tuber/create/$', create_tuber, name='add_tuber'),
    url(r'^login/$', tuber_login, name='login_tuber'),
    url(r'^logout/$', tuber_logout, name='logout_tuber'),
    url(r'^tubo/add/$', create_tubo, name='add_tubo'),
)

urlpatterns += patterns('',
    url(r'^tubo/(?P<pk>\d+)/$', TuboView.as_view(), name='view_tubo'),
#     url(r'^trabs/offers/(?P<pk>\d+)/edit/$', TrabOfferUpdate.as_view(), name='edit_trabo'),
    url(r'^tubo/(?P<pk>\d+)/delete/$', TuboDelete.as_view(), name='delete_tubo'),
#     url(r'^trabs/needs/add/$',     TrabNeedCreate.as_view(), name='add_trabn'),
#     url(r'^trabs/needs/(?P<pk>\d+)/$',  TrabNeedView.as_view(), name='view_trabn'),
#     url(r'^trabs/needs/(?P<pk>\d+)/edit/$', TrabNeedUpdate.as_view(), name='edit_trabn'),
#     url(r'^trabs/needs/(?P<pk>\d+)/delete/$', TrabNeedDelete.as_view(), name='delete_trabn'),
)
