from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, response, status
from cabinet.models import Cabinet
from idcs.models import Idcs
from .filter import IdcFilter
from .serializers import IdcSerializer
from .models import Idcs

class IdcViewset(viewsets.ModelViewSet):
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
    queryset = Idcs.objects.all()
    serializer_class = IdcSerializer
    filter_class = IdcFilter
    filter_fields = ("name",)
    
    def create(self, request, *args, **kwargs):
        ret = {"status":0}
        idcname = request.data["name"]
        letter = request.data["letter"]
        if Idcs.objects.filter(name__exact=idcname).count() != 0:
            ret["status"] = 1
            ret["errmsg"] = "IDC已存在"
            return response.Response(ret, status=status.HTTP_200_OK)
        elif Idcs.objects.filter(letter__exact=letter).count() != 0:
            ret["status"] = 1
            ret["errmsg"] = "字母简称已被占用"
            return response.Response(ret, status=status.HTTP_200_OK)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return response.Response(ret, status=status.HTTP_201_CREATED)

    #重写删除方法
    def destroy(self, request, *args, **kwargs):
        ret = {"status":0}
        instance = self.get_object()
        if Cabinet.objects.filter(idc_id__exact=instance.id).count() != 0:
            ret["status"] = 1
            ret["errmsg"] = "该IDC还有机柜记录，不能删除!"
            return response.Response(ret, status=status.HTTP_200_OK)

        self.perform_destroy(instance)
        return response.Response(ret, status=status.HTTP_200_OK)


