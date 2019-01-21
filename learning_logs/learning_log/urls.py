from django.conf.urls import url
from . import views

urlpatterns = [
    # 主页
    url(r'^$', views.index, name='index'),
    # 显示所有的主题
    url(r'^topics/$', views.topics, name='topics'),
    # 显示特定主题
    url(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    # 新建主题
    url(r'^new_topic/$', views.new_topic, name='new_topic'),
    # 新建条目
    url(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry, name='new_entry'),
    # 编辑条目
    url(r'^edit_entry/(?P<entry_id>\d+)/$', views.edit_entry, name='edit_entry'),
]