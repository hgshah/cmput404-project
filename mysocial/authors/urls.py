from django.urls import path

from . import views

app_name = 'authors'
urlpatterns = [
    path('', views.AuthorView.as_view()),
    path('<uuid:author_id>/', views.AuthorView.as_view()),
]