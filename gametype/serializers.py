from rest_framework import serializers
from provider.models import Provider
from gametype.models import GameType


class GameTypeSerializer(serializers.ModelSerializer):
    '''
    @class GameTypeSerializer
    @brief
        Serializer class for GameType
    '''

    def __init__(self, *args, **kwargs):
        '''
        '''

        super(GameTypeSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            opt_fields = self.context['request'].query_params.get('opt_fields')
            if opt_fields:
                opt_fields = opt_fields.split(',')
                # Remove not specified fields
                to_show = set(opt_fields)
                default = set(self.fields.keys())
                for field in default - to_show:
                    self.fields.pop(field)


    name = serializers.CharField(max_length=255)
    status = serializers.IntegerField(default=1)
    provider = serializers.PrimaryKeyRelatedField(required=False, queryset=Provider.objects.all())

    class Meta:
        model = Provider
        fields = ('name', 'status', 'provider')
