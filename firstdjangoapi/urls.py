"""firstdjangoapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Functewion views
    1. Add an import:  from my_app import vis
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.urls import path, include, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.documentation import include_docs_urls

# swager文档
schema_view = get_schema_view(
    openapi.Info(
        title="测试项目API",  # 必传
        default_version='v1.0',  # 必传
        description="测试工程接口文档",
        terms_of_service="https://www.xxxxx.com",
        contact=openapi.Contact(email="xxxxxx@163.com"),
        license=openapi.License(name="xx xxx"),
    ),
    public=True,
)

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('interfaces/', include('interfaces.urls')),
    path('envs/', include('envs.urls')),
    path('debugtalks/', include('debugtalks.urls')),
    path('configures/', include('configures.urls')),
    path('reports/', include('reports.urls')),
    path('testcases/', include('testcases.urls')),
    path('testsuites/', include('testsuites.urls')),
    path('users/', include('users.urls')),

    re_path(r'^static/(?P<path>.*)', serve, {'document_root': settings.STATIC_ROOT}, ),
    path('docs/', include_docs_urls(title="测试平台API文档")),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schemaredoc'),
    path('api/', include('rest_framework.urls')),
]
