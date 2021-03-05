import json

from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from web_services.models import Author, NewsStories
from web_services.serializers import AuthorSerializer, StorySerializer
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['GET', 'POST', 'DELETE'])
def authors_list(request):
    if "GET" == request.method:
        authors = Author.objects.all()
        name = request.GET.get('name', None)
        if name is not None:
            authors = authors.filter(name__contains=name)
        author_serializer = AuthorSerializer(authors, many=True)
        return JsonResponse(author_serializer.data, safe=False)
    elif "POST" == request.method:
        author_data = request.POST
        if author_data.get('username') is None:
            return JsonResponse({'msg': 'Username can not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        elif author_data.get('password') is None:
            return JsonResponse({'msg': 'Password can not be empty'}, status=status.HTTP_400_BAD_REQUEST)
        author_serializer = AuthorSerializer(data=author_data)
        if author_serializer.is_valid():
            author_serializer.save()
            return JsonResponse({'msg': 'success'}, status=status.HTTP_201_CREATED)
        return JsonResponse(author_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    if "POST" == request.method:
        author_data = request.POST
        if author_data.get('username') is None:
            return HttpResponse('Username can not be empty', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        elif author_data.get('password') is None:
            return HttpResponse('Password can not be empty', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        response = Author.objects.filter(username=author_data.get('username'), password=author_data.get('password'))
        if len(response) == 1:
            return HttpResponse('Successfully login', status=status.HTTP_200_OK)
        return HttpResponse('Invalid username or password', status=status.HTTP_400_BAD_REQUEST)
    return HttpResponse("Unknown Method", status=status.HTTP_405_METHOD_NOT_ALLOWED, content_type='text/plan')


@api_view(['POST'])
def logout(request):
    if "POST" == request.method:
        return HttpResponse('Successfully logout from system', status=status.HTTP_200_OK)
    return HttpResponse("Unknown Method", status=status.HTTP_405_METHOD_NOT_ALLOWED, content_type='text/plan')


@api_view(['POST'])
def post_story(request):
    if "POST" == request.method:
        story_data = request.POST
        if story_data.get('headline') is None:
            return HttpResponse('Headline can not be empty', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        elif story_data.get('category') is None:
            return HttpResponse('Category can not be empty', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        elif story_data.get('region') is None:
            return HttpResponse('Region can not be empty', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        elif story_data.get('details') is None:
            return HttpResponse('Details can not be empty', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        story_serializer = StorySerializer(data=story_data)
        if story_serializer.is_valid():
            try:
                story_serializer.save()
                return HttpResponse('Successfully saved story data', status=status.HTTP_201_CREATED)
            except NameError:
                print(NameError)
                return HttpResponse(story_serializer.errors, status=status.HTTP_400_BAD_REQUEST,
                                    content_type='text/plan')

        return HttpResponse('Invalid data provided', status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/plan')
    return HttpResponse("Unknown Method", status=status.HTTP_405_METHOD_NOT_ALLOWED, content_type='text/plan')


@api_view(['GET'])
def get_stories(request):
    if "GET" == request.method:
        stories = NewsStories.objects.all()
        # todo forgin key relation
        story_data = request.data
        if story_data.get('story_cat') is not None:
            stories = stories.filter(category__exact=story_data.get('story_cat'))
        if story_data.get('story_region') is not None:
            stories = stories.filter(region__exact=story_data.get('story_region'))
        if story_data.get('story_date') is not None:
            stories = stories.filter(date_time=story_data.get('story_date'))
        story_serializer = StorySerializer(stories, many=True)
        return JsonResponse({"stories": story_serializer.data}, safe=False, status=status.HTTP_200_OK)
    return HttpResponse("Unknown Method", status=status.HTTP_405_METHOD_NOT_ALLOWED, content_type='text/plan')


@api_view(['POST'])
def delete_story(request):
    if "POST" == request.method:
        story_data = request.data
        if story_data.get('story_key') is  None:
            return HttpResponse('Please provide valid story id', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        try:
            story = NewsStories.objects.get(pk=story_data.get('story_key'))
            return HttpResponse('Successfully deleted story data', status=status.HTTP_201_CREATED)
        except NewsStories.DoesNotExist:
            return HttpResponse('Failed to delete story', status=status.HTTP_503_SERVICE_UNAVAILABLE,
                                content_type='text/plan')
    return HttpResponse("Unknown Method", status=status.HTTP_405_METHOD_NOT_ALLOWED, content_type='text/plan')
