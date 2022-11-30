from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'common'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
] # django.contrib.auth 앱의 LoginView 클래스 활용
# LoginView는 자동으로 registration 템플릿 디렉터리에서 login.html 찾아서 디렉터리 바꾸려면 template_name='' 하기