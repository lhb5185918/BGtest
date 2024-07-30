from http import HTTPStatus
import dashscope


class AIAssistant:
    dashscope.api_key = 'sk-5584b57cffe2400ebc380649906b8d6a'
    def call_with_messages(self, messages_right=None, messages_wrong=None, messages_suggestion=None):
        if messages_right is not None:
            messages_r = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                          {'role': 'user', 'content': f'{messages_right}请告诉我这个方法作用是什么'}]
            response = dashscope.Generation.call(
                model="qwen-turbo",
                messages=messages_r,
                result_format='message',  # 将返回结果格式设置为 message
            )
            if response.status_code == HTTPStatus.OK:
                for i in response['output']['choices']:
                    return i['message']['content']
            else:
                return response
        elif messages_wrong is not None:
            messages_w = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                          {'role': 'user', 'content': f'{messages_wrong}请告诉我为什么出了问题'}]
            response = dashscope.Generation.call(
                model="qwen-turbo",
                messages=messages_w,
                result_format='message',  # 将返回结果格式设置为 message
            )
            if response.status_code == HTTPStatus.OK:
                for i in response['output']['choices']:
                    return i['message']['content']
            else:
                return response
        elif messages_suggestion is not None:
            messages_s = [{'role': 'system', 'content': 'You are a helpful assistant.'},
                          {'role': 'user', 'content': f'{messages_suggestion}青岛告诉我你的建议'}]
            response = dashscope.Generation.call(
                model="qwen-turbo",
                messages=messages_s,
                result_format='message',  # 将返回结果格式设置为 message
            )
            if response.status_code == HTTPStatus.OK:
                for i in response['output']['choices']:
                    return i['message']['content']
            else:
                return response
