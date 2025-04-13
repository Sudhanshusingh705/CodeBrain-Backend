# admin.py
from django.contrib import admin
from .models import Student, Trainer, Counsellor



class StudentAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')

class TrainerAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'is_active')

class CounsellorAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'is_active')

admin.site.register(Student, StudentAdmin)
admin.site.register(Trainer, TrainerAdmin)
admin.site.register(Counsellor, CounsellorAdmin)