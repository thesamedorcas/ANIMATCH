# Generated by Django 5.1.7 on 2025-03-27 02:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animals', '0008_alter_adoptionrequest_id_alter_animal_id_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Favourite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('animal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourited_by', to='animals.animal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'animal')},
            },
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
