from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/create/', views.create_post, name='create_post'),
    path('like/<int:pk>/', views.like_post, name='like_post'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
    path('profile/<int:profile_id>/follow/', views.follow_profile, name='follow_profile'),



]
