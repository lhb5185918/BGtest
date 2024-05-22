from django import forms
from web.forms.bootstrap import BootStrapForm
from web import models


class ProjectModelForm(BootStrapForm, forms.ModelForm):
    # desc = forms.CharField(widget=forms.Textarea(), label='描述', required=False)
    class Meta:
        # 重写Meta类，定义表单字段
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc': forms.Textarea()
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.request = request

    def clean_name(self):
        # 校验项目名称是否重复
        name = self.cleaned_data['name']
        exists = models.Project.objects.filter(name=name, creator=self.request.transaction.user).exists()
        if exists:
            raise forms.ValidationError('项目名已存在')
        max_num = self.request.transaction.price_policy.project_num
        count =models.Project.objects.filter(creator=self.request.transaction.user).count()
        if count >= max_num:
            raise forms.ValidationError('项目数量超限，最多只能创建%s个项目' % max_num)
        return name

