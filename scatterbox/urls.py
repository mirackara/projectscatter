from django.urls import include, path
from . import views

# URLConf
urlpatterns = [
    path('', views.indexHandler),
    path('search/', views.eventHandler),
    path('compare/', views.compareHandler)
]