from django.urls import path, include
from . import views
app_name = "users" 


urlpatterns = [
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('accounts/', include(('django.contrib.auth.urls', 'django.contrib.auth'), namespace='login')),
]