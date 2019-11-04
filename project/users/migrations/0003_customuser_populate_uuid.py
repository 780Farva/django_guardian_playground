import uuid

from django.db import migrations


def gen_uuid(apps, schema_editor):
    CustomUser = apps.get_model("users", "CustomUser")
    for row in CustomUser.objects.all():
        row.uuid = uuid.uuid4()
        row.save(update_fields=["uuid"])


class Migration(migrations.Migration):

    dependencies = [("users", "0002_customuser_uuid")]

    operations = [
        # omit reverse_code=... if you don't want the migration to be reversible.
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop)
    ]
