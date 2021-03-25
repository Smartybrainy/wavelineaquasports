from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

from .forms import CustomCreationForm, CustomChangeForm


class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomCreationForm
    form = CustomChangeForm
    model = CustomUser
    list_display = ['email',
                    'phone_number',
                    'country_code',
                    'full_name',
                    'is_staff',
                    'is_active',
                    'date_joined',
                    'phone_number_verified',
                    'two_factor_auth'
                    ]
    list_display_links = ['email',
                    'phone_number',
                    'country_code',
                    ]
    fieldsets = (
        (None, {'fields': ('password', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('OTP', {'fields': (
                    'full_name',
                    'phone_number_verified',
                    'phone_number',
                    'country_code',
                    'two_factor_auth'
                    )
                 })
    )
    add_fieldsets = (
        ('Add New User', {
            'classes': ('wide',),
            'fields': (
                'phone_number',
                'email',
                'password1',
                'password2',
                'is_staff',
                'is_active'
                )
        }
        ),
        ('OTP', {'fields': (
                    'full_name',
                    'phone_number_verified',
                    'country_code',
                    'two_factor_auth'
                    )
                 })
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)