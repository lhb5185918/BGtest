class BootStrapForm(object):  # 定义一个父类，用于给表单添加样式
    def __init__(self, request, *args, **kwargs):
        # 重写初始化方法
        super().__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            fields.widget.attrs['class'] = 'form-control'
            fields.widget.attrs['placeholder'] = '请输入{}'.format(fields.label)
