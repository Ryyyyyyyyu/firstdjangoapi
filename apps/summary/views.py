from django.db.models import Sum
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from configures.models import ConfiguresModel
from interfaces.models import InterfacesModel
from projects.models import ProjectsModel
from testcases.models import TestcasesModel
from testsuites.models import TestsuitsModel
from envs.models import EnvsModel
from debugtalks.models import DebugtalksModel
from reports.models import ReportsModel


class SummaryAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        user_info = {
            'username': user.username,
            'role': '管理员' if user.is_superuser else '普通用户',
            'date_joined': user.date_joined.strftime('%Y-%m-%d %H:%M:%S') if user.date_joined else '',
            'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S') if user.last_login else '',
        }

        projects_count = ProjectsModel.objects.count()
        interfaces_count = InterfacesModel.objects.count()
        testcases_count = TestcasesModel.objects.count()
        testsuits_count = TestsuitsModel.objects.count()
        configures_count = ConfiguresModel.objects.count()
        envs_count = EnvsModel.objects.count()
        debug_talks_count = DebugtalksModel.objects.count()
        reports_count = ReportsModel.objects.count()

        run_testcases_success_count = ReportsModel.objects.aggregate(Sum('success')).get('success__sum') or 0
        run_testcases_total_count = ReportsModel.objects.aggregate(Sum('count')).get('count__sum') or 0

        if run_testcases_total_count:
            success_rate = int((run_testcases_success_count / run_testcases_total_count) * 100)
            fail_rate = 100 - success_rate
        else:
            success_rate = 0
            fail_rate = 0

        statistics = {
            'projects_count': projects_count,
            'interfaces_count': interfaces_count,
            'testcases_count': testcases_count,
            'testsuits_count': testsuits_count,
            'configures_count': configures_count,
            'envs_count': envs_count,
            'debug_talks_count': debug_talks_count,
            'reports_count': reports_count,
            'success_rate': success_rate,
            'fail_rate': fail_rate,
        }

        return Response({'user_info': user_info, 'statistics': statistics})
