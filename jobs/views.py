from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .forms import JobForm
from .models import Job, JobApplicant

# --- Job Create ---
class JobCreateView(UserPassesTestMixin, CreateView):
    model = Job
    fields = ['job_title', 'job_description', 'min_offer', 'max_offer', 'location']
    template_name = 'jobs/job_form.html'

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('jobs:job_list_view')


# --- Job List ---
def job_list_view(request):
    query = request.GET.get('q')
    jobs = Job.objects.all()
    if query:
        jobs = jobs.filter(job_title__icontains=query)
    return render(request, 'jobs/job_list.html', {'jobs': jobs})


# --- Job Detail ---
def job_detail_view(request, pk):
    job = get_object_or_404(Job, pk=pk)
    user = request.user

    if not user.is_authenticated:
        return render(request, 'auth/401.html', status=401)

    applicants = JobApplicant.objects.filter(job=job)

    # Get the current user's application if exists
    try:
        user_application = JobApplicant.objects.get(user=user, job=job)
    except JobApplicant.DoesNotExist:
        user_application = None

    context = {
        'job': job,
        'user': user,
        'applicants': applicants,
        'user_application': user_application,
    }
    return render(request, 'jobs/job_detail.html', context)


# --- Job Update ---
class JobUpdateView(UserPassesTestMixin, UpdateView):
    form_class = JobForm
    template_name = 'jobs/job_update.html'
    queryset = Job.objects.all()

    def test_func(self):
        job = self.get_object()
        return self.request.user.is_staff or job.user == self.request.user

    def get_success_url(self):
        return reverse_lazy('jobs:job_detail_view', kwargs={'pk': self.object.pk})


# --- Job Delete ---
class JobDeleteView(UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'jobs/job_delete.html'
    success_url = reverse_lazy('jobs:job_list_view')

    def test_func(self):
        job = self.get_object()
        return self.request.user.is_staff or job.user == self.request.user


# --- Job Apply ---
def job_apply(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if not request.user.is_authenticated:
        return render(request, 'auth/401.html', status=401)

    try:
        existing_application = JobApplicant.objects.get(user=request.user, job=job)
    except JobApplicant.DoesNotExist:
        existing_application = None

    if request.method == 'POST':
        resume = request.FILES.get('resume')
        if not resume:
            messages.error(request, 'Please upload your resume.')
            return render(request, 'jobs/job_apply.html', {'job': job})
        
        if existing_application and existing_application.status != 'rejected':
            messages.error(request, 'You have already applied for this job.')
            return redirect('jobs:job_detail_view', pk=job.pk)

        if existing_application and existing_application.status == 'rejected':
            existing_application.resume = resume
            existing_application.status = 'pending'
            existing_application.save()
        else:
            JobApplicant.objects.create(job=job, user=request.user, resume=resume)
        
        messages.success(request, 'Application submitted successfully!')
        return redirect('jobs:job_detail_view', pk=job.pk)

    return render(request, 'jobs/job_apply.html', {'job': job})


# --- Job Reject ---
@login_required
def job_reject_view(request, applicant_id):
    applicant = get_object_or_404(JobApplicant, pk=applicant_id)
    if request.user != applicant.job.user:
        messages.error(request, "You don't have permission to reject this applicant.")
        return redirect('jobs:job_detail_view', pk=applicant.job.pk)

    applicant.status = 'rejected'
    applicant.save()
    messages.success(request, f"{applicant.user.username}'s application has been rejected.")
    return redirect('jobs:job_detail_view', pk=applicant.job.pk)
