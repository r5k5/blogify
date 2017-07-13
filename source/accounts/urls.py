from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
	url(r'^$', views.home_page, name='home_page'),	
	url(r'^login/$', views.login_view, name='login'),
	url(r'^register/$', views.register_view, name='register'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
]
