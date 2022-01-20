from rest_framework import routers

from testsuites import views


router = routers.DefaultRouter()
router.register('', views.TestcaseViewSet)

urlpatterns = [
]
urlpatterns += router.urls
