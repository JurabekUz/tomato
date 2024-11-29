from django.core.management.base import BaseCommand
from model.models import DataClass, DataModel
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = 'Insert data into DataClass model'

    def handle(self, *args, **kwargs):
        data_entries = [
            'Tomato___Bacterial_spot',
            'Tomato___Early_blight',
            'Tomato___Late_blight',
            'Tomato___Leaf_Mold',
            'Tomato___Septoria_leaf_spot',
            'Tomato___Spider_mites Two-spotted_spider_mite',
            'Tomato___Target_Spot',
            'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
            'Tomato___Tomato_mosaic_virus',
            'Tomato___healthy'
        ]
        # Assuming you have a DataModel instance to relate to
        data_model_instance = DataModel.objects.first()  # Get the first DataModel instance or create one

        for entry in data_entries:
            title = entry.replace('___', ' ').replace('_', ' ')
            label = entry

            # Create and save the DataClass instance
            try:
                data_class, created = DataClass.objects.get_or_create(
                    data_model=data_model_instance,
                    title=title,
                    label=label,
                    defaults={'description': _('Description for {}').format(title)}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created DataClass: {data_class}'))
                else:
                    self.stdout.write(self.style.WARNING(f'DataClass already exists: {data_class}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating DataClass for {entry}: {e}'))