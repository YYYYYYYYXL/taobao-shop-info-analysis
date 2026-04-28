from django.db import models


class AppUser(models.Model):
    ROLE_CHOICES = (  #ROLE_CHOICES是一个元组，包含了两个选项：ADMIN和USER。这些选项用于定义用户的角色，可以在创建或更新用户时选择其中一个。
        ("ADMIN", "ADMIN"),
        ("USER", "USER"),
    )

    username = models.CharField(max_length=20, unique=True)  #username字段是一个CharField，最大长度为20个字符，并且必须唯一。它用于存储用户的用户名，可以包含字母、数字和特殊字符，max_length参数限制了用户名的长度，unique=True确保每个用户名在数据库中是唯一的，不能重复，CharField是Django模型中的一个字段类型，用于存储字符串数据。它接受一个max_length参数，指定了该字段可以存储的最大字符数。在这个例子中，username字段的最大长度被设置为20个字符，这意味着用户的用户名不能超过20个字符。
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=50)   #name字段是一个CharField，最大长度为50个字符。它用于存储用户的姓名，可以包含字母、数字和特殊字符。
    email = models.EmailField(unique=True)   #EmailField是Django模型中的一个字段类型，用于存储电子邮件地址。它继承自CharField，并且添加了一些额外的验证功能，以确保输入的值是一个有效的电子邮件地址。unique=True参数确保每个电子邮件地址在数据库中是唯一的，不能重复。
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="USER")   #role字段是一个CharField，最大长度为20个字符，并且有一个choices参数，指定了可选的角色。choices参数接受一个元组，其中每个元素都是一个包含两个值的元组，第一个值是实际存储在数据库中的值，第二个值是显示给用户的选项。在这个例子中，ROLE_CHOICES定义了两个选项：ADMIN和USER。默认值被设置为USER，这意味着如果在创建用户时没有指定角色，则默认将其设置为USER。
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
