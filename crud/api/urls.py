from django.urls import path
from expense.views import expense_home, get_transection, TransectionAPI, expense_details,RegisterView, LoginView, ProfileView, AdminDashboardView, ManagerDashboardView , ForgotPasswordView, ResetPasswordView,logout_view


urlpatterns = [
    path('', expense_home, name='expense_home'), 
    path('get_transections/', get_transection, name='get_transections'),
    path('transections/', get_transection, name='get_transections'),  
    path('transections/create/', TransectionAPI.as_view(), name='create_transection'),  
    path('transections/get/', TransectionAPI.as_view(), name='get_transection'),  
    path('transections/update/', TransectionAPI.as_view(), name='update_transection'),  
    path('transections/partial-update/', TransectionAPI.as_view(), name='partial_update_transection'),  
    path('transections/delete/', TransectionAPI.as_view(), name='delete_transection'),  
    path('details/<int:id>/', expense_details, name='transection_detail'), 
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('manager-dashboard/', ManagerDashboardView.as_view(), name='manager_dashboard'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/<int:user_id>/<str:token>/', ResetPasswordView.as_view(), name='reset-password'), 
    path('logout/', logout_view, name='logout'),
]
