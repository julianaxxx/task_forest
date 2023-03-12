from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils import timezone
from django.views import View
from django.http import Http404
from django.shortcuts import render
from .models import Task, Pomodoro
from .forms import TaskForm
from datetime import timedelta

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'task/task_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(assigned_to=self.request.user)
        search_input = self.request.GET.get('search-area', '')
        status_filter = self.request.GET.get('status', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if search_input:
            queryset = queryset.filter(name__icontains=search_input)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_filter'] = self.request.GET.get('status')
        context['search_input'] = self.request.GET.get('search-area')
        return context


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    template_name = 'task/task_form.html'

    def form_valid(self, form):
        task = form.save(commit=False)
        if not task.start_time:
            task.start_time = timezone.now()
            task.status = 'In Progress'
        if task.is_complete():
            task.status = 'Completed'
        task.save()
        return super().form_valid(form)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    template_name = 'task/task_delete.html'


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'task/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['task'] = self.object
        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.assigned_to = self.request.user
        form.instance.status = 'New'
        pomodoro_count = form.cleaned_data['pomodoro_count']
        task = form.save()
        task.pomodoro_count = pomodoro_count
        task.save()
        for i in range(pomodoro_count):
            Pomodoro.objects.create(task=task, user=self.request.user, start_time=timezone.now())
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['pomodoro'] = Pomodoro.objects.get(task_id=self.kwargs.get('task_id'))
        except Pomodoro.DoesNotExist:
            context['pomodoro'] = None
        return context



class TimerView(View):
    template_name = 'task/timer.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'start_timer':
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                raise Http404("Task does not exist")

            # Create a new pomodoro session for the task
            pomodoro = Pomodoro.objects.create(task=task, user=request.user)
            pomodoro.start_timer()

            # Calculate the end time for the pomodoro session
            duration = timedelta(minutes=25 * task.pomodoro_count)
            end_time = pomodoro.start_time + duration

            context = {
                'timer_running': True,
                'time_elapsed': pomodoro.get_duration(),
                'task_id': task_id,
                'pomodoro_id': pomodoro.id,
                'end_time': end_time,
                'pomodoro_count': task.pomodoro_count,  # add pomodoro count to context
            }
            return render(request, self.template_name, context)
        elif request.POST.get('action') == 'stop_timer':
            pomodoro_id = request.POST.get('pomodoro_id')
            try:
                pomodoro = Pomodoro.objects.get(id=pomodoro_id)
            except Pomodoro.DoesNotExist:
                raise Http404("Pomodoro does not exist")

            pomodoro.stop_timer()
            task_id = pomodoro.task.id

            context = {
                'timer_running': False,
                'time_elapsed': pomodoro.get_duration(),
                'task_id': task_id,
                'pomodoro_count': pomodoro.task.pomodoro_count,  # add pomodoro count to context
            }
            return render(request, self.template_name, context)
        else:
            context = {}
            return render(request, self.template_name, context)
