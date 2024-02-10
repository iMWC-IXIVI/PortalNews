from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.contrib.auth.models import User


class StaffUser(models.Model):

    administrator = 'AD'
    moderator = 'MO'
    user_pos = 'US'

    STAFF_POSITION = [(administrator, 'Администратор'),
                      (moderator, 'Модератор'),
                      (user_pos, 'Пользователь')]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    staff_pos = models.CharField(max_length=2, choices=STAFF_POSITION, default=user_pos)
    premium = models.BooleanField(default=False)


class Author(models.Model):
    staff_user = models.OneToOneField('StaffUser', on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.staff_user.user.username

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).aggregate(pr=Sum('rating_post'))['pr']
        comment_rating = Comment.objects.filter(staff_user=self.staff_user).aggregate(cr=Sum('rating_comment'))['cr']
        post_comment_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Sum('rating_comment'))['pcr']

        self.author_rating = (post_rating if post_rating else 0) * 3 + (comment_rating if comment_rating else 0) + (post_comment_rating if post_comment_rating else 0)
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True)
    subscribe = models.ManyToManyField(User, through='Subscribes')

    def __str__(self):
        return self.name_category


class Post(models.Model):

    new = 'NE'
    article = 'AR'

    NAME_POSTS = [(new, 'Новостья'),
                  (article, 'Статья')]

    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    user_choice = models.CharField(max_length=2, choices=NAME_POSTS)
    creation_time_post = models.DateTimeField(auto_now_add=True)
    post_category_category = models.ManyToManyField('Category', through='PostCategory')
    title_post = models.CharField(max_length=100)
    text_post = models.TextField()
    rating_post = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title_post}: {self.text_post}'

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()

    def preview(self):
        return f'{self.text_post[:124]}...'

    def get_absolute_url(self):
        return reverse('post_detail', args=(str(self.id)))


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    staff_user = models.ForeignKey('StaffUser', on_delete=models.CASCADE)
    text_comment = models.TextField()
    creation_time_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()


class Subscribes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
