"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from api.views import login_view, signup_view, logout_view, create_post, fetch_posts, add_xp, get_single_post,fetch_comments, delete_post, delete_comment

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view),
    path('signup/', signup_view),
    path('logout/', logout_view),
    path('post/', create_post),
    path('posts/', fetch_posts),
    path('xp/', add_xp),
    path('posts/<int:id>/', get_single_post),
    path('comments/<int:id>/', fetch_comments),
    path('delete_post/<int:id>/', delete_post),
    path('delete_comment/<int:id>/', delete_comment)
]
