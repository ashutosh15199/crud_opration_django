from django.urls import path
from expense import views
from expense.views import expense_home, get_transection, TransectionAPI, expense_details

urlpatterns = [
    path('', expense_home, name='expense_home'),  # Homepage
    path('get_transections/', get_transection, name='get_transections'),
    path('transections/', get_transection, name='get_transections'),  # Get all transactions
    path('transections/create/', TransectionAPI.as_view(), name='create_transection'),  # Create
    path('transections/get/', TransectionAPI.as_view(), name='get_transection'),  # Get one
    path('transections/update/', TransectionAPI.as_view(), name='update_transection'),  # Update
    path('transections/partial-update/', TransectionAPI.as_view(), name='partial_update_transection'),  # Patch
    path('transections/delete/', TransectionAPI.as_view(), name='delete_transection'),  # Delete
    path('details/<int:id>/', expense_details, name='transection_detail'),  # Detail page for a single transaction
]
