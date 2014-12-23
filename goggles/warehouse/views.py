from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from goggles.warehouse import tasks
from goggles.warehouse.models import Profile
from goggles.warehouse.forms import (
    ImportJobForm, ProfileForm, ConversationActionForm)
from goggles.warehouse.utils import update_profile_info_async

from celery import chain


def login(request):
    return render(request, 'login.html', {})


def logout(request):
    auth.logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('warehouse:login')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {
        'import_jobs': request.user.importjob_set.all(),
        'profiles': request.user.profile_set.all(),
        'conversations': request.user.conversation_set.all(),
    })


@login_required
def job(request, pk):
    job = request.user.importjob_set.get(pk=pk)
    return render(request, 'job.html', {
        'job': job,
    })


@login_required
def job_new(request):
    if request.method == 'POST':
        form = ImportJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = request.user
            job.save()
            messages.info(
                request, 'Job %s created successfully.' % (job.name,))
            return redirect('warehouse:dashboard')
    else:
        form = ImportJobForm()

    return render(request, 'job_new.html', {
        'form': form,
    })


@login_required
def job_edit(request, pk):
    job = request.user.importjob_set.get(pk=pk)
    if request.method == 'POST':
        form = ImportJobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.info(
                request, 'Job %s updated successfully.' % (job.name,))
            return redirect('warehouse:dashboard')
    else:
        form = ImportJobForm(instance=job)
    return render(request, 'job_edit.html', {
        'job': job,
        'form': form,
    })


@login_required
def profile_new(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            if form.cleaned_data['update_session_info']:
                update_profile_info_async(
                    profile.pk,
                    form.cleaned_data['username'],
                    form.cleaned_data['password'])
            messages.info(
                request, 'Profile added, fetching session information.')
            return redirect('warehouse:dashboard')
    else:
        form = ProfileForm(initial={
            'update_session_info': True,
            'fetch_conversations': True,
        })

    return render(request, 'profile_new.html', {
        'form': form,
    })


@login_required
def profile(request, pk):
    profile = request.user.profile_set.get(pk=pk)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            if form.cleaned_data['update_session_info']:
                update_profile_info_async(
                    profile,
                    form.cleaned_data['username'],
                    form.cleaned_data['password'])
            messages.info(
                request,
                'Profile %s updated successfully.' % (profile.username,))
            return redirect('warehouse:dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {
        'profile': profile,
        'form': form,
    })


@login_required
def conversation(request, pk):
    all_conversations = request.user.conversation_set.all()
    conversation = request.user.conversation_set.get(pk=pk)
    if request.method == 'POST':
        form = ConversationActionForm(request.POST)
        if form.is_valid():
            response = form.handle_action(conversation)
            messages.info(request, response)
            return redirect('warehouse:conversation', pk=pk)
    else:
        form = ConversationActionForm()

    return render(request, 'conversation.html', {
        'conversation': conversation,
        'form': form,
    })
