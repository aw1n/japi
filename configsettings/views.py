from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import mixins, status, viewsets
from configsettings.models import CommissionSettings
from configsettings.serializers import CommissionSettingsSerializer


class CommissionSettingsViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, 
                                mixins.ListModelMixin, mixins.UpdateModelMixin, 
                                viewsets.GenericViewSet):
    '''
    @class AgentViewSet
    @brief
        Viewset for agent
    '''
    
    model = CommissionSettings
    serializer_class = CommissionSettingsSerializer
    queryset = CommissionSettings.objects.all()

    def list(self, request):
        response = {}
        queryset = CommissionSettings.objects.all()
        serializer = CommissionSettingsSerializer(queryset, context={"request":request}, many=True)
        response['status_code'] = status.HTTP_200_OK
        response['data'] = serializer.data
        return Response(response)