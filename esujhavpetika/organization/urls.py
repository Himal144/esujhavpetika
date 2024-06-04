from django.urls import path
from . import views 
from .views import organization_detail,organization_register,multi_department,dashboard
from django.contrib.auth import views as auth_views
 

urlpatterns = [
    path('organization/<int:id>/', organization_detail, name='organization_detail'),
    path("",views.baseapp, name='baseapp'),
    path("login/",views.login_form, name= "login"),
    path("signup/",views.signup_form , name = "signup"),
    path('organization/register/', organization_register, name='organization_register'),
    path('organization/multi_department/',multi_department, name='multi_department'),
    path('organization/dashboard/', dashboard, name='dashboard'),
    path('organization/register/multi-department/',multi_department, name='multi_department'),

     #urls for the email reset password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='organization/password_reset.html'),name='password_reset'),

    path('password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='organization/password_reset_done.html'),name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='organization/password_reset_confirm.html'),name='password_reset_confirm'),

    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="organization/password_reset_complete.html"),name='password_reset_complete'),
    path('feedback/',views.feedback,name='feedback'),
    path('handle-feedback-action/',views.handle_feedback_action,name="feedback-action")
    ]
