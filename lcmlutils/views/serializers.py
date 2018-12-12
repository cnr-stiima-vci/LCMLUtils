from lcmlutils.models import LCCS3Legend
from rest_framework import serializers


class LegendSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = LCCS3Legend
        fields = ('id', 'name', 'xml_text', 'link_type')

