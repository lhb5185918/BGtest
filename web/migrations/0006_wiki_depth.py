# Generated by Django 5.0.5 on 2024-06-12 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_alter_wiki_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='wiki',
            name='depth',
            field=models.IntegerField(default=1, verbose_name='深度'),
        ),
    ]
