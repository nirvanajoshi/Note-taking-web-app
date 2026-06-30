from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Note, Tag
from .forms import NoteForm, TagForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created! Please login.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'notes/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('note_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'notes/login.html')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user)
    
    search = request.GET.get('search')
    if search:
        notes = notes.filter(Q(title__icontains=search) | Q(content__icontains=search))
    
    tag_id = request.GET.get('tag')
    if tag_id:
        notes = notes.filter(tags__id=tag_id)
    
    tags = Tag.objects.filter(user=request.user)
    return render(request, 'notes/note_list.html', {
        'notes': notes,
        'tags': tags
    })

#add notes 
@login_required
def add_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('note_list')
    else:
        form = NoteForm()
    return render(request, 'notes/add_note.html', {'form': form})


#edit notes
@login_required
def edit_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated.')
            return redirect('note_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/edit_note.html', {'form': form})

#delete notes
@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        note.delete()
        return redirect('note_list')
    return render(request, 'notes/delete_note.html', {'note': note})

#toggle pin 
@login_required
def toggle_pin(request, note_id):
    note = get_object_or_404(Note, id=note_id, user=request.user)
    note.is_pinned = not note.is_pinned
    note.save()
    return redirect('note_list')

#tag list
@login_required
def tag_list(request):
    tags = Tag.objects.filter(user=request.user)
    return render(request, 'notes/tag_list.html', {'tags': tags})

#add tag 
@login_required
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'notes/add_tag.html', {'form': form})

#edit tag
@login_required
def edit_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    if request.method == 'POST':
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tag updated.')
            return redirect('tag_list')
    else:
        form = TagForm(instance=tag)
    return render(request, 'notes/edit_tag.html', {'form': form})

#delete tag
@login_required
def delete_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id, user=request.user)
    if request.method == 'POST':
        tag.delete()
        return redirect('tag_list')
    return render(request, 'notes/delete_tag.html', {'tag': tag})

