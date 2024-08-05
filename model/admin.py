from django.contrib import admin

from .models import DataModel, DataClass


@admin.register(DataModel)
class DataModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_time')
    list_filter = ('is_active',)
    search_fields = ('title',)


@admin.register(DataClass)
class DataClassAdmin(admin.ModelAdmin):
    list_display = ('data_model', 'title', 'is_active', 'created_time')
    search_fields = ('title',)
    list_filter = ['is_active', 'data_model']

