from rest_framework import viewsets
from lcmlutils.models import LCCS3Legend
from lcmlutils.views.serializers import LegendSerializer


class LegendViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = LCCS3Legend.objects.all()
    serializer_class = LegendSerializer

