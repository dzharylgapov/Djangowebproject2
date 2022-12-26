"""
Definition of models.
"""
import uuid
from django.db import models
from jsonfield import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from DjangoWebProject2 import settings
from celery.schedules import crontab


class Mailing(models.Model):
    mailing_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False)
    datetime_of_start = models.DateTimeField(
        null=True, 
        blank=True
    )
    datetime_of_end = models.DateTimeField(
        null=True, 
        blank=True
    )
    text = models.CharField(
        max_length=1000
    )
    mailing_filter = JSONField(
        null=True,
        blank=True
    )


class Message(models.Model):
    message_id = models.UUIDField(
         primary_key = True,
         default = uuid.uuid4,
         editable = False
    )
    datetime_of_sending = models.DateField()
    status = models.CharField(
        max_length=200
    )
    client = models.ForeignKey(
        'Client', 
        on_delete=models.CASCADE
    )
    mailing = models.ForeignKey(
        'Mailing', 
        on_delete=models.CASCADE
    )


class Client(models.Model):
    client_id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable = False)
    phone_number = models.CharField(
        max_length=200
    )
    phone_code = models.CharField(
        max_length=200
    )
    tag = models.CharField(
        max_length=200
    )
    timezone = models.CharField(
        max_length=200
    )



@receiver(post_save, sender=Mailing)
def post_save_mailing(sender, instance, created, **kwargs):
    datetime_of_start = instance.datetime_of_start
    try:
        settings.CELERY_BEAT_SCHEDULE["mailing-" + str(instance.mailing_id)] = {
            'task': 'app.tasks.send_mailing_task',
            'schedule': crontab(
                hour=datetime_of_start.hour, 
                minute=datetime_of_start.minute, 
                day_of_month=datetime_of_start.day, 
                month_of_year=datetime_of_start.month,
            ),
            'args': (instance.mailing_id,),
        }
        print(CELERY_BEAT_SCHEDULE)
    except AttributeError:
        pass

