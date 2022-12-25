from django.contrib import admin
from .models import User, Show

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username","first_name", "last_name")

class ShowAdmin(admin.ModelAdmin):
    list_display = ("id","name","channel","premiered","startyear","endyear","mostrecentairdate","status")

admin.site.register(User, UserAdmin)
admin.site.register(Show, ShowAdmin)