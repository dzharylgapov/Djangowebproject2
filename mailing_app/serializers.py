from rest_framework import serializers

from .models import Mailing, Client, Message


class MailingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mailing
        # depth = 1
        fields = ['mailing_id', 'datetime_of_start', 'datetime_of_end', 'text', 'mailing_filter']


class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        # depth = 1
        fields = ['client_id', 'phone_number', 'phone_code', 'tag', 'timezone']


class MessageSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    mailing = MailingSerializer()

    class Meta:
        model = Message
        # depth = 1
        fields = []
