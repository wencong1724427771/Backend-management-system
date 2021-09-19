from django import forms
from sales import models


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=16,
        min_length=3,
        error_messages={
            'max_length': '太长了',
            'min_length': '太短了',
            'required': '不能为空',     # 为空时触发
        },
        widget=forms.TextInput(attrs={'class': 'username', 'placeholder': '用户名',
                                     'autocomplete': 'off'})
    )
    password = forms.CharField(
        max_length=32,
        min_length=4,
        error_messages={
            'max_length': '太长了',
            'min_length': '太短了',
            'required': '不能为空',
        },
        widget=forms.PasswordInput(attrs={'class': 'password', 'placeholder': '输入密码',
                                          'oncontextmenu': 'return false', 'onpaste': 'return false'}),
    )
    r_password = forms.CharField(
        max_length=32,
        min_length=4,
        error_messages={
            'max_length': '太长了',
            'min_length': '太短了',
            'required': '不能为空',
        },
        widget=forms.PasswordInput(attrs={'class': 'r_password', 'placeholder': '确认密码',
                                          'oncontextmenu': 'return false', 'onpaste': 'return false'}),
    )
    telephone = forms.CharField(
        max_length=11,
        min_length=11,
        error_messages={
            'max_length': '太长了',
            'min_length': '太短了',
            'required': '不能为空',
        },
        widget=forms.TextInput(attrs={'class': 'phone_number', 'placeholder': '输入手机号码',
                                      'autocomplete': 'off', 'id': 'number'})
    )
    email = forms.EmailField(
        error_messages={
            'invalid': '必须是邮箱格式',
            'required': '不能为空',
        },
        widget=forms.EmailInput(attrs={'class': 'email', 'placeholder': '输入邮箱地址', 'oncontextmenu': 'return false',
                                       'onpaste': 'return false'})
    )  # xx@xx

    def clean(self):    # 全局钩子
        password = self.cleaned_data.get('password')
        r_password = self.cleaned_data.get('r_password')
        if password == r_password:
            return self.cleaned_data
        else:
            self.add_error('r_password', '两次密码不一致！')


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name,field in self.fields.items():
            # print(type(field))
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field,MultiSelectFormField):

                field.widget.attrs.update({'class':'form-control'})


class ConsultRecordModelForm(forms.ModelForm):
    class Meta:
        model = models.ConsultRecord
        fields = '__all__'
        exclude = ['delete_status']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name,field in self.fields.items():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field,MultiSelectFormField):

                field.widget.attrs.update({'class':'form-control'})


class EnrollmentModelForm(forms.ModelForm):
    class Meta:
        model = models.Enrollment
        fields = '__all__'
        exclude = ['delete_status']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field_name,field in self.fields.items():
            from multiselectfield.forms.fields import MultiSelectFormField
            if not isinstance(field,MultiSelectFormField):

                field.widget.attrs.update({'class':'form-control'})


class CourseRecordModelForm(forms.ModelForm):
    class Meta:
        model = models.CourseRecord
        fields = '__all__'
        # exclude = ['why_us','your_expectation','contract_approved','memo','delete_status']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for field_name, field in self.fields.items():
            # if field_name == 'customer':
            #     field.queryset = models.Customer.objects.filter(consultant__username=request.session.get('account'))
            field.widget.attrs.update({'class':'form-control'})
