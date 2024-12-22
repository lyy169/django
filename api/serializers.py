# serializers.py
from rest_framework import serializers
from notes.models import Topic, Entry

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'owner', 'created_at']

class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ['id', 'topic', 'text', 'created_at']
