import json, jwt
import datetime
from django.contrib.auth import authenticate
from django.http import QueryDict
from django.http.response import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from web_services.models import Author, NewsStories
from web_services.serializers import AuthorSerializer, StorySerializer

from rest_framework.decorators import api_view
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


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
        print(type(author_data))
        if author_data.get('username') is None:
            return HttpResponse('Username can not be empty', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        elif author_data.get('password') is None:
            return HttpResponse('Password can not be empty', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        response = Author.objects.filter(username__exact=author_data.get('username'),
                                         password__exact=author_data.get('password')).first()
        auth_serilizer = AuthorSerializer(response).data
        # response =json.loads(json.dumps(response))
        print(auth_serilizer.get('username'))
        if not auth_serilizer.get('username') is None:
            access_token = generate_access_token(auth_serilizer)
            refresh_token = generate_refresh_token(auth_serilizer)

            return JsonResponse(
                {"status": 'Successfully Login', 'access_token': access_token, 'refresh_token': refresh_token},
                safe=False, status=status.HTTP_200_OK)
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
        if not request.headers.get('Authorization'):
            return HttpResponse('Missing token', status=status.HTTP_401_UNAUTHORIZED,
                                content_type='text/plan')
        token = decode_token(request.headers.get('Authorization'))

        if (not isinstance(token, int)):
            return HttpResponse(token, status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        story_data = request.POST
        story_data = request.POST.copy()
        story_data['author'] = token

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
    print(request.user.is_authenticated)
    print(request.user)
    print(request.auth)
    if "GET" == request.method:
        if not request.headers.get('Authorization'):
            return HttpResponse('Missing token', status=status.HTTP_401_UNAUTHORIZED,
                                content_type='text/plan')
        token = decode_token(request.headers.get('Authorization'))

        if (not isinstance(token, int)):
            return HttpResponse(token, status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        stories = NewsStories.objects.filter(author_id=token).all()
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
        if not request.headers.get('Authorization'):
            return HttpResponse('Missing token', status=status.HTTP_401_UNAUTHORIZED,
                                content_type='text/plan')
        token = decode_token(request.headers.get('Authorization'))

        if (not isinstance(token, int)):
            return HttpResponse(token, status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        story_data = request.data
        if story_data.get('story_key') is None:
            return HttpResponse('Please provide valid story id', status=status.HTTP_400_BAD_REQUEST,
                                content_type='text/plan')
        try:
            story = NewsStories.objects.get(pk=story_data.get('story_key'),author_id=token)
            return HttpResponse('Successfully deleted story data', status=status.HTTP_201_CREATED)
        except NewsStories.DoesNotExist:
            return HttpResponse('Failed to delete story', status=status.HTTP_503_SERVICE_UNAVAILABLE,
                                content_type='text/plan')
    return HttpResponse("Unknown Method", status=status.HTTP_405_METHOD_NOT_ALLOWED, content_type='text/plan')


def generate_access_token(user):
    access_token_payload = {
        'user_id': user.get('id'),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=10, minutes=50),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256').decode('utf-8')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.get('id'),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256').decode('utf-8')

    return refresh_token


def decode_token(authorization_heaader):
    try:
        # header = 'Token xxxxxxxxxxxxxxxxxxxxxxxx'
        access_token = authorization_heaader.split(' ')[1]
        payload = jwt.decode(
            access_token, settings.SECRET_KEY, algorithms=['HS256'])
        user = Author.objects.filter(id=payload['user_id']).first()
        if user is None:
            return "User not found";
        return payload['user_id'];

    except jwt.ExpiredSignatureError:
        return "Expired token"
    except:
        return "Invalid token"
