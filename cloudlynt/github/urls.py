from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(
        r'^(?P<username>[A-Za-z0-9\-]+)/(?P<repo>[A-Za-z0-9\-\.]+)',
        'cloudlynt.github.views.build_lynt', name="build-github-lynt"),
)
