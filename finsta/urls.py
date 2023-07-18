"""finsta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignUpView.as_view(),name='register'),
    path('',views.SignInView.as_view(),name='login'),
    path('home/',views.IndexView.as_view(),name='home'),
    path('profiles/<int:pk>/change/',views.ProfileEditView.as_view(),name='profile-edit'),
    path('posts/<int:pk>/like',views.add_like_view,name='add-like'),
    path('posts/<int:pk>/comments/add/',views.comments_view,name='add-comment'),
    path('comments/<int:pk>',views.comment_remove_view,name='removecomment'),
    path('profile/<int:pk>',views.ProfileDetailView.as_view(),name='profile-detail'),
    path('profiles/<int:pk>/coverpic/change',views.coverpic_change_view,name='change-cover'),
    path('profiles/<int:pk>/profilepic/change',views.profilepic_change_view,name='change-propic'),
    path('profiles/all/',views.ProfileListView.as_view(),name='profile-list'),
    path('profiles/<int:pk>/follow',views.follow_user_view,name='follow'),
    path('profiles/<int:pk>',views.unfollow_user_view,name="unfollow"),
    path('posts/<int:pk>remove/',views.post_delete_view,name="post-remove"),
    path('logout',views.signout_view,name="logout"),
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
