from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('',views.index,name='index'),
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/',auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/passwordchange', auth_views.PasswordChangeView.as_view(template_name='user/password_change.html', success_url='password_change_done'), name='pwchange'),
    path('account/password_change_done/', views.password_change_done, name='password_change_done'),
    path('account/', views.account, name='account'),
    path('account/deposit/', views.deposit, name='deposit'),
    path('account/withdraw/', views.withdraw, name='withdraw'),
]
