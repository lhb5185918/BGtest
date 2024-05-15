# -*- coding: utf-8 -*-
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest


def send_sms(phone, sms_code, code):


    client = AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')
    template_param = {"code": code}
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    if sms_code == "register":
        request.add_query_param('SignName', "bug平台")
        request.add_query_param("TemplateCode", "SMS_465941723")
        request.add_query_param("TemplateParam", template_param)
        response = client.do_action_with_exception(request)
        result = [response.decode('utf-8'), code]
    elif sms_code == "login":
        request.add_query_param('SignName', "bug平台")
        request.add_query_param("TemplateCode", "SMS_466235059")
        request.add_query_param("TemplateParam", template_param)
        response = client.do_action_with_exception(request)
        result = [response.decode('utf-8'), code]

    else:
        result = ["短信类型错误"]

    return result

