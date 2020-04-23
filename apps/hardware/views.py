from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, response, status
from apps.hardware.filter import HardwareFilter
from apps.hardware.models import Hardware
from apps.hardware.serializers import HardwareSerializer


class HardwareViewset(viewsets.ModelViewSet):
    """
    list:
    返回idc列表
    create:
    创建idc记录
    retrieve:
    返回idc记录
    destroy
    删除idc记录
    update:
    更新idc记录
    """
    queryset = Hardware.objects.all()
    serializer_class = HardwareSerializer
    filter_class = HardwareFilter
    filter_fields = ("name", "manufacturer")

    def create(self, request, *args, **kwargs):
        ret = {"status":0}
        name = request.data["name"]
        if Hardware.objects.filter(name__exact=name).count() != 0:
            ret["status"] = 1
            ret["errmsg"] = "硬件已存在"
            return response.Response(ret, status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response.Response(ret, status=status.HTTP_201_CREATED)
