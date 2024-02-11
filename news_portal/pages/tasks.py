import os
from dotenv import load_dotenv

from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from models_portal.models import Post, Subscribes
from django.contrib.auth.models import User

from datetime import date, timedelta


load_dotenv()


@shared_task
def email_sending(post, form):
    html_content = render_to_string('message_email.html', {'post': post, 'pk_post': Post.objects.count()})

    for category in Subscribes.objects.all():
        if category.category in form.cleaned_data.get('post_category_category'):
            for user in User.objects.all():
                if user == category.user:
                    msg = EmailMultiAlternatives(subject=post.title_post,
                                                 from_email=os.getenv('DEFAULT_FROM_EMAIL'),
                                                 to=[user.email])
                    msg.attach_alternative(html_content, 'text/html')
                    msg.send()


@shared_task
def send_email_em():
    today = date.today()

    while today.weekday() != 0:
        today -= timedelta(1)

    post_orm = Post.objects.filter(creation_time_post__date__gte=today)

    html_content = render_to_string('sender_email.html', {'post_orm': post_orm, 'post_c': post_orm.count()})

    for user_sub in Subscribes.objects.all():
        for user in User.objects.all():
            if user_sub.user == user:
                msg = EmailMultiAlternatives(subject=f'Количество новостей - {post_orm.count()}',
                                             from_email=os.getenv('DEFAULT_FROM_EMAIL'),
                                             to=[user.email])
                msg.attach_alternative(html_content, 'text/html')
                msg.send()
