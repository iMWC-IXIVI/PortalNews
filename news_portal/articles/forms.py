from django import forms
from django.forms import ValidationError
from models_portal.models import Post


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title_post',
                  'text_post',
                  'author']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title_post')
        text = cleaned_data.get('text_post')

        if title == text:
            raise ValidationError('Текст не должен быть равен заголовку')
        return cleaned_data
