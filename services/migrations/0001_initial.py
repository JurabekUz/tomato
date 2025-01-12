# Generated by Django 5.0.6 on 2024-11-29 10:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('model', '0002_alter_dataclass_label_alter_dataclass_title'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Predict',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('percentage', models.PositiveIntegerField(default=0)),
                ('result', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='predicts', to='model.dataclass')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='predicts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PredictImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='predict_images/')),
                ('predict', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='services.predict')),
            ],
        ),
    ]
