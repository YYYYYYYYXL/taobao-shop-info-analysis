from django.db import models


class AppUser(models.Model):
    ROLE_CHOICES = (
        ("ADMIN", "ADMIN"),
        ("USER", "USER"),
    )

    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="USER")
    status = models.IntegerField(default=1)
    token = models.CharField(max_length=64, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    device_id = models.CharField(max_length=64, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "app_user"
        ordering = ["-id"]

    def __str__(self):
        return self.username
