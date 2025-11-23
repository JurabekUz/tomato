from django import forms
from django.contrib import admin
import os
import zipfile
from django.shortcuts import render, redirect
from django.urls import path
from django.core.files.base import ContentFile

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


# @admin.register(ImageData)
# class ImageDataAdmin(admin.ModelAdmin):
#     list_display = ['filename', 'level', 'detail_view']
#     list_display_links = ['detail_view']
#     list_filter = ['level']
#     readonly_fields = ['created_time', 'updated_time']
#
#     @admin.display(description='Fayl Nomi')
#     def filename(self, obj):
#         return obj.source.name
#
#     @admin.display(description='Batafsil')
#     def detail_view(self, obj):
#         return '>>>'


class ZipUploadForm(forms.Form):
    level = forms.ModelChoiceField(
        queryset=DiseaseLevel.objects.all(),
        required=True,
        label="Kasallik darajasi"
    )
    zip_file = forms.FileField(
        required=True,
        label="ZIP fayl"
    )


@admin.register(ImageData)
class ImageDataAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'imagedata/',
                self.admin_site.admin_view(self.upload_zip_view),
                name='imagedata_upload_zip'
            ),
        ]
        return custom_urls + urls

    def upload_zip_view(self, request):
        if request.method == 'POST':
            form = ZipUploadForm(request.POST, request.FILES)
            level_id = request.POST.get('level')

            if form.is_valid() and level_id:
                level = DiseaseLevel.objects.get(id=level_id)
                zip_file = request.FILES['zip_file']

                extracted_images = []
                with zipfile.ZipFile(zip_file) as z:
                    for name in z.namelist():
                        if name.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                            safe_name = os.path.basename(name)  # prevents path traversal
                            image_data = z.read(name)

                            file_obj = ContentFile(image_data, name=safe_name)

                            extracted_images.append(
                                ImageData(level=level, source=file_obj)
                            )

                ImageData.objects.bulk_create(extracted_images)
                return redirect('..')

        else:
            form = ZipUploadForm()

        return render(request, 'admin/upload_zip.html', {
            'form': form,
            'levels': DiseaseLevel.objects.all(),
            'title': 'ZIP orqali rasm yuklash',
        })

