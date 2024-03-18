from django.urls import path
from .views import SendMailAdd, NewsList, NewsDetail, NewsSearch, NewCreate, NewUpdate, NewDelete, authors_add

from django.views.decorators.cache import cache_page


urlpatterns = [path('', NewsList.as_view(), name='post_list'),
               path('<int:pk>/', NewsDetail.as_view(), name='post_detail'),
               path('search/', NewsSearch.as_view(), name='post_search'),
               path('create/', NewCreate.as_view(), name='post_create'),
               path('<int:pk>/update/', NewUpdate.as_view(), name='post_update'),
               path('<int:pk>/delete/', NewDelete.as_view(), name='post_delete'),
               path('upgrade/', authors_add, name='add_author'),
               path('subscribe/', SendMailAdd.as_view(), name='subscribe')]
