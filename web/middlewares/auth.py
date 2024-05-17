from django.utils.deprecation import MiddlewareMixin
from web.models import UserInfo


class AuthMiddleware(MiddlewareMixin):
    # 自定义中间件，用于获取用户对象
    def process_request(self,request):
        # 返回什么用户就是什么
        # 如果用户已经登录，那么request.user就是已经登录的用户对象
        user_id = request.session.get('user_id', 0)
        # 通过session获取用户id
        user_object = UserInfo.objects.filter(user_id=user_id).first()
        # 通过用户id获取用户对象
        request.tracer = user_object
        # 将用户对象赋值给request.tracer


