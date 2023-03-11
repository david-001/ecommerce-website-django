from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', views.register, name='register'),
    path('register-action', views.register_action, name='register-action'),
    path('email-verification/<str:uidb64>/<str:token>/',
         views.email_verification, name='email-verification'),
    path('email-verification-sent', views.email_verification_sent,
         name='email-verification-sent'),
    path('email-verification-success', views.email_verification_success,
         name='email-verification-success'),
    path('email-verification-failed', views.email_verification_failed,
         name='email-verification-failed'),

    # login logout
    path('my-login', views.my_login, name='my-login'),
    path('my-login-action', views.my_login_action, name='my-login-action'),
    path('user-logout', views.user_logout, name='user-logout'),

    # dashboard
    path('dashboard', views.dashboard, name='dashboard'),
    path('profile-management', views.profile_management, name='profile-management'),
    path('profile-management-action', views.profile_management_action,
         name='profile-management-action'),
    path('delete-account', views.delete_account, name='delete-account'),

    # password management
    # Submit our email form
    path('reset_password', auth_views.PasswordResetView.as_view(template_name="account/password/password-reset.html"),
         name='reset_password'),

    # Success meesage stating password reset email was sent
    path('reset_password_sent', auth_views.PasswordResetDoneView.as_view(template_name="account/password/password-reset-sent.html"),
         name='password_reset_done'),

    # Password reset link
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="account/password/password-reset-form.html"), name='password_reset_confirm'),

    # Success message stating that password was reset
    path('reset_password_complete', auth_views.PasswordResetCompleteView.as_view(
        template_name="account/password/password-reset-complete.html"), name='password_reset_complete'),

    # Manage shipping url
    path('manage-shipping', views.manage_shipping, name='manage-shipping'),
    path('manage-shipping-action', views.manage_shipping_action,
         name='manage-shipping-action'),

    # Track orders url
    path('track-orders', views.track_orders, name='track-orders'),

    # Admin login
    path('admin-login', views.admin_login, name='admin-login'),
    path('admin-login-action', views.admin_login_action, name='admin-login-action'),

    # Admin logout
    path('admin-logout', views.admin_logout, name='admin-logout'),

    # Admin dashboadrd
    path('admin-dashboard', views.admin_dashboard, name='admin-dashboard'),

    # Admin customer profile
    path('admin-customer-profile/<str:uid>',
         views.admin_customer_profile, name='admin-customer-profile'),

    # Admin retailer profile
    path('admin-retailer-profile/<str:uid>',
         views.admin_retailer_profile, name='admin-retailer-profile'),

    # Admin download orders
    path('admin-download-orders',
         views.admin_download_orders, name='admin-download-orders'),

    # Admin add category
    path('admin-add-category',
         views.admin_add_category, name='admin-add-category'),

    # Admin delete category
    path('admin-delete-category/<str:pk>',
         views.admin_delete_category, name='admin-delete-category'),

    # Admin approve retailer
    path('admin-approve-retailer/<str:pk>',
         views.admin_approve_retailer, name='admin-approve-retailer'),


    # Retailer register
    path('retailer-register',
         views.retailer_register, name='retailer-register'),


    # Retailer approval
    path('email-admin-approval/<str:uidb64>/<str:token>/',
         views.email_admin_approval, name='email-admin-approval'),

    # Retailer email sent
    path('email-retailer-sent',
         views.email_retailer_sent, name='email-retailer-sent'),

    # Retailer email success
    path('email-retailer-success',
         views.email_retailer_success, name='email-retailer-success'),

    # Retailer email failed
    path('email-retailer-failed',
         views.email_retailer_failed, name='email-retailer-failed'),

    # Retailer login
    path('retailer-login',
         views.retailer_login, name='retailer-login'),

    # Retailer logout
    path('retailer-logout',
         views.retailer_logout, name='retailer-logout'),

    # Retailer dashboard
    path('retailer-dashboard',
         views.retailer_dashboard, name='retailer-dashboard'),


    # Retailer product
    path('retailer-product/<str:pid>/',
         views.retailer_product, name='retailer-product'),


    # Retailer delete product
    path('retailer-delete-product/<str:pk>',
         views.retailer_delete_product, name='retailer-delete-product'),


    # Retailer download product
    path('retailer-download-products/<str:uid>/',
         views.retailer_download_products, name='retailer-download-products'),

    # Retailer profile
    path('retailer-profile/<str:uid>/',
         views.retailer_profile, name='retailer-profile'),



    # Retailer update delivery
    path('retailer-update-delivery/<str:oid>/',
         views.retailer_update_delivery, name='retailer-update-delivery'),




]
