from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'user'

urlpatterns = [
    path('',views.Index.as_view(),name='index'),
    path('register/', views.Register.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('login/',auth_views.LoginView.as_view(template_name='user/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account/passwordchange', auth_views.PasswordChangeView.as_view(template_name='user/password_change.html', success_url='password_change_done'), name='pwchange'),
    path('account/password_change_done/', views.password_change_done, name='password_change_done'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('account/deposit/', views.DepositView.as_view(), name='deposit'),
    path('account/withdraw/', views.WithdrawView.as_view(), name='withdraw'),
]
