# Generated by Django 5.2 on 2025-05-06 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_peopletoeat_alter_feeding_options_alter_feeding_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='peopletoeat',
            options={'verbose_name': 'Person to Eat', 'verbose_name_plural': 'People to Eat'},
        ),
        migrations.AddField(
            model_name='dino',
            name='people',
            field=models.ManyToManyField(to='main_app.peopletoeat'),
        ),
    ]
