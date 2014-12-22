# -*- coding: utf-8 -*-
import os
import subprocess
import uuid
from collections import Counter
from django.shortcuts import render_to_response
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


def tokenize_flake_output(lint_log):
    lint_error_lines = lint_log.split('\n')
    tokenized_lines = []
    for line in lint_error_lines:
        if not line:
            continue
        file_and_line, error_code, msg = line.split(' ', 2)
        file_path, line_no, column_no, _ = file_and_line.split(':')
        tokenized_lines.append({'file_path': file_path,
                                'line_no': line_no,
                                'column_no': column_no,
                                'error_code': error_code,
                                'error_message': msg})
    return tokenized_lines


def process_lint_errors(tokenized_log):
    lint_code_counter = Counter()
    error_warning_counter = Counter()
    for item in tokenized_log:
        lint_code_counter[item['error_code']] += 1
        if item['error_code'].startswith('E'):
            error_warning_counter['errors'] += 1
        else:
            error_warning_counter['warnings'] += 1
    return {
        'total': len(tokenized_log),
        'numbers_by_code': lint_code_counter,
        'errors_and_warnings': error_warning_counter
    }


def run_flake_on_repo(dir_path):
    process = subprocess.Popen(
        ['flake8', dir_path],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, errors = process.communicate()
    print output, process.returncode
    if process.returncode == 1:
        tokenized_output = tokenize_flake_output(
            output.replace(dir_path+'/', ''))

        return {
            'success': True,
            'lint_errors': True,
            'data': {
                'meta': process_lint_errors(tokenized_output),
                'tokenized_output': tokenized_output
            },
            'message': ''
        }
    elif process.returncode == 0:
        return {
            'success': True,
            'lint_errors': False,
            'message': 'Yo, No lint errors.',
            'data': None
        }
    else:
        return {
            'success': False,
            'message': ("Sorry, we're in a drunken stuper."
                        " When sober we'll fix the issue")
        }


def build_lynt(request, username, repo):
    dir_path = download_repo(username, repo)
    if not dir_path:
        return HttpResponse("LOL", status=404)

    result = run_flake_on_repo(dir_path)
    result.update({
        'username': username,
        'repo': repo
    })
    if result.get('success'):
        return render_to_response("github/build_lynt.html", result)

    return HttpResponse(result)
