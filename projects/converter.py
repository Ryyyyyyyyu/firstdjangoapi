from django.urls import converters, register_converter


class DateConverter(object):
    regex = r'\d{4}-(0[1-9]|1[0-2])-((0[1-9])|((1|2)[0-9])|30|31)'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value


register_converter(DateConverter, 'dater')
