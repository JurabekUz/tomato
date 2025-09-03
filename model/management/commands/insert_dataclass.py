from django.core.management.base import BaseCommand, CommandError
from model.models import DataClass, DataModel
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = 'Insert data into DataClass model for a given DataModel code'

    def add_arguments(self, parser):
        parser.add_argument('code', type=str, help='DataModel code')

    def handle(self, *args, **kwargs):
        data_entries = [
            'Healthy',
            'Phytophthora1',
            'Phytophthora2',
            'Phytophthora3',
            'Phytophthora4'
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