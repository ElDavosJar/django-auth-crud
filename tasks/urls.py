from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('tasks/', tasks, name='tasks'),
    path('tasks/completed/', completed_tasks, name='completed_tasks'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_pk>/', task_detail, name='task_detail'),
    path('tasks/<int:task_pk>/complete/', complete_task, name='complete_task'),
    path('tasks/<int:task_pk>/delete/', delete_task, name='delete_task'),
    
    path('logout/', signout, name='logout'),
    
    
]