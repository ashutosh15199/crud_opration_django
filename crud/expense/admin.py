from django.contrib import admin

from .models import Transection
from .userModel import CustomUser

from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    fieldsets=UserAdmin.fieldsets+(
        (None,{'fields':('role',)}),
    )

admin.site.register(CustomUser,CustomUserAdmin)    
admin.site.register(Transection)
