# Generated by Django 3.0a1 on 2019-10-09 04:53

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, null=True, verbose_name="indentifier"
            ),
        )
    ]
