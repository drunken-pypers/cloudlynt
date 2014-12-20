from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(
        r'^(?P<username>[A-Za-z0-9\-]+)/(?P<repo>[A-Za-z0-9\-]+)',
        'cloudlynt.github.views.build_lynt'),
)
