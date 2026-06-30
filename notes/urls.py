from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('', views.note_list, name='note_list'),
    path('notes/add/', views.add_note, name='add_note'),
    path('notes/edit/<int:note_id>/', views.edit_note, name='edit_note'),
    path('notes/delete/<int:note_id>/', views.delete_note, name='delete_note'),
    path('notes/pin/<int:note_id>/', views.toggle_pin, name='toggle_pin'),

    path('tags/', views.tag_list, name='tag_list'),
    path('tags/add/', views.add_tag, name='add_tag'),
    path('tags/edit/<int:tag_id>/', views.edit_tag, name='edit_tag'),
    path('tags/delete/<int:tag_id>/', views.delete_tag, name='delete_tag'),
]