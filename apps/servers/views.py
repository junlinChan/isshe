from django.core.cache import cache
from django.forms import model_to_dict
from rest_framework import mixins, viewsets, permissions, response, status
from rest_framework.response import Response

from apps.servers.remote import Remote
from .models import Server
from .serializers import ServerSerializer, AutoReportSerializer, AddServerSerializer
from .filter import ServerFilter

class ServerViewset(viewsets.ModelViewSet):
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
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    filter_class = ServerFilter
    filter_fields = ('hostname', 'idc', 'cabinet')
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = super(ServerViewset, self).get_queryset()
        queryset = queryset.order_by("id")
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        ip = instance.ip
        list = cache.get('iplist')
        num = list.index(ip)
        list.pop(num)
        cache.set('iplist', list, timeout=None)
        cache.delete_pattern(ip)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddServerViewset(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     viewsets.GenericViewSet):
    """
    create:
    创建主机

    update:
    修改主机
    """
    queryset = Server.objects.all()
    serializer_class = AddServerSerializer
    filter_class = ServerFilter
    filter_fields = ('ip')

    def create(self, request, *args, **kwargs):
        ret = {"status": 0}
        ip = request.data["ip"]
        username = request.data["username"]
        password = request.data["password"]
        if Server.objects.filter(ip__exact=ip).count() != 0:
            ret["status"] = 1
            ret["errmsg"] = "主机已存在"
            return response.Response(ret, status=status.HTTP_200_OK)
        try:
            r = Remote(host=ip, username=username, password=password)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            id = Server.objects.filter(ip=ip).values('id')[0]['id']
            list = cache.get('iplist')
            if list:
                list.append(ip)
                info = []
                info.append(id)
                info.append(username)
                info.append(password)
                cache.set(ip, info, timeout=None)
                cache.set('iplist', list, timeout=None)
            else:
                iplist = []
                iplist.append(ip)
                cache.set('iplist', iplist, timeout=None)
                info = []
                info.append(id)
                info.append(username)
                info.append(password)
                cache.set(ip, info, timeout = None)
            return response.Response(ret, status=status.HTTP_201_CREATED)
        except Exception as e:
            ret["status"] = 1
            ret["errmsg"] = "添加失败"
            return response.Response(ret, status=status.HTTP_200_OK)

class ServerCountViewset(viewsets.ViewSet,mixins.ListModelMixin):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Server.objects.all()

    def list(self, request, *args, **kwargs):
        data = self.get_server_nums()
        return response.Response(data)

    def get_server_nums(self):
        ret = {
            "count": self.queryset.count(),
            "vm_host_num": self.queryset.filter(server_type__exact='虚拟机').count(),
            "phy_host_num": self.queryset.filter(server_type__exact='物理机').count(),
            "cloud_host_num": self.queryset.filter(server_type__exact='云服务器').count(),
            "online_host_num": self.queryset.filter(status__exact='在线').count(),
            "abnormal_host_num": self.queryset.filter(status__exact='异常').count(),
            "line_host_num": self.queryset.filter(status__exact='离线').count()
        }
        return ret

# class ServerCollectViewset(mixins.CreateModelMixin,
#                           viewsets.GenericViewSet):
#     """
#     采集信息
#     """
#     queryset = Server.objects.all()
#     serializer_class = AutoReportSerializer
#     permission_classes = (permissions.AllowAny,)
#
#     def create(self, request, *args, **kwargs):
#         ip = request.data.get("ip", 0)
#         username = request.data.get("username", None)
#         password = request.data.get("password", None)
#         try:
#             r = Remote(host=ip, username=username, passowrd=password)
#
#         serializer = self.get_serializer(data=request.data)
#
#         # serializer.is_valid(raise_exception=True)
#         # self.perform_create(serializer)
#         # headers = self.get_success_headers(serializer.data)
#         # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
