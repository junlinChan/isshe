from django.db import models
from idcs.models import Idcs

# Create your models here.
class Cabinet(models.Model):
    name = models.CharField("机柜名称", max_length=50, help_text="机柜名称")
    idc = models.ForeignKey(Idcs, verbose_name="所在机房", help_text="所在机房", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'resources_cabinet'
        ordering = ["id"]