from django import forms
from .models import Service


class ServiceForm(forms.ModelForm):
    """Form for adding new services from the frontend"""
    
    class Meta:
        model = Service
        fields = ['name', 'description', 'port', 'protocol', 'category', 'icon_name', 'order']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-white focus:border-accent focus:outline-none',
                'placeholder': 'Service Name (e.g., Gitea)'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-white focus:border-accent focus:outline-none',
                'placeholder': 'Brief description of the service',
                'rows': 3
            }),
            'port': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-white focus:border-accent focus:outline-none',
                'placeholder': 'Port number (e.g., 3000)'
            }),
            'protocol': forms.Select(attrs={
                'class': 'w-full px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-white focus:border-accent focus:outline-none'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-white focus:border-accent focus:outline-none'
            }),
            'icon_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-white focus:border-accent focus:outline-none',
                'placeholder': 'Bootstrap icon class (e.g., bi-git)'
            }),
            'order': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 bg-dark-card border border-dark-border rounded-lg text-white focus:border-accent focus:outline-none',
                'placeholder': 'Display order (lower = first)',
                'value': 0
            }),
        }
