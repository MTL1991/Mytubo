from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from ppal.models import *

class TuberInline(admin.StackedInline):
    model = Tuber
    can_delete = False

class UserAdmin(UserAdmin):
    list_display = ('username','email','tuber', 'id')
    inlines = (TuberInline, )

class TuboAdmin(admin.ModelAdmin):
    list_display = ('id','title','tuber')
    ordering = ('id',)
    search_fields = ('title','tuber','description')



admin.site.unregister(User)
admin.site.register(User, UserAdmin)
