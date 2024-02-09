from django.contrib import admin

from main_app.models import Employee, Contacts

# Register your models here.
admin.site.site_header = "Spreading smiles System"
admin.site.index_title = "Spreading smiles"


class Employeeadmin(admin.ModelAdmin):
    list_display = ["name", "email", "dob", "disabled"]
    search_fields = ["name", "email"]
    list_filter = ["disabled"]


admin.site.register(Employee, Employeeadmin)
admin.site.register(Contacts)




