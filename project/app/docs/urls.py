from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('app.docs.views',
    url(r'^$', 'overview', name="docs_overview"),
)