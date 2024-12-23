from django import forms
from notes.models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title']  # 主题的标题

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']  # 条目的标题
