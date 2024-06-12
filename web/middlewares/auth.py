from django.utils.deprecation import MiddlewareMixin
from web.models import UserInfo, Transaction, PricePolicy, Project, ProjectUser
from django.shortcuts import redirect
from django.conf import settings
import datetime


class AuthMiddleware(MiddlewareMixin):
    # 自定义中间件，用于获取用户对象
    def process_request(self, request):
        # 返回什么用户就是什么
        # 如果用户已经登录，那么request.user就是已经登录的用户对象
        user_id = request.session.get('user_id', 0)
        # 通过session获取用户id
        user_object = UserInfo.objects.filter(user_id=user_id).first()
        # 通过用户id获取用户对象
        request.tracer = user_object
        # 将用户对象赋值给request.tracer
        # 防止死循环，设置登录白名单，在setting中设置
        # 获取当前用户访问的url
        # 如果访问的url在白名单中，那么就不进行拦截
        whit_url = settings.LOGIN_WHITE_URL_LIST
        reurl = request.path_info
        if reurl in whit_url:
            return
        # 检查用户是否已经登录
        # 如果已经登录，那么request.user就是用户对象
        # 如果未登录，那么request.user就是AnonymousUser对象
        if not request.tracer:
            return redirect('/login/')

        # 登录成功后访后台管理时获取用户额度
        # 获取用户额度
        _object = Transaction.objects.filter(user=user_object, status=2).order_by('-id').first()
        # 判断是否已过期
        current_datetime = datetime.datetime.now()
        if _object.end_datetime and _object.end_datetime < current_datetime:
            # 如果已过期，获取免费额度
            _object = Transaction.objects.filter(user=user_object, status=2, price_policy__category=1).first()
        request.transaction = _object

    def process_view(self, request, view, args, kwargs):
        if not request.path_info.startswith('/manage/'):
            return
        project_id = kwargs.get('project_id')  # 获取项目id
        project_object = Project.objects.filter(creator=request.transaction.user, id=project_id).first()  # 判断当前用户是否有权限访问该项目
        if project_object:
            request.project = project_object
            return
        project_user_object = ProjectUser.objects.filter(user=request.transaction.user, project_id=project_id).first()
        if project_user_object:
            request.project = project_user_object.project
            return

        return redirect('/project/list/')

