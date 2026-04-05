from django.urls import path
from .views import user_login, admin_dashboard, teacher_dashboard, student_dashboard, home
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),  # ✅ IMPORTANT FIX

    path('login/', user_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('student/dashboard/', student_dashboard, name='student_dashboard'),
]