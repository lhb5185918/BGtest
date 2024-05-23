class BootStrapForm(object):  # 定义一个父类，用于给表单添加样式

    bootstrap_class_exclude = []


    def __init__(self, request, *args, **kwargs):
        # 重写初始化方法
        super().__init__(*args, **kwargs)
        for name, fields in self.fields.items():
            if name in self.bootstrap_class_exclude:
                continue
            fields.widget.attrs['class'] = 'form-control'  # 为每个字段增加form-control样式
            fields.widget.attrs['placeholder'] = '请输入{}'.format(fields.label)
