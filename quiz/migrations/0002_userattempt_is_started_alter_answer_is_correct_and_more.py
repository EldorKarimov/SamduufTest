# Generated by Django 5.1.3 on 2024-12-19 07:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userattempt',
            name='is_started',
            field=models.BooleanField(default=False, verbose_name='is started'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name='is correct'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='quiz.question', verbose_name='question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='is available'),
        ),
        migrations.AlterField(
            model_name='question',
            name='is_multiple_choice',
            field=models.BooleanField(default=False, verbose_name='is multiple choice'),
        ),
        migrations.AlterField(
            model_name='question',
            name='mark',
            field=models.IntegerField(default=1, verbose_name='mark'),
        ),
        migrations.AlterField(
            model_name='question',
            name='name',
            field=models.TextField(verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='question',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.test', verbose_name='test'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='attempt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_answers', to='quiz.userattempt', verbose_name='attempt'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='is_correct',
            field=models.BooleanField(verbose_name='is correct'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.question', verbose_name='question'),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='selected_answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.answer', verbose_name='selected answer'),
        ),
        migrations.AlterField(
            model_name='userattempt',
            name='date_taken',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date taken'),
        ),
        migrations.AlterField(
            model_name='userattempt',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='is completed'),
        ),
        migrations.AlterField(
            model_name='userattempt',
            name='score',
            field=models.IntegerField(verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='userattempt',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.test', verbose_name='test'),
        ),
        migrations.AlterField(
            model_name='userattempt',
            name='time_taken',
            field=models.DurationField(verbose_name='time taken'),
        ),
        migrations.AlterField(
            model_name='userattempt',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]