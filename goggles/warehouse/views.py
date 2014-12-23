from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

from goggles.warehouse.forms import ImportJobForm


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
    })


@login_required
def job(request, pk):
    job = request.user.importjob_set.get(pk=pk)
    return render(request, 'job.html', {
        'job': job,
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
