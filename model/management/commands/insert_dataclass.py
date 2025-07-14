from django.core.management.base import BaseCommand, CommandError
from model.models import DataClass, DataModel
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = 'Insert data into DataClass model for a given DataModel code'

    def add_arguments(self, parser):
        parser.add_argument('code', type=str, help='DataModel code')

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
        code = kwargs['code']
        try:
            data_model_instance = DataModel.objects.get(code=code, is_active=True)
        except DataModel.DoesNotExist:
            raise CommandError(f'DataModel with code "{code}" does not exist or is not active.')

        for index, entry in enumerate(data_entries):
            title = entry.replace('___', ' ').replace('_', ' ')

            # Create and save the DataClass instance
            try:
                data_class, created = DataClass.objects.get_or_create(
                    data_model=data_model_instance,
                    title=title,
                    index=index,
                    defaults={'description': _('Description for {}').format(title)}
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Successfully created DataClass: {data_class}'))
                else:
                    self.stdout.write(self.style.WARNING(f'DataClass already exists: {data_class}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating DataClass for {entry}: {e}'))