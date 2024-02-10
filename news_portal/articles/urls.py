from django.urls import path
from .views import ArticleCreate, ArticleUpdate, ArticleDelete, ArticleList, ArticleDetail, ArticleSearch


urlpatterns = [path('', ArticleList.as_view(), name='article_list'),
               path('<int:pk>/', ArticleDetail.as_view(), name='article_detail'),
               path('search/', ArticleSearch.as_view(), name='article_search'),
               path('create/', ArticleCreate.as_view(), name='article_create'),
               path('<int:pk>/update/', ArticleUpdate.as_view(), name='article_update'),
               path('<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete')]
