from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from models_portal.models import Post
from django.core.mail import mail_admins


@receiver(post_save, sender=Post)
def signal_post_create(sender, instance, created, **kwargs):
    if created:
        subject = f'Создана новая запись с названием: {instance.title_post}'
    else:
        subject = f'Запись {instance.title_post} изменена!!!'

    mail_admins(subject=subject,
                message=f'Содержание поста: {instance.text_post[:200]}...')


@receiver(post_delete, sender=Post)
def signals_post_delete(sender, instance, **kwargs):
    mail_admins(subject=f'Удален пост: {instance.title_post} пользователем {instance.author}',
                message=f'Содержимое поста: {instance.text_post}')
