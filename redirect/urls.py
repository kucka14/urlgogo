from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('terms_conditions', views.terms_conditions, name='terms_conditions'),
	path('privacy_policy', views.privacy_policy, name='privacy_policy'),
	path('cookies_policy', views.cookies_policy, name='cookies_policy'),
	path('robots.txt', views.robots, name='robots'),
	path('sitemap.xml', views.sitemap, name='sitemap'),
    path('c7001667f5e7626138e9e4334f4a9766/', views.c7001667f5e7626138e9e4334f4a9766, name='c7001667f5e7626138e9e4334f4a9766'),     
    path('e35e6da7bdbc4c0bec05f32bea5c6ae1/', views.e35e6da7bdbc4c0bec05f32bea5c6ae1, name='e35e6da7bdbc4c0bec05f32bea5c6ae1'),
    path('ec8db41d74c36b954821ab64f8226de0/', views.ec8db41d74c36b954821ab64f8226de0, name='ec8db41d74c36b954821ab64f8226de0'),
    path('<str:in_url>/', views.redirecter, name='redirecter'),
]
