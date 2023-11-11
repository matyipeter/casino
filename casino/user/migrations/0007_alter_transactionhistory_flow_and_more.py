# Generated by Django 4.2.7 on 2023-11-11 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0006_winninghistory_transactionhistory"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transactionhistory",
            name="flow",
            field=models.FloatField(default=0.0, verbose_name="$"),
        ),
        migrations.AlterField(
            model_name="winninghistory",
            name="win",
            field=models.FloatField(default=0.0, verbose_name="$"),
        ),
    ]
