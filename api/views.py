from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect, render, get_object_or_404
from pyexpat.errors import messages
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from api.serializers import TopicSerializer, EntrySerializer
from notes.models import Topic, Entry
from django.contrib import messages
from .forms import TopicForm, EntryForm  # 你需要创建一个TopicForm来处理主题的表单
from notes.models import Topic, Entry
@login_required
def home(request):
    topics = Topic.objects.all()  # 获取所有主题
    for topic in topics:
        topic.entries = Entry.objects.filter(topic=topic)  # 获取每个主题下的条目
    return render(request, 'home.html', {'topics': topics})
# 创建主题视图
@login_required
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user  # 设置当前用户为主题的拥有者
            new_topic.save()
            return redirect('home')  # 创建成功后返回首页
    else:
        form = TopicForm()

    return render(request, 'registration/create_topic.html', {'form': form})

# 创建条目视图
@login_required
def create_entry(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id, owner=request.user)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic  # 将条目绑定到对应主题
            new_entry.save()
            return redirect('home')  # 创建成功后返回首页
    else:
        form = EntryForm()

    return render(request, 'registration/create_entry.html', {'form': form, 'topic': topic})
# 处理获取所有主题和创建主题
@api_view(['GET', 'POST'])
@login_required
def topic_list(request):
    if request.method == 'GET':
        topics = Topic.objects.all()  # 获取所有主题
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TopicSerializer(data=request.data)  # 序列化传入的数据
        if serializer.is_valid():
            serializer.save()  # 保存数据
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 处理单个主题的详细信息（获取、更新、删除）
@api_view(['GET', 'POST', 'DELETE'])
@login_required
def topic_detail_byid(request, id):
    try:
        topic = Topic.objects.get(id=id)  # 获取具体主题
    except Topic.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TopicSerializer(topic)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TopicSerializer(topic, data=request.data)  # 更新主题数据
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        topic.delete()  # 删除主题
        return Response(status=status.HTTP_204_NO_CONTENT)  # 返回204 No Content，表示成功删除


@login_required
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user  # 设置当前用户为主题的拥有者
            new_topic.save()
            return redirect('home')  # 创建成功后重定向到首页
    else:
        form = TopicForm()

    return render(request, 'registration/create_topic.html', {'form': form})
# 处理某个主题下的条目（获取、创建）
@api_view(['GET', 'POST'])
@login_required
def entry_list(request, topic_id):
    try:
        topic = Topic.objects.get(id=topic_id)  # 获取指定的主题
    except Topic.DoesNotExist:
        return Response({'detail': 'Topic not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        entries = Entry.objects.filter(topic=topic)  # 获取该主题下的所有条目
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(topic=topic)  # 绑定条目到指定的主题
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 处理单个条目的详细信息（获取、更新、删除）
@api_view(['GET', 'POST', 'DELETE'])
@login_required
def entry_detail_byid(request, topic_id, entry_id):
    try:
        topic = Topic.objects.get(id=topic_id)  # 获取指定的主题
    except Topic.DoesNotExist:
        return Response({'detail': 'Topic not found.'}, status=status.HTTP_404_NOT_FOUND)

    try:
        entry = Entry.objects.get(id=entry_id, topic=topic)  # 获取指定主题下的条目
    except Entry.DoesNotExist:
        return Response({'detail': 'Entry not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EntrySerializer(entry)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EntrySerializer(entry, data=request.data)  # 更新条目数据
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        entry.delete()  # 删除条目
        return Response(status=status.HTTP_204_NO_CONTENT)  # 返回204 No Content，表示成功删除
# 注册视图
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '注册成功！请登录。')
            return redirect('login')
        else:
            messages.error(request, '注册失败，请检查输入的内容。')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# 登录视图
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # 重定向到首页，或其他你需要的页面    # 注意：重定向的位置不是网址名，而是方法函数明
        else:
            messages.error(request, '用户名或密码不正确。')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

# 登出视图
def logout_view(request):
    logout(request)
    return redirect('login')  # 登出后重定向到登录页