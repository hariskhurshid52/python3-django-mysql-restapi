from rest_framework import serializers
from web_services.models import Author, NewsStories


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id',
                  'name',
                  'username',
                  'password')


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsStories
        fields = (
            'headline',
            'id',
            'category',
            'author',
            'details',
            'region')
