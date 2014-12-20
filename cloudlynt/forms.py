# -*- coding: utf-8 -*-


from django import forms


class HomePageForm(forms.Form):
    github_user = forms.CharField(
        label='Github User/Owner Name', required=True)

    github_repo = forms.CharField(
        label='Github Repo Name', required=True)
