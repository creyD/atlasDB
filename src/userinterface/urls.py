from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

urlpatterns = [
    # User login and logout views
    path('login/', LoginView.as_view(template_name='userinterface/login_form.html'), name='user_login'),
    path('logout/', LogoutView.as_view(), name='user_logout'),
    path('home/', views.user_home, name='user_home'),

    # Task views
    path('my_tasks/', views.my_tasks, name='my_tasks'),
    path('task/<int:taskid>/', views.details, name='task'),
    path('task/<int:taskid>/edit', views.task_update, name='task_edit'),
    path('task/<int:taskid>/download', views.task_download, name='task_download'),

    path('upload/', views.upload, name='upload'),

    path('stages/', views.stages, name='stages'),
    path('stage/<int:stagenumber>/', views.stage, name='stage'),
    path('subjects/', views.subjects, name='subjects'),
    path('subject/<int:subjectid>/', views.subject, name='subject'),

    path('search/', views.searchoverview, name='search'),
    path('search/<str:keyword>/', views.search, name='search'),

    path('stage_<int:stagenumber>&subject_<int:subjectid>/', views.stagesubject, name='stagesubject'),

    # General, public views
    path('help/', views.help_page, name='help'),
    path('impressum/', views.impressum, name='impressum'),
    path('', views.welcome, name='welcome')
]
