# Generated by Django 4.2 on 2024-10-28 04:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_rename_text_question_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='text',
            new_name='name',
        ),
    ]