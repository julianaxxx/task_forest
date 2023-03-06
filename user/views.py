from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, FormView
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .form import CustomUserCreationForm
from task.models import Task
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from io import BytesIO
import base64

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.conf import settings




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

        new_count = Task.objects.filter(assigned_to=self.request.user, status='New').count()
        in_progress_count = Task.objects.filter(assigned_to=self.request.user, status='In Progress').count()
        completed_count = Task.objects.filter(assigned_to=self.request.user, status='Completed').count()
        total_count = new_count + in_progress_count + completed_count

        if total_count > 0:
            completed_percentage = round(completed_count / total_count * 100, 2)
        else:
            completed_percentage = 0

        labels = ['New', 'In Progress', 'Completed']
        values = [new_count, in_progress_count, completed_count]
        colors = ['#FFC107', '#007BFF', '#28A745']
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
        ax.set_title('Task Status')
        ax.axis('equal')
        plt.tight_layout()

        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        chart_image = ContentFile(buffer.getvalue())
        buffer.close()

        chart_image_base64 = base64.b64encode(chart_image.read()).decode('utf-8')
        chart_image_data_uri = f"data:image/png;base64,{chart_image_base64}"

        context['new_count'] = new_count
        context['in_progress_count'] = in_progress_count
        context['completed_count'] = completed_count
        context['completed_percentage'] = completed_percentage
        context['task_status_image'] = chart_image_data_uri

        return context