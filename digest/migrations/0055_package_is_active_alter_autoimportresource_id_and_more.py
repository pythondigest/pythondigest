# Generated by Django 4.1.6 on 2023-03-05 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("digest", "0054_autoimportresource_is_active_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="package",
            name="is_active",
            field=models.BooleanField(default=True, verbose_name="Is active"),
        ),
        migrations.AlterField(
            model_name="autoimportresource",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="autoimportresource",
            name="language",
            field=models.CharField(
                choices=[("ru", "Russian"), ("en", "English")],
                default="en",
                max_length=255,
                verbose_name="Language of content",
            ),
        ),
        migrations.AlterField(
            model_name="issue",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="item",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="itemclscheck",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="keyword",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="keywordgfk",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="package",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="parsingrules",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="resource",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="section",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
    ]