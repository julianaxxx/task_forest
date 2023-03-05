
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Task


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task/task_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(assigned_to=self.request.user)
        search_input = self.request.GET.get('search-area')
        status_filter = self.request.GET.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if search_input:
            queryset = queryset.filter(name__icontains=search_input)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status')
        context['search_input'] = self.request.GET.get('search-area') or ''
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'task/task_detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'description', 'status']
    success_url = reverse_lazy('tasks')
    template_name = 'task/task_form.html'

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'status']
    success_url = reverse_lazy('tasks')
    template_name = 'task/task_form.html'


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'task/task_delete.html'
