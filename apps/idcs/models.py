from django.db import models

# Create your models here.
class Idcs(models.Model):
    letter = models.CharField("idc字母简称", max_length=15, unique=True, help_text="字母简称")
    name = models.CharField("idc名称", max_length=30, help_text="idc名称")
    address = models.CharField("idc具体地址", max_length=255, null=True, help_text="idc具体地址")
    tel = models.CharField("负责人电话", max_length=15, null=True, blank=True, help_text="负责人电话")
    mail = models.EmailField("负责人邮箱", max_length=255, null=True, blank=True, help_text="负责人邮箱")
    remark = models.CharField("备注说明", max_length=255, null=True, blank=True, help_text="备注说明")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'resources_idc'
        ordering = ["id"]