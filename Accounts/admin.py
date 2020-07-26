from django.contrib import admin
from .models import Accounts
# Register your models here.


class AccountsAdmin(admin.ModelAdmin):
    list_display = ['Email', 'UserName', 'date_joined', 'Updated_Time']
    readonly_fields = ['Updated_Time']
    search_fields = ['Email', 'UserName']


admin.site.register(Accounts, AccountsAdmin)
