from django import forms
from django.forms import ValidationError
from models_portal.models import Post
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title_post',
                  'text_post',
                  'author',
                  'post_category_category']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title_post')
        text = cleaned_data.get('text_post')

        if title == text:
            raise ValidationError('Текст не должнен быть равен заголвоку')
        return cleaned_data


class SignUpForm(SignupForm):

    def save(self, request):
        user = super(SignUpForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
