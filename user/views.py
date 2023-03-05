from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .form import CustomUserCreationForm
from task.models import Task


class RegisterView(FormView):
    template_name = 'user/register.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'user/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Retrieve the number of tasks in each status for the current user
        new_count = Task.objects.filter(assigned_to=self.request.user, status='New').count()
        in_progress_count = Task.objects.filter(assigned_to=self.request.user, status='In Progress').count()
        completed_count = Task.objects.filter(assigned_to=self.request.user, status='Completed').count()
        total_count = new_count + in_progress_count + completed_count

        # Calculate the percentage of completed tasks
        if total_count > 0:
            completed_percentage = round(completed_count / total_count * 100, 2)
        else:
            completed_percentage = 0

        # Add the analytical data to the context
        context['new_count'] = new_count
        context['in_progress_count'] = in_progress_count
        context['completed_count'] = completed_count
        context['completed_percentage'] = completed_percentage

        return context