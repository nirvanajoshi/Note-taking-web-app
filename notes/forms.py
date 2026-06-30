from django import forms
from .models import Note, Tag

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'tags', 'is_pinned']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'is_pinned': forms.CheckboxInput(attrs={'class': 'form-check-input', 'role': 'switch'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Note title...'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 8, 'placeholder': 'Write your note here...'}),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tag name...'}),
        }