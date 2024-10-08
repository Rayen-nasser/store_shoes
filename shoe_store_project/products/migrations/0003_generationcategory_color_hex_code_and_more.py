# Generated by Django 4.2.13 on 2024-06-22 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_created_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='GenerationCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='color',
            name='hex_code',
            field=models.CharField(default='000000', max_length=6),
        ),
        migrations.AddField(
            model_name='product',
            name='generation_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.generationcategory'),
        ),
    ]
