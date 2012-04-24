from django.conf.urls.defaults import patterns, url
from django.conf.urls import include
from app.customer.api import CustomerResource

entry_resource = CustomerResource()

urlpatterns = patterns('app.customer.views',
    url(r'^$', 'overview', name="customer_overview"),
    (r'^new/$', 'new'),
    (r'^(?P<id>\w+)/view/$', 'view'),
    (r'^(?P<id>\w+)/edit/$', 'edit'),
    (r'^api/', include(entry_resource.urls)),


)