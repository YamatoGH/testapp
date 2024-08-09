# Generated by Django 5.0.6 on 2024-08-01 06:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("testapp", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="test",
            old_name="title",
            new_name="name",
        ),
        migrations.RemoveField(
            model_name="test",
            name="description",
        ),
        migrations.RemoveField(
            model_name="test",
            name="file",
        ),
        migrations.RemoveField(
            model_name="test",
            name="group",
        ),
        migrations.RemoveField(
            model_name="test",
            name="words",
        ),
        migrations.AddField(
            model_name="word",
            name="test",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="words",
                to="testapp.test",
            ),
            preserve_default=False,
        ),
    ]
