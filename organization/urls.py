from django.urls import path
from . import views 
from .views import organization_detail,organization_register,multi_department,dashboard,insights
from django.contrib.auth import views as auth_views
from .forms import MyPasswordChangeForm
 

urlpatterns = [
    path('details/', organization_detail, name='organization_detail'),
    path("account/login/",views.login_form, name= "login"),
    path("account/logout/",views.user_logout,name="logout"),
    path("account/signup/",views.signup_form , name = "signup"),
    path('account/register/', organization_register, name='organization_register'),
    path('multi_department/',multi_department, name='multi_department'),
    path('dashboard/', dashboard, name='dashboard'),
    path('insights/', insights, name='insights'),
    path('register/multi-department/',multi_department, name='multi_department'),

     #urls for the email reset password
    path('account/password_reset/', auth_views.PasswordResetView.as_view(template_name='organization/password_reset.html'),name='password_reset'),

    path('account/password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='organization/password_reset_done.html'),name='password_reset_done'),

    path('account/password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='organization/password_reset_confirm.html'),name='password_reset_confirm'),

    path("account/password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="organization/password_reset_complete.html"),name='password_reset_complete'),
    path('feedback/',views.feedback,name='feedback'),
    path('handle-feedback-action/',views.handle_feedback_action,name="feedback-action"),
    path('handle-department-action/',views.handle_department_action,name="department-action"),
    path('qr-templates/',views.get_organization_qr_templates,name="organization-qr-tempaltes"),
    path('account/settings/',views.account_settings,name='account_settings'),
    path('account/settings/edit-account/',views.edit_account,name='edit_account'),
    path('account/password_change/', auth_views.PasswordChangeView.as_view(form_class=MyPasswordChangeForm), name='password_change'),
    path('account/password_change/done/', views.password_change_done, name='password_change_done')
    ]
