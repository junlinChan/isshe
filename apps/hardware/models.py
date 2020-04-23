from django.db import models

# Create your models here.
class Hardware(models.Model):
    name = models.CharField("名称", null=True, max_length=36, help_text="名称")
    manufacturer = models.CharField("厂商", max_length=255, help_text="厂商")
    model_name = models.CharField("型号", null=True, max_length=36, help_text="名称")
    work_voltage = models.CharField("工作电压", null=True, max_length=12, help_text="工作电压")
    re_inputvoltage = models.CharField("推荐输入电压", null=True, max_length=12, help_text="推荐输入电压")
    max_inputvoltage = models.CharField("极限输入电压", null=True, max_length=12, help_text="极限输入电压")
    flash = models.CharField("闪存", null=True, max_length=64, help_text="闪存")
    sram = models.CharField("SRAM", null=True, max_length=64, help_text="SRAM")
    nums = models.IntegerField("数量", null=True, help_text="数量")

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'resources_hardware'
