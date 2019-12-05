from django.urls import path
from . import views
urlpatterns = [
    path('', views.get_page_1, name = 'search-get_page_1'),
    path('success/', views.search_page, name='search-search_page'),
]
