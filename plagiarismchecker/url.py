from django.urls import path
from . import views
from .views import compare_images, home

urlpatterns = [
    path('', views.home, name='compare-master-mainpage'),
    path('plag/', views.plagiarism, name='compare-master-plagiarism'),
    path('compare/', views.fileCompare, name='compare'), 
    path('test/', views.test, name='Test'),
    path('filetest/', views.filetest, name='filetest'),
    path('twofiletest1/', views.twofiletest1, name='twofiletest1'),
    path('twofilecompare1/', views.twofilecompare1, name='twofilecompare1'),
    path('list/', views.listcompare, name='compare-master-list'),
    path('compare_images/', views.compare_images, name='compare_images'),

    
]
