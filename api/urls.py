# urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('topics/', views.topic_list, name='topic_list'),
    path('topics/<int:id>/', views.topic_detail_byid, name='topic_detail_byid'),
    path('topics/<int:topic_id>/entries/', views.entry_list, name='entry_list'),
    path('topics/<int:topic_id>/entries/<int:entry_id>/', views.entry_detail_byid, name='entry_detail_byid'),
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # 添加密码重置、密码修改等默认视图
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
