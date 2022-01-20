import json
import os
import yaml

from testcases.models import TestcasesModel
from debugtalks.models import DebugtalksModel
from envs.models import EnvsModel
from configures.models import ConfiguresModel


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
