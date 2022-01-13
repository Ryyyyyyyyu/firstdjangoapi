from rest_framework import routers

from reports import views


router = routers.DefaultRouter()
router.register('', views.ReportViewSet)

urlpatterns = [
]
urlpatterns += router.urls
