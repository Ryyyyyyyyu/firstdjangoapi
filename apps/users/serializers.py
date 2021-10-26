# -*- coding: UTF-8 -*-
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(help_text='确认密码', label='确认密码', write_only=True, min_length=6,
                                             max_length=20, error_messages={'min_length': '仅允许6~20个字符的确认密码',
                                                                            'max_length': '仅允许6~20个字符的确认密码'
                                                                            })
    token = serializers.CharField(help_text='token', label='token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'password_confirm', 'token')
        extra_kwargs = {
            'username': {
                'help_text': '用户名',
                'label': '用户名',
                'min_length': 4,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许4~20个字符的用户名',
                    'max_length': '仅允许4~20个字符的用户名'
                    }
            },
            'email': {
                'help_text': '邮箱',
                'label': '邮箱',
                'required': 'True',
                'write_only': 'True',
                # 邮箱的重复校验
                'validators': [UniqueValidator(queryset=User.objects.all(), message='邮箱已存在')]
            },
            'password': {
                'help_text': '密码',
                'label': '密码',
                'write_only': 'True',
                'error_messages': {'min_length': '仅允许6~20个字符的密码',
                                   'max_length': '仅允许6~20个字符的密码'
                                   }
            }
        }

    def validate(self, attrs):
        if attrs.get('password') == attrs.get('password_confirm'):
            attrs.pop('password_confirm')
            return attrs
        else:
            raise serializers.ValidationError('两次密码不一致！')

    def create(self, validated_data):
        # user = User.objects.create(**validated_data)
        # 调用User模型对象方法创建普通用户
        user = User.objects.create_user(**validated_data)
        # 生成token
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        user.token = token
        return user
