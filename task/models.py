from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User



class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    STATUS_CHOICES = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed')
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    due_date = models.DateField(blank=True, null=True, default=None)
    pomodoro_count = models.IntegerField(default=0)


    @property
    def total_pomodoro(self):
        return self.pomodoro.count()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['status']

from django.db import models
from django.utils import timezone


class Pomodoro(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='pomodoro_sessions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'{self.task.name} - Pomodoro {self.id}'

    def start_timer(self):
        self.start_time = timezone.now()
        self.save()

    def pause_timer(self):
        pass

    def resume_timer(self):
        pass

    def stop_timer(self):
        self.end_time = timezone.now()
        self.save()

    def get_duration(self):
        duration = self.end_time - self.start_time
        seconds = duration.total_seconds()
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return timedelta(hours=hours, minutes=minutes, seconds=seconds)

    def is_active(self):
        return self.end_time is None

    class Meta:
        ordering = ['-start_time']
