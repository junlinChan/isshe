from django.db import models
from idcs.models import Idcs
from cabinet.models import Cabinet

# Create your models here.
class Server(models.Model):
    manufacturer = models.CharField("制造商", null=True, max_length=255, help_text="制造商")
    os = models.CharField("操作系统", max_length=100, blank=True, default=None, help_text="操作系统")
    hostname = models.CharField("主机名", max_length=50, default=None, blank=True, db_index=True, help_text="主机名")
    ip = models.CharField("IP", max_length=32, default=None, db_index=True, help_text="IP")
    cpu = models.CharField("CPU型号", max_length=250, blank=True, default=None, help_text="CPU信息")
    #cpu_count = models.CharField("物理CPU个数", max_length=5, blank=True, default=None, help_text="物理CPU个数")
    #cpu_core_count = models.CharField("CPU核数", max_length=5, blank=True, default=None, help_text="CPU核数")
    # disk = models.CharField("硬盘信息", max_length=300, blank=True, null=True, help_text="硬盘信息")
    cpu_use = models.CharField("CPU使用率", max_length=12, null=True, help_text="CPU使用率")
    mem_use = models.CharField("内存使用率", max_length=12, null=True, help_text="内存使用率")
    username = models.CharField("主机用户名", max_length=32, default=None, help_text="主机用户名")
    password = models.CharField("主机密码", max_length=32, default=None, help_text="主机密码")
    mem = models.CharField("内存信息", max_length=100, blank=True, default=None, help_text="内存信息")
    status = models.CharField("状态", max_length=32, null=True, db_index=True, help_text="状态")
    server_type = models.CharField("主机类型", max_length=32, null=True, help_text="主机类型")
    uuid = models.CharField("UUID", max_length=100, blank=True, db_index=True, null=True, unique=True, help_text="UUID")
    network_name = models.CharField("网卡设备名", null=True, max_length=255, help_text="网卡设备名")
    network_mac = models.CharField("网卡mac地址", null=True, max_length=32, help_text="网卡mac地址")
    disk_name = models.CharField("硬盘名", null=True, max_length=32, help_text="硬盘名")
    disk_size = models.CharField("硬盘大小", null=True, max_length=32, help_text="硬盘大小")
    sn = models.CharField("SN", max_length=40, db_index=True, blank=True, null=True, help_text="SN")
    model_name = models.CharField("型号", max_length=255, blank=True, default=None, help_text="型号")
    last_check = models.DateTimeField("上次检测时间", auto_now=True, help_text="上次检测时间")
    use = models.CharField("用途", max_length=35, default=None, help_text="用途")
    idc = models.ForeignKey(Idcs, verbose_name="所在机房", null=True, help_text="所在机房", on_delete=models.CASCADE)
    cabinet = models.ForeignKey(Cabinet, verbose_name="所在机柜", null=True, help_text="所在机柜", on_delete=models.CASCADE)

    def __str__(self):
        return "{}[{}]".format(self.hostname, self.ip)

    class Meta:
        db_table = 'resources_server'