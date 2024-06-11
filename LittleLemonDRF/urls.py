from django.urls import path
from . import views
urlpatterns = [
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.MenuItemDetail.as_view()),
    path('categories', views.CategoryView.as_view()),
]
