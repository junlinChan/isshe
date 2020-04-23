"""isshe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

router = DefaultRouter()

from users.router import user_router
from groups.router import group_router
from menu.router import menu_router
from idcs.router import idc_router
from cabinet.router import cabinet_router
from servers.router import servers_router
from permissions.router import permission_router
from hardware.router import hadware_router
#from zabbix.router import zabbix_router

router.registry.extend(user_router.registry)
router.registry.extend(group_router.registry)
router.registry.extend(menu_router.registry)
router.registry.extend(idc_router.registry)
router.registry.extend(cabinet_router.registry)
router.registry.extend(servers_router.registry)
router.registry.extend(permission_router.registry)
router.registry.extend(hadware_router.registry)
#router.registry.extend(zabbix_router.registry)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^docs/', include_docs_urls("开源运维平台"))
]
