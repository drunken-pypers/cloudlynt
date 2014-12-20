# -*- coding: utf-8 -*-
import os
import subprocess
import uuid
from django.http import HttpResponse


def _generate_tar_url(username, repo):
    return "https://github.com/{}/{}/archive/master.tar.gz".format(
        username, repo)


def download_repo(username, repo):
    url = _generate_tar_url(username, repo)
    dir_path = "/tmp/{}".format(uuid.uuid4().hex)
    os.mkdir(dir_path)
    return_code = subprocess.call('curl -L {} | tar -xz -C {}'.format(
        url, dir_path), shell=True)

    if not return_code:
        return "{}/{}-master".format(dir_path, repo)
    else:
        return False


def run_flake_on_repo(dir_path):
    process = subprocess.Popen(
        ['flake8', dir_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = process.communicate()
    print output, process.returncode
    if process.returncode == 1:
        return '<code>{}</code>'.format(
            output.replace('\n', '<br/>').replace(dir_path, ''))
    elif process.returncode == 0:
        return "Yo"
    else:
        return ("Sorry, we're in a drunken stuper."
                " When sober we'll fix the issue")


def build_lynt(request, username, repo):
    dir_path = download_repo(username, repo)
    if not dir_path:
        return HttpResponse("LOL", status=404)

    result = run_flake_on_repo(dir_path)
    return HttpResponse(result)
