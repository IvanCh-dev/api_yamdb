# Generated by Django 2.2.16 on 2022-11-15 13:56

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Жанр')),
                ('slug', models.SlugField(unique=True, verbose_name='Адрес')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Жанр')),
                ('slug', models.SlugField(unique=True, verbose_name='Адрес')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название произведения')),
                ('description', models.TextField(blank=True, max_length=255, null=True, verbose_name='Описание')),
                ('year', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(2022, message='Нельзя добавлять произведения, которые еще не вышли')], verbose_name='Дата публикации')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='apiart.Category', verbose_name='Категория')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='TitleGenre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='genretitles', to='apiart.Genre')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genretitles', to='apiart.Title')),
            ],
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(through='apiart.TitleGenre', to='apiart.Genre', verbose_name='Жанр произведения'),
        ),
    ]
