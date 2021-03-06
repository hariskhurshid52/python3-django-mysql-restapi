from rest_framework import serializers
from news_agency.models import NewsAgency


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsAgency
        fields = ('id',
                  'agency_name',
                  'website',
                  'code')



