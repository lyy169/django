from django import forms
from notes.models import Topic, Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['title', 'public']  # 添加 public 字段
        labels = {'title': '标题', 'public': '公开'}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']  # 条目的标题
