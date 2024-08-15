from django.contrib import admin
from .models import Policy, Category

@admin.register(Policy)
class PolicyAdmin(admin.ModelAdmin):
    list_display = ('id', 'policy_name', 'category', 'status') 
    list_filter = ('status', 'category') 

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') 