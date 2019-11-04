import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("users", "0003_customuser_populate_uuid")]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, unique=True, verbose_name="indentifier"
            ),
        )
    ]
