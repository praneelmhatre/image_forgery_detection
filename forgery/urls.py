from django.urls import path
from . import views
from .views import *
#from .views import UpdateProperties,DeleteProperties,AddProperties,UserRegister

urlpatterns= [
    path('',views.index,name='index'),
    path('index',views.index,name='index'),
    path('index.html',views.index,name='index'),
    path('aboutus.html',views.aboutus,name='aboutus'),
    path('results.html',views.result,name='result'),
    path('success/', success, name='success'),
    path('media/',views.media,name='media'),
]