from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Job


# ======== login/register pages ==================================
def login(request):
    context = {
        'title': 'Login',
    }
    return render(request, 'users/login.html', context)

def process_login(request):
    print(request.POST)
    if User.objects.validate(request.POST):
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
    else:
        error = 'Email or password is incorrect, please verify or register.'
        messages.error(request, error)
        return redirect('/login')
    return redirect('/dashboard')

def process_register(request):
    errors = User.objects.register_validate(request.POST)

    if errors:
        for error in errors:
            messages.error(request, error)
    else:
        user =User.objects.create_user(request.POST)
        print(user.f_name)
        request.session['user_id'] = user.id
        return redirect('/dashboard')
    return redirect('/login')

# ========= create/edit Jobs pages =============================================

def addjob(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    context = {
        'title': 'Add Job',
    }
    return render(request, 'users/add_job.html', context)

def addjob_verify(request):
    errors = Job.objects.addjob_verify(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
    else:
        job = Job.objects.create_job(request.POST, request.session['user_id'])
        return redirect('/dashboard')
    return redirect('/addjob')

def create_job_for_user(request, job_id):
    job = Job.objects.get(id=job_id)
    user = User.objects.get(id=request.session['user_id'])
    job.worker = user
    job.save()
    return redirect('/dashboard')

def edit_job(request, job_id):
    job = Job.objects.get(id=job_id)
    context = {
        'title':'Edit Job',
        'job' : job
    }
    return render(request, 'users/edit_job.html', context)

def update_job_verify(request):
    errors = Job.objects.addjob_verify(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        job = Job.objects.get(id=request.POST['id'])
        context = {
            'title': 'Edit Job',
            'job': job
        }
        return render(request, 'users/edit_job.html', context)
    else:
        job = Job.objects.get(id=request.POST['id'])
        job.title=request.POST['title']
        job.description=request.POST['description']
        job.location=request.POST['location']
        job.save()
    return redirect('/dashboard')

# ============= View job/Dasboard pages==========================================

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    name = User.objects.get(id=request.session['user_id'])
    users = User.objects.all()
    jobs = Job.objects.all()
    context = {
        'name':name,
        'title': 'Dashboard',
        'jobs':jobs,
        'users':users,
    }

    return render(request, 'users/dashboard.html', context)

def view_job(request, job_id):
    job = Job.objects.get(id=job_id)
    context = {
        'title': 'View Job',
        'job':job,
    }
    return render(request, 'users/view_job.html', context)

# ============= logout, delete/cancel pages==========================================

def delete(request, job_id):
    job = Job.objects.get(id=job_id)
    job.delete()
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/login')
