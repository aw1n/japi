from rest_framework import viewsets, mixins
from .models import Provider
from .serializers import ProviderSerializer 

# Create your views here.
class ProviderViewSet(mixins.ListModelMixin,
                      viewsets.GenericViewSet):

    model = Provider
    serializer_class = ProviderSerializer
    queryset = Provider.objects.all()

   