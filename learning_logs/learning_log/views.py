from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from .models import Topic,Entry
from .forms import TopicForm, EntryForm


# Create your views here.
def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_log/index.html')

@login_required
def topics(request):
    """显示所有的主题"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}

    return render(request, 'learning_log/topics.html',context)

@login_required
def topic(request, topic_id):
    """显示特定主题及其所有条目"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request,'learning_log/topic.html', context)

@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':
        # 如果未提交数据
        form = TopicForm()
    else:
        # 提交数据,对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            # 先保存 但是不提交，因为后面要修改，后面也会提交
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_log:topics'))

    context = {'form': form}
    return render(request, 'learning_log/new_topic.html', context)

@login_required
def new_entry(request,topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_log:topic', args=[topic_id]))

    context = {'topic': topic ,'form':form}
    return render(request, 'learning_log/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        #初次请求,使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        #提交了数据,处理数据
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_log:topic',args=[topic.id]))

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_log/edit_entry.html', context)




