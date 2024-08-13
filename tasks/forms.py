from django.forms import ModelForm
from .models import Task
from django import forms

# Create a form for the Task model
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title of the task'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter the description of the task'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input text-center'}),
        
        }
        
    
