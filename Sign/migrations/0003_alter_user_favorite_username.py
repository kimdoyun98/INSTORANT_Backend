# Generated by Django 3.2.13 on 2022-07-06 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Sign', '0002_user_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_favorite',
            name='username',
            field=models.ForeignKey(db_column='username', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
