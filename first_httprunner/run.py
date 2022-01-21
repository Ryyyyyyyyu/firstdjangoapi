# -*- coding: UTF-8 -*-
from httprunner.api import HttpRunner

hr = HttpRunner()
summary = hr.run(r'D:\PycharmProjects\firstdjangoapi\projects_dir\20220121152032\自动化测试平台项目\登录接口_自动化测试平台项目\登录接口_正向用例.yaml')
print(summary)
