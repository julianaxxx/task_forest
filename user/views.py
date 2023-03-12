import math
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
from django.contrib.auth.decorators import login_required
from task.models import Task
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from pet.models import Pet, Species




class RegisterView(FormView):
    template_name = 'user/register.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('welcome')

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
        pet = Pet.objects.filter(user=self.request.user).first()
        context['pet'] = pet
        context['Species'] = Species
        context['pet_name'] = pet.name if pet else None
        return context

def dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)

    if not tasks:
        message = "You have no tasks assigned."
        return render(request, 'user/dashboard.html', {'message': message})

    new_count = tasks.filter(status='New').count()
    in_progress_count = tasks.filter(status='In Progress').count()
    completed_count = tasks.filter(status='Completed').count()
    total_count = new_count + in_progress_count + completed_count

    completed_percentage = round(completed_count / total_count * 100, 2) if total_count > 0 else 0

    labels = ['New', 'In Progress', 'Completed']
    values = [new_count, in_progress_count, completed_count]
    colors = ['#63A58D', '#CBA2C9', '#CBA2C9']
    fig, ax = plt.subplots()
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%')
    ax.set_title('Task Status')
    ax.axis('equal')
    plt.tight_layout()

    fig.patch.set_facecolor((68/255, 100/255, 120/255, 0))

    buffer = BytesIO()
    fig.savefig(buffer, format='png', bbox_inches='tight')
    chart_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()

    context = {
        'new_count': new_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'completed_percentage': completed_percentage,
        'chart_image': chart_image,
    }

    return render(request, 'user/dashboard.html', context)
