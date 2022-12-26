from datetime import datetime
import time
import requests
import json

from celery import shared_task
from .models import Mailing, Client, Message
from DjangoWebProject2.settings import PROBE_TOKEN, CELERY_BEAT_SCHEDULE


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True)
def send_mailing_task(self, mailing_id):
    mailing = Mailing.objects.get(mailing_id=mailing_id)
    print("lol")
    print("mailing", mailing)
    if mailing.datetime_of_start.year == datetime.now().year \
            and mailing.datetime_of_end > datetime.now():

        mailing_filter = json.loads(mailing.mailing_filter)
        filter_tag = mailing_filter['tag']
        filter_phone_code = mailing_filter['phone_code']

        if filter_tag != "" or filter_phone_code != "":
            if filter_tag != "":
                clients = Client.objects.filter(tag=filter_tag)
            if filter_phone_code != "":
                clients = Client.objects.filter(phone_code=filter_phone_code)
        else:
            clients = Client.objects.all()
        print(1111)
        for client in clients:
            print("heh")
            message = Message.objects.get_or_create(client=client, status="not send", mailing=mailing)
            url = "https://probe.fbrq.cloud/v1/send/" + message.message_id

            payload = json.dumps({
              "id": message.message_id,
              "phone": client.phone_number,
              "text": mailing.text
            })
            headers = {
              'accept': 'application/json',
              'Authorization': 'Bearer ' + PROBE_TOKEN,
              'Content-Type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200:
                message.datetime_of_sending = datetime.now()
                message.status = "sended"
                message.save()
    else:
        del CELERY_BEAT_SCHEDULE["mailing-" + mailing_id]
    


