from django.urls import path

from . import views

app_name = 'authors'
urlpatterns = [
    path(f'{app_name}/', views.AuthorView.as_view()),
    path(f'{app_name}/<uuid:author_id>/', views.AuthorView.as_view()),
    path('remote-node/', views.RemoteNodeView.as_view()),
]
