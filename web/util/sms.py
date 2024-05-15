# -*- coding: utf-8 -*-
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
import random


def send_sms(phone):


    client = AcsClient(access_key_id, access_key_secret, 'cn-hangzhou')

    code = ''.join(random.sample('0123456789', 4))
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
    request.add_query_param('SignName', "bug平台")
    request.add_query_param("TemplateCode", "SMS_465941723")
    request.add_query_param("TemplateParam", template_param)
    response = client.do_action_with_exception(request)
    result = {"response":response.decode(),"code":code}

    return result




print(send_sms("18660282391"))