from rest_framework import serializers
from tracker.models import APIRequestLog

class TrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = APIRequestLog