from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('' ,views.home,name = 'home'),
    path('search/',views.search,name='search'),
    path('about_us/',views.about_us,name='about_us'),
    path('create_post/',views.create_post , name = 'create_post'),
    path('post_success/',views.post_success, name = 'post_success'),
    path('post_detail/<slug:slug>',views.post_detail,name = 'post_detail'),
    path('profile/',views.user_dashboard,name = 'profile'),
    path('post_update/<int:id>/',views.post_update,name= 'post_update'),
    path('post_delete/<int:id>/',views.post_delete,name='post_delete'),
    path('signup/',views.signup,name = 'signup'),
    path('login/',auth_views.LoginView.as_view(template_name = 'login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'logout.html'), name='logout'),
]