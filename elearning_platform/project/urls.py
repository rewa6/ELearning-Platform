from django.urls import path
from .views import RegisterView, LoginView, LogoutView, EndUserLoginView
from . import views

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/enduser-login/', EndUserLoginView.as_view(), name='enduser-login'),
    
     # PROFILE
    path('user/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('user/endusers/', views.UserEndUserListView.as_view(), name='user-endusers'),

    # SUBSCRIPTION
    path('subscribe/', views.SubscriptionCreateView.as_view(), name='subscribe'),
    path('subscribe/status/', views.SubscriptionStatusView.as_view(), name='subscribe-status'),
    path('subscribe/renew/', views.SubscriptionRenewView.as_view(), name='subscribe-renew'),
    path('subscribe/reminder/', views.SubscriptionReminderEmailView.as_view(), name='subscribe-reminder'),

    # END USER MANAGEMENT
    path('endusers/generate/', views.EndUserGenerateView.as_view(), name='enduser-generate'),
    path('endusers/', views.EndUserListView.as_view(), name='enduser-list'),
    path('endusers/<int:id>/deactivate/', views.EndUserDeactivateView.as_view(), name='enduser-deactivate'),
    path('endusers/validate/', views.EndUserValidateView.as_view(), name='enduser-validate'),

    # MODULES
    path('modules/upload/', views.ModuleUploadView.as_view(), name='module-upload'),
    path('modules/<int:id>/publish/', views.ModulePublishToggleView.as_view(), name='module-publish'),
    path('modules/', views.ModuleListView.as_view(), name='module-list'),
    path('modules/<int:id>/', views.ModuleDetailView.as_view(), name='module-detail'),
    path('modules/<int:id>/launch/', views.ModuleLaunchView.as_view(), name='module-launch'),

    # USER DASHBOARD
    path('user/dashboard/', views.UserDashboardView.as_view(), name='user-dashboard'),
    path('user/certifications/', views.UserCertificationsView.as_view(), name='user-certifications'),

    # ADMIN DASHBOARD
    path('admin/users/', views.AdminUsersListView.as_view(), name='admin-users'),
    path('admin/endusers/', views.AdminEndUsersListView.as_view(), name='admin-endusers'),
    path('admin/expiring-soon/', views.AdminExpiringSoonView.as_view(), name='admin-expiring-soon'),
    #path('admin/modules/', views.AdminModulesControlView.as_view(), name='admin-modules'),

]

