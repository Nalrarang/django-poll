from django.conf.urls import url
from . import views

urlpatterns = [
    # Main Page Render
    url(r'^$', views.poll_main, name='poll_main'),
    # Result Page Render
    url(r'^result/$', views.poll_result, name='poll_result'),
    # Vote Request 
    url(r'^poll/vote/$', views.poll_vote, name='poll_vote'),
]