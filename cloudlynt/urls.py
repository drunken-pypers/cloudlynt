from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^github/', include('cloudlynt.github.urls')),
)
