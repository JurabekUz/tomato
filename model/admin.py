from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import DataModel, DataClass


@admin.register(DataModel)
class DataModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'code',  'disease_type', 'is_active', 'created_time')
    list_filter = ('is_active', 'disease_type')
    search_fields = ('title',)

    readonly_fields = ('disease_type_info',)

    def disease_type_info(self, obj):
        levels = obj.disease_type.disease_levels.all()
        items = "".join(f"<li>{lvl.title}</li>" for lvl in levels)
        return mark_safe(f"<b>{obj.disease_type.title}</b><ul>{items}</ul>")

    disease_type_info.short_description = "Disease Type & Levels"


# @admin.register(DataClass)
# class DataClassAdmin(admin.ModelAdmin):
#     list_display = ('data_model', 'title', 'index', 'is_active', 'created_time')
#     search_fields = ('title',)
#     list_filter = ['is_active', 'data_model']

