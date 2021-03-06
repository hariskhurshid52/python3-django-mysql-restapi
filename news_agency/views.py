from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from news_agency.serializers import AgencySerializer
from news_agency.models import NewsAgency
# Create your views here.


@api_view(['POST'])
def register_news_agency(request):
    if "POST" == request.method:
        agency_data = request.POST
        if agency_data.get('agency_name') is None:
            return HttpResponse('Agency name can not be empty', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        elif agency_data.get('website') is None:
            return HttpResponse('Website can not be empty', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        elif agency_data.get('code') is None:
            return HttpResponse('Code can not be empty', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')

        agency_serializer = AgencySerializer(data=agency_data)
        if agency_serializer.is_valid():
            try:
                agency_serializer.save()
                return HttpResponse('Successfully saved agency data', status=status.HTTP_201_CREATED)
            except NameError:
                return HttpResponse(agency_serializer.errors, status=status.HTTP_400_BAD_REQUEST,
                                    content_type='text/plan')

        return HttpResponse('Invalid data provided', status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/plan')
    return HttpResponse("Unknown Method", status=status.HTTP_405_METHOD_NOT_ALLOWED, content_type='text/plan')


@api_view(['GET'])
def get_news_agency_list(request):
    if "GET" == request.method:

        agencies_data = NewsAgency.objects.all()
        story_serializer = AgencySerializer(agencies_data, many=True)
        return JsonResponse({"Agencies": story_serializer.data}, safe=False, status=status.HTTP_200_OK)
    return HttpResponse("Unknown Method", status=status.HTTP_405_METHOD_NOT_ALLOWED, content_type='text/plan')
