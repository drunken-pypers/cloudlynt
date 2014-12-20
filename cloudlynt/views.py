# -*- coding: utf-8 -*-


from django.shortcuts import render_to_response, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from cloudlynt.forms import HomePageForm


def home(request):
    if request.method == 'POST':
        form = HomePageForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(
                reverse(
                    "build-github-lynt",
                    kwargs={
                        "username": form.cleaned_data['github_user'],
                        "repo": form.cleaned_data['github_repo']
                    }
                )
            )

    else:
        form = HomePageForm()

    return render_to_response(
        "home.html", {"form": form},
        context_instance=RequestContext(request))
