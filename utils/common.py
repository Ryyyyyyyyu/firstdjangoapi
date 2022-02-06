import json
import logging
import os
from datetime import datetime

import yaml

from httprunner.task import HttpRunner
from rest_framework.response import Response

from firstdjangoapi import settings
from testcases.models import TestcasesModel
from debugtalks.models import DebugtalksModel
from envs.models import EnvsModel
from configures.models import ConfiguresModel
from reports.models import ReportsModel


logger = logging.getLogger('mytest')


def generate_testcase_file(instance: TestcasesModel, env: EnvsModel, testcase_dir_path):
    # 创建项目命名目录
    project_name = instance.interface.project.name
    testcase_dir_path = os.path.join(testcase_dir_path, project_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)
        debugTalk_obj = DebugtalksModel.objects.filter(project__name=project_name).first()
        with open(os.path.join(testcase_dir_path, 'debugtalk.py'), 'w', encoding='utf-8') as f:
            f.write(debugTalk_obj.debugtalk)

    interface_name = instance.interface.name
    testcase_dir_path = os.path.join(testcase_dir_path, interface_name)
    if not os.path.exists(testcase_dir_path):
        os.makedirs(testcase_dir_path)

    # 创建yaml用例文件
    testcase_list = []
    include_data = json.loads(instance.include, encoding='utf-8')
    config_id = include_data.get('config')
    base_url = env.base_url if env.base_url else ''

    if config_id is not None:
        config_obj = ConfiguresModel.objects.filter(id=config_id).first()
        config_dict = json.loads(config_obj.request, encoding='utf-8')
        config_dict['config']['request']['base_url'] = base_url
    else:
        config_dict = {
            'config': {
                'name': instance.name,
                'request': {
                    'base_url': base_url
                }
            }
        }

    testcase_list.append(config_dict)

    # 处理前置用例
    testcase_id_list = include_data.get('testcase')
    if testcase_id_list:
        for testcase_id in testcase_id_list:
            testcase_qs = TestcasesModel.objects.filter(id=testcase_id)
            if testcase_qs.exists():
                testcase_obj = testcase_qs.first()
                try:
                    testcase_request = json.loads(testcase_obj.request, encoding='utf-8')
                except Exception as e:
                    print(e)
                    continue
                testcase_list.append(testcase_request)

    # 处理需执行用例
    try:
        testcase_request = json.loads(instance.request, encoding='utf-8')
        testcase_list.append(testcase_request)
    except Exception as e:
        print(e)
        pass

    testcase_dir_path = os.path.join(testcase_dir_path, instance.name + '.yaml')
    with open(testcase_dir_path, 'w', encoding='utf-8') as f:
        yaml.dump(testcase_list, f, allow_unicode=True)


def run_testcase(instance: TestcasesModel, testcase_dir_path):
    """执行测试用例"""
    # 创建HttpRunner对象
    hr = HttpRunner()

    try:
        hr.run(testcase_dir_path)
    except Exception as e:
        print(e)
        return Response({'msg': '用例执行失败', 'status': 1})

    report_id = create_report(hr, instance)
    return Response({'id': report_id, 'msg': '执行成功，详情见测试报告'})


def create_report(runner: HttpRunner, instance: TestcasesModel):
    """
    创建测试报告
    """
    report_name = instance.name

    time_stamp = int(runner.summary['time']['start_at'])
    start_datetime = datetime.fromtimestamp(time_stamp).strftime('%Y%m%d %H%M%S')
    runner.summary['time']['start_datetime'] = start_datetime
    runner.summary['time']['duration'] = round(runner.summary['time']['duration'], 3)
    report_name = report_name if report_name else start_datetime
    runner.summary['html_report_name'] = report_name

    for item in runner.summary.get('details'):
        try:
            for record in item.get('records'):
                record['meta_data']['response']['content'] = record['meta_data']['response']['content'].decode('utf-8')
                record['meta_data']['response']['cookies'] = dict(record['meta_data']['response']['cookies'])

                request_body = record['meta_data']['request']['body']
                if isinstance(request_body, bytes):
                    record['meta_data']['request']['body'] = request_body.decode('utf-8')
        except Exception as e:
            print(e)
            continue

    try:
        summary = json.dumps(runner.summary, ensure_ascii=False)
    except Exception as e:
        print(e)
        return Response({'msg': '测试报告数据转化有误'})

    report_name = f'{report_name}_{datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")}'
    html_report_template_path = os.path.join(settings.BASE_DIR, 'reports_template/extent_report_template.html')
    report_path = runner.gen_html_report(html_report_name=report_name, html_report_template=html_report_template_path)

    with open(report_path, encoding='utf-8') as html:
        reports = html.read()

    test_report = {
        'name': report_name,
        'result': runner.summary.get('success'),
        'success': runner.summary.get('stat').get('successes'),
        'count': runner.summary.get('stat').get('testsRun'),
        'html': reports,
        'summary': summary,
    }
    report_obj = ReportsModel.objects.create(**test_report)
    return report_obj.id
