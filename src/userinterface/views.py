from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required

from .models import Task, Subject
from .forms import UploadForm

import os
from django.conf import settings

# USER HANDLING
def user_login(request):
    return render(request, 'userinterface/login_form.html')


def user_logout(request):
    return HttpResponse('Logout Page.')


def welcome(request):
    if request.user.is_authenticated:
        return redirect('user_home')
    return render(request, 'userinterface/main.html')


# GENERAL
def help(request):
    return render(request, 'userinterface/help.html')


def impressum(request):
    return render(request, 'userinterface/impressum.html')


# DATA OVERVIEW
@login_required
def user_home(request):
    context = {
        'tasks': Task.objects.all(),
        'keywords': 'Home - ' + request.user.username
    }

    return render(request, 'userinterface/taskview.html', context)


@login_required
def my_tasks(request):
    my_tasks = Task.objects.filter(teacher=request.user)

    context = {
        'tasks': my_tasks,
        'tasknumber': len(my_tasks),
        'keywords': 'My tasks (' + request.user.username + ')',
    }

    return render(request, 'userinterface/taskview.html', context)


@login_required
def stages(request):
    return render(request, 'userinterface/overview.html', { 'stages': range(1, 14) })


@login_required
def stage(request, stagenumber):
    taskfilter = Task.objects.filter(stage=int(stagenumber))

    context = {
        'stage': stagenumber,
        'tasks': taskfilter,
        'keywords': 'Filter: Stage ' + str(stagenumber),
        'subjects': Subject.objects.all(),
        'tasknumber': len(taskfilter)
    }

    return render(request, 'userinterface/taskview.html', context)


@login_required
def subjects(request):
    return render(request, 'userinterface/overview.html', { 'subjects': Subject.objects.all() })


@login_required
def subject(request, subjectid):
    subject = Subject.objects.get(subject_id=subjectid)
    taskfilter = Task.objects.filter(subject=subject)

    context = {
        'subject': subject.subject_name,
        'tasks': taskfilter,
        'keywords': 'Filter: Subject ' + subject.subject_name,
        'tasknumber': len(taskfilter)
    }

    return render(request, 'userinterface/taskview.html', context)


@login_required
def stagesubject(request, stagenumber, subjectid):
    subject = Subject.objects.get(subject_id=subjectid)
    taskfilter = Task.objects.filter(stage=stagenumber, subject_id=subject)

    context = {
        'subject': subject.subject_name,
        'tasks': taskfilter,
        'keywords': 'Filter: Stage ' + str(stagenumber) + ' and subject ' + subject.subject_name,
        'tasknumber': len(taskfilter)
    }

    return render(request, 'userinterface/taskview.html', context)


@login_required
def details(request, taskid):
    task = Task.objects.get(task_id=taskid)

    context = {
        'task': task,
        'owner': (True if str(task.teacher) == str(request.user.username) else False)
    }

    return render(request, 'userinterface/details.html', context)


# SEARCH FUNCTIONALITY
@login_required
def searchoverview(request):
    return render(request, 'userinterface/searchbar.html')


@login_required
def search(request, keyword):
    results = Task.objects.filter(task_name__contains=keyword)

    if len(results) == 0:
        raise Http404('No tasks found.')

    context = {
        'keywords': 'Search: ' + str(keyword),
        'tasks': results
    }

    return render(request, 'userinterface/taskview.html', context)


# CONTENT UPLOAD
@login_required
def upload(request):
    form = UploadForm()

    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            Task.objects.get_or_create(
                teacher=request.user,
                task_name=form.cleaned_data['task_name'],
                subject=form.cleaned_data['subject'],
                stage=form.cleaned_data['stage'],
                document=request.FILES['document']
            )
            return redirect('user_home')

    return render(request, 'userinterface/upload.html', { 'form': form })


# CONTENT DOWNLOAD
@login_required
def download(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            return response
    raise Http404('File does not exist.')