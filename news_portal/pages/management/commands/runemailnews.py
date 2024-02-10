import logging

from datetime import date, timedelta

from models_portal.models import Post, Subscribes
from django.contrib.auth.models import User

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def my_job():
    today = date.today()

    while today.weekday() != 0:
        today = today - timedelta(1)

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


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week=0),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),

            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")