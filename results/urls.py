from django.urls import path
from .views import add_marks, view_marks, edit_marks, delete_marks, download_result

urlpatterns = [
    path('add/', add_marks, name='add_marks'),
    path('view/', view_marks, name='view_marks'),
    path('edit/<int:pk>/', edit_marks, name='edit_marks'),
    path('delete/<int:pk>/', delete_marks, name='delete_marks'),
    path('download/', download_result, name='download_result'),
]