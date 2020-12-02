from django.urls import path
from . import views

app_name = 'actividades'
urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('update/<int:id>', views.update, name='update'),
    path('remove/<int:id>/', views.remove, name='remove'),
    path('random/', views.random, name='random'),
    path('cat/', views.cat, name='cat'),
]