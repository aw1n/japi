from rest_framework import serializers
from provider.models import Provider
from gametype.models import GameType
from jaguar.lib.optionfieldsfilter import OptionFieldsFilter


class GameTypeSerializer(OptionFieldsFilter, serializers.ModelSerializer):
    '''
    @class GameTypeSerializer
    @brief
        Serializer class for GameType
    '''

    type = serializers.IntegerField(source='id')
    name = serializers.CharField(max_length=255)
    status = serializers.IntegerField(default=1)
        
    class Meta:
        model = Provider
        fields = ('name', 'status', 'type')
