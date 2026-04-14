from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AppUser",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("username", models.CharField(max_length=20, unique=True)),
                ("password", models.CharField(max_length=128)),
                ("name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("role", models.CharField(choices=[("ADMIN", "ADMIN"), ("USER", "USER")], default="USER", max_length=20)),
                ("status", models.IntegerField(default=1)),
                ("token", models.CharField(blank=True, max_length=64, null=True)),
                ("avatar", models.CharField(blank=True, max_length=255, null=True)),
                ("device_id", models.CharField(blank=True, max_length=64, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "app_user",
                "ordering": ["-id"],
            },
        ),
    ]
