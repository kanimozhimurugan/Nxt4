from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.contrib.auth import views
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView, RedirectView
from nxt.views import login, logout, password_change
from friendship.views import sortby_users, view_friends
from userprofile.views import EditProfile
from collegelist.views import *
from feeds.views import *
admin.autodiscover()
urlpatterns = [
    url(r'^/?$', RedirectView.as_view(url='login/'), name="homepage"),  
    url(r'^subvtle/$', TemplateView.as_view(template_name='django_messages/subvtle.html')),
    url(r'feeds/postfeed/', add_post, name="Postfeed"),
    url(r'feeds/post/', post, name="post"),
    url(r'addcollege/', addcollege, name="addcollege"),
    url(r'getcollege/', getcollege, name="getcollege"),
    url(r'^profile/', EditProfile, name="editprofile"),
    url(r'^accounts/', include('registration.urls')),
    url(r'^friends/',include('friendship.urls')),
    url(r'^messages/',include('django_messages.urls')),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', views.logout_then_login, name='logout'),
    url(r'^password_change/$', views.password_change, name='password_change'),
    url(r'^password_change/done/$', views.password_change_done, name='password_change_done'),
    url(r'^passwordreset/$', views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    url(r'^siteadmin/', include(admin.site.urls)),
    ] + static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
