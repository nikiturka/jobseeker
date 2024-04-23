# Generated by Django 5.0.4 on 2024-04-23 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('employees', models.IntegerField()),
                ('contact_info', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=64)),
                ('profile_picture', models.IntegerField()),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('contact_info', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('required_experience', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('responsibilities', models.TextField()),
                ('requirements', models.TextField()),
                ('benefits', models.TextField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.company')),
            ],
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'Ожидает рассмотрения'), ('accepted', 'Принят'), ('rejected', 'Отклонён')], default='pending', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.user')),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.vacancy')),
            ],
        ),
    ]
