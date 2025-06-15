from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cards/', views.card_list, name='card_list'),
    path('cards/add/', views.add_card, name='add_card'),
    path('cards/<int:pk>/edit/', views.edit_card, name='edit_card'),
    path('cards/<int:pk>/delete/', views.delete_card, name='delete_card'),
    path('cards/train/', views.train, name='train'),
]
