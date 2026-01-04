from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path("logout/", auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("post_login/", views.login_redirect_view, name='post_login'),
    path("client_home/", views.client_home, name='client_home'),
    path("employer_home/", views.employer_home, name='employer_home'),
    path("insured_home/", views.insured_home, name='insured_home'),
    path("profile_update/", views.profile_update, name='profile_update'),
    path("insurance_contributions/", views.insurance_contributions, name='insurance_contributions'),
    path("print_insurance_history/", views.print_insurance_history, name='print_insurance_history'),
    path("apd_submission/", views.apd_submission, name='apd_submission'),
    path("code_info/", views.code_info, name='code_info'),
    path("get_last_contribution/", views.get_last_contribution, name='get_last_contribution'),
    path("current_obligations/", views.current_obligations, name='current_obligations'),
    path("unsettled_overdue/", views.unsettled_overdue, name='unsettled_overdue'),
    path("settled_overdue/", views.settled_overdue, name='settled_overdue'),
    path("employees/", views.employees_list, name='employees_list'),
    path("payments/", views.payments_screen, name='payments'),
]