from rest_framework import serializers
from tracker.models import APIRequestLog, LoginRecord

class TrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRequestLog


class LoginRecordSerializer(serializers.ModelSerializer):
    '''
    '''

    class Meta:
        model = LoginRecord
