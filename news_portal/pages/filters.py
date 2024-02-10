from django_filters import FilterSet, CharFilter, DateFilter, ModelChoiceFilter
from django import forms
from models_portal.models import Author


class PostFilter(FilterSet):

    title_post = CharFilter(lookup_expr='icontains',
                            label='Название')

    author_id = ModelChoiceFilter(empty_label='Все авторы',
                                  label='Автор',
                                  queryset=Author.objects.all())

    creation_time_post = DateFilter(widget=forms.DateInput(attrs={'type': 'date'}),
                                    label='Дата',
                                    lookup_expr='date__gte')
