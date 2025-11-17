from django.contrib import admin

from .models import PlantType, DiseaseLevel, DiseaseType, ImageData


class DiseaseTypeInline(admin.TabularInline):
    model = DiseaseType
    extra = 0


@admin.register(PlantType)
class PlantTypeAdmin(admin.ModelAdmin):
    inlines = [DiseaseTypeInline]
    list_display = ['title', 'is_active']
    readonly_fields = ['created_time', 'updated_time']
    search_fields = ['title',]
    list_filter = ['is_active',]


class DiseaseLevelInline(admin.TabularInline):
    model = DiseaseLevel
    extra = 0


@admin.register(DiseaseType)
class DiseaseTypeAdmin(admin.ModelAdmin):
    inlines = [DiseaseLevelInline]
    list_display = ['title', 'plant', 'is_active']
    readonly_fields = ['created_time', 'updated_time']
    search_fields = ['title', 'plant__title']
    list_filter = ['is_active', 'plant']

    # @display
    # def tomato(self, obj):
    #     return obj.tomato.title


@admin.register(DiseaseLevel)
class DiseaseLevelAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'is_active']
    readonly_fields = ['created_time', 'updated_time']
    search_fields = ['title', 'type__plant__title', 'type__title']
    search_help_text = 'Kasallik darajasi, pomidor turi, kasallik nomlari orqali izlang'
    list_filter = ['type', 'is_active']


@admin.register(ImageData)
class ImageDataAdmin(admin.ModelAdmin):
    list_display = ['filename', 'level', 'detail_view']
    list_display_links = ['detail_view']
    list_filter = ['level']
    readonly_fields = ['created_time', 'updated_time']

    @admin.display(description='Fayl Nomi')
    def filename(self, obj):
        return obj.source.name

    @admin.display(description='Batafsil')
    def detail_view(self, obj):
        return '>>>'
