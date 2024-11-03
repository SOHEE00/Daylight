"""
URL configuration for TodoBoard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index, name='index'),
    path('createTodo/',views.Create_todo, name='create_Todo'),
    path('deleteTodo/',views.Todo_delete, name='Todo_Delete'),
    path('updatePage/update/', views.Update_todo, name='Update_todo'),
    path('updatePage/<str:todo_id>/',views.Todo_update, name='Todo_update'),
    path('markAsDone/',views.markDone, name='markDone'),
    path('markAsStar/',views.markStar, name='markAsStar'),
    path('deleteDone/',views.delete_done,name='delete_done'),
    path('updateModal/', views.update_modal, name='update_modal'),
    path('timesheet/', views.timesheet, name='timesheet'),
    path('starpage/', views.starpage, name='starpage'),
    path('starpage/Delete_Star/',views.delete_star, name='delete_star'),
    path('sharedPage/', views.sharedpage, name='sharedPage'),
    path('main/', views.main, name='main'),
    path('login/', views.custom_login_view, name='login'),
    path('loginsheet/',views.loginsheet, name='loginsheet'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)