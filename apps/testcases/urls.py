from rest_framework import routers

from testcases import views


router = routers.DefaultRouter()
router.register('', views.TestcaseViewSet)

urlpatterns = [
]
urlpatterns += router.urls
