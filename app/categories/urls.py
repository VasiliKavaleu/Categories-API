from django.urls import path

from . import views


urlpatterns = [
    path('', views.CategoriesList.as_view(), name='add_categories'),
    path('<int:pk>/', views.CategoryDetail.as_view(), name='list_category'),
]