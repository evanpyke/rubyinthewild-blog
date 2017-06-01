from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='list'),
    url(r'^blog/new/$', views.post_new, name='new'),
    url(r'^blog/drafts/$', views.post_draft_list, name='draft_list'),
    url(r'^blog/(?P<slug>[-\w]+)/$', views.post_detail, name='detail'),
    url(r'^blog/(?P<slug>[-\w]+)/comment/$', views.add_comment_to_post, name='comment'),
    url(r'^blog/(?P<slug>[-\w]+)/edit/$', views.post_edit, name='edit'),
    url(r'^blog/(?P<slug>[-\w]+)/publish/$', views.post_publish, name='publish'),
    url(r'^blog/(?P<slug>[-\w]+)/remove/$', views.post_remove, name='remove'),
]

    # url(r'^post/(?P<slug>[-\w]*)-(?P<pk>\d+)/$', views.post_detail, name='detail'),
