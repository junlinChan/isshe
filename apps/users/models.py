from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from menu.models import Menu

# Create your models here.
class User(AbstractUser):
    name = models.CharField("姓名", max_length=32, null=True, help_text="姓名")
    phone = models.CharField("电话", max_length=11, null=True, help_text="电话")

    class Meta:
        verbose_name = "用户"
        ordering = ["id"]
        db_table = 'auth_user'

    def __str__(self):
        return self.username

    def get_view_permissions(self):
        if self.is_superuser:
            return Menu.objects.all()
        return Menu.objects.filter(groups__in=self.groups.all())