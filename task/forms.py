from django import forms
from .models import Task
from django.contrib.auth.models import User

    
class TaskForm(forms.ModelForm):
    pomodoro_count = forms.IntegerField(min_value=1, label='Pomodoro Count')

    class Meta:
        model = Task
        fields = ['name', 'description', 'due_date','pomodoro_count']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})
        }

    