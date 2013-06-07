from django.conf.urls.defaults import patterns, url
from django.conf.urls import include

urlpatterns = patterns('focusbackup.app.customer.views',
    url(r'^$', 'overview', name="customer_overview"),
    (r'^new/$', 'new'),
    (r'^(?P<id>\w+)/view/$', 'view'),
    (r'^(?P<id>\w+)/edit/$', 'edit'),


)