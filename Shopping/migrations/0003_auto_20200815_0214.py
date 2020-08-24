# Generated by Django 3.1 on 2020-08-15 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Shopping', '0002_product_dod'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brand',
            name='catid',
        ),
        migrations.AddField(
            model_name='brand',
            name='catid',
            field=models.ManyToManyField(to='Shopping.Category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Brand'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shopping.product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='review',
            name='pid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shopping.product', verbose_name='Product'),
        ),
    ]
